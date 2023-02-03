import discord
import asyncio
import misc
from discord.ext import commands


async def disconnect_bot(ctx):
    vc = ctx.guild.voice_client
    await vc.disconnect()
    vc.cleanup()


class Command(commands.Cog):
    def __init__(self, client, player):
        self.client = client
        self.bot = None
        self.bot_channel_name = None
        self.bot_channel_id = None
        self.bot_channel_member_num = None

        self.player = player

        self.caller_channel_name = None
        self.caller_channel_id = None

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        if not await self.join(ctx):
            return

        query = " ".join(args)
        if self.player.search(query) is False:
            await ctx.send("Bot has failed to find the song.")
            return

        self.player.player(ctx)

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        if await self.get_caller_channel(ctx) is False:
            ctx.send("You are not connected to a voice channel.")
            return False

        try:
            self.player.vc = await self.caller_channel_name.connect(
                timeout=.5, reconnect=True, self_mute=False, self_deaf=True)
        except discord.ClientException:
            if self.get_bot_channel_info(ctx) is False:
                await ctx.send("Failed in *get_channel_info*. Please report the issue to **sheriff**. Thank you!")
                return False
            if self.bot_channel_member_num == 1:
                self.player.clear_music_queue()
                await disconnect_bot(ctx)
                await self.join(ctx)
                return True
            else:
                if self.caller_channel_name == self.bot_channel_name:
                    return True
                else:
                    await ctx.send("Bot is already connected to a voice channel.")
                    return False
        except asyncio.TimeoutError:
            await ctx.send("Bot could not connect to the voice channel in time.")
            return False
        else:
            await ctx.send("Bot has connected to " + str(self.caller_channel_name))
            return True

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.bot_channel_member_num == 1:
            await disconnect_bot(ctx)
            await ctx.send("Bye!")
            return

        if await self.get_caller_channel(ctx) is False:
            ctx.send("Bot is in the voice channel with other user(s).")
            return
        else:
            if self.caller_channel_id == self.bot_channel_id:
                await disconnect_bot(ctx)
                await ctx.send("Bye!")
                return
            else:
                await ctx.send("Bot is in the voice channel with other user(s).")
                return

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        if await self.get_caller_channel(ctx) is False:
            ctx.send("You are not connected to a voice channel.")
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.caller_channel_id != self.bot_channel_id:
            await ctx.send("Can't skip. Join the voice channel to control the bot.")
            return

        if self.player.skip_music(ctx) is False:
            await ctx.send("Nothing is playing.")
            return

        skipped_song = misc.italicize(self.player.current_song['title'])
        await ctx.send("**Skipped: ** " + skipped_song)
        return

    @commands.command()
    async def pause(self, ctx):
        if await self.get_caller_channel(ctx) is False:
            ctx.send("You are not connected to a voice channel")
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.pause_music(ctx) is False:
                await ctx.send("Nothing to pause.")
            else:
                title = misc.italicize(self.player.current_song['title'])
                await ctx.send("**Paused: ** " + title)
        else:
            await ctx.send("Can't pause. Join the voice channel to control the bot.")

    @commands.command()
    async def resume(self, ctx):
        if await self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.resume_music(ctx) is False:
                await ctx.send("Nothing to resume.")
            else:
                title = misc.italicize(self.player.current_song['title'])
                await ctx.send("**Resumed: ** " + title)
        else:
            await ctx.send("Can't resume. Join the voice channel to control the bot.")

    @commands.command(aliases=['c'])
    async def current(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return
        await ctx.send(self.player.current_music(ctx))

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel.")
            return
        if self.player.is_queue_empty(ctx):
            await ctx.send("The queue is empty.")
            return
        await ctx.send(self.player.get_queue_content())

    @commands.command()
    async def remove(self, args):
        pass

    @commands.command()
    async def shuffle(self, ctx):
        pass

    @commands.command()
    async def loop(self, ctx):
        pass

    @commands.command()
    async def helpme(self, ctx):
        await ctx.send("Current list of commands:\n"
                       "\t-[play, p]\n"
                       "\t-[join, j]\n"
                       "\t-[leave, l]\n"
                       "\t-[pause] \n"
                       "\t-[resume]\n"
                       "\t-[skip, s]\n"
                       "\t-[current, c]\n"
                       "\t-[queue, q]\n"
                       "\t-[loop]\n")

    def get_bot_channel_info(self, ctx):
        self.bot = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if self.bot is None:
            # await ctx.send(msg)
            return False

        self.bot_channel_id = self.bot.channel.id
        self.bot_channel_name = self.client.get_channel(self.bot_channel_id)
        self.bot_channel_member_num = len(self.bot_channel_name.members)
        return True

    async def get_caller_channel(self, ctx):
        caller = ctx.author.voice
        if caller is None:
            return False

        self.caller_channel_name = caller.channel
        self.caller_channel_id = caller.channel.id
        return True
