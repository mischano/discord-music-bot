import asyncio
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
                    await vc.disconnect()
                    vc.cleanup()
                if not vc.is_connected():
                    break   

    def set_timeout(self, val):
        self.timeout = val

help_string = "Current list of commands:"
# help_string = "Current list of commands:\n"
# "\t-[play, p]\n"
# "\t-[join, j]\n"
# "\t-[quit, q]\n"
# "\t-[pause] \n"
# "\t-[resume]\n"
# "\t-[skip, s]\n"
# "\t-[current, c]\n"
# "\t-[list, l]\n"
# "\t-[loop]\n"
# "The bot is still in development. If you have __bug reports__, "
# "please contact **sheriff**."   