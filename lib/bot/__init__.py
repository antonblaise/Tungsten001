from random import choice
from configobj import ConfigObj
import requests
from discord import Intents, Embed, File, DMChannel
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger 
from requests import get
from datetime import datetime
import os, platform
from utils.autoFunc import *
from utils.messenger import *
from ..db import db
from glob import glob
from discord.ext.commands import (CommandNotFound, BadArgument)
from asyncio import sleep

# Disable warnings
import warnings
warnings.filterwarnings("ignore")

PREFIX = "/"
OWNER_IDS = [532991098822328322] # Owner
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")] if platform.system() == "Windows" else [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]

# return the name of any cogs in a list
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self): # Initially, not ready
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog): # Set the cogs to ready
        for cog in COGS:
            setattr(self, cog, True)

    def all_ready(self): # Check if all cogs are ready, return True or False
        for cog in COGS:
            if getattr(self, cog):
                print(f"[+] {cog} cog is ready!")
            else:
                pass
                # print(f"[-] {cog} cog is NOT ready.")
        return all([getattr(self, cog) for cog in COGS])

class TimeKeeper():
    def __init__(self):
        self.get_period()
        self.get_second()
        self.full_time_now()
        self.hour_min_now()
        pass

    def full_time_now(self):
        self.full_time = datetime.now().strftime("%H:%M:%S")

    def hour_min_now(self):
        self.hour_min = datetime.now().strftime("%H:%M")

    def get_period(self):
        self.hour_now = int(datetime.now().strftime("%H"))
        if self.hour_now >= 2 and self.hour_now < 12:
            period = "morning"
        elif self.hour_now >= 12 and self.hour_now < 17:
            period = "afternoon"
        else:
            period = "evening"
        self.period_now = period
    
    def get_second(self):
        self.sec_now = int(datetime.now().strftime("%S"))
        

