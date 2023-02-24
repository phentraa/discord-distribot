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


def get_member(name: str):
    return discord.utils.get(get_guild().members, name=name)


def remove_mentions_from(message_content: str) -> str:
    return re.sub('<@[0-9]*>', '', message_content)


# EVENT HANDLERS -------------------------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = get_guild()

    print(f'Connected to the following guild: {guild.name} - {guild.id}')
    # print('Members:')
    # print('\n'.join([member.name for member in guild.members]))


@bot.event
async def on_message(message: discord.Message):

    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    # print(f'Message on: #{message.channel.name}')
    # print(f'Author: {message.author}')
    # print(f'Content: {message.content}')
    # member_to = get_member(name='Kovács Péter')

    if bot.user.mentioned_in(message):
        await message.add_reaction(('\N{PARTY POPPER}'))

        clean_content = remove_mentions_from(message.content)

        for user in message.mentions:
            if user == bot.user:
                continue
            # print(f'Message to: {user} --> {clean_content}')
            await user.create_dm()
            await user.dm_channel.send(clean_content)


@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error on event {event}')
    print(f'Problem: {args[0]}')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send('Something aint right with this command...')


# COMMANDS -------------------------------------------------------------------------------------------------------------

@bot.command(name='users', help='Shows users grouped by roles. Extended: users admin --> only users with admin role')
async def show_users_by_group(ctx, role: str = commands.parameter(default='all', description='Add a specific role')):
    print(f'Value of the role parameter: {role}')
    await ctx.send('I will show the users grouped by roles.')


@bot.command(name='roles', help='Shows the available roles on the guild.')
async def show_roles(ctx):
    available_roles = 'none'
    await ctx.send(f'Available roles:\n {available_roles}')


if __name__ == '__main__':
    bot.run(TOKEN)
