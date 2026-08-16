"""ロギング設定モジュール。"""
import os
import re
import glob
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from .config import LOG_LEVEL, LOG_DIR, LOG_RETENTION_DAYS

DATE_LOG_PATTERN = re.compile(r"^\d{8}\.log$")


class DailyLogFileHandler(TimedRotatingFileHandler):
    """logs/yyyymmdd.log という名前で当日分のログを出力し、
    深夜0時に前日分を確定させ、LOG_RETENTION_DAYSより古いログファイルを
    自動削除するハンドラ。"""

    def __init__(self, log_dir, backup_count):
        self._log_dir = log_dir
        today_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        super().__init__(today_path, when="midnight", interval=1, backupCount=backup_count, encoding="utf-8")

    def doRollover(self):
        # 標準のローテーション処理(ファイル名末尾に日付を付ける動作)は使わず、
        # 単純に新しい日付のファイルへ切り替えるだけにする。
        if self.stream:
            self.stream.close()
            self.stream = None
        self.baseFilename = os.path.join(self._log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        self.stream = self._open()
        self._delete_old_logs()

    def _delete_old_logs(self):
        log_files = sorted(
            f for f in glob.glob(os.path.join(self._log_dir, "*.log"))
            if DATE_LOG_PATTERN.match(os.path.basename(f))
        )
        excess = len(log_files) - self.backupCount
        for old_file in log_files[:max(excess, 0)]:
            try:
                os.remove(old_file)
            except OSError:
                pass


file_handler = DailyLogFileHandler(LOG_DIR, LOG_RETENTION_DAYS)

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
