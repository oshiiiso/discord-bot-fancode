"""ボット全体で使用する設定値・定数を定義するモジュール。"""
import os
from dotenv import load_dotenv

try:
    load_dotenv()
except UnicodeDecodeError as e:
    raise RuntimeError(
        ".env ファイルの文字コードがUTF-8ではありません。"
        "エディタで開いてUTF-8(BOMなし)で保存し直してください。"
        f"(詳細: {e})"
    ) from e

# ==================== 【設定】 ====================
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').strip().upper()

# このBotが反応するサーバーID(未設定なら制限なし)
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# コマンドプレフィックス(開発用・本番用で分けたい場合のためenv化)
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')

# 交換コードの自動チェック間隔(時間)
CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', 1))

# ログファイルの保持日数(これを超えた古いログは自動削除される)
LOG_RETENTION_DAYS = int(os.getenv('LOG_RETENTION_DAYS', 30))

# プロジェクトルート・生成ファイルの保存先ディレクトリ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

GAME_CONFIG = {
    "genshin": {
        "name": "原神",
        "url": "https://genshin-impact.fandom.com/wiki/Promotional_Code",
        "channel_id": int(os.getenv("GENSHIN_CHANNEL_ID", 0)),
        "color": 0x00ffcc,
        "redeem_url": "https://genshin.hoyoverse.com/ja/gift?code="
    },
    "starrail": {
        "name": "崩壊：スターレイル",
        "url": "https://honkai-star-rail.fandom.com/wiki/Redemption_Code",
        "channel_id": int(os.getenv("STARRAIL_CHANNEL_ID", 0)),
        "color": 0x00bfff,
        "redeem_url": "https://hsr.hoyoverse.com/gift?code="
    },
    "zzz": {
        "name": "ゼンレスゾーンゼロ",
        "url": "https://zenless-zone-zero.fandom.com/wiki/Redemption_Code",
        "channel_id": int(os.getenv("ZZZ_CHANNEL_ID", 0)),
        "color": 0xffcc00,
        "redeem_url": "https://zenless.hoyoverse.com/redemption?code="
    },
    "wuthering": {
        "name": "鳴潮",
        "url": "https://wutheringwaves.fandom.com/wiki/Redemption_Code",
        "channel_id": int(os.getenv("WUTHERING_CHANNEL_ID", 0)),
        "color": 0x9933ff,
        "redeem_url": None
    }
}
# ========================================================
