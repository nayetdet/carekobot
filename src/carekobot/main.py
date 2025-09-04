import asyncio
import discord
from discord.ext import commands
from src.carekobot.cogs import register_cogs
from src.carekobot.config import Config

bot = commands.Bot(command_prefix=Config.BOT_DEFAULT_PREFIX, intents=discord.Intents.all(), help_command=None)
discord.utils.setup_logging()

async def main() -> None:
    await register_cogs(bot)
    await bot.start(Config.BOT_DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
