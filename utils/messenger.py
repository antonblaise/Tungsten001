from datetime import datetime
from random import choice, randint
from requests import get
from discord import DMChannel, Intents
from lib.bot.__init__ import Bot, TimeKeeper

timekeeper = TimeKeeper()
bot = Bot()

intents = Intents.default()
intents.members = True

async def directMessage(message):
    if isinstance(message.channel, DMChannel): # When someone PMs the bot
        print(f"[{datetime.now().strftime('%H:%M:%S')}] if isinstance(message.channel, DMChannel):")
        if message.content.lower() == "ovpn":
            print(f"[{datetime.now().strftime('%H:%M:%S')}] if message.content.lower() == 'ovpn':")
            await bot.send_ovpn(message)
        elif message.content.lower() in ["ip","ipinfo"]:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] elif message.content.lower() in ['ip,'ipinfo']:")
            await message.channel.send(get('https://ipinfo.io/').content.decode('utf8'))
            await bot.man_log_ip(message)
        elif message.content.lower() in ["iplog","logip"]:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] elif message.content.lower() in ['iplog','logip']:")
            await bot.man_log_ip(message)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] else:")
            res_directMessage = await casualMessaging(message)
            return res_directMessage
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] outer else")
        if bool([ele for ele in ['894108315896938548','@eula'] if(ele in message.content.lower())]):
        # If someone pings the bot
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message.author.name} mentioned the bot.")
            if [ele for ele in ["weather"] if(ele in message.content.lower())]:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] weather forecast on request by {message.author.name}")
                return "weather forecast request"
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] if mention in message.content:")
                res_directMessage = await casualMessaging(message)
                return res_directMessage
        else:
            pass

async def casualMessaging(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] casualMessaging")
    check1 = bool([ele for ele in ["hi","hello","hey"] if(ele in message.content.lower())])
    check2 = bool([ele for ele in ["good morning","good evening","good afternoon"] if(ele in message.content.lower())])
    check3 = bool([ele for ele in ["good night","goodnight","goodnite","g9 ","gud9"] if(ele in message.content.lower())])
    check4 = bool([ele for ele in ["tq ","thank you","thx ","thanks","arigato"] if(ele in message.content.lower())])
    check5 = bool([ele for ele in ["love you"] if(ele in message.content.lower())])
    check6 = bool([ele for ele in ["who is this","who are you","introduce yourself","self introduce","self intro"] if(ele in message.content.lower())])
    check7 = bool([ele for ele in ["how are you","how's it going"] if(ele in message.content.lower())])
    subcheck1 = bool([ele for ele in ["❤️","😘","💕"] if(ele in message.content)])
    print(f"[{datetime.now().strftime('%H:%M:%S')}] subcheck: {subcheck1}")
    if check1:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] if check1:")
        reply = f"{choice(('Hello', 'Hi', 'Hey', 'Konichiwa','Good '+timekeeper.period_now))} {message.author.name}! "
        if subcheck1:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Adding random heart emojis")
            for _ in range(randint(1, 3)):
                reply += f'{choice(("❤️","😘","💕"))}'
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FINAL REPLY: {reply}")
        await message.channel.send(reply)
    elif check2:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif check2:")
        reply = f"{'Good '+timekeeper.period_now} {message.author.name}! "
        if subcheck1:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Adding random heart emojis")
            for _ in range(randint(1, 3)):
                reply += f'{choice(("❤️","😘","💕"))}'
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FINAL REPLY: {reply}")
        await message.channel.send(reply)
    elif check3:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif check3:")
        reply = f"Good night, {message.author.name}. {choice(('Sweet dreams.', 'Have a good sleep.', 'Hope you sleep well.'))} "
        if subcheck1:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Adding random heart emojis")
            for _ in range(randint(1, 3)):
                reply += f'{choice(("❤️","😘","💕"))}'
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FINAL REPLY: {reply}")
        await message.channel.send(reply)
    elif check4:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif check4:")
        await message.channel.send(f"{choice(('No prob!', 'My pleasure!', 'Glad to help! :heart:'))} ")
    elif check5:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif check5:")
        reply = f"{choice(('Love you too!', '', 'Love you!'))} "
        for _ in range(randint(0, 4)):
            reply += f'{choice(("❤️","😘","💕"))}'
        reply += f" {message.author.mention}"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FINAL REPLY: {reply}")
        await message.channel.send(reply)
    elif check6:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif check6:")
        return "name card"
    elif check7:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif check7:")
        apos = "'"
        await message.channel.send(f"{choice(('Doing great! :sunglasses:', 'Feeling productive! :muscle:', f'I{apos}m good! Thanks for asking, {message.author.mention}! :wink:'))} ")
    elif subcheck1:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] elif subcheck1:")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Adding random heart emojis")
        reply = f""
        for _ in range(randint(1, 3)):
            reply += f'{choice(("❤️","😘","💕"))}'
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FINAL REPLY: {reply}")
        await message.channel.send(reply)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] casualMessaging: else")

