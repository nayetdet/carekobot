import asyncio
import discord
from typing import Optional, Dict
from discord import Guild, VoiceClient
from src.carekobot.utils.tts_utils import TTSUtils

class TTSTask:
    __queues: Dict[int, asyncio.Queue] = {}
    __tasks: Dict[int, asyncio.Task] = {}

    @classmethod
    async def add(cls, text: str, guild: Guild) -> None:
        if guild.id not in cls.__queues:
            cls.__queues[guild.id] = asyncio.Queue()

        await cls.__queues[guild.id].put(text.lower().strip())
        if guild.id not in cls.__tasks or cls.__tasks[guild.id].done():
            cls.__tasks[guild.id] = asyncio.create_task(cls.play(guild))

    @classmethod
    async def remove(cls, guild: Guild) -> None:
        await cls.clear(guild)
        if guild.id in cls.__queues:
            del cls.__queues[guild.id]

        if guild.id in cls.__tasks:
            del cls.__tasks[guild.id]

    @classmethod
    async def play(cls, guild: Guild) -> None:
        queue: asyncio.Queue = cls.__queues[guild.id]
        voice_client: Optional[VoiceClient] = guild.voice_client
        if not voice_client:
            return

        while True:
            text: str = await queue.get()
            if not voice_client or not voice_client.is_connected():
                queue.task_done()
                await asyncio.sleep(1)
                continue

            async with TTSUtils.say(text) as fp:
                voice_client.play(discord.FFmpegPCMAudio(fp, pipe=True))
                while voice_client.is_playing():
                    await asyncio.sleep(1)

            queue.task_done()

    @classmethod
    async def stop(cls, guild: Guild) -> None:
        voice_client: Optional[VoiceClient] = guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        if guild.id in cls.__tasks and not cls.__tasks[guild.id].done():
            cls.__tasks[guild.id].cancel()
            await cls.__tasks[guild.id]

    @classmethod
    async def clear(cls, guild: Guild) -> None:
        cls.__queues[guild.id] = asyncio.Queue()
        await cls.stop(guild)
