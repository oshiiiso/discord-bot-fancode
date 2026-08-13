"""Discord交換コード通知Bot エントリーポイント。"""
import discord
from discord.ext import commands

from fancode_bot.config import TOKEN
from fancode_bot.events import setup_events
from fancode_bot.commands import setup_commands

if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN が .env に設定されていません。")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

setup_events(bot)
setup_commands(bot)

if __name__ == "__main__":
    bot.run(TOKEN)
