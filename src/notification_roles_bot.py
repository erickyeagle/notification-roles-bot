#!/usr/bin/env python

# Imports
import os
import sys
from discord import Embed, Guild, Member, Permissions, Role
from discord.ext.commands import Bot, bot_has_guild_permissions, CommandError, CommandInvokeError, CommandNotFound, Context, guild_only, MissingRequiredArgument, NoPrivateMessage, RoleConverter, TooManyArguments
from typing import Optional

# Strings
GUILD_CONTEXT_REQUIRED_ERROR   = 'Uh-oh...this command is only valid in a guild context!'
ROLE_ADD_TO_GUILD_ERROR        = 'Uh-oh...the role "{0}" could not be added to your guild!'
ROLE_ADD_TO_MEMBER_ERROR       = 'Uh-oh...the role {0.mention} could not be added to you!'
ROLE_ADDED_TO_GUILD            = 'The role {0.mention} has been added to your guild!'
ROLE_ADDED_TO_MEMBER           = 'The role {0.mention} has been added to you!'
ROLE_FOUND_IN_GUILD_ERROR      = 'Uh-oh...your guild already has the role {0.mention}!'
ROLE_FOUND_IN_MEMBER_ERROR     = 'Uh-oh...you already have the role {0.mention}!'
ROLE_NOT_COMPATIBLE_ERROR      = 'Uh-oh...the role {0.mention} is not a notification role!'
ROLE_NOT_FOUND_IN_GUILD_ERROR  = 'Uh-oh...your guild does not have the role "{0}"!'
ROLE_NOT_FOUND_IN_MEMBER_ERROR = 'Uh-oh...you don\'t have the role {0.mention}!'
ROLE_REMOVED_FROM_MEMBER       = 'The role {0.mention} has been removed from you!'
SYNTAX                         = 'Syntax: !nr {list | {add | sub[scribe] | unsub[scribe]} ROLE}'
UNHANDLED_EXCEPTION            = 'It looks like you found a bug in Notification Roles Bot. If you would like to help us out, please file an issue on [GitHub](https://github.com/erickyeagle/notification-roles-bot/issues). Thank you!'

# Initializes the bot.
bot: Bot = Bot(case_insensitive = True, command_prefix = '!', help_command = None)

# Converts a role name or mention string into a Role object.
async def convert_str_to_role(context: Context, role_str: str) -> Optional[Role]:
    try:
        role: Optional[Role] = await RoleConverter().convert(context, role_str)
        return role
    except:
        return None

# Returns whether the role is a notification role. A role is a notification role if 1) it is
# mentionable, 2) it has no permissions, and 3) the role is in the bot's roles list.
def is_notification_role(guild: Guild, role: Role) -> bool:
    return role.mentionable == True               and \
           role.permissions == Permissions.none() and \
           role in guild.me.roles

# Loads the Discord bot token from the environment and starts the bot.
def run():
    notification_roles_bot_token: str = os.environ.get('NOTIFICATION_ROLES_BOT_TOKEN')
    if not notification_roles_bot_token:
        print('The environment variable "NOTIFICATION_ROLES_BOT_TOKEN" is not set!', file = sys.stderr)
        return
    bot.run(notification_roles_bot_token)

# This is the initial bot command entrance. This bot uses command groups for specific behavior.
@bot.group(case_insensitive = True)
@bot_has_guild_permissions(manage_roles = True, read_messages = True, send_messages = True)
@guild_only()
async def nr(context: Context):
    if context.invoked_subcommand is None:
        raise CommandInvokeError

