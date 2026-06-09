---
title: Lesson 010 — Stock Selection: Defensive Investor の 7 Statistical Tests
phase: 1
date: 2026-06-09
estimated_reading: ~10 min
---

# Lesson 010 — Stock Selection: Defensive Investor の 7 Statistical Tests

## 1 行で
Graham が Defensive Investor 向けに定めた 7 つの定量スクリーンは、「安全性・安定性・割安感」を同時に要求する最低限のフィルターであり、どの銘柄を "考慮に値する" リストに載せるかを機械的に絞り込む。

---

## なぜ今それをやるか

Lesson 009 では Defensive Investor の Portfolio Policy（60/40 原則・分散・品質基準）を概念レベルで学んだ。本日はその **定量的な実装**——Graham が Chapter 14 で提示した 7 statistical tests——を完全に習得する。Schweitzer v6 でスクリーニングロジックを組む際、あるいはファンドインタビューで「どう銘柄を絞るか」を問われた際に、即座に構造化して答えられるようにする。

---

## Core Content

### Graham の 7 Statistical Tests（Defensive Investor 向け）

Graham は *The Intelligent Investor* Chapter 14 で以下 7 基準を提示した。これらを全て満たす銘柄だけが Defensive Investor の検討対象になる。

| # | 基準 | Graham の数値 | 意図 |
|---|------|-------------|------|
| 1 | **Adequate size** | 売上高 ≥ $1 億（製造業）/ 総資産 ≥ $5,000 万（公益） | 小型・薄商い回避。流動性・事業安定性の proxy |
| 2 | **Strong financial condition** | 流動比率（Current Ratio）≥ 2.0 × ／ 長期負債 ≤ 純運転資本 | 短期・長期両方の支払い能力を要求 |
| 3 | **Earnings stability** | 直近 10 年間、赤字年度ゼロ | 景気サイクル全体での耐性を確認 |
| 4 | **Dividend record** | 直近 20 年間、無配年度ゼロ | 株主還元の継続性。経営者の規律の代理指標 |
| 5 | **Earnings growth** | 直近 10 年で EPS が +33%以上 成長（= 年率 約 3%） | 実質的に事業価値が減耗していないこと |
| 6 | **Moderate P/E** | 直近 3 年平均 EPS 比で PER ≤ 15× | 高値掴みを防ぐ |
| 7 | **Moderate price-to-assets ratio** | PBR ≤ 1.5×（ただし PER×PBR ≤ 22.5 を推奨） | 資産価値に比した過大評価を防ぐ |

### ルール 6＋7 の統合式

Graham は **PER × PBR ≤ 22.5** という乗算ルールを提案した。これにより、

- 超低 PBR（0.5×）なら PER は 45× まで許容
- 逆に PBR が 2.0× なら PER は 11.25× 以下が必要

…と柔軟なトレードオフを可能にした。この式は今でも Quant スクリーンの原型として有効。

### なぜ "7 全部" が必要か

Graham の主張のポイントは「一つでも欠けると他の強みで補えない」こと。たとえば：

- 財務安定（基準 2）は強いが赤字歴がある（基準 3 ×）→ 景気後退時に致命的
- EPS 成長（基準 5）は十分だが PER 25×（基準 6 ×）→ 成長が折り込まれており MOS がない

全基準の同時充足が、Defensive Investor にとっての **Margin of Safety の定量的表現** である。

### 日本株への適用上の注意点

| 論点 | Graham 原文 | 日本適用時の調整 |
|------|------------|----------------|
| サイズ基準 | $1 億売上（1980年代基準） | 売上高 100 億円超・時価総額 300 億円超が実務的目安 |
| 流動比率 2× | 製造業に適用 | 銀行・保険は除外。事業会社でも業種差大 |
| 20 年無配 | 厳しすぎる | リーマン・東日本震災で減配した企業は多い。10 年・15 年に緩和可 |
| PER ≤ 15× | 現在の TSE Prime 中央値は 15〜18× 程度 | スクリーン後に残る銘柄は限られる |
| PBR ≤ 1.5× | 日本株の 約 45% が PBR<1 の現状（2024） | この基準は日本では通りやすい |

---

## Reo への実用的 Application

**ウォッチリスト照合（Long side）**

| 銘柄 | 推定 PBR | 推定 PER | 基準 2（流動比率） | 概略評価 |
|------|---------|---------|-----------------|---------|
| 8864 武蔵コーポ | 〜1.2× | 〜12× | 要確認 | 6/7 基準通過候補 |
| 5451 淀川製鋼 | 〜0.6× | 〜10× | 高い傾向 | 典型的 Graham 銘柄候補 |
| 1969 高砂熱学 | 〜1.0× | 〜12× | 安定 | 配当継続性を確認要 |
| 4204 積水化学 | 〜1.5× | 〜15× | 十分 | 基準 6×7 がギリギリ |
| 1928 積水ハウス | 〜1.3× | 〜12× | 安定 | 20 年配当継続？要調査 |

**Schweitzer v6 スクリーニングへの組み込み**
- v6 の初期スクリーンに「PER×PBR ≤ 22.5」と「10 年赤字なし」を追加することで、Graham 基準の Defensive Investor フィルターを自動化できる。
- 特に **EPS 10 年成長 +33%** は「価値破壊企業を除外するための最低ハードル」として有用——これを下回る企業は実質的にインフレに負けている。

**ファンドインタビュー対応**
Camphora・Kaname・AVI London などの Engagement / Activist Fund は「なぜこの銘柄を選んだか」を問う。Graham の 7 基準で **スクリーニング通過率が低い理由**（例：PBR<1 でも EPS が縮小傾向）を説明できると、「ファンダメンタルズから入り、カタリストを重ねる」思考プロセスが伝わる。

---

## Self-test（明日説明できるか）

1. **Graham の基準 6 と基準 7 を単独適用するのではなく、乗算（PER×PBR ≤ 22.5）で使う意図は何か？**

2. **「20 年無配なし」基準が日本株に厳しすぎる理由を 2 つ挙げ、どの年数に緩和すれば実務的か説明せよ。**

3. **ウォッチリストの 5451 淀川製鋼が Graham の 7 基準を通過しやすい理由と、おそらく引っかかる基準を推論せよ。**

---

## Source
- Benjamin Graham, *The Intelligent Investor*, Chapter 14 "Stock Selection for the Defensive Investor" (revised edition, 1973)
- Jason Zweig コメンタリー同章（PBR×PER 乗算の解説）
- TSE 資料「PBR1 倍割れ企業の分布」2024 年版（基準 7 の日本適用に関する考察は筆者による）

---

## 次回（Lesson 011）: Stock Selection for the Enterprising Investor の bargain issues
Graham が Enterprising Investor 向けに定めた「掘り出し物株（Bargain Issues）」の探し方——NCAV スクリーン前夜の論理と、Defensive との基準差分を学ぶ。
