# https://discordpy.readthedocs.io/en/stable/index.html

import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message: discord.Message):
    print(f'Message on: #{message.channel.name}') # AttributeError: 'DMChannel' object has no attribute 'name'
    print(f'Author: {message.author}')
    print(message.content)
    await message.add_reaction('\N{PARTY POPPER}')

    guild = discord.utils.get(client.guilds, name=GUILD)
    member_to = discord.utils.get(guild.members, name='Kovács Péter')

    await member_to.create_dm()
    await member_to.dm_channel.send(message.content)


@client.event
async def on_ready():
    """Called after the connection established and the server sent back a lot of information."""
    print(f'{client.user} has connected to Discord!')

    # 1. variation
    # for guild in client.guilds:
    #     if guild.name == GUILD:
    #         print(f'Connected to the following guild: {guild.name} - {guild.id}')
    #         print('Members:')
    #         print('\n'.join([member.name for member in guild.members]))
    #         break

    # 2. variation
    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f'Connected to the following guild: {guild.name} - {guild.id}')
    print('Members:')
    print('\n'.join([member.name for member in guild.members]))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, üdv a csatornán! :)')

client.run(TOKEN)