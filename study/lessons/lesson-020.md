---
title: Lesson 020 — Bargain Issues: Net-Net NCAV の Graham signature
phase: 1
date: 2026-06-22
estimated_reading: ~10 min
---

# Lesson 020 — Bargain Issues: Net-Net NCAV の Graham signature

## 1 行で
Graham が最も信頼したバーゲン手法は「株価が流動資産から全負債を引いた額（NCAV）の 2/3 以下」であること——企業の事業価値をゼロとみなした上で、清算価値さえ買い値を上回るという究極の Margin of Safety。

---

## なぜ今それをやるか

Lesson 018・019 でDefensive / Enterprising の 7 criteria を学んだ。それらは「質の良い普通株を安く買う」アプローチだった。本日の NCAV はその **極端な特殊ケース**：事業など評価しない、純粋に貸借対照表の清算価値だけで割安を定義する。

日本市場は 2026 年現在でも TSE PBR<1 企業が約 40% 存在し、NCAV 銘柄が世界最多級の市場でもある。FIG IBD 出身の Reo には馴染みの深い「清算ロジック」を株式投資の文脈で再武装できる。

---

## Core Content

### 1. NCAV の定義

**Net Current Asset Value (NCAV)**
$$\text{NCAV} = \text{流動資産} - \text{総負債（流動 + 固定）}$$

Graham が示した購入基準：
$$\text{株価} \leq \frac{2}{3} \times \frac{\text{NCAV}}{\text{発行済株式数}}$$

つまり **NCAV per share の 67% 以下** で売られている株のみ対象とする。

### 2. なぜ「2/3」か

| 割引の理由 | 内容 |
|---|---|
| 流動資産の換金ロス | 現金以外の受取手形・棚卸資産は市場価格ではなく簿価で計上 |
| 固定資産を ¥0 評価 | 土地・設備はおまけ扱い——これが核心的な安全余裕 |
| 経営リスク・倒産コスト | 清算を強制された場合の手続きコスト・タイムラグ |
| 分散が前提 | 個別で外れてもポートフォリオ全体ではプラスになる |

### 3. NCAV < PBR の違い

混乱しやすいポイントを整理する。

| 指標 | 分母 | 固定資産 |
|---|---|---|
| P/B（PBR） | 純資産（= 総資産 − 総負債） | **含む** |
| P/NCAV | 流動資産 − 総負債 | **含まない**（ゼロ評価） |

PBR<1 は「純資産より安い」。NCAV<株価 はさらに厳しく「固定資産を捨てても損しない水準」。

### 4. Graham の実績データ（1926–1956）

- 30 年間のバックテストで NCAV 銘柄の平均リターンは **市場の約 2 倍超**
- 個別銘柄の 3 分の 1 は損失を出したが、ポートフォリオ全体で補えた
- 保有期間は 1〜3 年が典型、催化剤（M&A・自社株買い）待ち

### 5. 現代の日本市場での発見方法

```
スクリーニング式：
  (流動資産 ÷ 発行済株式数) - (総負債 ÷ 発行済株式数) × 0.67 > 株価

注意事項：
  ・銀行・保険は流動資産概念が異なるため除外
  ・持株会社も実態純資産が別会計のため要調整
  ・連続赤字で現金が燃え続けているキャッシュバーン銘柄は罠
```

### 6. Graham Net-Net の「死亡原因」3 パターン

| パターン | メカニズム | 対処 |
|---|---|---|
| Melting ice cube | 毎年赤字でNCAVが縮小 | FCFまたはEBITDAがプラスか確認 |
| Zombie | 経営陣がキャッシュを守り続け催化剤ゼロ | 株主提案・アクティビスト有無 |
| Trap | 流動資産の中に不良在庫・不回収債権 | 棚卸日数・DSO の経年変化 |

---

## Reo への実用的 application

**ショートサイド連動**：Reo の Short ウォッチリスト（4477・6027 など）は事業悪化銘柄だが、NCAV 分析をかけると「清算しても株主に価値が残るか」という Floor 価格が分かる。Floor が現在株価に近いほど、ショートのダウンサイドは限定的という逆の示唆になる——ショートエントリーの前に NCAV check を必ずかける習慣。

**Kaname Capital・Camphora Capital 面接文脈**：両ファンドは日本の低 PBR・低 PBR 解消テーマに強い。「NCAV より安い銘柄を見つけて、どう催化剤を特定するか」は典型的な 1 次面接の事例問題になる。Graham の定義を正確に言えた上で「現代の触媒は政策保有株売却 or TOB プレミアム」と接続できると差別化になる。

**Schweitzer v6 ポートフォリオ**：Long 銘柄の 8864（日本エスコン）・1969（高砂熱学）はPBR 1 倍前後。これらは NCAV バーゲンではないが、安全余裕の計算手順（NCAV → EPV → DDM と積み上げるフレームワーク）の土台として有効。

**FIG 出身的視点**：銀行（8393 りそな）はNCAV が意味を持たない（融資資産が流動資産）が、Tangible Book Value ≒ NCAV の精神的な類似概念。解体価値 vs 継続価値の二分法は Lesson 103 DDM で再登場する。

---

## Self-test（明日説明できるか）

1. **NCAV の正確な計算式を述べよ。なぜ固定資産をゼロにするのか。**
2. **P/NCAV と PBR の違いを数値例で説明せよ。（例：流動資産 100、固定資産 50、総負債 60、株価 20、発行済株式 5 株）**
3. **Reo のショートウォッチリストの 1 銘柄に NCAV チェックをかける場合、「Melting Ice Cube」リスクをどう確認するか。具体的な指標を 2 つ挙げよ。**

---

## Source
- Benjamin Graham, *The Intelligent Investor* (Rev. Ed.), Ch. 15 "Stock Selection for the Enterprising Investor" & Ch. 7
- Graham & Dodd, *Security Analysis* (6th Ed.), Ch. 43 "Specific Aspects of Security Valuation: Net Current Asset Value"
- Oppenheimer, Henry R. "Ben Graham's Net Current Asset Values: A Performance Update." *Financial Analysts Journal*, 1986 — 30 年実績データの出典

---

## 次回（Lesson 021）: Asset-rich Companies — Hidden Value

土地・有価証券・ブランドなど BS に映りにくい「隠れた価値」を発掘する手法。日本企業の持合株解消・含み資産 play と直結する。NCAV が流動資産の清算価値なら、次は固定資産の再評価価値を考える。
