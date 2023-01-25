import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


async def disconnect_bot(ctx, msg):
    vc = ctx.guild.voice_client
    await vc.disconnect()
    if len(msg) != 0:
        await ctx.send(msg)


class Command(commands.Cog):
    def __init__(self, client):
        # Bot
        self.bot = client
        self.channel_name = None
        self.channel_id = None
        self.channel_member_num = None

    @commands.command()
    async def play(self, ctx, *args):
        """
        1. you are not connected to vc. Error
        2. bot is not connected to vc.  Connect bot & play
        3. you and bot (alone) are in different vc. Connect bot & play
        4. you and bot (not alone) are in different vc. Error
        5. you and bot are in the same vc. Play
        """
        if not await self.join(ctx):
            print("doesn't play")
        else:
            print("plays")

    @commands.command()
    async def join(self, ctx):
        """
        1. you are not connected to vc. Error
        2. bot is not connected to vc.  Connect bot
        3. you and bot (alone) are in different vc. Connect bot
        4. you and bot (not alone) are in different vc. Error
        5. you and bot are in the same vc. Error
        """
        caller = ctx.author.voice
        if caller is None:
            await ctx.send("You are not connected to a voice channel.")
            return False

        caller_channel = caller.channel
        try:
            await caller_channel.connect(timeout=.5, self_mute=False, self_deaf=True)
            return True
        except discord.ClientException:
            # if self.get_channel_info(ctx) is None:
            #     await ctx.send("Bot is not connected to a voice channel.")
            #     return
            self.get_channel_info(ctx)
            if self.channel_member_num == 1:
                await disconnect_bot(ctx, "")
                await caller_channel.connect(timeout=.5, self_mute=False, self_deaf=True)
                return True
            else:
                if caller_channel == self.channel_name:
                    return True
                else:
                    await ctx.send("Bot is already connected to a voice channel.")
                # if same channel return true, else error msg and return false
                # return  # fail
        except TimeoutError:
            await ctx.send("Bot connection timed out.")

    @commands.command()
    async def leave(self, ctx):
        if self.get_channel_info(ctx) is False:
            await ctx.send("Bot is not connected to a voice channel...")
            return

        if self.channel_member_num == 1:
            await disconnect_bot(ctx, "Bye!")
            return

        caller_channel_obj = ctx.author.voice
        if caller_channel_obj is None:
            await ctx.send("Sorry, can't leave. I'm in the voice channel with someone.\n")
            return
        else:
            caller_channel_id = caller_channel_obj.channel.id
            if caller_channel_id == self.channel_id:
                await disconnect_bot(ctx, "Bye!")
                return
            else:
                await ctx.send("Sorry, can't leave. I'm in the different voice "
                               "channel (not alone!).\n")
                return

    def get_channel_info(self, ctx):
        bot_channel_obj = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_channel_obj is None:
            return False

        self.channel_id = bot_channel_obj.channel.id
        self.channel_name = self.bot.get_channel(self.channel_id)
        self.channel_member_num = len(self.channel_name.members)
        return True
