# Discord Bot - FanCode

HoYoverse 系ゲーム（原神・崩壊：スターレイル・ゼンレスゾーンゼロ・鳴潮）の交換コードを Wiki（Fandom）から取得し、Discord に通知する Bot（Python + discord.py）

個人・身内利用向けに開発した Bot です。ソースは公開していますが、**不特定多数向けの配布・運用は想定していません**。使う場合は自分でセットアップするか、信頼できる人が管理するサーバーでのみ利用してください。

- リポジトリ: https://github.com/oshiiiso/discord-bot-fancode
- 不具合・要望: [Issues](https://github.com/oshiiiso/discord-bot-fancode/issues)
- 使い方: [docs/USER.md](docs/USER.md)

## 機能概要

- 各ゲームの交換コードを定期チェック（デフォルト 1 時間ごと）
- 有効なコード一覧を Embed の固定メッセージとして自動更新
- 新規コード追加時に別途通知（3 日後に自動削除）
- `/check` `/status` `/codes` `/history` などのスラッシュコマンド

## ディレクトリ構成

```
main.py                 # エントリーポイント
fancode_bot/            # Bot 本体（スクレイピング・通知・コマンド）
docs/USER.md            # セットアップ・運用ガイド
data/                   # 実行時データ（.gitignore）
logs/                   # ログ（.gitignore）
```

## 開発環境セットアップ

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # トークン・チャンネル ID を編集
python main.py
```

詳細な手順・権限設定・コマンド一覧は [docs/USER.md](docs/USER.md) を参照。

### 環境変数（`.env`）

| 変数 | 説明 | デフォルト |
|---|---|---|
| `DISCORD_BOT_TOKEN` | Bot トークン | —（必須） |
| `GUILD_ID` | 動作させるサーバー ID | 未設定時は制限なし |
| `GENSHIN_CHANNEL_ID` 等 | 各ゲームの通知チャンネル ID | —（必須） |
| `CHECK_INTERVAL_HOURS` | 自動チェック間隔（時間） | `1` |
| `LOG_LEVEL` | DEBUG / INFO / WARNING / ERROR | `INFO` |
| `LOG_RETENTION_DAYS` | ログ保持日数 | `30` |

`.env` は Git に含めません。

## ブランチ運用

| ブランチ | 用途 |
|---------|------|
| **develop** | 日常の開発 |
| **main** | 確定版（develop からマージ。タグ `v*` で版を管理） |

### 普段の開発

```powershell
git checkout develop
# 作業 → commit → push
git push origin develop
```

### 確定版を出す（例: v0.1.0）

```powershell
git checkout main
git merge develop -m "release: v0.1.0"
git tag v0.1.0
git push origin main --tags
git checkout develop
```

## 注意事項

- Fandom Wiki のスクレイピングに依存しています。サイト側の変更・障害のリスクは自己責任でください。
- 本 Bot は個人サーバー向けです。公開サービスとしての提供は想定していません。

## ライセンス

MIT License — Copyright (c) 2026 oshiiiso

詳細は [LICENSE](LICENSE) を参照。
