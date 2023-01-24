import discord
import os
from command import Command
from discord.ext import commands
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        await client.add_cog(Command(client))


    client.run(TOKEN)
