import discord
import os
from command import Command
from player import Player
from discord.ext import commands
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    # TOKEN = os.getenv("TOKEN")
    TOKEN = "MTA2NjYwMjAwODg4NDMwMTg1NA.G7pms3.CBmh1kJTdzA9Dleo-yyv8GWSbaviQk4EtZdfPw"
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        player = Player(client)
        await client.add_cog(player)
        await client.add_cog(Command(client, player))


    client.run(TOKEN)
