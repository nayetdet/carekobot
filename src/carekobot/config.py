import os

class Config:
    BOT_DEFAULT_PREFIX: str = os.getenv("BOT_DEFAULT_PREFIX")
    BOT_TTS_API_URL: str = os.getenv("BOT_TTS_API_URL")
    BOT_TTS_VOICE_MODEL: str = os.getenv("BOT_TTS_VOICE_MODEL")
    BOT_DISCORD_TOKEN: str = os.getenv("BOT_DISCORD_TOKEN")
