import logging
import os
import sys

import discord
import dotenv

from . import configuration
from . import roles

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s (%(name)s): %(message)s")

# Load environment variables
dotenv.load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ENV = os.environ.get("ENV", "production")

# Load config
file = "config.yaml"
if len(sys.argv) > 1:
    file = sys.argv[1]
config = configuration.load(file)
configuration.validate(config)

logger.info(f"Using '{ENV}' environment")
env = config["environments"][ENV]
logger.debug(f"Environment: {env}")

# Setup Discord API
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await roles.apply_perms(client, config["roles"], env)

    logger.info("Tasks finished. Disconnecting from gateway")
    await client.close()

client.run(BOT_TOKEN, log_handler=None)
