import asyncio

import discord
import dequeue
import youtube_dl.utils
from discord.ext import commands
from youtube_dl import YoutubeDL


class Player(commands.Cog):
    def __init__(self, bot):
        # Bot
        self.bot = bot
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        # Player
        self.vc = None
        self.current_song = None
        self.last_added = None
        self.is_playing = False
        self.paused = False

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

    async def player(self, ctx):
        if self.is_playing is True:
            await ctx.send("Added to queue: " + self.last_added['title'])
            return
        else:
            self.play_music(ctx)
            return

    def play_music(self, ctx):
        if dequeue.size() > 0:
            self.is_playing = True
            self.current_song = dequeue.pop_left()
            url = self.current_song['source']
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_music(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send("Now playing " + self.current_song['title']), self.bot.loop)
            return

        self.is_playing = False
        return

    def pause_music(self):
        pass

    def resume_music(self):
        pass
