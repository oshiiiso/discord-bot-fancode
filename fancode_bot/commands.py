"""管理用のスラッシュコマンド（/clear, /check, /ping, /status, /codes, /history）を登録するモジュール。"""
from datetime import datetime, timedelta

import discord
from discord import app_commands

from .config import GAME_CONFIG, CHECK_INTERVAL_HOURS
from .logger_setup import debug_log, info_log
from .storage import (
    delete_game_files,
    load_last_check,
    load_codes_data,
    load_history,
    remove_pending_addition_notices_for_channel,
)
from .checker import run_check_all_games
from .embeds import create_list_embed

GAME_CHOICES = [app_commands.Choice(name="全ゲーム", value="all")] + [
    app_commands.Choice(name=cfg["name"], value=key) for key, cfg in GAME_CONFIG.items()
]
GAME_ONLY_CHOICES = [
    app_commands.Choice(name=cfg["name"], value=key) for key, cfg in GAME_CONFIG.items()
]


def setup_commands(bot):
    """/clear, /check, /ping, /status, /codes, /history コマンドをbotに登録する。"""

    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
            return
        if isinstance(error, app_commands.CheckFailure):
            # サーバー制限(restrict_to_configured_guild)等で弾かれた場合
            return
        info_log(f"[エラー] コマンド実行中に例外が発生しました: {error}")
        if interaction.response.is_done():
            await interaction.followup.send("エラーが発生しました。", ephemeral=True)
        else:
            await interaction.response.send_message("エラーが発生しました。", ephemeral=True)

    @bot.tree.command(name="clear", description="指定ゲーム(または全ゲーム)のメッセージ・保存データを削除する")
    @app_commands.describe(target="対象ゲーム(未指定なら全ゲーム)", amount="削除するメッセージ件数(既定100件)")
    @app_commands.choices(target=GAME_CHOICES)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_messages(interaction: discord.Interaction, target: str = "all", amount: int = 100):
        await interaction.response.defer(ephemeral=True)

        targets = GAME_CONFIG.items() if target == "all" else (
            [(target, GAME_CONFIG[target])] if target in GAME_CONFIG else []
        )
        if not targets:
            await interaction.followup.send(f"指定されたゲームキー '{target}' は存在しません。", ephemeral=True)
            return

        for key, game_config in targets:
            channel = bot.get_channel(game_config["channel_id"])
            if not channel:
                info_log(f"[警告] {game_config['name']} のチャンネルが見つかりません。")
                continue
            try:
                deleted = await channel.purge(limit=amount)
                info_log(f"[ログ] {channel.name} でメッセージを {len(deleted)} 件削除しました。")
            except Exception as e:
                info_log(f"[エラー] {channel.name} の削除中に例外が発生しました: {e}")

            # 保存されているtxtファイルも削除する
            for filename in delete_game_files(key):
                debug_log(f"{filename} を削除しました。")
            remove_pending_addition_notices_for_channel(game_config["channel_id"])

        scope = "全ゲーム" if target == "all" else GAME_CONFIG[target]["name"]
        await interaction.followup.send(f"{scope}のメッセージと保存データを削除しました。", ephemeral=True)

    @bot.tree.command(name="check", description="即座に全ゲームの交換コードチェックを手動実行する")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def manual_check(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await run_check_all_games(bot)
        await interaction.followup.send("手動チェックが完了しました。", ephemeral=True)

    @bot.tree.command(name="ping", description="Botの応答速度を確認する")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True)

    @bot.tree.command(name="status", description="各ゲームの稼働状況(最終確認・次回チェック・件数)を確認する")
    async def status(interaction: discord.Interaction):
        now = datetime.now()
        lines = []
        for key, cfg in GAME_CONFIG.items():
            last_check = load_last_check(key)
            codes_data = load_codes_data(key)
            count = len(codes_data)

            if last_check:
                next_check = last_check + timedelta(hours=CHECK_INTERVAL_HOURS)
                remaining = (next_check - now).total_seconds()
                last_str = last_check.strftime("%Y-%m-%d %H:%M")
                if remaining > 0:
                    remaining_min = int(remaining // 60)
                    next_str = f"あと約{remaining_min}分"
                else:
                    next_str = "まもなく実行"
            else:
                last_str = "未実行"
                next_str = "不明"

            lines.append(f"**【{cfg['name']}】** 有効コード {count}件 ｜ 最終確認: {last_str} ｜ 次回チェック: {next_str}")

        embed = discord.Embed(
            title="Bot稼働状況",
            description="\n".join(lines),
            color=0x3498db,
        )
        embed.timestamp = now
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="codes", description="指定ゲームの現在有効な交換コード一覧をその場で確認する")
    @app_commands.describe(target="確認したいゲーム")
    @app_commands.choices(target=GAME_ONLY_CHOICES)
    async def codes(interaction: discord.Interaction, target: str):
        cfg = GAME_CONFIG.get(target)
        if not cfg:
            await interaction.response.send_message(f"指定されたゲームキー '{target}' は存在しません。", ephemeral=True)
            return
        codes_data = load_codes_data(target)
        embed = create_list_embed(cfg["name"], codes_data, cfg)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="history", description="指定ゲームの直近のコード追加・削除履歴を確認する")
    @app_commands.describe(target="確認したいゲーム", count="表示する件数(既定10件)")
    @app_commands.choices(target=GAME_ONLY_CHOICES)
    async def history(interaction: discord.Interaction, target: str, count: int = 10):
        cfg = GAME_CONFIG.get(target)
        if not cfg:
            await interaction.response.send_message(f"指定されたゲームキー '{target}' は存在しません。", ephemeral=True)
            return

        entries = load_history(target)[-count:]
        if not entries:
            await interaction.response.send_message(f"【{cfg['name']}】の履歴はまだありません。", ephemeral=True)
            return

        lines = []
        for entry in reversed(entries):
            ts = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
            label = "追加" if entry["type"] == "added" else "削除(期限切れ)"
            code_str = ", ".join(f"`{c}`" for c in entry["codes"])
            lines.append(f"{ts} ｜ {label} ｜ {code_str}")

        embed = discord.Embed(
            title=f"【{cfg['name']}】履歴（直近{len(entries)}件）",
            description="\n".join(lines),
            color=cfg["color"],
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
