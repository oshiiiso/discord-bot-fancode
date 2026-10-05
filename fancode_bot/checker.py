"""全ゲームの交換コードチェック処理のコアロジックを担当するモジュール。"""
import discord

from .config import GAME_CONFIG
from .logger_setup import debug_log, info_log
from .storage import (
    load_saved_codes,
    save_current_codes,
    load_message_id,
    save_message_id,
    sent_codes_exists,
    save_codes_data,
    save_last_check,
    append_history,
)
from .scraper import fetch_latest_codes
from .embeds import create_list_embed
from .addition_notices import register_addition_notice


async def run_check_all_games(bot):
    """全ゲームのコードチェック処理本体（初回・定期実行共通）"""
    debug_log("=== 全ゲームの定期チェックを開始 ===")

    for key, config in GAME_CONFIG.items():
        try:
            channel = bot.get_channel(config["channel_id"])
            if not channel:
                info_log(f"[警告] {config['name']} のチャンネルが見つかりません。")
                continue

            is_first_run = not sent_codes_exists(key)

            current_codes = fetch_latest_codes(key, config["url"])
            if current_codes is None:
                # ページ取得やテーブル解析に失敗した場合は、
                # 「有効なコードが0件」として誤保存しないようスキップする。
                info_log(f"[警告] {config['name']} のコード取得に失敗したため、今回のチェックをスキップします。")
                continue

            saved_codes = load_saved_codes(key)
            current_keys = set(current_codes.keys())

            added_codes = current_keys - saved_codes
            removed_codes = saved_codes - current_keys

            if added_codes or removed_codes or is_first_run:
                save_current_codes(key, current_keys)

                if not is_first_run:
                    if added_codes:
                        info_log(f"【{config['name']}】新しい交換コードが追加されました: {', '.join(added_codes)}")
                        append_history(key, "added", added_codes)
                    if removed_codes:
                        del_code_str = ", ".join([f"`{c}`" for c in removed_codes])
                        info_log(f"【{config['name']}】コードが期限切れになりました: {del_code_str}")
                        append_history(key, "removed", removed_codes)

            # 一覧の固定メッセージは、変更の有無に関わらず毎回編集して
            # 「最終確認」時刻を更新する。
            save_codes_data(key, current_codes)
            save_last_check(key)
            fixed_msg_id = load_message_id(key)
            embed = create_list_embed(config["name"], current_codes, config)

            if fixed_msg_id:
                try:
                    msg = await channel.fetch_message(fixed_msg_id)
                    await msg.edit(embed=embed)
                    debug_log(f"【{config['name']}】一覧メッセージを更新しました。")
                except discord.NotFound:
                    msg = await channel.send(embed=embed)
                    save_message_id(key, msg.id)
                    info_log(f"【{config['name']}】一覧メッセージが見つからず、新規投稿しました。")
            else:
                msg = await channel.send(embed=embed)
                save_message_id(key, msg.id)
                info_log(f"【{config['name']}】新しく一覧メッセージを投稿しました。")

            # コードが追加された場合のみ、別途お知らせメッセージを投稿する(3日後に自動削除)
            if not is_first_run and added_codes:
                code_str = ", ".join(f"`{c}`" for c in added_codes)
                notice = await channel.send(
                    f"🎉 【{config['name']}】新しい交換コードが追加されました：{code_str}",
                )
                register_addition_notice(bot, notice)

            if not (added_codes or removed_codes or is_first_run):
                debug_log(f"【{config['name']}】変更はありません。")
        except Exception as e:
            # 1ゲームのエラーでループ全体が止まらないようにする
            info_log(f"[エラー] {config['name']} の処理中に例外が発生しました: {e}")

    debug_log("=== 全ゲームのチェックが完了しました ===")
