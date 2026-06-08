---
title: Lesson 009 — General Portfolio Policy — defensive 側の 7-criteria 完全版
phase: 1
date: 2026-06-08
estimated_reading: ~10 min
---

# Lesson 009 — General Portfolio Policy: Defensive 側の 7-criteria 完全版

## 1 行で
Graham の "守備型" 投資家がポートフォリオに組み入れる株式には**7 つの定量スクリーン**があり、それを全て通過した銘柄だけを buy list に載せる。

---

## なぜ今それをやるか

Lesson 004–008 では守備型と積極型の概念的分離、60/40 の論拠、インフレ耐性、サイクルのパターンを学んだ。今夜は「ではどんな株を買うのか」の**操作的定義**に入る。Graham は理念を語るだけでなく、数字で切る。この 7 criteria は Lesson 010（Defensive Investor の 7 statistical tests）の伏線でもあり、来週の Phase 2 会計ブロックの前に "何を測るか" を先にインストールしておく狙いがある。

---

## Core Content

### 7 つの基準（The Intelligent Investor, Ch.14 完全版）

| # | 基準名 | Graham の閾値 | 現代的読み替え |
|---|--------|--------------|--------------|
| 1 | **Adequate size** | 売上 ≥ $100M（工業）/ 総資産 ≥ $50M（公益） | 時価総額換算で流動性確保・TSE Prime なら ~300–500 億円目安 |
| 2 | **Sufficiently strong financial condition** | 流動比率 ≥ 2.0×、長期負債 ≤ 純運転資本 | 銀行・保険は別建て（P/TBV, BIS 比率で代替） |
| 3 | **Earnings stability** | 過去 10 年間、赤字なし | 赤字期間ゼロが条件。リーマン・コロナを挟んでも黒字維持か |
| 4 | **Dividend record** | 過去 20 年間、途絶えなし | 増配でなくてよい。無配落としの歴史がないこと |
| 5 | **Earnings growth** | 過去 10 年 EPS 累計で ≥ +33%（≒ 3% CAGR） | インフレ調整済みで実質成長があるか |
| 6 | **Moderate P/E** | 直近 3 年平均 EPS で PER ≤ 15× | 単年 EPS での PER より景気平均化 PER（Shiller 型） |
| 7 | **Moderate price-to-assets** | PBR ≤ 1.5×、または PER × PBR ≤ 22.5 | 複合スクリーン：PER 15× × PBR 1.5× = 22.5 がハードルライン |

### 複合スクリーン（基準 6 × 7）の意味

Graham が「PER 15 かつ PBR 1.5 以下」とせず**積の 22.5 以下**を許容したのは、高 ROE 株（PBR が張っても PER が低い）をスクリーンアウトしすぎない実用的な妥協である。式として：

```
PER × PBR ≤ 22.5
例） PER = 9× / PBR = 2.4× → 9 × 2.4 = 21.6 ✓（合格）
    PER = 15× / PBR = 1.6× → 15 × 1.6 = 24.0 ✗（不合格）
```

### なぜ 7 つ全部必要か

各基準は異なるリスクを捕捉している：

- **1–2**（サイズ・財務安定）→ 流動性リスク・倒産リスク
- **3–4**（安定性・配当）→ 景気耐性・経営姿勢
- **5**（成長）→ 実質購買力の維持
- **6–7**（バリュエーション）→ 過払いリスク

この 7 基準は **"safety margin の入口チェックリスト"** であり、全部通過しても安全を保証しないが、大きな損失を蒙るリスクを統計的に下げる設計だ。

---

## Reo への実用的 application

### 長期 watchlist への機械的適用

**8393 りそなホールディングス（Long）**
- サイズ ✓（銀行は総資産換算で十分）
- 財務安定：流動比率は銀行には不適。BIS Tier1 ~12% で代替 → ✓
- 10 年無赤字 ✓（コロナも黒字維持）
- 20 年配当継続：2008 公的資金返済後で途絶え歴あり → 要確認
- EPS 成長 +33%：利ざや圧縮で要検証
- PER × PBR：PER ~9× / PBR ~0.7× → 6.3 ✓ 余裕合格

**4204 積水化学（Long）**
- 10 年無赤字 ✓、20 年連続配当 ✓
- PER ~11× / PBR ~1.2× → 13.2 ✓
- EPS 10 年 +33%：住宅・インフラ事業でほぼ達成 ✓

**ショート候補精査**：基準 3（赤字歴）か基準 6–7（PER × PBR > 22.5）で弾かれる銘柄は "defensive investor が本来買わない株" → 高バリュエーション株の崩落リスクを裏打ちするショート論拠になりうる。

### Camphora / Kaname 面接での使い方

これらのファンドは「なぜその株を守備的に保有できるか」の規律を問う。Graham 7 criteria を暗唱できると、**スクリーニング → ファンダメンタル分析** の 2 段構造を示せる。「まず Graham フィルターで 500 社から 30 社に絞り、そこから DCF と M-Score で精査する」と言えれば工程の説明力が高い。

---

## Self-test（明日説明できるか）

1. **Graham の 7 criteria を番号順に言えるか？** — 特にバリュエーション 2 基準の複合スクリーン（PER × PBR ≤ 22.5）の計算式を含めて。

2. **PER = 12×、PBR = 2.0× の銘柄は Graham の基準 6–7 を通過するか？** — 積 = 24.0 → 不合格。ではどのような調整が考えられるか（EPS を 3 年平均化するなど）。

3. **8393 りそなに Graham 7 criteria を当てはめたとき、最も "グレーゾーン" になりそうな基準はどれか、その理由は？**

---

## Source
- Graham, B. *The Intelligent Investor* (rev. ed. 2003), Chapter 14 "Stock Selection for the Defensive Investor" — 7 criteria の一次定義
- Zweig commentary (同書 pp.348–368) — 現代株式市場への読み替えの補足
- 基準の現代適用（PBR < 1 TSE 圧力文脈）は筆者によるアレンジ

---

## 次回（Lesson 010）: Stock Selection — Defensive Investor の 7 statistical tests
Lesson 009 が "何を基準にするか" なら、010 は **Graham 自身が実際に数字をどう計算・比較したか** の実践編。4 社の比較表を使って統計検定の手順をなぞる。Reo の watchlist から 1 銘柄を選んで同じ表を作ってみると定着が速い。
