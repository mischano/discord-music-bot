import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from inspect import currentframe, getframeinfo

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

    @client.command()
    async def join(ctx):
        voice = ctx.author.voice
        if voice is None:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = voice.channel
        try:
            await channel.connect(timeout=.5, self_mute=False, self_deaf=True)
        except discord.ClientException:
            await ctx.send("Bot is already connected to a voice channel.")
        except TimeoutError:
            await ctx.send("Bot connection timed out.")

    @client.command()
    async def leave(ctx):
        """
        If the bot is not in a voice channel, raise exception   DONE
        If the bot is by itself, then leave make the bot leave.
        If leave is called by a member in the same voice chat, then bot leaves.
        If leave is called by a member in a different voice chat:
            1. If the bot by itself then bot leaves.
            2. If the voice chat has other memebrs, then bot doesnt leave.
        """
        channel_obj = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if channel_obj is None:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        channel_id = channel_obj.channel.id
        current_channel = client.get_channel(channel_id)
        if current_channel is None:
            f_info = getframeinfo(currentframe())
            await ctx.send("usage: channel not found. %s : %s" % (f_info.filename, f_info.lineno))

        channel_members = len(current_channel.members)

        if channel_members == 1:
            vc = ctx.guild.voice_client
            await vc.disconnect()
            await ctx.send("Bye!")
            return
        

    client.run(TOKEN)
