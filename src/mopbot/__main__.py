import argparse
import logging
import os

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

# Load command-line arguments
parser = argparse.ArgumentParser(
    prog="mopbot", description="A declarative configuration tool for Discord servers."
)
parser.add_argument("file", nargs="?", default="config.yaml", help="The config file to use.")
parser.add_argument(
    "-C",
    "--check",
    action="store_true",
    help="Validate the config file against the schema but take no action.",
)
args = parser.parse_args
args = parser.parse_args()

# Load config
config = configuration.load(args.file)
configuration.validate(config)
if args.check is True:
    exit()

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
