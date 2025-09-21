import asyncio
import discord
import logging
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from discord import Guild, VoiceClient
from src.carekobot.utils.tts_utils import TTSUtils

@dataclass
class TTSTaskData:
    queue: asyncio.Queue[Tuple[str, str]]
    task: Optional[asyncio.Task[None]]

class TTSTask:
    __data: Dict[int, TTSTaskData] = {}

    @classmethod
    async def add(cls, guild: Guild, arg: str, voice: str) -> None:
        data: TTSTaskData = cls.__data.setdefault(guild.id, TTSTaskData(queue=asyncio.Queue(), task=None))
        await data.queue.put((arg.lower().strip(), voice))
        if not data.task or data.task.done():
            data.task = asyncio.create_task(cls.play(guild))

    @classmethod
    async def remove(cls, guild: Guild) -> None:
        await cls.clear(guild)
        cls.__data.pop(guild.id, None)

    @classmethod
    async def play(cls, guild: Guild) -> None:
        data: TTSTaskData = cls.__data[guild.id]
        queue: asyncio.Queue = data.queue

        try:
            while True:
                voice_client: Optional[VoiceClient] = guild.voice_client
                if not voice_client:
                    await asyncio.sleep(1)
                    continue

                arg, voice = await queue.get()
                try:
                    async with TTSUtils.say(arg, voice=voice) as fp:
                        voice_client.play(discord.FFmpegPCMAudio(fp, pipe=True))
                        while voice_client.is_playing():
                            await asyncio.sleep(1)
                except Exception as e: logging.error(f"[TTSTask] TTS playback failed: {e}")
                finally: queue.task_done()
        except asyncio.CancelledError as e:
            voice_client: Optional[VoiceClient] = guild.voice_client
            if voice_client and voice_client.is_playing():
                voice_client.stop()

            data.queue = asyncio.Queue()
            data.task = None
            raise e

    @classmethod
    async def stop(cls, guild: Guild) -> None:
        voice_client: Optional[VoiceClient] = guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

    @classmethod
    async def clear(cls, guild: Guild) -> None:
        if (data := cls.__data.get(guild.id)) and (task := data.task):
            task.cancel()
            try: await task
            except asyncio.CancelledError:
                pass

            data.task = None
        await cls.stop(guild)
