from typing import Optional
from discord.ext.commands import Cog, command
from lib.bot import Bot
from lib.bot.__init__ import *
from discord import Embed
from datetime import datetime
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

class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Settings changer
    @command(name="set", brief="Edit settings. Run \"/set\" for more detail.", help="Edit settings. Run \"/set\" for more detail.", hidden=False, pass_context=True)
    async def setting(self, ctx, function: Optional[str], feature: Optional[str], *args: Optional[str]):
        async with ctx.channel.typing():
            binary_choices = ["on","off","true","false","yes","no"]
            all_features =  [
                                'enable',
                                'hush', 'mute',
                                'hours', 'time',
                                'interval', 'intervals', 'step', 'steps', 'period', 'periods',
                                'future','forecast','length',
                                'cities','city'
                            ] # 16 elements (end = 15)
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
            # Embed 1
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
_future_ - {all_features[12:14]}
_cities_ - {all_features[15]}
                                """, 
                            False
                        ),
                        (
                            "> Show current settings",
                            f"""/set show
/set settings
/set view
                            """,
                            False
                        )]
            print(f"[{datetime.now().strftime('%H:%M:%S')}] embed - Step 3 DONE")
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] embed - Step 4 DONE")
            
            # Embed 2
            embed2 = Embed(title="> **Current settings**", 
                            description=f"""Current configurations for the auto functions""",
                            colour=0x00FF32,
                            timestamp=datetime.utcnow()
                            )
            embed2.set_thumbnail(url="https://data.whicdn.com/images/355435488/original.gif")
            fields2 = [
                        (
                            "> Auto IP Logging",
                            f"""*Enabled* - {'Yes' if ConfigObj("./data/db/auto_params.ini")['AUTO_IP']['enable_auto_ip'].lower() == 'true' else 'No'}
*Time (24hr format)* - {config['AUTO_IP']['hours_auto_ip']}
*Muted* - {'Yes' if ConfigObj("./data/db/auto_params.ini")['AUTO_IP']['hush_auto_ip'].lower() == 'true' else 'No'}
                            """,
                            False
                        ),
                        (
                            "> Auto Weather Forecast",
                            f"""*Enabled* - {'Yes' if ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['enable_auto_weather'].lower() == 'true' else 'No'}
*Time (24hr format)* - {config['AUTO_WEATHER']['hours_auto_weather']}
*Interval (hours)* - {config['AUTO_WEATHER']['interval_auto_weather']}
*Hours into the future* - {config['AUTO_WEATHER']['future_auto_weather']}
*Cities* - {', '.join(config['AUTO_WEATHER']['cities_auto_weather']).title()}
                            """,
                            False
                        ),
                        (
                            "> Usage guide",
                            """/set <function> <on/off>
/set <function> <feature> <input>
Run \"/set\" or \"/set help\" for full usage guide.
                            """,
                            False
                        )
                    ]
            for name, value, inline in fields2:
                embed2.add_field(name=name, value=value, inline=inline)

        # Start
        has_error = False # Initially, nothing wrong
        if function == None and feature == None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] if function == None and feature == None:")
            await ctx.channel.send(embed=embed)
        elif feature == None:
            if str(function).lower() in ['help','manual','guide']:
                await ctx.channel.send(embed=embed)
            elif str(function).lower() in ['show','settings','view']:
                await ctx.channel.send(embed=embed2)
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
                else: # Feature not found
                    await ctx.channel.send(f"Sorry {choice(('😣', '😅', '😕'))} \"{feature}\" feature is not available.")
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
                        elif str(feature).lower() == all_features[11:14]:
                            nfeature = 'future'
                            usage = f"<how many hours to forecast>"
                            example = "6"
                        await ctx.channel.send(f"> Usage: /set {function} {feature} {usage}\n     Example: /set {function} {feature} {example}")
                    else: # If args is NOT empty, process the args to be the correct format for each case scenario
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] <{feature}> Preprocess the arg.")
                        if str(feature).lower() in all_features[14:16]: # Case 1: Cities
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
                        elif str(feature).lower() in all_features[5:14]: # Case 2: Interval or future (can only accept one number)
                            nfeature = 'future' if str(feature).lower() in all_features[11:14] else 'interval'
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

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Settings")

def setup(bot):
        bot.add_cog(Settings(bot))