# Adds a notification role to the guild.
@nr.command(ignore_extra = False)
@bot_has_guild_permissions(manage_roles = True, read_messages = True, send_messages = True)
@guild_only()
async def add(context: Context, role_str: str):
    role: Optional[Role] = await convert_str_to_role(context, role_str)
    if role is not None:
        await context.reply(embed = Embed(description = ROLE_FOUND_IN_GUILD_ERROR.format(role)))
        return
    guild:       Optional[Guild] = context.guild
    permissions: Permissions     = Permissions().none()
    role: Optional[Role] = await guild.create_role(mentionable = True, name = role_str, permissions = permissions)
    if role is None:
        await context.reply(embed = Embed(description = ROLE_ADD_TO_GUILD_ERROR.format(role_str)))
        return
    await guild.me.add_roles(role)
    await context.reply(embed = Embed(description = ROLE_ADDED_TO_GUILD.format(role)))

# Lists all notification roles for the current guild.
@nr.command(ignore_extra = False)
@bot_has_guild_permissions(manage_roles = True, read_messages = True, send_messages = True)
@guild_only()
async def list(context: Context):
    guild: Optional[Guild] = context.guild
    roles: [Role]          = [role for role in guild.roles if is_notification_role(guild, role)]
    if roles is not None and len(roles) > 0:
        await context.reply(embed = Embed(description = ", ".join(map(lambda role: role.mention, roles))))

# Subscribes a user to a notification role.
@nr.command(aliases = ['sub'], ignore_extra = False)
@bot_has_guild_permissions(manage_roles = True, read_messages = True, send_messages = True)
@guild_only()
async def subscribe(context: Context, role_str: str):
    role: Optional[Role] = await convert_str_to_role(context, role_str)
    if role is None:
        await context.reply(embed = Embed(description = ROLE_NOT_FOUND_IN_GUILD_ERROR.format(role_str)))
        return
    guild: Optional[Guild] = context.guild
    if not is_notification_role(guild, role):
        await context.reply(embed = Embed(description = ROLE_NOT_COMPATIBLE_ERROR.format(role)))
        return
    member: Member = context.author
    if role in member.roles:
        await context.reply(embed = Embed(description = ROLE_FOUND_IN_MEMBER_ERROR.format(role)))
        return
    await member.add_roles(role)
    await context.reply(embed = Embed(description = ROLE_ADDED_TO_MEMBER.format(role)))

# Unsubscribes a user from a notification role.
@nr.command(aliases = ['unsub'], ignore_extra = False)
@bot_has_guild_permissions(manage_roles = True, read_messages = True, send_messages = True)
@guild_only()
async def unsubscribe(context: Context, role_str: str):
    role: Optional[Role] = await convert_str_to_role(context, role_str)
    if role is None:
        await context.reply(embed = Embed(description = ROLE_NOT_FOUND_IN_GUILD_ERROR.format(role_str)))
        return
    guild: Optional[Guild] = context.guild
    if not is_notification_role(guild, role):
        await context.reply(embed = Embed(description = ROLE_NOT_COMPATIBLE_ERROR.format(role)))
        return
    member: Member = context.author
    if not role in member.roles:
        await context.reply(embed = Embed(description = ROLE_NOT_FOUND_IN_MEMBER_ERROR.format(role)))
        return
    await member.remove_roles(role)
    await context.reply(embed = Embed(description = ROLE_REMOVED_FROM_MEMBER.format(role)))
    if len(role.members) == 1 and guild.me in role.members:
        await role.delete()

# The default command error handler provided by the bot.
@bot.event
async def on_command_error(context: Context, error: CommandError):
    if isinstance(error, CommandNotFound):
        return
    if isinstance(error, (CommandInvokeError, MissingRequiredArgument, TooManyArguments)):
        await context.reply(embed = Embed(description = SYNTAX))
        return
    if isinstance(error, NoPrivateMessage):
        await context.reply(embed = Embed(description = GUILD_CONTEXT_REQUIRED_ERROR))
        return
    embed: Embed = Embed()
    embed.add_field(name = error, value = UNHANDLED_EXCEPTION)
    await context.reply(embed=embed)

# Called when the client is done preparing the data received from Discord.
@bot.event
async def on_ready():
    print('\n{0.user} is online!'.format(bot))

# The "main" method essentially. The body of this conditional is executed when this script is
# executed as the main module (ie. not imported by another module)
if __name__ == '__main__':
    run()
