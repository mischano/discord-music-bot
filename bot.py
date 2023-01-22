import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def run():
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.command()
    async def play(ctx):
        await ctx.send("hello!")

    client.run(TOKEN)
