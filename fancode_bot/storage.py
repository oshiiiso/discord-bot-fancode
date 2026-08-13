"""送信済みコード・固定メッセージIDの永続化を担当するモジュール。"""
import os

from .config import DATA_DIR


def _sent_codes_path(game_key):
    return os.path.join(DATA_DIR, f"sent_codes_{game_key}.txt")


def _msg_id_path(game_key):
    return os.path.join(DATA_DIR, f"msg_id_{game_key}.txt")


def sent_codes_exists(game_key):
    return os.path.exists(_sent_codes_path(game_key))


def load_saved_codes(game_key):
    filename = _sent_codes_path(game_key)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def save_current_codes(game_key, codes_set):
    filename = _sent_codes_path(game_key)
    with open(filename, "w", encoding="utf-8") as f:
        for code in codes_set:
            f.write(f"{code}\n")


def load_message_id(game_key):
    filename = _msg_id_path(game_key)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            val = f.read().strip()
            return int(val) if val.isdigit() else None
    return None


def save_message_id(game_key, msg_id):
    filename = _msg_id_path(game_key)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(msg_id))


def delete_game_files(game_key):
    """指定ゲームの保存済みファイル（sent_codes, msg_id）を削除する。"""
    deleted = []
    for path in (_sent_codes_path(game_key), _msg_id_path(game_key)):
        if os.path.exists(path):
            os.remove(path)
            deleted.append(path)
    return deleted
