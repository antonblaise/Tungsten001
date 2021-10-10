import os

requirements = [
    "discord.py",
    "apscheduler",
    "requests",
    "configobj",
    "configparser",
    "pytest-shutil",
    "typing",
    "-U git+https://github.com/Rapptz/discord-ext-menus"
]

for package in requirements:
    os.system(f"pip install {package}")