import discord
import asyncio
from discord.ext import commands


async def disconnect_bot(ctx, msg):
    vc = ctx.guild.voice_client
    await vc.disconnect()
    # self.cleanup()
    if len(msg) != 0:
        await ctx.send(msg)


class Command(commands.Cog):
    def __init__(self, client, player):
        # Bot
        self.client = client
        self.bot_channel_name = None
        self.bot_channel_id = None
        self.bot_channel_member_num = None

        # Player
        self.player = player

        # Caller
        self.caller_channel_name = None
        self.caller_channel_id = None

    def cleanup(self):
        self.bot_channel_name = None
        self.bot_channel_id = None
        self.bot_channel_member_num = None

        # Caller
        self.caller_channel_name = None
        self.caller_channel_id = None

        # Player
        self.player.vc = None
        self.player.is_playing = False
        self.player.paused = False
        self.player.current_song = None
        self.player.last_added = None

    async def get_caller_channel(self, ctx, msg):
        caller = ctx.author.voice
        if caller is None:
            await ctx.send(msg)
            return False

        self.caller_channel_name = caller.channel
        self.caller_channel_id = caller.channel.id
        return True

    @commands.command()
    async def play(self, ctx, *args):
        if not await self.join(ctx):
            return

        query = " ".join(args)
        if self.player.search(query) is False:
            await ctx.send("Could not find the song")
            return

        await self.player.player(ctx)

    @commands.command()
    async def isconnected(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        print("is_connected(): ", voice.is_connected())

        _id = voice.channel.id
        print("bot is connected to channel: " + str(ctx.bot.get_channel(_id)))

        voice2 = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        print("is_connected(): ",  voice2.is_connected())

        _id2 = voice2.channel.id
        print("bot is connected to channel: ", str(ctx.bot.get_channel(_id2)))

        # voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # print(voice.is_connected())
        # _id = voice.channel.id
        # print(voice.get_channel(_id))
        # bot_channel_obj = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        # if bot_channel_obj is None:
        #     return False
        #
        # self.bot_channel_id = bot_channel_obj.channel.id
        # self.bot_channel_name = self.bot.get_channel(self.bot_channel_id)
        # self.bot_channel_member_num = len(self.bot_channel_name.members)
        # print(id)
        # print(voice.get_channel(_id).memebers)

        # self.bot_channel_name = self.bot.get_channel(self.bot_channel_id)
        # self.bot_channel_member_num = len(self.bot_channel_name.members)

    @commands.command()
    async def join(self, ctx):
        caller = ctx.message.author.voice
        if caller is None:
            await ctx.send("You are not connected to a voice channel")
            return
        await caller.channel.connect(timeout=5, reconnect=False, self_mute=False, self_deaf=True)
        print("Never executes")
        # if await self.get_caller_channel(ctx, "You are not connected to voice channel.") is False:
        #     return False
        # try:
        #     # VoiceChannel.connect never returns! Bug from API's side.
        #     self.player.vc = await self.caller_channel_name.connect(timeout=.5, reconnect=False, self_mute=False,
        #                                                             self_deaf=True)
        #     # return True
        # except discord.ClientException:  # You already connected to a voice channel
        #     if self.get_channel_info(ctx) is False:
        #         await ctx.send("Failed in *get_channel_info*.")
        #         return False
        #     if self.bot_channel_member_num == 1:
        #         print("single channel member")
        #         voice_client = ctx.message.guild.voice_client
        #         print(voice_client.is_connected())
        #         await voice_client.disconnect()
        #         # await disconnect_bot(ctx, "")  # try using move_to
        #         # self.player.vc = await self.caller_channel_name.connect(timeout=.5, reconnect=False, self_mute=False,
        #                                                                 # self_deaf=True)
        #         return True
        #     else:
        #         if self.caller_channel_name == self.bot_channel_name:
        #             print("already in the same channel")
        #             return True
        #         else:
        #             await ctx.send("Bot is already connected to a voice channel.")
        #             return False
        # except asyncio.TimeoutError:
        #     print("HELL")
        #     await ctx.send("Bot could not connect to the voice channel in time.")

    @commands.command()
    async def leave(self, ctx):
        if self.get_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel...")
            return

        if self.bot_channel_member_num == 1:
            await disconnect_bot(ctx, "Bye!")
            return

        if await self.get_caller_channel(ctx, "Sorry, can't leave. I'm in the voice channel with someone.\n") is False:
            return
        else:
            if self.caller_channel_id == self.bot_channel_id:
                await disconnect_bot(ctx, "Bye!")
                return
            else:
                await ctx.send("Sorry, can't leave. I'm in the different voice "
                               "channel (not alone!).\n")
                return

    @commands.command()
    async def skip(self, ctx):
        pass

    @commands.command()
    async def shuffle(self, ctx):
        pass

    @commands.command()
    async def pause(self, ctx):
        if await self.get_caller_channel(ctx, "You are not connected to voice channel") is False:
            return

        if self.get_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.pause_music() is False:
                await ctx.send("Nothing to pause")
            else:
                title = '*' + self.player.current_song['title'] + '*'
                await ctx.send("**Paused: ** " + title)
        else:
            await ctx.send("Cannot pause. Join the voice channel to control the bot.")

    @commands.command()
    async def resume(self, ctx):
        pass

    @commands.command()
    async def loop(self, ctx):
        pass

    def get_channel_info(self, ctx):
        bot_channel_obj = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_channel_obj is None:
            return False

        self.bot_channel_id = bot_channel_obj.channel.id
        self.bot_channel_name = self.bot.get_channel(self.bot_channel_id)
        self.bot_channel_member_num = len(self.bot_channel_name.members)
        return True
