import discord
import asyncio
import stylizer
import playlist
# import settings
from stylizer import *
from discord.ext import commands


async def disconnect_bot(ctx):
    vc = ctx.guild.voice_client
    await vc.disconnect()
    vc.cleanup()
    playlist.clear_all()


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
            await ctx.send(f"Couldn't find the song {emj_face_palm}")
            return

        self.player.player(ctx)


    @commands.command(aliases=['j'])
    async def join(self, ctx):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return False

        try:
            self.player.vc = await self.caller_channel_name.connect(
                timeout=.5, reconnect=True, self_mute=False, self_deaf=True
                )
        except discord.ClientException:
            if self.get_bot_channel_info(ctx) is False:
                await ctx.send("Failed in *get_channel_info*. Please report the issue to **sheriff**. Thank you!")
                return False
            if self.bot_channel_member_num == 1:
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
            
            await ctx.send(f"{emj_notes} Connected to {self.caller_channel_name} {emj_notes}")
            return True


    @commands.command(aliases=['q', 'leave'])
    async def quit(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.bot_channel_member_num == 1:
            await disconnect_bot(ctx)
            await ctx.send(f"Bye! {emj_v_hand}")
            return

        if self.get_caller_channel(ctx) is False:
            ctx.send(f"In the voice channel with other user(s) {emj_clown}")
            return
        else:
            if self.caller_channel_id == self.bot_channel_id:
                await disconnect_bot(ctx)
                await ctx.send(f"Bye! {emj_v_hand}")
                return
            else:
                await ctx.send(f"In the voice channel with other user(s) {emj_clown}")
                return


    @commands.command(aliases=['s', 'next', 'n'])
    async def skip(self, ctx):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.caller_channel_id != self.bot_channel_id:
            await ctx.send(f"Can't skip. Join the voice channel first {emj_clown}")
            return

        if self.player.skip_music(ctx) is False:
            await ctx.send("Playlist is empty.")
            return  

        skipped_song = stylizer.italicize(self.player.current_song['title'])
        await ctx.send(f"**Skipped: ** \n> {skipped_song} {emj_ok_hand}")
        return


    @commands.command()
    async def pause(self, ctx):
        if self.get_caller_channel(ctx) is False:
            ctx.send("You are not connected to a voice channel.")
            return

        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return

        if self.caller_channel_name == self.bot_channel_name:
            if self.player.pause_music(ctx) is False:
                await ctx.send(f"Can't pause. Nothing is playing.")
            else:
                title = stylizer.italicize(self.player.current_song['title'])
                await ctx.send(f"{emj_pause} **Paused: ** \n> {title}")
        else:
            await ctx.send(f"Can't pause. Join the voice channel first {emj_clown}")


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
                await ctx.send("Can't resume. Nothing is paused.")
            else:
                title = stylizer.italicize(self.player.current_song['title'])
                await ctx.send(f"{emj_resume} **Resumed: ** \n> {title}")
        else:
            await ctx.send(f"Can't resume. Join the voice channel first {emj_clown}")


    @commands.command(aliases=['c'])
    async def current(self, ctx):
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return
        if self.player.current_music(ctx) is False:
            await ctx.send("Playlist is empty.")
        else:
            title = stylizer.italicize(self.player.current_song['title'])
            await ctx.send(f"**Currently playing: ** \n> {title}")
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
        await ctx.send(f"**Playing: ** \n> {self.player.current_song['title']}\n**Playlist: ** \n> {queue}")
        return


    @commands.command()
    async def remove(self, ctx, *args):
        if self.get_caller_channel(ctx) is False:
            await ctx.send("You are not connected to a voice channel.")
            return
        if self.get_bot_channel_info(ctx) is False:
            await ctx.send("Not connected to a voice channel.")
            return
        if self.caller_channel_name != self.bot_channel_name:
            await ctx.send(f"Can't remove. Join the voice channel first {emj_clown}")
            return
        
        input = "".join(args)
        try:
            elem = int(input)
        except ValueError:
            await ctx.send(f"Can't read the number {emj_nerd}")
            return

        song = playlist.get_at_index(elem - 1)
        if playlist.remove(elem - 1) is False:
            await ctx.send(f"Number is out of range {emj_skull}")
        else:
            await ctx.send(f"{italicize(song)} is removed from the playlist {emj_ok_hand}")
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
            await ctx.send(f"Can't shuffle. Join the voice channel first {emj_clown}")
            return
        
        if self.player.shuffle_music() is False:
            await ctx.send("Not enough songs in the playlist to shuffle.")
        else:
            await ctx.send(f"{emj_shuffle} Shuffled.")

        return


    @commands.command()
    async def loop(self, ctx):
        pass


    @commands.command()
    async def add(self, ctx):
        pass


    @commands.command()
    async def helpme(self, ctx):
        with open ("command_list.txt") as f:
            msg = "\n> $".join([line.rstrip('\n') for line in f])
        await ctx.send(f"{msg}\n\nIf you encounter bugs, please inform __sheriff__ {emj_sun_shine}")                  
        

    def get_bot_channel_info(self, ctx):
        self.bot = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if self.bot is None:
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
