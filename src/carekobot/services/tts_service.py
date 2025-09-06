import re
import discord
from typing import List, Optional
from discord import VoiceClient
from discord.ext import commands
from src.carekobot.models.guild_config import GuildConfig
from src.carekobot.repositories.guild_config_repository import GuildConfigRepository
from src.carekobot.services.miscellaneous_service import MiscellaneousService
from src.carekobot.services.voice_channel_service import VoiceChannelService
from src.carekobot.tasks.tts_task import TTSTask
from src.carekobot.utils.tts_utils import TTSUtils

class TTSService:
    @classmethod
    async def say(cls, ctx: commands.Context, *, arg: str) -> None:
        if not await VoiceChannelService.join(ctx, notify_on_success=False):
            return

        for content, name in re.findall(r"(<:(\w+):\d+>)", arg):
            arg = arg.replace(content, name)

        guild_config: GuildConfig = await GuildConfigRepository.get(ctx.guild.id, auto_create=True)
        await TTSTask.add(ctx.guild, arg=arg, voice=guild_config.get_voice())

    @classmethod
    async def stop(cls, ctx: commands.Context) -> None:
        voice_client: Optional[VoiceClient] = await VoiceChannelService.ensure_voice(ctx)
        if not voice_client:
            return

        await MiscellaneousService.react(ctx)
        await TTSTask.stop(ctx.guild)

    @classmethod
    async def clear(cls, ctx: commands.Context) -> None:
        voice_client: Optional[VoiceClient] = await VoiceChannelService.ensure_voice(ctx)
        if not voice_client:
            return

        await MiscellaneousService.react(ctx)
        await TTSTask.clear(ctx.guild)

    @classmethod
    async def voice(cls, ctx: commands.Context, *, arg: str) -> None:
        if arg not in await TTSUtils.voices():
            await MiscellaneousService.send(ctx, arg="Por favor, insira uma voz válida!")
            return

        guild_config: GuildConfig = await GuildConfigRepository.get(ctx.guild.id, auto_create=True)
        if guild_config.voice == arg:
            await MiscellaneousService.send(ctx, arg="Essa voz já está definida como padrão neste servidor!")
            return

        await GuildConfigRepository.update_voice(ctx.guild.id, arg)
        await MiscellaneousService.react(ctx)

    @classmethod
    async def voices(cls, ctx: commands.Context) -> None:
        all_voices: List[str] = await TTSUtils.voices()
        guild_config: GuildConfig = await GuildConfigRepository.get(ctx.guild.id, auto_create=True)
        current_voice: str = guild_config.get_voice()

        if not all_voices:
            await MiscellaneousService.send(ctx, arg="Nenhuma voz disponível no momento!")
            return

        formatted_voices: List[str] = []
        for voice in all_voices:
            if voice == current_voice:
                formatted_voices.append(f"✅ **{voice}**")
            else: formatted_voices.append(f"☑️ {voice}")

        embed: discord.Embed = discord.Embed(
            title="🔊 Vozes disponíveis",
            description="Escolha uma voz para o TTS:"
        )

        embed.add_field(
            name="",
            value="\n".join(formatted_voices),
            inline=False
        )

        await ctx.send(embed=embed)
        await MiscellaneousService.react(ctx)
