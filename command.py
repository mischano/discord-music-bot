import discord
import asyncio
import misc
import playlist
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
            await ctx.send("Couldn't find the song.")
            return

        self.player.player(ctx)

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return False

        try:
            self.player.vc = await self.caller_channel_name.connect(
                timeout=.5, reconnect=True, self_mute=False, self_deaf=True)
        except discord.ClientException:
            if self.get_bot_channel_info(ctx) is False:
                await ctx.send("Failed in *get_channel_info*. Please report the issue to **sheriff**. Thank you!")
                return False
            if self.bot_channel_member_num == 1:
                self.player.clear_playlist()
                await disconnect_bot(ctx)
                await self.join(ctx)
                return True
            else:
                if self.caller_channel_name == self.bot_channel_name:
                    return True
                else:
                    await ctx.send("Already connected to a voice channel.")
                    return False
        except asyncio.TimeoutError:
            await ctx.send("Couldn't connect to the voice channel in time.")
            return False
        else:
            await ctx.send("Connected to " + str(self.caller_channel_name))
            return True

    # REDO THIS! 
    @commands.command(aliases=['q'])
    async def quit(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.bot_channel_member_num == 1:
            await disconnect_bot(ctx)
            await ctx.send("Bye!")
            return

        if self.get_caller_channel(ctx) is False:
            ctx.send("In the voice channel with other user(s).")
            return
        else:
            if self.caller_channel_id == self.bot_channel_id:
                await disconnect_bot(ctx)
                await ctx.send("Bye!")
                return
            else:
                await ctx.send("In the voice channel with other user(s).")
                return

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.caller_channel_id != self.bot_channel_id:
            await ctx.send("Can't skip. Join the voice channel first.")
            return

        if self.player.skip_music(ctx) is False:
            await ctx.send("Playlist is empty.")
            return  

        skipped_song = misc.italicize(self.player.current_song['title'])
        await ctx.send("**Skipped: ** " + skipped_song)
        return

    @commands.command()
    async def pause(self, ctx):
        if self.get_caller_channel(ctx) is False:
            ctx.send("You are not connected to a voice channel")
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.pause_music(ctx) is False:
                await ctx.send("Can't pause. Playlist is empty.")
            else:
                title = misc.italicize(self.player.current_song['title'])
                await ctx.send("**Paused: ** " + title)
        else:
            await ctx.send("Can't pause. Join the voice channel first.")

    @commands.command()
    async def resume(self, ctx):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.resume_music(ctx) is False:
                await ctx.send("Can't resume. Playlist is empty.")
            else:
                title = misc.italicize(self.player.current_song['title'])
                await ctx.send("**Resumed: ** " + title)
        else:
            await ctx.send("Can't resume. Join the voice channel first.")

    @commands.command(aliases=['c'])
    async def current(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return
        if self.player.current_music(ctx) is False:
            await ctx.send("Playlist is empty.")
        else:
            title = misc.italicize(self.player.current_song['title'])
            await ctx.send("**Currently playing: ** " + title)
        return

    @commands.command(aliases=['l'])
    async def list(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return
        if playlist.is_empty():
            await ctx.send("Playlist is empty.")
            return
        queue = playlist.get_all()
        msg = "**Current playlist: **\n" + queue
        await ctx.send(msg)

    @commands.command()
    async def remove(self, ctx, *args):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return
        if self.caller_channel_name != self.bot_channel_name:
            await ctx.send("Can't remove. Join the voice channel first.")
            return
        
        input = "".join(args)
        try:
            elem = int(input)
        except ValueError:
            await ctx.send("Can't read the number.")
            return
        
        if playlist.remove(elem) is False:
            await ctx.send("Number is out of range.")
        else:
            await ctx.send("Song is removed from the playlist.")
        return
        

    @commands.command()
    async def shuffle(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return
        if self.get_caller_channel(ctx) is False:
            await ctx.send("User is not connected to a voice channel.")
            return
        if self.caller_channel_name != self.bot_channel_name:
            await ctx.send("Can't shuffle. Join the voice channel first.")
            return
        
        if self.player.shuffle_music is False:
            await ctx.send("Not enough songs in the playlist to shuffle.")
        else:
            await ctx.send("Shuffled.")

        return

    @commands.command()
    async def loop(self, ctx):
        pass

    @commands.command()
    async def helpme(self, ctx):
        await ctx.send("Current list of commands:\n"
                       "\t-[play, p]\n"
                       "\t-[join, j]\n"
                       "\t-[quit, q]\n"
                       "\t-[pause] \n"
                       "\t-[resume]\n"
                       "\t-[skip, s]\n"
                       "\t-[current, c]\n"
                       "\t-[list, l]\n"
                       "\t-[loop]\n"
                       "The bot is still in development. If you have __bug reports__, "
                       "please contact **sheriff**.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(member)
        print(before)
        print(after)
        if before.channel is None and after.channel is not None:
            if after.channel.id == self.caller_channel_id:
                return
                # await member.guild.system_channel.send("Alarm!")

    def get_bot_channel_info(self, ctx):
        self.bot = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if self.bot is None:
            # await ctx.send(msg)
            return False

        self.bot_channel_id = self.bot.channel.id
        self.bot_channel_name = self.client.get_channel(self.bot_channel_id)
        self.bot_channel_member_num = len(self.bot_channel_name.members)
        return True

    def get_caller_channel(self, ctx):
        caller = ctx.author.voice
        if caller is None:
            return False

        self.caller_channel_name = caller.channel
        self.caller_channel_id = caller.channel.id
        return True
