import os
import discord
import random
from typing import List, Optional
from discord.ext import commands
from src.carekobot.config import Config

class MiscellaneousService:
    @classmethod
    async def send(cls, ctx: commands.Context, text: str, delete_after: Optional[int] = None) -> None:
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets"))
        images_path: List[str] = [x for x in os.listdir(assets_dir) if x.lower().endswith((".png", ".webp", ".jpg", ".jpeg"))]
        if not images_path:
            return

        image_path: str = random.choice(images_path)
        await ctx.channel.send(
            embed=discord.Embed().set_author(name=text, icon_url=f"attachment://{image_path}"),
            file=discord.File(os.path.join(assets_dir, image_path), filename=image_path),
            delete_after=delete_after
        )

    @classmethod
    async def help(cls, ctx: commands.Context) -> None:
        prefix: str = Config.BOT_DEFAULT_PREFIX
        embed: discord.Embed = discord.Embed(
            title="🤖 CarekoBot",
            description="Comandos disponíveis para TTS e voz:"
        )

        embed.add_field(
            name="🎧 TTS",
            value=(
                f"`{prefix}say <texto>` — Reproduz sua mensagem\n"
                f"`{prefix}stop` — Para a fala atual imediatamente\n"
                f"`{prefix}clear` — Esvazia toda a fila de falas"
            ),
            inline=False
        )

        embed.add_field(
            name="🔊 Canal de Voz",
            value=(
                f"`{prefix}join` — Faz o bot entrar no seu canal de voz\n"
                f"`{prefix}leave` — Remove o bot do canal de voz"
            ),
            inline=False
        )

        embed.set_thumbnail(url=ctx.bot.user.avatar.url if ctx.bot.user.avatar else ctx.bot.user.default_avatar.url)
        embed.set_footer(text="CarekoBot • Um bot de TTS bem carequinha ao seu dispor!!!")
        await ctx.send(embed=embed)
