# Tungsten001
This is my personal Discord bot, named after my favourite DPS in [Genshin Impact](https://genshin.hoyoverse.com/en/), Eula Lawrence,
codenamed the toughest metal on earth, tungsten.

# Requirements
Please run the __requirements.py__ to install the necessary packages for this program.

# Usage - do these before running the bot
### Prepare Discord bot token and gather IDs
- Save your Discord bot token in **/lib/bot/token.0** (Create one if it's not there)
</br>[How to Get a Discord Bot Token](https://www.writebots.com/discord-bot-token/)
- Modify **/lib/bot/\_\_init\_\_.py** `line 224` with your Discord server ID, 
  `line 225` with the text channel ID that you want the bot to send messages to,
  and `line 19` with your account ID (NOT your username). 
</br>[Where can I find my User/Server/Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
- For the IDs mentioned above, you can just right click on them and click "Copy ID".
### Get your own OpenWeatherMap API key
- Save your OpenWeatherMap API key in **/data/db/openweathermap_api.0** (Create one if it's not there)
</br>[OpenWeatherMap API key](https://openweathermap.org/api)
### Prepare the OpenVPN cert of our own WiFi
- Go to [your home WiFi router's webpage](192.168.0.1)
- Here's an [example for TP-Link routers](https://www.tp-link.com/us/support/faq/1239/) that you may follow. The procedures should be similar for other routers.
- Put the OpenVPN cert in **/data/db/OpenVPN_cert/SAMPLE.ovpn** (Create one if it's not there)
### What you can do at first run 
- The bot responds to `/<command>`, send `/help` to view command lists.
- To request weather forecast, send: `@<the bot> weather <city or town>`
- There are several settings that are customisable. Send `/set` to see the full details.
- As a side note, you can also direct message (DM) the bot, but she only responds to some very primitive messages like greetings. Try it out!

# Functions
## Checks public IP information of my home network.
- The IP address is essential to generate an OpenVPN certificate and use it to connect to my home network from anywhere over the internet.

## Regularly updates IP address
- At a given time interval, it checks and logs the IP address of my home network in a log file. If nothing is changed, it won't do anything, and it will report that nothing has changed since last record.

## Generate and send OpenVPN certificate
- By fetching the latest public IP address of my home network, an OpenVPN certificate is generated and sent through a text channel.

## Weather forecast
- Hourly weather forecast for a city or town can be given both on request and automatically following a schedule, i.e. once per 4 hours. This feature is powered by OpenWeatherMap API.

## More is on the way!
- There's no specific task that I need Eula to handle for me. The repository and the coding might be a kinda sloppy and disorganised, but whenever I get an idea in my head, I'm just gonna add it in. After all, this is my very first time using Git/Github, and this is just my personal helper bot. Nonetheless, do feel free to clone it and play around as you like!

# Customisations
- The command prefix can be changed at `line 18` of __/lib/bot/\_\_init\_\_.py__.
- Other parameters can be found and edited in **./data/db/auto_params.ini**, which is **NOT** present until you run the code for the first time. It copies the **./data/db/default_auto_params.ini** on first boot, and after that, **auto_params.ini** can be edited freely through the commands `/set <your input>` and `/reset`.
- Run `/help set` or `/set` to see the full details.

# Debugging
- When you run launcher.py on a terminal, you can see detailed (or perhaps unintelligible) outputs that can be used for debugging, namely to detect where and what have gone wrong. It's mainly for my personal use, but you can always edit them for your own utilisation inside the scripts anyway.
- If you receive any sort of error message when starting the program, don't worry. As long as you see "\[+\] Bot ready" and ">> Debugging...", you're ready to go.

# Error/Warning messages on start
### TypeError: object NoneType can't be used in 'await' expression
```
_ClientEventTask exception was never retrieved
future: <ClientEventTask state=finished event=on_connect coro=<bound method Bot.on_connect of <lib.bot.Bot object at 0xffffb1517a30>> exception=TypeError("object NoneType can't be used in 'await' expression")>
Traceback (most recent call last):
  File "/home/$USER/.local/lib/python3.10/site-packages/discord/client.py", line 348, in _run_event
    await self.on_error(event_name, *args, **kwargs)
  File "/home/$USER/.local/lib/python3.10/site-packages/discord/client.py", line 343, in _run_event
    await coro(*args, **kwargs)
TypeError: object NoneType can't be used in 'await' expression
```
- It is nothing fatal. To eliminate this error message, go to `/home/$USER/.local/lib/python3.10/site-packages/discord/client.py` (on Linux) or `<Your Python installation path>\Lib\site-packages\discord\client.py` (on Windows), `line 341` and edit the function's content as follows:
```
async def _run_event(self, coro, event_name, *args, **kwargs):
        # try:
        #     await coro(*args, **kwargs)
        # except asyncio.CancelledError:
        #     pass
        # except Exception:
        #     try:
        #         await self.on_error(event_name, *args, **kwargs)
        #     except asyncio.CancelledError:
        #         pass
        try:
            await coro(*args, **kwargs)
        except:
            pass
```
### PytzUsageWarning
```
/home/$USER/.local/lib/python3.10/site-packages/apscheduler/util.py:436: PytzUsageWarning: The localize method is no longer necessary, as this time zone supports the fold attribute (PEP 495). For more details on migrating to a PEP 495-compliant implementation, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html
  return tzinfo.localize(dt)
```
- Include these lines of code at the beginning of `/lib/bot/__init__.py` to disble all warnings:
```
# Disable warnings
import warnings
warnings.filterwarnings("ignore")
```
