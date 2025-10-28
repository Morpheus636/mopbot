import os
import sys

import discord

from . import configuration
from . import roles

# Config checking
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ENV = os.environ.get("ENV", "production")
file = "config.yaml"
if len(sys.argv) > 1:
    file = sys.argv[1]
config = configuration.load(file)
configuration.validate(config)
env = config["environments"][ENV]

# Setup Discord API
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await roles.apply_perms(client, config["roles"], env)
    await client.close()

client.run(BOT_TOKEN)
