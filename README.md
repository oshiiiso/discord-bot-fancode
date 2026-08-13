# Discord Bot - FanCode

HoYoverse系ゲーム（原神・崩壊：スターレイル・ゼンレスゾーンゼロ・鳴潮）の交換コードを
Wiki(Fandom)から自動取得し、Discordチャンネルに通知するBot

## 機能

- 1時間ごとに各ゲームの最新交換コードを自動チェック
- 新規コードをEmbedで通知（期限切れのコードは通知対象から除外）
- `!check` で手動チェックを即時実行
- `!clear` でメッセージ・保存データを削除
- `!ping` でBotの死活確認

## ディレクトリ構成

```
main.py           # エントリーポイント
fancode_bot/
  config.py       # 設定・定数（GAME_CONFIG等）
  logger_setup.py # ロガー設定
  storage.py      # 保存済みコード・メッセージIDの読み書き
  scraper.py      # Wikiスクレイピング・期限判定
  embeds.py       # Discord Embed生成・送信
  checker.py      # 全ゲームチェックのコアロジック
  events.py       # on_ready・定期実行タスク
  commands.py     # !clear, !check, !ping コマンド
data/             # 生成される保存データ(.gitignore対象)
logs/             # ログファイル(.gitignore対象)
```

## セットアップ
1. 依存パッケージのインストール

    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. プロジェクトルートに`.env.example` ファイルから `.env` をコピー

    ```
    DISCORD_BOT_TOKEN=your_bot_token_here
    DEBUG_MODE=False
    GENSHIN_CHANNEL_ID=your_channel_id
    STARRAIL_CHANNEL_ID=your_channel_id
    ZZZ_CHANNEL_ID=your_channel_id
    WUTHERING_CHANNEL_ID=your_channel_id
    ```

3. 通知するDiscordチャンネル4つを作成（場所・名称自由）
    ```
    通知カテゴリ
    ├原神コード
    ├スタレコード
    ├ゼンゼロコード
    └鳴潮コード
    ```

4. 各チャンネルのIDを`.env`の対応する項目に設定

5. Botを起動

    ```powershell
    python main.py
    ```

## コマンド一覧

| コマンド | 説明 | 権限 |
|---|---|---|
| `!check` | 全ゲームのコードチェックを即時実行 | manage_messages |
| `!clear [ゲームキー\|all] [件数]` | 指定ゲーム(または全ゲーム)のメッセージ・保存データを削除 | manage_messages |
| `!ping` | Botの応答速度を確認 | 誰でも |

## 対応ゲーム

- `genshin`: 原神
- `starrail`: 崩壊：スターレイル
- `zzz`: ゼンレスゾーンゼロ
- `wuthering`: 鳴潮
