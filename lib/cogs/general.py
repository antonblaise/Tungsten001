from typing import Optional
from discord.ext.commands import Cog, command
from apscheduler.triggers.cron import CronTrigger
from discord import File, Embed, Activity, ActivityType
from lib.bot import Bot
from lib.bot.__init__ import *
import os
from requests import get
from random import choice
from datetime import datetime
from configobj import ConfigObj
import shutil

config = ConfigObj("./data/db/auto_params.ini")
bot = Bot()

class General(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._message = "listening /help"
        self.ten_sec_intv = "0,10,20,30,40,50"
        
        bot.scheduler.add_job(self.set, CronTrigger(second=self.ten_sec_intv))   

    @property
    def message(self):
        return self._message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
            raise ValueError("Invalid activity type.")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.bot.change_presence(activity=Activity(
        name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
        ))

    @command(name="whoisthis", aliases=["whoareyou","bot"], brief='Self introduction from bot' ,hidden=False, pass_context=False)
    async def whoisthis(self, ctx):
        s = int(datetime.now().strftime("%S"))
        embed = Embed(title="Tungsten001", 
                            description="Hi, nice to meet you! My name is Eula Lawrence from Mondstadt!",
                            colour=0x30F9FF,
                            timestamp=datetime.utcnow()
                            )
        eula_gif = ["https://c.tenor.com/-oLI6ZeCrkgAAAAd/eula-genshin-impact.gif", "https://c.tenor.com/RPRayyQVRV0AAAAd/genshin-eula.gif"]
        embed.set_image(url=eula_gif[s%2])
        fields = [("Name", "Eula Lawrence", True),
                    ("Codename", "Tungsten001", True),
                    ("Specialty", "Home VPN", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.channel.send(embed=embed)

    @command(name="echo", brief='Repeat after me', hidden=True, pass_context=False)
    async def echo(self, ctx, arg1, arg2):
        if not arg1 == None:
            await ctx.channel.send(arg1)
            if not arg2 == None:
                await ctx.channel.send(arg2)

    # Settings changer
    @command(name="set", brief="Change settings", hidden=False, pass_context=True)
    async def setting(self, ctx, function: Optional[str], feature: Optional[str], *args: Optional[str]):
        print(f"args = {args}")
        print(f"tyep of args = {type(args)}")
        binary_choices = ["on","off","true","false","yes","no"]
        binary_dict = {
                        "on": True,
                        "off": False,
                        "true": True,
                        "false": False,
                        "yes": True,
                        "no": False
                        }
        if function == None and feature == None:
            await ctx.channel.send("/help set")
        elif feature == None:
            functions = "hush" if str(function).lower() == "autoip" else "interval | length | city/cities"
            await ctx.channel.send(f"Please specify a feature. 📝\n     /set {function} < on/off | hours | {functions} >")
        else:
            if str(function).lower() == "autoip":
                if str(feature).lower() in ["hours","hush"]:
                    if bool(args) == False: # If args is empty
                        usage = f"< true/yes/on | false/no/off >" if str(feature).lower() == "hush" else f"<which {feature}>"
                        example = f"true" if str(feature).lower() == "hush" else f"6,12,18"
                        await ctx.channel.send(f"Usage: /set {function} {feature} {usage}\nExample: /set {function} {feature} {example}")
                    else: # If args is NOT empty
                        config['AUTO_IP'][f'{str(feature).lower()}_auto_ip'] = binary_dict[f'{args[0]}']
                        config.write()
                        await ctx.channel.send(f"Settings updated successfully.\n     [{str(function).upper()}] {feature}_auto_ip = {binary_dict[f'{str(args[0]).lower()}']}")
                elif str(feature).lower() in binary_choices:
                    config['AUTO_IP']['enable_auto_ip'] = binary_dict[f'{str(feature).lower()}']
                    config.write()
                    await ctx.channel.send(f"Settings updated successfully.\n     [{str(function).upper()}] enable_auto_ip = {binary_dict[str(feature).lower()]}")
            elif str(function).lower() == "autoweather":
                if str(feature).lower() in ["hours","interval","length","cities","city"]:
                    if bool(args) == False: # If args is empty
                        if str(feature).lower() in ["hours","cities"]:
                            usage = f"<which {feature}>"
                            example = f"6,12,18" if str(feature).lower() == "hours" else "New York, London"
                        elif str(feature).lower() == "interval":
                            usage = f"< {feature} >"
                            example = "1"
                        elif str(feature).lower() == "length":
                            usage = f"< how many hours to forecast >"
                            example = "6"
                        await ctx.channel.send(f"Usage: /set {function} {feature} {usage}\nExample: /set {function} {feature} {example}")
                    else:
                        if str(feature).lower() in ['city','cities']:
                            feature = 'cities'
                            # preprocess the arg
                            a = ""
                            for i in range(len(args)): a += f"{args[i]} " 
                            if "," in a:
                                if len(a.strip().split(', ')) == 1:
                                    args = a.strip().split(',')
                                else:
                                    args = a.strip().split(', ')
                            else:
                                args = a.strip()
                        else:
                            pass
                        config['AUTO_WEATHER'][f'{str(feature).lower()}_auto_weather'] = args
                        config.write()
                        await ctx.channel.send(f"Settings updated successfully.\n     [{str(function).upper()}] {feature}_auto_weather = {str(args).lower()}")
                elif str(feature).lower() in binary_choices:
                    config['AUTO_WEATHER']['enable_auto_weather'] = binary_dict[f'{str(feature).lower()}']
                    config.write()
                    await ctx.channel.send(f"Settings updated successfully.\n     [{str(function).upper()}] enable_auto_weather = {binary_dict[str(feature).lower()]}")

    @command(name="reset", brief="Reset all settings", hidden=False, pass_context=False)
    async def reset(self, ctx):
        shutil.copyfile('./data/db/default_auto_params.ini', './data/db/auto_params.ini')
        await ctx.channel.send("All settings and parameters for the auto functions are reset to default.")

    @command(name="hello", aliases=["hi","hey"], brief='Greet the bot', hidden=True, pass_context=False)
    async def greet(self, ctx):
        print(">> HELLO")
        self.hour_now = int(datetime.now().strftime("%H"))
        if self.hour_now >= 5 and self.hour_now < 12:
            self.period_now = "morning"
        elif self.hour_now >= 12 and self.hour_now < 17:
            self.period_now = "afternoon"
        else:
            self.period_now = "evening"
        good = f"Good {self.period_now}"
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', good))} {ctx.author.mention}!")

    @command(name="ipinfo", aliases=["ipcheck"], brief='Check home network IP info', pass_context=False, hidden=False)
    async def ip_info(self, ctx):
        self.ipInfo = get('https://ipinfo.io/').content.decode('utf8')
        await ctx.send(self.ipInfo)
    
    @command(name="logip", aliases=["iplog"], brief='Record/Update the IP', pass_context=False, hidden=False)
    async def log_ip(self, ctx):
        print(">> Logging IP")
        log_path = "./data/db/ip.log"
        log_content = open(log_path).read().splitlines()
        if log_content == []:
            log_content = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{get('https://ifconfig.me').content.decode('utf8')}"
            open(log_path,'w').write(log_content)
            log_content = open(log_path).read().splitlines()
            self.ip_report = f"IP address has been recorded on {log_content[0]}."
        else:
            if log_content[1] == get('https://ifconfig.me').content.decode('utf8'):
                self.ip_report = f"The IP address has not changed since {log_content[0]}."
            else:
                log_content[0] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                log_content[1] = get('https://ifconfig.me').content.decode('utf8')
                open(log_path,'w').write('\n'.join(log_content))
                self.ip_report = f"IP address has been updated on {log_content[0]}."
        await ctx.send(self.ip_report)

    @command(name="ovpn", aliases=["vpncert","homevpn"], brief='Send the latest OpenVPN cert', pass_context=False, hidden=False)
    async def send_ovpn(self, ctx):
        timecode = datetime.now().strftime("%d%m%Y-%H%M%S")
        # Generate latest OpenVPN cert
        file_path = "./data/db/OpenVPN_cert/"
        lines = open(file_path+"SAMPLE.ovpn").read().splitlines()
        ip_addr = get('https://ifconfig.me').content.decode('utf8')
        lines[0] = 'remote '+str(ip_addr)+' 1194'
        file_name = "TCP-Antonius-home_"+str(timecode)+".ovpn"
        open(file_path+file_name,'w').write('\n'.join(lines))
        await ctx.send(file=File(file_path + file_name)) # Send it
        os.remove(file_path+file_name) # Remove the file to avoid cluttering

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("General")

def setup(bot):
        bot.add_cog(General(bot))