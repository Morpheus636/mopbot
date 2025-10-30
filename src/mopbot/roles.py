import logging

import discord

logger = logging.getLogger(__name__)


class Role:
    def __init__(this, config_id: str, discord_id: int, guild: discord.Guild):
        """Instantiates a Role object used to store role attributes locally to optimize API calls.

        Args:
            config_id (str): The identifier from config.yml used to define this role.
            discord_id (int): The Discord ID associated with this role in the active environmment.
            guild(discord.Guild): the discord.py Guild object representing the active environment.
        """
        this.config_id = config_id
        this.discord_id = discord_id
        this.guild = guild
        this.perms = discord.Permissions()

    async def update_perms(this, new_perms: dict) -> None:
        """Apples the specified permissions to the stored discord.Permissions object.
        Changes are not applied via the Discord API until Role.apply() is called.

        Args:
            new_perms (dict): A dictionary of permissions to apply, where the keys are names of
            discord.Permissions attributes and the values are booleans.
        """
        for perm in new_perms:
            setattr(this.perms, perm, new_perms[perm])
        logger.info(f"Updating role '{this.config_id}' (Role ID: {this.discord_id}): {this.perms}")

    async def apply(this) -> None:
        """Applies"""
        logger.info(f"Applying changes to role {this.config_name}")
        await this.guild.get_role(this.discord_id).edit(permissions=this.perms)


async def apply_roles(client: discord.Client, role_definitions: dict, env: dict) -> None:
    """Overwrites roles' permissions with the ones configured by the bot.
    
    Args:
        client (discord.Client): A connected discord.py client for making API calls.
        role_definitions (list): All role definitions from the config file (see schema.json).
        env (dict): The active environment defined in the config file (see schema.json).
    """
    guild = client.get_guild(env["guild_id"])
    roles = {}

    # Apply each definition top to bottom:
    for definition in role_definitions:
        for config_id in definition["roles"]:

            # Get or make a Role object.
            role = roles.get(config_id)
            if role is None:
                role = Role(config_id, env["roles"][config_id], guild)
                roles[config_id] = role

            # Add the configured permissions to the Role object.
            await role.update_perms(definition["permissions"])

    # Unless running as a dry run, apply the changes to each role via the API.
    if env["dry_run"] is False:
        for role in roles:
            await role.apply()
