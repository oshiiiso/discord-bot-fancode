# Discord Bot - FanCode

HoYoverse系ゲーム（原神・崩壊：スターレイル・ゼンレスゾーンゼロ・鳴潮）の交換コードを
Wiki(Fandom)から自動取得し、Discordチャンネルに通知するBot

## 機能

- 1時間ごとに各ゲームの最新交換コードを自動チェック
- 現在有効なコード一覧をEmbedで固定メッセージとして投稿・自動更新（期限切れのコードは一覧から除外）
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
1. Discord Botを `Discord Developer Portal` で作成し下記を設定
    1. `Oauth2` の`OAuth2 URLジェネレーターのスコープ `bot`を選択
    2. Botの権限で下記を設定
    ```
    テキストの権限
    - メッセージを送る
    - メッセージを管理
    - リンクを埋め込み
    - メッセージ履歴を読む
    ```
    3.Botを自身のサーバーへ追加する

2. 依存パッケージのインストール

    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. プロジェクトルートに`.env.example` ファイルから `.env` をコピー

    ```
    LOG_LEVEL=INFO

    DISCORD_BOT_TOKEN=xxxxxxxxxx
    GUILD_ID=123456789012345678

    COMMAND_PREFIX=!
    CHECK_INTERVAL_HOURS=1
    LOG_RETENTION_DAYS=30

    GENSHIN_CHANNEL_ID=123456789012345678
    STARRAIL_CHANNEL_ID=123456789012345678
    ZZZ_CHANNEL_ID=123456789012345678
    WUTHERING_CHANNEL_ID=123456789012345678
    ```

    - `LOG_LEVEL`
      - 出力するログレベル(DEBUG、INFO、WARNING、ERROR)
    - `GUILD_ID`
      - Botが動作するサーバー(Guild)を1つに限定するための設定
        開発用サーバーと本番サーバーで別々のBotトークンを使う場合の保険として、
        指定したサーバー以外ではコマンドが一切反応しなくなる(未設定: 制限なし)
    - `COMMAND_PREFIX`
      - 開発用と本番用でコマンドのプレフィックスを変えたい場合に変更する(未設定: `!`)
    - `CHECK_INTERVAL_HOURS`
      - は交換コードの自動チェック間隔(未設定: 1時間)
    - `LOG_RETENTION_DAYS`
      - ログファイルの保持日数
        ログは日付ごとに自動でローテーションされ、この日数を超えた古いログファイルは自動削除(未設定: 30日)

4. 通知するDiscordチャンネル4つを作成（場所・名称自由）
    ```
    通知カテゴリ
    ├原神コード
    ├スタレコード
    ├ゼンゼロコード
    └鳴潮コード
    ```

5. サーバー、チャンネルのIDを`.env`の対応する項目に設定

6. Botを起動

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
