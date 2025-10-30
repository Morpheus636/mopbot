import logging

import discord

logger = logging.getLogger(__name__)
MISSING = discord.utils.MISSING


class Role:
    def __init__(this, config_id: str, discord_id: int, guild: discord.Guild):
        """Instantiates a Role object used to store role attributes locally to optimize API calls.

        Args:
            config_id (str): The identifier from config.yml used to define this role.
            discord_id (int): The Discord ID associated with this role in the active environmment.
            guild(discord.Guild): the discord.py Guild object representing the active environment.
        """
        this.config_id: str = config_id
        this.discord_id: int = discord_id
        this.guild: discord.Guild = guild
        this.name: str = MISSING
        this.color: int = MISSING
        this.hoist: bool = MISSING
        this.mentionable: bool = MISSING
        this.perms: discord.Permissions = discord.Permissions()
        this._updated_nodes: list = []

    async def update_settings(
        this, name: str = None, color: str = None, hoist: bool = None, mentionable: bool = None
    ) -> None:
        """Updates the stored role settings.
        Changes are not applied via the Discord API until Role.apply() is called.

        Args:
            name (str, optional): The new name for the role.
            color (str, optional): The new color code for the role.
            hoist (bool, optional): Whether or not the role is displayed separately.
            mentionable (bool, optional): Whether or not the role is mentionable by everyone.
        """
        if name is not None:
            if this.name is not MISSING:
                logger.warning(f"Name for role '{this.config_id}' is being overwritten")
            this.name = name
            logger.info(
                f"Updating role '{this.config_id}' (Role ID: {this.discord_id}): name={this.name}"
            )

        if color is not None:
            if this.color is not MISSING:
                logger.warning(f"Color for role '{this.config_id}' is being overwritten")
            # Convert hex color string to integer. Allows for leading # but does not require it.
            this.color = int(color.lstrip("#"), 16)
            logger.info(
                f"Updating role '{this.config_id}' (Role ID: {this.discord_id}): color={this.color}"
            )

        if hoist is not None:
            if this.hoist is not MISSING:
                logger.warning(f"Hoist for role '{this.config_id}' is being overwritten")
            this.hoist = hoist
            logger.info(
                f"Updating role '{this.config_id}' (Role ID: {this.discord_id}): hoist={this.hoist}"
            )

        if mentionable is not None:
            if this.mentionable is not MISSING:
                logger.warning(f"Mentionable for role '{this.config_id}' is being overwritten")
            this.mentionable = mentionable
            logger.info(
                f"Updating role '{this.config_id}' (Role ID: {this.discord_id}): mentionable={this.mentionable}"
            )

    async def update_perms(this, new_perms: dict) -> None:
        """Apples the specified permissions to the stored discord.Permissions object.
        Changes are not applied via the Discord API until Role.apply() is called.

        Args:
            new_perms (dict): A dictionary of permissions to apply, where the keys are names of
            discord.Permissions attributes and the values are booleans.
        """
        for perm in new_perms:
            if perm in this._updated_nodes:
                logger.warning(
                    f"Permission '{perm}' for role '{this.config_id}' is being overwritten."
                )
            else:
                this._updated_nodes.append(perm)
            setattr(this.perms, perm, new_perms[perm])
        logger.info(f"Updating role '{this.config_id}' (Role ID: {this.discord_id}): {this.perms}")

    async def apply(this) -> None:
        """Applies"""
        logger.info(f"Applying changes to role {this.config_name}")
        role = this.guild.get_role(this.discord_id)
        await role.edit(
            name=this.name,
            permissions=this.perms,
            color=this.color,
            hoist=this.hoist,
            mentionable=this.mentionable,
        )


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
            if definition.get("permissions"):
                await role.update_perms(definition["permissions"])

            # Add the other role options to the Role object.
            await role.update_settings(
                name=definition.get("name"),
                color=definition.get("color"),
                hoist=definition.get("hoist"),
                mentionable=definition.get("mentionable"),
            )

    # Unless running as a dry run, apply the changes to each role via the API.
    if env["dry_run"] is False:
        for role in roles:
            await role.apply()
