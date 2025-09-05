from typing import Optional
from beanie import Document
from src.carekobot.config import Config

class GuildConfig(Document):
    guild_id: int
    prefix: Optional[str]
    voice: Optional[str]

    def get_prefix(self) -> str:
        return self.prefix if self.prefix else Config.BOT_DEFAULT_PREFIX

    def get_voice(self) -> str:
        return self.voice if self.voice else Config.TTS_DEFAULT_VOICE_MODEL
