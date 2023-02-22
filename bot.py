import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Called after connection established and the server sent back a lot of information."""
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        if guild.name == GUILD:
            print(f'Connected to the following guild: {guild.name} - {guild.id}')
            print('Members:')
            print('\n'.join([member.name for member in guild.members]))
            break


client.run(TOKEN)