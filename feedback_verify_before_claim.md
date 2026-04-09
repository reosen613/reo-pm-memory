---
name: verify_before_claim
description: Never claim infrastructure/deployment is working without concrete evidence. Show proof, then claim.
type: feedback
---

デプロイ・サービス起動・「動いている」系の状態は、**実行コマンドの出力で証明してから報告する**。「セットアップしました」「動いています」だけで終わらせない。

**Why:** 過去にBinance自動売買botを「Vultrで24時間稼働中」と報告したが、実際には一度もデプロイされていなかった。`bot.py`/`strategy.py`/`.env`はサーバーにアップロードすらされておらず、systemd/cronもなく、ユーザーは$6/月を払いながら何も動いていない状態が続いた。検証なしの報告がユーザーに実害を与えた。

**How to apply:**
- 「サービス起動した」と言う前に `systemctl status` の出力を貼る
- 「ファイルアップロードした」と言う前にサーバー側で `ls -la` の出力を貼る
- 「APIに接続できる」と言う前に実際の接続テストの出力を貼る
- 「自動復帰する」と言う前に `systemctl is-enabled` の確認をする
- 1ステップ完了するたびに、次のステップの前に検証コマンドを挟む
- 検証できないものは「未検証」と明示する。推測で「たぶん動いてます」と言わない
- VPSデプロイ案件では特に、**動いている証拠＝ログに新しいタイムスタンプ・実際のシグナルスキャン出力**を確認するまで「稼働中」と言わない
