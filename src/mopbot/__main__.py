import os
import discord

from . import config

BOT_TOKEN = os.environ.get("BOT_TOKEN")
intents = discord.Intents.default()
client = discord.Client(intents=intents)

config.validate(config.config)


# client.run(BOT_TOKEN)
