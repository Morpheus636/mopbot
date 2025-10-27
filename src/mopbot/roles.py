import discord

from .config import config

async def apply_perms(client):
    """Overwrites roles' permissions with the ones configured by the bot."""
    guild = client.get_guild(config["guild_id"])
    for category in config["roles"]:
        configured_perms = category["permissions"]
        for role in category["role_ids"]:
            new_perms = discord.Permissions()
            for perm in configured_perms:
                setattr(new_perms, perm, configured_perms[perm])
            await guild.get_role(role).edit(permissions=new_perms)
