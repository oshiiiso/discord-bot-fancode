"""Discordへの表示関連（Embed生成）を担当するモジュール。"""
from datetime import datetime

import discord

from .scraper import translate_expiry


def create_list_embed(game_name, current_codes, config):
    embed = discord.Embed(
        title=f"【{game_name}】現在有効な交換コード一覧",
        color=config["color"]
    )
    if not current_codes:
        embed.description = "現在、有効な交換コードはありません。"
        return embed

    show_reward = config.get("show_reward", False)

    lines = []
    for code, info in current_codes.items():
        expiry_jp = translate_expiry(info.get("expiry", "不明"))
        rewards = info.get("reward", "")

        if config.get("redeem_url"):
            link = f"{config['redeem_url']}{code}"
            link_part = f"[🔗 入力する]({link})"
        else:
            link_part = "🎮 ゲーム内で入力"

        block = f"🔸 **`{code}`**\n{link_part}　|　⏳ {expiry_jp}"
        if show_reward and rewards:
            block += f"\n🎉 {rewards}"
        lines.append(block)

    # 1フィールドの上限(1024文字)を超えないよう分割してフィールド追加
    current_chunk = ""
    for line in lines:
        addition = line + "\n\n"
        if len(current_chunk) + len(addition) > 1024:
            embed.add_field(name="\u200b", value=current_chunk, inline=False)
            current_chunk = ""
        current_chunk += addition
    if current_chunk:
        embed.add_field(name="\u200b", value=current_chunk, inline=False)

    embed.set_footer(text=f"合計 {len(current_codes)} 件 ｜ 1時間ごとに自動更新中")
    embed.timestamp = datetime.now()
    return embed
