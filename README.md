# Tungsten001
This is my personal Discord bot, named after my favourite DPS in Genshin Impact, Eula Lawrence,
codenamed the toughest metal on earth, tungsten.

# Usage
- Save your Discord bot token in /lib/bot/token.0 (Create one if it's not there)
- Modify /lib/bot/\_\_init\_\_.py line 224 with your Discord server ID, 
  line 225 with the text channel ID that you want the bot to send messages to,
  and line 19 with your account ID (NOT your username). 
- For the IDs mentioned above, you can just right click on them and click "Copy ID".
- Save your OpenWeatherMap API key in /data/db/openweathermap_api.0 (Create one if it's not there)
- The bot responds to /\<command\>, send /help to view command lists.
- To request weather forecast, send: @\<the bot\> weather \<city or town\>
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
- The command prefix can be changed at line 18 of __/lib/bot/\_\_init\_\_.py__.
- Other parameters can be found and edited in ./data/db/auto_params.py
- The settings for auto weather forecast and auto ip logging can also be edited using the /\set command.