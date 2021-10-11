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
from time import sleep

bot = Bot()

print(f"[+] auto_params.ini is present.") if bool(ConfigObj("./data/db/auto_params.ini")) else print(f"[-] auto_params.ini is not present.")

while not bool(ConfigObj("./data/db/auto_params.ini")):
    print(f">> Copy: default_auto_params.ini -> auto_params.ini")
    ini = open("./data/db/default_auto_params.ini").read()
    open("./data/db/auto_params.ini","w").write(ini)
    print("[+] Done") if bool(ConfigObj("./data/db/auto_params.ini")) else print("[-] Failed. Trying again.")
    sleep(1)

config = ConfigObj("./data/db/auto_params.ini")

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
        try:
            await self.bot.change_presence(activity=Activity(
            name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
            ))
        except ConnectionResetError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}]\n[-] Error: Connection reset")

    def load_config():
        config = ConfigObj("./data/db/auto_params.ini")

    @command(name="whoisthis", aliases=["whoareyou","bot"], brief='Self introduction from bot', help='Self introduction from bot' ,hidden=False, pass_context=False)
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

    @command(name="echo", brief='Repeat your sentence.', help='Repeat your sentence.', hidden=True, pass_context=False)
    async def echo(self, ctx, arg1, arg2):
        if not arg1 == None:
            await ctx.channel.send(arg1)
            if not arg2 == None:
                await ctx.channel.send(arg2)

    # Settings changer
    @command(name="set", brief="Edit settings. Run \"/set\" for more detail.", help="Edit settings. Run \"/set\" for more detail.", hidden=False, pass_context=True)
    async def setting(self, ctx, function: Optional[str], feature: Optional[str], *args: Optional[str]):
        binary_choices = ["on","off","true","false","yes","no"]
        all_features =  [
                            'enable',
                            'hush', 'mute',
                            'hours', 'time',
                            'interval', 'intervals', 'step', 'steps', 'period', 'periods',
                            'future','forecast',
                            'cities','city'
                        ]
        print(f"[{datetime.now().strftime('%H:%M:%S')}] all_features DONE")
        binary_dict = {
                        "on": True,
                        "off": False,
                        "true": True,
                        "false": False,
                        "yes": True,
                        "no": False
                        }
        print(f"[{datetime.now().strftime('%H:%M:%S')}] binary_dict DONE")
        embed = Embed(title="> **/set** - Usage Guide", 
                        description=f"""/set <function> <on/off>
/set <function> <feature> <input>
                                         """,
                        colour=0xFF28D7,
                        timestamp=datetime.utcnow()
                        )
        print(f"[{datetime.now().strftime('%H:%M:%S')}] embed - Step 1 DONE")
        embed.set_thumbnail(url="https://c.tenor.com/CgDf35tjlD4AAAAd/eula-genshin-impact.gif")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] embed - Step 2 DONE")
        fields = [
                    (
                        "> Functions",
                        """Auto IP Logging: **autoip**
Auto Weather Forecast: **autoweather**
                             """,
                        False
                    ),
                    (
                        "> Examples with on/off, features and inputs", 
                        """/set <function> off
/set <function> enable true
/set <function> hours "4,10,16"
/set <function> interval 1
/set <function> future 5
/set <function> cities New York, Tokyo
                             """, 
                        False
                    ),
                    (
                        "> Replaceables", 
                        f"""_on_ - yes, true
_off_ - no, false
_hours_ - {all_features[4]}
_interval_ - {', '.join(all_features[6:11])}
_future_ - {all_features[12]}
_cities_ - {all_features[14]}
                             """, 
                        False
                    )]
        print(f"[{datetime.now().strftime('%H:%M:%S')}] embed - Step 3 DONE")
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] embed - Step 4 DONE")
        
        # Start
        has_error = False# Initially, nothing wrong
        if function == None and feature == None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] if function == None and feature == None:")
            await ctx.channel.send(embed=embed)
        elif feature == None:
            if str(function).lower() in ['help','manual','guide']:
                await ctx.channel.send(embed=embed)
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] elif feature == None:")
                functions = "hush" if str(function).lower() == "autoip" else "interval | future | city/cities"
                await ctx.channel.send(f"> Please specify a feature. 📝\n     /set {function} <on/off | hours | {functions}>")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] else: GOING INTO LAYER 2")
            if str(function).lower() == "autoip":
                print(f"[{datetime.now().strftime('%H:%M:%S')}] if str(function).lower() == autoip:")
                if str(feature).lower() in all_features[1:5]: # for hush and hours
                    if bool(args) == False: # If args is empty
                        usage = f"<true/yes/on | false/no/off>" if str(feature).lower() in all_features[1:3] else f"<{feature}>"
                        example = f"true" if str(feature).lower() == "hush" else f"6,12,18"
                        await ctx.channel.send(f"> Usage: /set {function} {feature} {usage}\n     Example: /set {function} {feature} {example}")
                    else: # If args is NOT empty
                        if str(feature).lower() in all_features[1:3]: # hush
                            nfeature = 'hush'
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] nfeature = 'hush', args[0] = {args[0]}")
                            config['AUTO_IP'][f'{nfeature}_auto_ip'] = binary_dict[f'{args[0]}']
                            config.write()
                            await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] {feature}_auto_ip = {binary_dict[f'{str(args[0]).lower()}']}")
                        else: # hours
                            nfeature = 'hours'
                            config['AUTO_IP'][f'{str(nfeature).lower()}_auto_ip'] = args[0]
                            config.write()
                            await self.bot.rescheduleJob('auto_ip', args[0])
                            await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] {feature}_auto_ip = {args[0]}")
                elif str(feature).lower() in binary_choices: # If set function on/off
                    config['AUTO_IP']['enable_auto_ip'] = binary_dict[f'{str(feature).lower()}']
                    config.write()
                    await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] enable_auto_ip = {binary_dict[str(feature).lower()]}")
                elif str(feature).lower() == "enable": # Special case, if enable is mentioned
                    if bool(args) == True:
                        config['AUTO_IP'][f'{str(feature).lower()}_auto_ip'] = binary_dict[f'{args[0]}']
                        config.write()
                        await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] {feature}_auto_ip = {binary_dict[f'{str(args[0]).lower()}']}")
                    else:
                        await ctx.channel.send(f"Usage: /set {function} {feature} <true/yes/on | false/no/off>\n     Example: /set {function} {feature} true")
            elif str(function).lower() == "autoweather":
                print(f"[{datetime.now().strftime('%H:%M:%S')}] elif str(function).lower() == autoweather:")
                if str(feature).lower() in all_features:
                    """
                    All the instances of "nfeatures" below 
                    are to categorise each feature given in the command correctly,
                    allowing more flexibility.
                    """ 
                    if bool(args) == False: # If args is empty
                        if str(feature).lower() in all_features[3:5] or str(feature).lower() in all_features[13:15]:
                            nfeature = 'hours' if str(feature).lower() in all_features[3:5] else 'cities'
                            usage = f"<which {feature}>"
                            example = f"6,12,18" if str(feature).lower() == "hours" else "New York, London"
                        elif str(feature).lower() == all_features[5:11]:
                            nfeature = 'interval'
                            usage = f"<{feature}>"
                            example = "1"
                        elif str(feature).lower() == all_features[11:13]:
                            nfeature = 'future'
                            usage = f"<how many hours to forecast>"
                            example = "6"
                        await ctx.channel.send(f"> Usage: /set {function} {feature} {usage}\n     Example: /set {function} {feature} {example}")
                    else: # If args is NOT empty, process the args to be the correct format for each case scenario
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] <{feature}> Preprocess the arg.")
                        if str(feature).lower() in ['city','cities']: # Case 1: Cities
                            nfeature = 'cities'
                            a = ""
                            for i in range(len(args)): a += f"{args[i]} " 
                            if "," in a:
                                if len(a.strip().split(', ')) == 1:
                                    args = a.strip().split(',')
                                else:
                                    args = a.strip().split(', ')
                            else:
                                args = a.strip() # Store the product back into args
                        elif str(feature).lower() in all_features[5:13]: # Case 2: Interval or future (can only accept one number)
                            nfeature = 'future' if str(feature).lower() in all_features[11:13] else 'interval'
                            if len(args[0].split(',')) == 1:
                                args = args[0].split(',')[0] # Store the product back into args
                            else:
                                has_error = True
                                await ctx.channel.send(f"> /set {function} {feature} <{feature}>\n     Sorry, I can only accept one value for <{feature}>... {choice(('😣', '😅', '😕'))}")
                        elif str(feature).lower() in all_features[3:5]: # Case 3: Hours (can accept one or more numbers)
                            nfeature = 'hours'
                            args = args[0]
                        else:
                            pass                        
                        # After assigning the correct value to args
                        try:
                            if has_error:
                                pass
                            else:
                                config['AUTO_WEATHER'][f'{str(nfeature).lower()}_auto_weather'] = args
                                config.write()
                                if nfeature == 'hours':
                                    await self.bot.rescheduleJob('auto_wf', args)
                                else:
                                    pass
                                await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] {nfeature}_auto_weather = {str(args).lower()}")
                        except UnboundLocalError:
                            await ctx.channel.send(f"> Please try again.")
                elif str(feature).lower() in binary_choices:
                    config['AUTO_WEATHER']['enable_auto_weather'] = binary_dict[f'{str(feature).lower()}']
                    config.write()
                    await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] enable_auto_weather = {binary_dict[str(feature).lower()]}")
                elif str(feature).lower() == "enable": # Special case, if enable is mentioned
                    if bool(args) == True:
                        config['AUTO_WEATHER'][f'{str(feature).lower()}_auto_weather'] = binary_dict[f'{args[0]}']
                        config.write()
                        await ctx.channel.send(f"> Settings updated successfully. ✅\n     [{str(function).upper()}] {feature}_auto_weather = {binary_dict[f'{str(args[0]).lower()}']}")
                    else:
                        await ctx.channel.send(f"> Usage: /set {function} {feature} <true/yes/on | false/no/off>\n     Example: /set {function} {feature} true")
                else: # If feature not found
                    await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send(embed=embed)
                    

    @command(name="reset", brief="Reset all settings", help="Reset all settings", hidden=False, pass_context=False)
    async def reset(self, ctx):
        shutil.copyfile('./data/db/default_auto_params.ini', './data/db/auto_params.ini')
        await ctx.channel.send("> All settings and parameters for the auto functions are reset to default. ✨")

    @command(name="hello", aliases=["hi","hey"], brief='Greet the bot', help='Greet the bot', hidden=True, pass_context=False)
    async def greet(self, ctx):
        print(">> HELLO")
        self.hour_now = int(datetime.now().strftime("%H"))
        if self.hour_now>= 5 and self.hour_now <12:
            self.period_now = "morning"
        elif self.hour_now>= 12 and self.hour_now <17:
            self.period_now = "afternoon"
        else:
            self.period_now = "evening"
        good = f"Good {self.period_now}"
        await ctx.send(f"> {choice(('Hello', 'Hi', 'Hey', good))} {ctx.author.mention}!")

    @command(name="ipinfo", aliases=["ipcheck"], brief='Check home network IP info', help='Check home network IP info', pass_context=False, hidden=False)
    async def ip_info(self, ctx):
        self.ipInfo = get('https://ipinfo.io/').content.decode('utf8')
        await ctx.send(self.ipInfo)
    
    @command(name="logip", aliases=["iplog"], brief='Record/Update the IP', help='Record/Update the IP', pass_context=False, hidden=False)
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

    @command(name="ovpn", aliases=["vpncert","homevpn"], brief='Send the latest OpenVPN cert', help='Send the latest OpenVPN cert', pass_context=False, hidden=False)
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