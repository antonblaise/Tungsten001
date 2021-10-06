from lib.bot import bot
import os

VERSION = "1.4.3"

os.system('cls' if os.name == 'nt' else 'clear')
bot.run(VERSION)
