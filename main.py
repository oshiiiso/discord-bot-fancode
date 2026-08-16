"""Discord交換コード通知Bot エントリーポイント。"""
import discord
from discord.ext import commands

from fancode_bot.config import TOKEN, GUILD_ID, COMMAND_PREFIX
from fancode_bot.events import setup_events
from fancode_bot.commands import setup_commands

if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN が .env に設定されていません。")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.check
async def restrict_to_configured_guild(ctx):
    # GUILD_IDを設定していれば、それ以外のサーバーでのコマンドを無視する
    if not GUILD_ID:
        return True
    return ctx.guild is not None and ctx.guild.id == GUILD_ID


setup_events(bot)
setup_commands(bot)

if __name__ == "__main__":
    bot.run(TOKEN)
