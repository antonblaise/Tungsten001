from random import choice
from requests import get
from datetime import datetime
from discord import Embed

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
            embed = Embed(title=f"{city.upper()}, {datetime.now().strftime('%Y-%m-%d')}", description="6-hour weather forecast.", colour=0x30F9FF, timestamp=datetime.utcnow())             
            field = []
            binary = [True,False]
            for hours in range(len(x['hourly'][0:6])):
                    field.append((f"{datetime.utcfromtimestamp(x['hourly'][hours]['dt']+x['timezone_offset']).strftime('%H:%M')} {emojis[icon_codes.index(x['hourly'][hours]['weather'][0]['icon'])]} {str(round(x['hourly'][hours]['temp']-273.15, 2))}°C", 
                                                            x['hourly'][hours]['weather'][0]['description'], binary[hours%2]))
            for name, value, inline in field:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=choice((random_eula_stickers)))
            embed.set_footer(text=f"Scheduled forecast")
            return embed
        else:
            return "Sorry, I can't fetch the weather data... "

async def autoLogIp():
        print(">> Logging IP automatically")
        log_path = "./data/db/ip.log"
        log_content = open(log_path).read().splitlines()
        timeNow = datetime.now().strftime("%H:%M:%S")
        dateToday = datetime.now().strftime("%d-%m-%Y")
        if log_content == []:
            log_content = f"{dateToday} {timeNow}\n{get('https://ifconfig.me').content.decode('utf8')}"
            open(log_path,'w').write(log_content)
            log_content = open(log_path).read().splitlines()
            r = f"IP address has been recorded on {log_content[0]}."
        else:
            if log_content[1] == get('https://ifconfig.me').content.decode('utf8'):
                r = f"The IP address has not changed since {log_content[0]}."
            else:
                log_content[0] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                log_content[1] = get('https://ifconfig.me').content.decode('utf8')
                open(log_path,'w').write('\n'.join(log_content))
                r = f"IP address has been updated on {log_content[0]}."
        return r