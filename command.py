import discord
import asyncio
import time
from discord.ext import commands


class Command(commands.Cog):
    def __init__(self, client, player):
        # Bot
        self.client = client
        self.bot = None
        self.bot_channel_name = None
        self.bot_channel_id = None
        self.bot_channel_member_num = None

        # Player
        self.player = player

        # Caller
        self.caller_channel_name = None
        self.caller_channel_id = None

    @commands.command()
    async def play(self, ctx, *args):
        if not await self.join(ctx):
            print("Failed to join")
            return

        query = " ".join(args)
        if self.player.search(query) is False:
            await ctx.send("Fail: song was not found.")
            return

        # time.sleep(4)
        await self.player.player(ctx)

    @commands.command()
    async def stop(self, ctx):
        self.player.vc.stop()
        return

    @commands.command()
    async def join(self, ctx):
        if await self.get_caller_channel(ctx, "You are not connected to a voice channel.") is False:
            return False
        try:
            self.player.vc = await self.caller_channel_name.connect(timeout=.5, reconnect=True, self_mute=False,
                                                                    self_deaf=True)
            if isinstance(self.player.vc, discord.VoiceProtocol): 
                # print("inside isinstance:\n\n")
                await ctx.send("Bot has connected to " + str(self.caller_channel_name))
            return True
        except discord.ClientException:
            # Not sure if 'if' statement will ever execute because if it does, it means that bot is connected to 
            # some voice channel. If it is connected, then get_bot_channel_info should not return False. 
            if self.get_bot_channel_info(ctx) is False:
                await ctx.send("Failed in *get_channel_info*. Please report the issue to **sheriff**. Thank you!")
                return False
            if self.bot_channel_member_num == 1:
                self.player.clear_music_queue()
                # await self.bot.move_to(self.caller_channel_name)
                # check if vc cleaning is needed! 
                await disconnect_bot(ctx, "")
                await self.join(ctx)                
                return True
            else:
                if self.caller_channel_name == self.bot_channel_name:
                    # await ctx.send("Bot is in the voice channel with you.")
                    return True
                else:
                    await ctx.send("Bot is already connected to a voice channel.")
                    return False
        except asyncio.TimeoutError:
            await ctx.send("Bot could not connect to the voice channel in time.")

    @commands.command()
    async def leave(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.bot_channel_member_num == 1:
            await disconnect_bot(ctx, "Bye!")
            return

        if await self.get_caller_channel(ctx, "Bot is in the voice channel with other user(s).") is False:
            return
        else:
            if self.caller_channel_id == self.bot_channel_id:
                await disconnect_bot(ctx, "Bye!")
                return
            else:
                await ctx.send("Bot is in the voice channel with other user(s).")
                return

    @commands.command()
    async def skip(self, ctx):
        if await self.get_caller_channel(ctx, "You are not connected to a voice channel.") is False:
            return False
        
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return
        
        if self.caller_channel_id != self.bot_channel_id:
            await ctx.send("Can't skip. Join the voice channel to control the bot.")
            return 
        else:
            skipped_song = self.player.current_song['title']
            if self.player.skip_music(ctx) is False:
                await ctx.send("Nothing is playing.")
            else:
                await ctx.send("**Skipped: **" + skipped_song)
                return

    @commands.command()
    async def shuffle(self, ctx):
        pass

    @commands.command()
    async def pause(self, ctx):
        if await self.get_caller_channel(ctx, "You are not connected to a voice channel") is False:
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.pause_music() is False:
                await ctx.send("Nothing to pause.")
            else:
                title = '*' + self.player.current_song['title'] + '*'
                await ctx.send("**Paused: ** " + title)
        else:
            await ctx.send("Can't pause. Join the voice channel to control the bot.")

    @commands.command()
    async def resume(self, ctx):
        if await self.get_caller_channel(ctx, "You are not connected to a voice channel.") is False:
            return
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return
        
        if self.caller_channel_name == self.bot_channel_name:
            if self.player.resume_music() is False:
                await ctx.send("Nothing to resume.")
            else:
                title = '*' + self.player.current_song['title'] + '*'
                await ctx.send("**Resumes: ** " + title)
        else:
            await ctx.send("Can't resume. Join the voice channel to control the bot.")

    @commands.command()
    async def loop(self, ctx):
        pass

    def get_bot_channel_info(self, ctx):
        self.bot = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if self.bot is None:
            return False

        self.bot_channel_id = self.bot.channel.id
        self.bot_channel_name = self.client.get_channel(self.bot_channel_id)
        self.bot_channel_member_num = len(self.bot_channel_name.members)
        return True

    async def get_caller_channel(self, ctx, msg):
        caller = ctx.author.voice
        if caller is None:
            await ctx.send(msg)
            return False

        self.caller_channel_name = caller.channel
        self.caller_channel_id = caller.channel.id
        return True


async def disconnect_bot(ctx, msg):
    vc = ctx.guild.voice_client
    await vc.disconnect()
    if len(msg) != 0:
        await ctx.send(msg)
