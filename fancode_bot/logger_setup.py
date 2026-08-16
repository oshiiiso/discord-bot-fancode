"""ロギング設定モジュール。"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from .config import LOG_LEVEL, LOG_DIR, LOG_RETENTION_DAYS

# 日付ごとにログファイルを分け(bot.log.YYYY-MM-DD)、LOG_RETENTION_DAYS日分だけ残して
# それより古いものは自動削除する。cron等での手動管理は不要。
file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, "bot.log"),
    when="midnight",
    interval=1,
    backupCount=LOG_RETENTION_DAYS,
    encoding="utf-8",
)
file_handler.suffix = "%Y-%m-%d"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        file_handler,
    ]
)
logger = logging.getLogger("fancode-bot")


def debug_log(message):
    """LOG_LEVEL=DEBUG の時のみ出力するログ"""
    logger.debug(message)


def info_log(message):
    """常に出力するログ（重要な状態変化・エラーなど）"""
    logger.info(message)
