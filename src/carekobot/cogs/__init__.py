from discord.ext import commands
from src.carekobot.cogs.events_cog import EventsCog
from src.carekobot.cogs.miscellaneous_cog import MiscellaneousCog
from src.carekobot.cogs.tts_cog import TTSCog
from src.carekobot.cogs.voice_channel_cog import VoiceChannelCog

async def register_cogs(bot: commands.Bot):
    await bot.add_cog(EventsCog(bot))
    await bot.add_cog(MiscellaneousCog(bot))
    await bot.add_cog(TTSCog(bot))
    await bot.add_cog(VoiceChannelCog(bot))
