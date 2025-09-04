import logging
from discord.ext import commands
from src.carekobot.services.miscellaneous_service import MiscellaneousService

class MiscellaneousCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Miscellaneous Cog has been loaded!")

    @commands.command(aliases=["h"])
    async def help(self, ctx: commands.Context) -> None:
        await MiscellaneousService.help(ctx)
