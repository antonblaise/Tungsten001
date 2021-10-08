from discord.ext.commands import Cog, command
from apscheduler.triggers.cron import CronTrigger
from discord import File, Embed, Activity, ActivityType
from lib.bot import Bot
from lib.bot.__init__ import *
import os
from requests import get
from random import choice
from datetime import datetime

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
    async def echo(self, ctx, arg):
        if not arg == None:
            await ctx.channel.send(arg)

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