import os
import discord

from . import config
from . import roles

# Config checking
BOT_TOKEN = os.environ.get("BOT_TOKEN")
config.validate(config.config)

# Setup Discord API
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await roles.apply_perms(client)
    await client.close()

client.run(BOT_TOKEN)
