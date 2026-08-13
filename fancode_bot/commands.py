"""開発用のBotコマンド（!clear, !check）を登録するモジュール。"""
from discord.ext import commands

from .config import GAME_CONFIG
from .logger_setup import debug_log, info_log
from .storage import delete_game_files
from .checker import run_check_all_games


def setup_commands(bot):
    """!clear, !check コマンドをbotに登録する。"""
    @bot.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(ctx, target: str = "all", amount: int = 100):
        """!clear [ゲームキー|all] [数字] で指定ゲーム(または全ゲーム)のメッセージ・保存データを削除する"""
        try:
            await ctx.message.delete()
        except Exception:
            pass
        targets = GAME_CONFIG.items() if target == "all" else (
            [(target, GAME_CONFIG[target])] if target in GAME_CONFIG else []
        )
        if not targets:
            await ctx.send(f"指定されたゲームキー '{target}' は存在しません。", delete_after=3)
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

        scope = "全ゲーム" if target == "all" else GAME_CONFIG[target]["name"]
        await ctx.send(f"{scope}のメッセージと保存データを削除しました。", delete_after=3)


    @bot.command(name='check')
    @commands.has_permissions(manage_messages=True)
    async def manual_check(ctx):
        """!check で即座に全ゲームのコードチェックを手動実行する"""
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send("手動チェックを開始します...", delete_after=3)
        await run_check_all_games(bot)
        await ctx.send("手動チェックが完了しました。", delete_after=3)


    @bot.command(name='ping')
    async def ping(ctx):
        """!ping でBotの応答速度を確認する"""
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send(f"Pong! {round(bot.latency * 1000)}ms", delete_after=3)
