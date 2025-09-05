import discord
import logging
from discord.ext import commands
from src.carekobot.repositories.guild_config_repository import GuildConfigRepository
from src.carekobot.services.events_service import EventsService

class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Events Cog has been loaded!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        await EventsService.on_guild_join(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        await EventsService.on_guild_remove(guild)
        await GuildConfigRepository.delete(guild.id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await EventsService.on_message(self.bot, message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        await EventsService.on_message_edit(self.bot, before, after)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        await EventsService.on_voice_state_update(self.bot, member, before, after)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        await EventsService.on_command_error(ctx, error)
