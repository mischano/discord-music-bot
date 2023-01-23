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
        bot_channel_obj = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_channel_obj is None:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        bot_channel_id = bot_channel_obj.channel.id
        bot_current_channel = client.get_channel(bot_channel_id)
        if bot_current_channel is None:
            f_info = getframeinfo(currentframe())
            await ctx.send("usage: channel not found. %s : %s" % (f_info.filename, f_info.lineno))

        channel_members = len(bot_current_channel.members)

        if channel_members == 1:
            await disconnect_bot(ctx)
            return

        caller_channel_obj = ctx.author.voice
        if caller_channel_obj is None:
            await ctx.send("Sorry, can't leave. I'm in the voice channel with someone.\n")
            return
        else:
            caller_channel_id = caller_channel_obj.channel.id
            if caller_channel_id == bot_channel_id:
                await disconnect_bot(ctx)
                return
            else:
                await ctx.send("Sorry, can't leave. I'm in the different voice "
                               "channel (not alone!).\n")
                return

    async def disconnect_bot(ctx):
        vc = ctx.guild.voice_client
        await vc.disconnect()
        await ctx.send("Bye!")

    client.run(TOKEN)
