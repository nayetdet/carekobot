from typing import Optional
from discord import VoiceChannel, VoiceClient
from discord.ext import commands
from src.carekobot.services.miscellaneous_service import MiscellaneousService

class VoiceChannelService:
    @classmethod
    async def join(cls, ctx: commands.Context, notify_on_success: bool = True) -> None:
        if not ctx.author.voice or not ctx.author.voice.channel:
            await MiscellaneousService.send(ctx, arg="Por favor, conecte-se a um canal de voz!")
            return

        voice_channel: Optional[VoiceChannel] = ctx.author.voice.channel
        voice_client: Optional[VoiceClient] = ctx.guild.voice_client

        if voice_client:
            if notify_on_success and voice_client.channel.id == voice_channel.id:
                await MiscellaneousService.send(ctx, arg="Já estou conectado ao seu canal de voz!")
                return

            await voice_client.move_to(voice_channel)
        else: await voice_channel.connect()
        if notify_on_success:
            await MiscellaneousService.react(ctx)

    @classmethod
    async def leave(cls, ctx: commands.Context, notify_on_success: bool = True) -> None:
        voice_client: Optional[VoiceClient] = await cls.ensure_voice(ctx)
        if not voice_client:
            return

        await voice_client.disconnect()
        if notify_on_success:
            await MiscellaneousService.react(ctx)

    @classmethod
    async def ensure_voice(cls, ctx: commands.Context) -> Optional[VoiceClient]:
        if not ctx.author.voice or not ctx.author.voice.channel:
            await MiscellaneousService.send(ctx, arg="Você precisa estar em um canal de voz para me desconectar!")
            return None

        voice_client: Optional[VoiceClient] = ctx.guild.voice_client
        if not voice_client:
            await MiscellaneousService.send(ctx, arg="Não estou conectado a nenhum canal de voz!")
            return None

        return voice_client
