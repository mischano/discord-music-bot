import asyncio
import playlist
from stylizer import *
from discord.ext import commands


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.timeout = 300

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.id == self.client.user.id:
            return

        if before.channel is None:
            vc = after.channel.guild.voice_client
            elapsed_time = 0
            while True:
                await asyncio.sleep(1)
                elapsed_time += 1
                if vc.is_playing() and not vc.is_paused():
                    elapsed_time = 0
                if elapsed_time == self.timeout:
                    await member.guild.system_channel.send(f"Disconnected due to inactivity {emj_v_hand}")
                    await vc.disconnect()
                    vc.cleanup()
                    playlist.clear_all()
                if not vc.is_connected():
                    break   

    def set_timeout(self, val):
        self.timeout = val
