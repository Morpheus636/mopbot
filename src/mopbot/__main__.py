import os
import sys

import discord

from . import configuration
from . import roles

# Config checking
BOT_TOKEN = os.environ.get("BOT_TOKEN")
file = "config.yaml"
if len(sys.argv) > 1:
    file = sys.argv[1]
config = configuration.load(file)
configuration.validate(config)

# Setup Discord API
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await roles.apply_perms(client, config)
    await client.close()

client.run(BOT_TOKEN)
