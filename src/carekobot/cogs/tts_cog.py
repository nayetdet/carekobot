import logging
from discord.ext import commands
from src.carekobot.services.tts_service import TTSService

class TTSCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("TTS Cog has been loaded!")

    @commands.command(aliases=[""])
    async def say(self, ctx: commands.Context, *, arg: str) -> None:
        await TTSService.say(ctx, arg=arg)

    @commands.command(aliases=["s"])
    async def stop(self, ctx: commands.Context) -> None:
        await TTSService.stop(ctx)

    @commands.command(aliases=["c"])
    async def clear(self, ctx: commands.Context) -> None:
        await TTSService.clear(ctx)

    @commands.command()
    async def voice(self, ctx: commands.Context, *, arg: str) -> None:
        await TTSService.voice(ctx, arg=arg)

    @commands.command()
    async def voices(self, ctx: commands.Context) -> None:
        await TTSService.voices(ctx)