class Bot(BotBase):
    def __init__(self):
        self.prefix = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.timekeeper = TimeKeeper()
        self.scheduler = AsyncIOScheduler()
        self.fiveSecIntv = '0,5,10,15,20,25,30,35,40,45,50,55'
        self.random_eula_stickers = open("./data/db/Eula_chibi.stickers").read().splitlines()

        db.autosave(self.scheduler)
        
        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def setup(self):
        if platform.system() not in ['Windows', 'Linux']:
            print("\n\nSorry, this bot can only run on Windows and Linux. Thank you!\n\n")
            exit()

        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f">> {cog} cog loaded.")

        while not self.check_ini_file(): # Must make sure autoparams.ini is present first
            continue


        print("[+] Setup complete.")

    def run(self, version):
        self.VERSION = version
        open("data/db/database.db", "a+")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nTungsten001 a.k.a. Eula Lawrence (v{self.VERSION})\n\tby Antonius Blaise\n")
        print(f"\tRunning on {platform.system()}\n")
        print(">> Running setup...")
        self.setup()

        with open("./lib/bot/token.0","r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print(">> Running bot...")
        super().run(self.TOKEN, reconnect=True)

    def say_hi():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Hi!")

    async def rescheduleJob(self, jobID, newSchedule):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] rescheduleJob")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Before reschedule: \n{self.scheduler.get_job(jobID)}")
        self.scheduler.reschedule_job(jobID, trigger=CronTrigger(hour=newSchedule))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] After reschedule: \n{self.scheduler.get_job(jobID)}")


    async def name_card(self, message):
        async with self.stdout.typing():
            s = int(datetime.now().strftime("%S"))
            embed = Embed(title="> **Tungsten001**", 
                                description="Hi, nice to meet you! My name is Eula Lawrence from Mondstadt!",
                                colour=0x30F9FF,
                                timestamp=datetime.utcnow()
                                )
            eula_gif = ["https://c.tenor.com/-oLI6ZeCrkgAAAAd/eula-genshin-impact.gif", "https://c.tenor.com/RPRayyQVRV0AAAAd/genshin-eula.gif"]
            embed.set_image(url=eula_gif[s%2])
            fields = [("> Name", "Eula Lawrence", True),
                        ("> Codename", "Tungsten001", True),
                        ("> Specialties", "Home VPN\nWeather forecast", True)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        await message.channel.send(embed=embed)

    async def send_ovpn(self, message):
        async with message.channel.typing():
            timecode = datetime.now().strftime("%d%m%Y-%H%M%S")
            # Generate latest OpenVPN cert
            file_path = "./data/db/OpenVPN_cert/"
            lines = open(file_path+"SAMPLE.ovpn").read().splitlines()
            try:
                ip_addr = get('https://ifconfig.me').content.decode('utf8')
            except requests.exceptions.ConnectionError:
                ip_addr = get('https://ipinfo.io/ip').content.decode('utf8')
            lines[0] = 'remote '+str(ip_addr)+' 1194'
            file_name = "TCP-Antonius-home_"+str(timecode)+".ovpn"
            open(file_path+file_name,'w').write('\n'.join(lines))
        await message.channel.send(file=File(file_path + file_name)) # Send it
        os.remove(file_path+file_name) # Remove the file to avoid cluttering

    async def auto_log_ip(self):
        if ConfigObj("./data/db/auto_params.ini")['AUTO_IP']['enable_auto_ip'].lower() == "true":
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Doing scheduled IP check... 🧐🧐")
            res = await autoLogIp()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {res}")
            if ConfigObj("./data/db/auto_params.ini")['AUTO_IP']['hush_auto_ip'].lower() == "true":
                pass
            else:
                await self.stdout.send("Doing scheduled IP check... 🧐🧐")
                await self.stdout.send(res)
        else:
            pass
        
    async def man_log_ip(self, message):
        async with message.channel.typing():
            print(">> Logging IP manually")
            log_path = "./data/db/ip.log"
            log_content = open(log_path).read().splitlines()
            try:
                ip_addr = get('https://ifconfig.me').content.decode('utf8')
            except:
                ip_addr = get('https://ipinfo.io/ip').content.decode('utf8')
            if log_content == []:
                log_content = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{ip_addr}"
                log_content = open(log_path).read().splitlines()
                self.ip_report = f"IP address has been recorded on {log_content[0]}."
            else:
                if log_content[1] == ip_addr:
                    self.ip_report = f"The IP address has not changed since {log_content[0]}."
                else:
                    log_content[0] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    log_content[1] = ip_addr
                    open(log_path,'w').write('\n'.join(log_content))
                    self.ip_report = f"IP address has been updated on {log_content[0]}."
        await message.channel.send(self.ip_report)

    async def auto_weather_forecast(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ConfigObj('./data/db/auto_params.ini')['AUTO_WEATHER']['enable_auto_weather'].lower() == 'true'}")
        if ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['enable_auto_weather'].lower() == "true":
            cities = ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['cities_auto_weather']
            for c in cities:
                async with self.stdout.typing():
                    embed = await autoWeatherForecast(c)
                if isinstance(embed, str):
                    await self.stdout.send(embed)
                else:
                    await self.stdout.send(embed=embed)
        else:
            pass

    async def weather_forecast(self, message, place, length):
        api_key = str(open("./data/db/openweathermap_api.0").read())
        print(f"[{datetime.now().strftime('%H:%M:%S')}] city = {place}")
        icon_codes = ['01d','02d','03d','04d',
                        '09d','10d','11d','13d',
                        '50d','01n','02n','03n',
                        '04n','10n','11n','13n',
                        '50n']
        emojis = [':sunny:',':partly_sunny:',':white_sun_cloud:',':cloud:',
                        ':cloud_rain:',':white_sun_rain_cloud:', ':cloud_lightning:',':snowflake:',
                        ':fog:',':sunny:',':partly_sunny:',':white_sun_cloud:',
                        ':cloud:',':white_sun_rain_cloud:',':cloud_lightning:',':snowflake:',
                        ':fog:']
        print(f"[{datetime.now().strftime('%H:%M:%S')}] http://api.openweathermap.org/geo/1.0/direct?q={place}&limit=5&appid={api_key}")
        geocode = get(f"http://api.openweathermap.org/geo/1.0/direct?q={place}&limit=5&appid={api_key}").json()
        lat, lon = geocode[0]['lat'], geocode[0]['lon']
        exclude_parts = "current,minutely,daily,alerts"
        x = get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}").json()
        if 'hourly' in x:
            async with message.channel.typing():
                self.weather_embed = Embed(title=f"> **{place.upper()}**, {datetime.now().strftime('%Y-%m-%d')}", description=f"{length}-hour weather forecast.", colour=0x30F9FF, timestamp=datetime.utcnow())             
                field = []
                for hours in range(len(x['hourly'][0:length])):
                    field.append((
                        f"{datetime.utcfromtimestamp(x['hourly'][hours]['dt']+x['timezone_offset']).strftime('%H:%M')} {emojis[icon_codes.index(x['hourly'][hours]['weather'][0]['icon'])]}", 
                        f"> {str(round(x['hourly'][hours]['temp']-273.15, 2))}°C\n> *{str(round(x['hourly'][hours]['feels_like']-273.15, 2))}°C*\n> _{x['hourly'][hours]['weather'][0]['description']}_", 
                        True
                                ))
                for name, value, inline in field:
                    self.weather_embed.add_field(name=name, value=value, inline=inline)
                self.weather_embed.set_thumbnail(url=choice((self.random_eula_stickers)))
                self.weather_embed.set_footer(text=f"Requested by {message.author.name}")
            await message.channel.send(embed=self.weather_embed)
        else:
            await message.channel.send("Sorry, I can't fetch the weather data... :worried:")

    def check_ini_file(self):
        # print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking if auto_params.ini is still present...")
        if not os.path.isfile("./data/db/auto_params.ini"): # if the .ini file is gone
            print(f"[-] The auto_params.ini file does not exist or is gone.")
            print(f">> Restoring from default_auto_params.ini.")
            while not os.path.isfile("./data/db/auto_params.ini"):
                print(">> Loading ...")
                ini = open("./data/db/default_auto_params.ini").read()
                open("./data/db/auto_params.ini","w").write(ini)
            print("[+] Done.")
        else:
            pass
            # print(f"[{datetime.now().strftime('%H:%M:%S')}] No issue with auto_params.ini.")
        return os.path.isfile("./data/db/auto_params.ini")
        
    def on_connect(self):
        print(f"[+] Bot connected.")

    async def on_disconnect(self):
        print("[-] Bot disconnected.")

    async def on_error(self, err, *args, **kwargs): # Error handling
        if err == "on_command_error":
            await args[0].send("An error has occurred.")
        raise

    async def on_command_error(self, ctx, exc): # Command error
        if isinstance(exc, CommandNotFound):
            await ctx.send("Command not found.")
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(718122840544641084) # Discord server
            self.stdout = self.get_channel(783349409806024755) # Text channel. self.stdout can be used anywhere in this script
            self.scheduler.add_job(self.auto_log_ip, CronTrigger(hour=ConfigObj("./data/db/auto_params.ini")['AUTO_IP']['hours_auto_ip']), id='auto_ip') # Log IP every 6 hours    
            self.scheduler.add_job(self.auto_weather_forecast, CronTrigger(hour=ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['hours_auto_weather']), id='auto_wf') # Weather forecast
            self.scheduler.add_job(self.timekeeper.get_period, CronTrigger(second=self.fiveSecIntv))
            self.scheduler.add_job(self.check_ini_file, CronTrigger(second=self.fiveSecIntv))
            self.scheduler.start()
            
            
            while not self.cogs_ready.all_ready(): # Wait for all cogs to be ready before doing bot ready
                await sleep(0.5)

            self.ready = True
            print("[+] Bot ready\n>> Debugging...")

        else:
            print("[+] Bot reconnected.")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Auto log ip on boot")
        await self.auto_log_ip()

    # Messaging
    async def on_message(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] GOT MESSAGE from {message.author.name}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Message: {message.content}")
        cond1 = bool(not message.author.bot) # Message is not from bot
        cond2 = bool(not isinstance(message.channel, DMChannel)) # Message is not DM
        cond3 = bool(not bool([ele for ele in [f'{bot.user.id}','@eula'] if(ele in message.content.lower())])) # Bot is not tagged
        print(f"[{datetime.now().strftime('%H:%M:%S')}] cond1: {cond1}; cond2: {cond2}; cond3: {cond3}")
        if cond2 and cond3:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] cond2 and cond3 fulfilled: await self.process_commands(message)")
            await self.process_commands(message) # Process commands if the message is not a DM and the bot is not mentioned
        elif cond1:  # When someone PMs/tags the bot and the message if NOT from the bot herself
            async with message.channel.typing():
                print(f"[{datetime.now().strftime('%H:%M:%S')}] cond1 fulfilled")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] else: await directMessage(message)")
            res_directMessage = await directMessage(message)

        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] res_directMessage: {res_directMessage}")
        except:
            pass

        try:
            if res_directMessage == "weather forecast request":
                m = message.content.split(" ")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] m = {m}")
                try:
                    length = int(m[len(m)-1]) # If the command ends with a number
                    lengthGiven = True
                    lengthCheck = 4
                except:
                    length = 6
                    lengthGiven = False
                    lengthCheck = 3
                
                if len(m) == lengthCheck: # If name of city only has one word
                    n = m[2]
                else:
                    if lengthGiven:
                        n = " ".join(m[2:len(m)-1])
                    else:
                        n = " ".join(m[2:len(m)])
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] n = {n}")
                
                if len(n.strip().split(', ')) == 1:
                    cities = n.strip().split(",")
                else:
                    cities = n.strip().split(", ")
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] cities = {cities}")
                for city in cities:
                    await self.weather_forecast(message, city, length)
            elif res_directMessage == "name card":
                await self.name_card(message)
            else:
                pass
        except:
            pass
    
    
bot = Bot()
