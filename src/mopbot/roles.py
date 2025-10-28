import logging

import discord

logger = logging.getLogger(__name__)

async def apply_perms(client, roles, env):
    """Overwrites roles' permissions with the ones configured by the bot."""
    guild = client.get_guild(env["guild_id"])
    for category in roles:
        configured_perms = category["permissions"]
        for role in category["roles"]:
            new_perms = discord.Permissions()
            for perm in configured_perms:
                setattr(new_perms, perm, configured_perms[perm])
    
            role_id = env["roles"][role]
            logger.info(f"Updating role '{role}' (Role ID: {role_id}): {new_perms}")
            await guild.get_role(role_id).edit(permissions=new_perms)
