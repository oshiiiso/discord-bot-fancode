"""Botのイベントハンドラ・定期実行タスクを登録するモジュール。"""
import asyncio
from datetime import datetime, timedelta

from discord.ext import tasks

from .config import CHECK_INTERVAL_HOURS
from .logger_setup import debug_log, info_log
from .checker import run_check_all_games


def setup_events(bot):
    """on_ready イベントと定期チェックタスクをbotに登録する。"""

    @tasks.loop(hours=CHECK_INTERVAL_HOURS)
    async def check_all_games_loop():
        await run_check_all_games(bot)

    @check_all_games_loop.before_loop
    async def before_check_all_games_loop():
        """
        起動直後に1回即時チェックを実行し、その後は毎回の間隔で実行する。
        間隔が1時間の場合は毎時00分に揃うように待機する。
        """
        await bot.wait_until_ready()

        info_log("[初回実行] 起動直後のチェックを実行します。")
        await run_check_all_games(bot)

        now = datetime.now()
        if CHECK_INTERVAL_HOURS == 1:
            next_run = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        else:
            next_run = now + timedelta(hours=CHECK_INTERVAL_HOURS)
        wait_seconds = (next_run - now).total_seconds()
        debug_log(f"[待機] 次回実行まで {int(wait_seconds)} 秒待機します。")
        await asyncio.sleep(wait_seconds)

    @bot.event
    async def on_ready():
        info_log(f'=== {bot.user.name} が起動しました ===')
