# FanCode 交換コード通知 Bot 使い方

HoYoverse 系ゲームの交換コードを Wiki から取得し、Discord チャンネルへ通知します。

> **個人・身内利用向け**  
> 信頼できるサーバーでのみ運用してください。不具合・要望は [Issues](https://github.com/oshiiiso/discord-bot-fancode/issues) へ。

---

## セットアップ

### 1. Discord Bot の準備

1. [Discord Developer Portal](https://discord.com/developers/applications) で Bot を作成
2. **OAuth2 URL Generator** で `bot` と `applications.commands` を選択
3. Bot 権限の例:
   - メッセージを送る / 管理 / リンクを埋め込み / メッセージ履歴を読む
4. サーバーに Bot を招待

### 2. 環境構築

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

`.env` を編集（最低限）:

- `DISCORD_BOT_TOKEN` … Bot トークン
- `GUILD_ID` … サーバー ID（推奨。他サーバーでの誤動作を防げる）
- `GENSHIN_CHANNEL_ID` / `STARRAIL_CHANNEL_ID` / `ZZZ_CHANNEL_ID` / `WUTHERING_CHANNEL_ID` … 各ゲームの通知チャンネル

### 3. チャンネル構成の例

```
通知カテゴリ
├ 原神コード
├ スタレコード
├ ゼンゼロコード
└ 鳴潮コード
```

チャンネル名は自由です。ID を `.env` に設定してください。

### 4. 起動

```powershell
python main.py
```

起動後、各チャンネルに有効コード一覧の固定メッセージが投稿・更新されます。

---

## コマンド一覧

| コマンド | 説明 | 権限 |
|---|---|---|
| `/check` | 全ゲームのコードチェックを即時実行 | manage_messages |
| `/clear [target] [amount]` | 指定ゲーム（または全ゲーム）のメッセージ・保存データを削除 | manage_messages |
| `/status` | 各ゲームの最終確認・次回チェック・件数を確認 | 誰でも |
| `/codes <target>` | 指定ゲームの有効コード一覧を表示 | 誰でも |
| `/history <target> [count]` | 指定ゲームの追加・削除履歴を表示 | 誰でも |
| `/ping` | 応答速度を確認 | 誰でも |

### 対応ゲーム（`target` の値）

| 値 | ゲーム |
|---|---|
| `genshin` | 原神 |
| `starrail` | 崩壊：スターレイル |
| `zzz` | ゼンレスゾーンゼロ |
| `wuthering` | 鳴潮 |
| `all` | 全ゲーム（`/clear` のみ） |

---

## よくある質問

**Q. 通知が来ない**  
A. 各 `*_CHANNEL_ID` と Bot のチャンネル権限を確認してください。`/check` で手動実行し、`logs/` のログも見てください。

**Q. 固定メッセージが更新されない**  
A. Bot に「メッセージを管理」「メッセージ履歴を読む」権限があるか確認してください。`/clear` でリセットしてから再起動も試せます。

**Q. スラッシュコマンドが出ない**  
A. `GUILD_ID` を設定して Bot を再起動してください。

**Q. Wiki の構造が変わって動かなくなった**  
A. Fandom 側の変更が原因のことがあります。[Issues](https://github.com/oshiiiso/discord-bot-fancode/issues) で報告してください。

---

## 問い合わせ

不具合・要望は GitHub の [Issues](https://github.com/oshiiiso/discord-bot-fancode/issues) からお願いします。

- **トークンや `.env` の内容は Issue に貼らないでください**
- ログを添える場合は個人情報・トークンを除いてください

---

## 注意

- 交換コードの正確性は Wiki 依存です。公式発表と照合してください
- チェック間隔は `CHECK_INTERVAL_HOURS` で調整できます
