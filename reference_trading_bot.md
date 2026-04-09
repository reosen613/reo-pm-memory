---
name: trading_bot_project
description: Binance 24h auto-trading bot - Vultr稼働中だがアカウント制限でUSDT建て取引不可 → 戦略改修必要
type: reference
---

## 現状（2026-04-09 更新）

- **稼働状況: systemd稼働中だが取引執行不可（設計と権限のミスマッチ）**
- **🚨 致命的制約: BinanceアカウントがTRD_GRP_008制限**
  - USDT建てスポット取引（BTCUSDT/ETHUSDT/SOLUSDT/BNBUSDT/XRPUSDT）すべて`code=-2010 "This symbol is not permitted for this account"`で拒否
  - Convert APIもJPY→USDTおよびBTC→USDTは`code=345125 "pair temporarily unavailable"`で拒否
  - JPY建てスポット（BTCJPY/ETHJPY/SOLJPY/BNBJPY/XRPJPY）は全部TRADING可、Convert BTC→JPYも可
  - 原因推定: 地域・KYCベースの取引グループ制限（おそらく日本居住者向けBinance JP制約）
- **2026-04-09の検証経緯**:
  1. ユーザー指示でJPY 15,000 → USDT両替を試行
  2. BTCJPY市場買い成功（0.00131968 BTC取得）
  3. BTCUSDT市場売りで`-2010 not permitted`発覚 → 制約判明
  4. BTCJPY市場売りでロールバック完了（最終損失: 約38 JPY ≒ $0.24、BTCダスト6.8e-07残）
  5. 最終残高: JPY 49,961.63 / USDT 0 / BTC dust
- **bot.pyは現状動いてもシグナル発生時に必ず注文エラーで死ぬ** → 戦略をJPY建てに改修するか、別取引所へ移行が必要

**Why:** ユーザーは「動いている」と理解していたが、設計（USDT建て）とアカウント制約（JPYのみ）が根本的に非互換だった
**How to apply:** ユーザーが「botどうなってる？」と聞いたら、systemctl statusだけでなく**この制約を必ず思い出して告げる**。USDT入金/両替は不可能。改修パスは `bot.py`/`strategy.py` をJPY建てに書き換え（BET_JPY=3000等）+ historical CSV再生成。

---

## サーバー / アクセス情報

- **Vultr本番**: `45.32.46.255`（Tokyo, Ubuntu 24.04, $6/月）
- **SSH鍵**: `C:\Users\reoak\.ssh\vultr_trading_bot`（ed25519, パスワードなし）
- **rootパスワード**: `C:\Users\reoak\.vultr_secrets\vultr_root.txt`（鍵認証失敗時のフォールバック用）
- **接続コマンド**: `ssh -i ~/.ssh/vultr_trading_bot root@45.32.46.255`
- **本番ディレクトリ**: `/opt/trading-bot/`
- **venv**: `/opt/trading-bot/venv/bin/python`
- **systemdサービス名**: `trading-bot.service`
- **ログファイル**: `/var/log/trading-bot.log`

## 運用コマンド（Vultr側）

- 状態確認: `systemctl status trading-bot`
- ログ確認: `tail -f /var/log/trading-bot.log`
- 再起動: `systemctl restart trading-bot`
- 停止: `systemctl stop trading-bot`
- journalctl: `journalctl -u trading-bot --since '1 hour ago'`

## ローカル開発環境

- **`C:\trading-bot\`** （OneDrive配下ではなくCドライブ直下、ローカル開発用）
- Git初期化済み（`.env`, `positions.json`, `__pycache__` は `.gitignore` で除外）
- バックアップ: `C:\Users\reoak\OneDrive\デスクトップ\Reo Akutsu\15_TradingBot_Backup\`

## 呼び戻しキーワード
ユーザーが以下のような言葉を使ったらこのプロジェクトを指している：
- 「自動売買」「トレーディングボット」「Binance」
- 「仮想通貨のやつ」「クリプトのやつ」
- 「BTCのbot」

## 構成ファイル（C:\trading-bot\）
- `bot.py` — メインループ（4時間サイクル、ポジション監視、エントリー/エグジット、メール通知）
- `strategy.py` — シグナル検出（200MA + 20本ブレイクアウト + 出来高1.5倍 + 1D足トレンドフィルター）
- `backtest.py` — バックテスト
- `fetch_data.py` — Binance過去データ取得
- `test_connection.py` — API接続確認
- `.env` — Binance APIキー（平文・要注意、Vultrにも同じものをアップロード済み）

## 戦略仕様
- 対象: BTC/ETH/SOL/BNB/XRP（USDT建て）
- エントリー: 4H足で `200MA上 + 20本高値ブレイク + 出来高1.5倍 + 1D足200MA上`
- SL -3% / TP +6% / 最大保有240時間（10日）
- 1トレード20 USDT、最大同時3ポジション
- ライブラリ: `python-binance`（ccxtではない）

## Binance APIキー設定
- IPホワイトリスト: ローカルIP + Vultr 45.32.46.255 が登録済み
- APIキーが`-2015 Invalid API-key, IP, or permissions`を返す場合はホワイトリスト要確認
