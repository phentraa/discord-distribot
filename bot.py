import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

# SETTINGS -------------------------------------------------------------------------------------------------------------
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


def get_intents():
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content = True

    return intents


bot = commands.Bot(command_prefix='!', intents=get_intents())

# UTILITY FUNCTIONS ----------------------------------------------------------------------------------------------------


def get_guild():
    return discord.utils.get(bot.guilds, name=GUILD)


def get_member_by(name: str):
    return discord.utils.get(get_guild().members, name=name)


def get_members_of(role: discord.Role) -> set:
    return set(filter(lambda member: role in member.roles, get_guild().members))


def get_role_by(name: str) -> discord.Role:
    return discord.utils.get(get_guild().roles, name=name)


def remove_mentions_from(message_content: str) -> str:
    return re.sub('<@&*[0-9]*>', '', message_content)


# EVENT HANDLERS -------------------------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = get_guild()

    print(f'Connected to the following guild: {guild.name} - {guild.id}')


@bot.event
async def on_message(message: discord.Message):

    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    if bot.user.mentioned_in(message):
        await message.add_reaction('\N{ROBOT FACE}')

        clean_content = remove_mentions_from(message.content)
        header = f'From {message.author.name} on #{message.channel}\n{message.jump_url}\n\n'

        recipients = set()

        for role in message.role_mentions:
            recipients.update(get_members_of(role))

        for user in message.mentions:
            if user != bot.user:
                recipients.add(user)

        for recipient in recipients:
            await recipient.create_dm()
            await recipient.dm_channel.send(header + clean_content)


@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error on event {event}')
    print(f'Problem: {args[0]}')


@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send('Something aint right with this command...')


# COMMANDS -------------------------------------------------------------------------------------------------------------

@bot.command(name='users', help='Shows users grouped by roles. Extended: users admin --> only users with admin role')
async def show_users_by_group(ctx, role: str = commands.parameter(default='all', description='Add a specific role')):
    message = f'A szerver felhasználói szerepek szerint (role={role}):\n'
    groups = dict()
    if role == 'all':
        for member in get_guild().members:
            for role in member.roles:
                if role.name == '@everyone':
                    continue
                if role.name not in groups.keys():
                    groups[role.name] = []
                groups[role.name].append(member.name)

        for role, users in groups.items():
            message += f'{role} --> {" ".join(users)}\n'
    else:
        role_members = get_members_of(get_role_by(role))
        member_names = [member.name for member in role_members]
        message += ' '.join(member_names)

    await ctx.send(message)


@bot.command(name='roles', help='Shows the available roles on the guild.')
async def show_roles(ctx):
    message = 'A szerveren elérhető szerepek:\n'
    for role in get_guild().roles:
        message += f'- {role.name.replace("@","")}\n'
    await ctx.send(message)


if __name__ == '__main__':
    bot.run(TOKEN)
