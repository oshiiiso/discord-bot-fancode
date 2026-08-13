"""ロギング設定モジュール。"""
import os
import logging

from .config import DEBUG_MODE, LOG_DIR

logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "bot.log"), encoding="utf-8")
    ]
)
logger = logging.getLogger("fancode-bot")


def debug_log(message):
    """DEBUG_MODE=True の時のみ出力するログ"""
    logger.debug(message)


def info_log(message):
    """常に出力するログ（重要な状態変化・エラーなど）"""
    logger.info(message)
