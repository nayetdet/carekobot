import re
import asyncio
import discord
from typing import Optional
from discord import VoiceChannel
from discord.ext import commands
from src.carekobot.config import Config
from src.carekobot.services.tts_service import TTSService
from src.carekobot.tasks.tts_task import TTSTask

class EventsService:
    @classmethod
    async def on_guild_remove(cls, guild: discord.Guild) -> None:
        await TTSTask.remove(guild)

    @classmethod
    async def on_voice_state_update(cls, bot: commands.Bot, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        voice_channel: Optional[VoiceChannel] = after.channel or before.channel
        if not voice_channel:
            return

        if bot.user == member and after.channel != before.channel:
            await TTSTask.clear(voice_channel.guild)

        if bot.user in voice_channel.members:
            for _ in range(60):
                if any(not x.bot for x in voice_channel.members):
                    return
                await asyncio.sleep(1)

            if voice_channel.guild.voice_client:
                await voice_channel.guild.voice_client.disconnect(force=True)

    @classmethod
    async def on_message_edit(cls, bot: commands.Bot, before: discord.Message, after: discord.Message) -> None:
        prefix: str = Config.BOT_DEFAULT_PREFIX
        if re.search(rf"^{re.escape(prefix)}(say)?", after.content):
            ctx: commands.Context = await bot.get_context(after)
            await TTSService.say(ctx, text=after.content)
