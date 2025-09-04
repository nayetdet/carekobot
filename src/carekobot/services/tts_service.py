import re
from discord.ext import commands
from src.carekobot.services.voice_channel_service import VoiceChannelService
from src.carekobot.tasks.tts_task import TTSTask

class TTSService:
    @classmethod
    async def say(cls, ctx: commands.Context, *, text: str) -> None:
        await VoiceChannelService.join(ctx, notify_on_success=False)
        for content, name in re.findall(r"(<:(\w+):\d+>)", text):
            text = text.replace(content, name)

        await TTSTask.add(text, ctx.guild)

    @classmethod
    async def stop(cls, ctx: commands.Context) -> None:
        await TTSTask.stop(ctx.guild)

    @classmethod
    async def clear(cls, ctx: commands.Context) -> None:
        await TTSTask.clear(ctx.guild)
