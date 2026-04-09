---
name: mck_ppt_shortcut
description: McKinsey風PowerPointショートカットadd-in - v1完成済み、追加編集の可能性あり、将来的な販売も検討
type: project
---

## 現状（2026-04-09時点）

- **ステータス: v1完成・アウトプット完了**
- PowerPoint add-in（.ppam）として動作
- VBA + AutoHotKey連携、align-by-first-selected等の機能を実装
- クイックアクセスツールバー化まで完了
- **次のアクション: 当面なし**（必要に応じて編集する程度）
- **将来の可能性: 販売を検討**（McK出身者・コンサル業界向けプロダクトとして）

**Why:** McK時代のPPT作業効率化を再現するツール。完成したので一旦区切り。販売はマネタイズの選択肢
**How to apply:** ユーザーが「ショートカット直したい」と言ったら編集モード、「販売どうしよう」と言ったらプロダクト化の議論モードで応答する

## プロジェクト場所
`01_Mckinsey\01_Shortcut\02_PPT`

## 呼び戻しキーワード
- 「McKのadd-in」「ショートカット」「PPTのアレ」「.ppam」「VBA」
- 「アライン揃えるやつ」「align-by-first-selected」

## 技術構成
- `.ppam` PowerPoint Add-in形式
- VBAマクロ（コンパイルエラー対応済み）
- AutoHotKey（.ahk）連携でキーバインド
- クイックアクセスツールバー登録済み
