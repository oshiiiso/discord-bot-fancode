"""Discord交換コード通知Bot エントリーポイント。"""
import discord
from discord.ext import commands

from fancode_bot.config import TOKEN, GUILD_ID
from fancode_bot.events import setup_events
from fancode_bot.commands import setup_commands

if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN が .env に設定されていません。")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)


async def restrict_to_configured_guild(interaction: discord.Interaction) -> bool:
    # GUILD_IDを設定していれば、それ以外のサーバーでのコマンドを無視する
    if not GUILD_ID:
        return True
    return interaction.guild is not None and interaction.guild.id == GUILD_ID


bot.tree.interaction_check = restrict_to_configured_guild

setup_events(bot)
setup_commands(bot)

if __name__ == "__main__":
    bot.run(TOKEN)
