from contextlib import asynccontextmanager
import aiohttp
from io import BytesIO
from typing import AsyncGenerator, Any
from src.carekobot.config import Config

class TTSUtils:
    @classmethod
    @asynccontextmanager
    async def say(cls, text: str) -> AsyncGenerator[BytesIO, Any]:
        fp: BytesIO = BytesIO()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{Config.BOT_TTS_API_URL}/v1/audio/speech",
                json={
                    "input": text,
                    "voice": Config.BOT_TTS_VOICE_MODEL,
                    "model": "kokoro",
                    "response_format": "mp3",
                    "lang_code": "p"
                }
            ) as response:
                async for chunk in response.content.iter_chunked(1024):
                    fp.write(chunk)

        fp.seek(0)
        try: yield fp
        finally:
            fp.close()
