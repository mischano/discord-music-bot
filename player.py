import discord
import playlist
import asyncio
import misc
import youtube_dl.utils
from discord.ext import commands
from youtube_dl import YoutubeDL


def is_music_playing(ctx):
    caller = ctx.voice_client
    if caller is None:
        return False
    return caller.is_playing()

def is_music_paused(ctx):
    return ctx.voice_client.is_paused()


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None
        self.current_song = None
        self.last_added = None

    def search(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except youtube_dl.utils.DownloadError or youtube_dl.utils.ExtractorError:
                return False

        result = {'source': info['formats'][0]['url'], 'title': info['title']}
        playlist.add_right(result)
        self.last_added = result
        return True

    def player(self, ctx):
        if is_music_playing(ctx):
            song_title = misc.italicize(self.last_added['title'])
            asyncio.run_coroutine_threadsafe(ctx.send("**Added to playlist: ** " + song_title), self.bot.loop)
        else:
            self.play_music(ctx)
        return

    def play_music(self, ctx):
        if playlist.size() <= 0 or is_music_playing(ctx) is True:
            return 

        self.current_song = playlist.pop_left()
        url = self.current_song['source']
        song_title = misc.italicize(self.current_song['title'])

        for attempt in range(3):
            try:
                ret = discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS)
            except discord.ClientException:
                asyncio.run_coroutine_threadsafe(
                        ctx.send("FFmpegPCMAudio has failed. Trying to reconnected...\n"), self.bot.loop
                )
            else:
                for i in range(3):
                    try:
                        self.vc.play(ret, after=lambda e: self.play_music(ctx))
                    except discord.ClientException:
                        print("Failed in self.vc.play: ClientException.")
                        # await ctx.send("Failed in self.vc.play: ClientException.")
                        # asyncio.run_coroutine_threadsafe(ctx.send("Failed in self.vc.play: ClientException."), self.bot.loop)
                    except TypeError:
                        print("Failed in self.vc.play: TypeError")
                        # await ctx.send("Failed in self.vc.play: TypeError")
                        # asyncio.run_coroutine_threadsafe(ctx.send("Failed in self.vc.play: TypeError"), self.bot.loop)
                    except discord.opus.OpusError:
                        print("Failed in self.vc.play: OpusError")
                        # asyncio.run_coroutine_threadsafe(ctx.send("Failed in self.vc.play: OpusError"), self.bot.loop)
                        # await ctx.send("Failed in self.vc.play: OpusError")
                    else:
                        asyncio.run_coroutine_threadsafe(ctx.send("**Now playing: ** " + song_title), self.bot.loop)
                        return
                    # break
        # print("Do I get here?")
        # asyncio.run_coroutine_threadsafe(ctx.send("Do I get here?"), self.bot.loop)


    def pause_music(self, ctx):
        if is_music_paused(ctx) is True or is_music_playing(ctx) is False:
            return False
        self.vc.pause()
        return True

    def resume_music(self, ctx):
        if is_music_paused(ctx) is False or is_music_playing(ctx) is True:
            return False
        self.vc.resume()
        return True

    def skip_music(self, ctx):
        if playlist.is_empty() is True:
            if is_music_paused(ctx) is False and is_music_playing(ctx) is False:
                return False
            else:
                self.vc.stop()
                return True
        else:
            self.vc.stop()
            self.play_music(ctx)
            return True
        
    def remove_music(self, elem):
        return playlist.remove(elem)

    def current_music(self, ctx):
        if is_music_playing(ctx) is True or is_music_paused(ctx) is True:
            return True
        return False
    
    def shuffle_music(self):
        if playlist.size() <= 0:
            return False
        playlist.shuffle_all()
        return True

    def clear_playlist(self):
        self.vc.stop()
        self.current_song = None
        self.last_added = None
        playlist.clear_all()
