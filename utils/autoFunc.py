from random import choice
from requests import get
from datetime import datetime
from discord import Embed
from configobj import ConfigObj

async def autoWeatherForecast(city):
        api_key = str(open("./data/db/openweathermap_api.0").read())
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
        geocode = get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}").json()
        lat, lon = geocode[0]['lat'], geocode[0]['lon']
        exclude_parts = "current,minutely,daily,alerts"
        random_eula_stickers = open("./data/db/Eula_chibi.stickers").read().splitlines()
        x = get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}").json()
        if 'hourly' in x:
            embed = Embed(title=f"> **{city.upper()}**, {datetime.now().strftime('%Y-%m-%d')}", description=f"{int(ConfigObj('./data/db/auto_params.ini')['AUTO_WEATHER']['future_auto_weather'])}-hour weather forecast.", colour=0x30F9FF, timestamp=datetime.utcnow())             
            field = []
            offset = 0 if int(ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['interval_auto_weather']) == 1 else 1
            for hours in range(0, len(x['hourly'][0:int(ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['future_auto_weather'])]) + offset, int(ConfigObj("./data/db/auto_params.ini")['AUTO_WEATHER']['interval_auto_weather'])):
                field.append((
                        f"{datetime.utcfromtimestamp(x['hourly'][hours]['dt']+x['timezone_offset']).strftime('%H:%M')} {emojis[icon_codes.index(x['hourly'][hours]['weather'][0]['icon'])]}", 
                        f"> {str(round(x['hourly'][hours]['temp']-273.15, 2))}°C\n> *{str(round(x['hourly'][hours]['feels_like']-273.15, 2))}°C*\n> _{x['hourly'][hours]['weather'][0]['description']}_", 
                        True
                                ))
            for name, value, inline in field:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=choice((random_eula_stickers)))
            embed.set_footer(text=f"Scheduled forecast")
            return embed
        else:
            return f"> Sorry, I can't fetch the weather data... {choice(('😣', '😅', '😕'))}"

async def autoLogIp():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Logging IP automatically")
        open("data/db/ip.log", "a+")
        log_path = "./data/db/ip.log"
        log_content = open(log_path).read().splitlines()
        timeNow = datetime.now().strftime("%H:%M:%S")
        dateToday = datetime.now().strftime("%d-%m-%Y")
        try:
            ip_addr = get('https://ifconfig.me').content.decode('utf8')
        except:
            ip_addr = get('https://ipinfo.io/ip').content.decode('utf8')
        
        if log_content == []:
            log_content = f"{dateToday} {timeNow}\n{ip_addr}"
            open(log_path,'w').write(log_content)
            log_content = open(log_path).read().splitlines()
            r = f"> IP address has been recorded on {log_content[0]}."
        else:
            if log_content[1] == ip_addr:
                r = f"> The IP address has not changed since {log_content[0]}."
            else:
                log_content[0] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                log_content[1] = ip_addr
                open(log_path,'w').write('\n'.join(log_content))
                r = f"> IP address has been updated on {log_content[0]}."
        return r