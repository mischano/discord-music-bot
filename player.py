import discord
import dequeue
import asyncio
import youtube_dl.utils
from discord.ext import commands
from youtube_dl import YoutubeDL


def is_music_playing(ctx):
    return ctx.voice_client.is_playing()


def is_music_paused(ctx):
    return ctx.voice_client.is_paused()


def italicize(txt):
    return '*' + txt + '*'


class Player(commands.Cog):
    def __init__(self, bot):
        # Bot
        self.bot = bot

        # Youtube
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        # Player
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
        dequeue.add_right(result)
        self.last_added = result
        return True

    def player(self, ctx):
        if is_music_playing(ctx):
            song_title = italicize(self.last_added['title'])
            asyncio.run_coroutine_threadsafe(ctx.send("**Added to queue: ** " + song_title), self.bot.loop)
            # await ctx.send("**Added to queue: ** " + song_title)
            return
        else:
            self.play_music(ctx)
            return

    def play_music(self, ctx):
        if dequeue.size() > 0:
            self.current_song = dequeue.pop_left()
            url = self.current_song['source']
            song_title = italicize(self.current_song['title'])
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_music(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send("**Now playing: ** " + song_title), self.bot.loop)
            return

        return

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
        if dequeue.is_empty() is True:
            if is_music_paused(ctx) is False and is_music_playing(ctx) is False:
                return False
            else:
                self.vc.stop()
                return True
        else:
            self.vc.stop()
            self.play_music(ctx)
            return True

    def clear_music_queue(self):
        self.vc.stop()
        self.current_song = None
        self.last_added = None
        dequeue.clear_all()
