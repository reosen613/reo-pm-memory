---
title: Lesson 011 — Stock Selection: Enterprising Investor の bargain issues
phase: 1
date: 2026-06-10
estimated_reading: ~10 min
---

# Lesson 011 — Stock Selection: Enterprising Investor の bargain issues

## 1 行で
グレアムの積極的投資家は「市場が見落とした安売り」を 2 種類に分類し、価格がファンダメンタルズを下回る**客観的な証拠**を要求する。

---

## なぜ今それをやるか
前回（Lesson 010）は守備的投資家の 7 statistical tests を学んだ。今回は同じ Graham の枠組みの「攻め側」：積極的投資家が実際にどのように銘柄を発掘するか、そのロジックを解剖する。Schweitzer v6 ポートフォリオの Long サイドには現在 8864・5451・1969 などが入っており、「なぜバーゲンか」を言語化する訓練として直結する。

---

## Core Content

### 1. Bargain Issue とは何か

Graham の定義は厳格だ：

> "A bargain issue is one that, on the basis of facts established by analysis, appears to be worth considerably more than it is selling for."

「かなり（considerably）」が重要。10% 安では足りない。Graham は最低でも **価値の 2/3 以下の価格** を目安とした（Margin of Safety の論理）。

---

### 2. 二種類の Bargain Issue

| 種別 | 定義 | 主な発見ルート |
|------|------|--------------|
| **Bargain Type 1 — 過小評価された利益銘柄** | 現在の収益力が低く見えるが、正常化 EPS は市場評価より高い | 景気循環・一時費用の剥落・市場の過剰反応 |
| **Bargain Type 2 — Net-Net (NCAV) 銘柄** | 株価 < 流動資産 − 全負債（NCAV per share） | 成長性ゼロでも清算価値で勝つ |

両者に共通する **前提**：  
- 業績が戻る根拠、または資産が消滅しない根拠が論理的に示せること  
- 単なる「安い」ではなく **「不当に安い」** こと

---

### 3. NCAV の計算（Type 2 の核心）

```
NCAV = 流動資産（CA） − 総負債（Total Liabilities）
NCAV per share = NCAV ÷ 発行済株式数
```

Graham は **NCAV per share の 2/3 以下**で取引されている銘柄を買い対象とした。

**数値例（仮想日本企業）**

| 項目 | 金額（百万円） |
|------|--------------|
| 現預金 | 5,000 |
| 売掛金 | 3,000 |
| 棚卸資産 | 2,000 |
| **流動資産合計** | **10,000** |
| 流動負債 | 4,000 |
| 固定負債 | 2,000 |
| **総負債** | **6,000** |
| **NCAV** | **4,000** |
| 発行済株式数 | 10M 株 |
| **NCAV/share** | **400 円** |
| Graham 買い水準 | **≤ 267 円** (400 × 2/3) |

---

### 4. Bargain Type 1 の具体的 criteria（積極的投資家の 6 基準）

Graham は Enterprising Investor 向けに以下の追加スクリーンを提示した：

1. **Current ratio ≥ 1.5** — 短期流動性
2. **Debt / NWC ≤ 1.1** — 純運転資本に対する負債が低い
3. **EPS positive** — 過去 5 年ゼロ赤字
4. **Dividend record** — 何らかの配当実績あり
5. **Earnings no worse than 1/3 below 5-year avg** — 近年の落ち込みが軽微
6. **P/E ≤ 9x** — 低評価のバリュエーション水準

守備的投資家（Lesson 010）の 7 criteria より緩い代わりに、発掘コストを自分で負う。

---

### 5. よく引用される批判と Graham の反論

**批判**：NCAV 銘柄は「ゾンビ企業」であり、清算が起きなければ意味がない。  
**Graham の答え**：統計的には、NCAV 未満で買ったバスケットは 1−3 年で平均を上回る。個別リスクはバスケット（20 銘柄以上）で分散する。重要なのは**価格そのものが安全マージン**となること。

---

### 6. 2026 年の日本市場への適用

TSE の PBR < 1 圧力（Lesson 029 で詳述予定）に伴い、現在も **PBR < 1 かつ現預金 > 時価総額** の銘柄が東証に複数存在する。これは Graham 的 NCAV には達しないが、精神的な後継だ。

AVI London や Oasis が日本市場に照準を当てているのはこの「バリュエーション格差」が残存するためであり、Lesson 011 の理論的背景がそのままアクティビスト戦略の土台になる。

---

## Reo への実用的 application

**Schweitzer v6 Long 側の検証軸として：**

- **8864（パルテック）** — 不動産持合い解消が進む過程で、保有資産の簿価とNCAV的分析が効く。「純資産 vs. 株価」の比較は Graham Type 2 の変形
- **5451（淀川製鋼）** — 製造業 PBR 0.5x 台。流動資産構成が厚い典型的 Type 2 候補。現預金・売掛・棚卸の合計 vs 総負債を有報で確認したか？
- **1969（高砂熱学）** — 建設セクター cyclical。Type 1 の「正常化 EPS」アプローチが合う

**ファンド面接 tip：**  
Camphora・Kaname・AVI のいずれも「なぜその株が安いのか」を構造的に聞いてくる。「PBR が低い」だけでは不十分。「流動資産の質」「負債構造」「正常化利益水準」の 3 点セットで答えられると Graham の解像度が伝わる。

---

## Self-test（明日説明できるか）

1. Graham の Bargain Issue の 2 分類を言葉で説明せよ。NCAV の計算式は？
2. 積極的投資家の 6 基準のうち、バリュエーション水準に関するものはどれか？P/E 何倍以下？
3. あなたのロング候補 1 銘柄について、流動資産・総負債の概数を思い出し、NCAV per share を大まかに試算せよ。現在の株価は NCAV の何 % か？

---

## Source
- Benjamin Graham, *The Intelligent Investor*, Rev. Ed. — Ch. 15 "Stock Selection for the Enterprising Investor"
- Graham, *Security Analysis* (4th ed.) — Part IV, Ch. 26-28
- Graham's NCAV statistical data: 本文内の 1930s バックテスト参照（Tweedy Browne 1992 replication でも追証）

---

## 次回 (Lesson 012): Things to Avoid — warrants, IPOs, secondary issues
ワラント・IPO・二次案件という「魅力的に見えて罠になりやすい」3 つのカテゴリを、Graham がなぜ積極的に避けたかを学ぶ。Reo の Short サイド（4477/4911 など新興・グロース系）への接続が強い。
