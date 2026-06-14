---
title: Lesson 015 — Security Analysis for the Lay Investor: General Approach
phase: 1
date: 2026-06-14
estimated_reading: ~10 min
---

# Lesson 015 — Security Analysis for the Lay Investor: General Approach

## 1 行で
Graham は「素人にとってのセキュリティ分析」を、個別銘柄の天才的目利きではなく、**再現可能な基準の機械的適用**と定義した。

---

## なぜ今それをやるか

Lesson 001–014 では Mr. Market・Margin of Safety・Defensive vs Enterprising の枠組みを学んだ。  
今日のテーマはその「実行フェーズ」の入口：*実際に銘柄を見る際、何をどの順番で見るか*。  
Phase 2（会計）・Phase 4（Damodaran）へ進む前に、Graham の「分析の地図」を頭に入れておくと後のレッスンが全部つながる。

---

## Core Content

### 1. Graham が言う「分析」とは何か

> "Security analysis is concerned with the **safety** of the investment and the **return** to be expected from it."

Graham は分析を三層に分けた：

| 層 | 問い | 一般投資家向け優先度 |
|---|---|---|
| ① 企業の性質と見通し | このビジネスは理解できるか？ | ★★★ |
| ② 経営陣の質 | 株主に誠実か？ | ★★☆ |
| ③ 財務構造と実績 | 数字は安全性を支えているか？ | ★★★ |

**素人への処方箋**：③を機械的フィルターとして使い、①②を補完に回す。フィルターを通過したものだけ深掘りする。

---

### 2. 分析の 4 ステップ（Graham Chapter 11 整理）

```
Step 1: Business Summary（事業理解）
   ↓
Step 2: Financial Statistics（定量スクリーニング）
   ↓
Step 3: Balance Sheet Strength（財務健全性）
   ↓
Step 4: Dividend Record（株主還元の継続性）
```

**Step 1 — Business Summary**  
- 何を売っているか、市場での地位は？  
- 過去 10 年の EPS トレンド（上昇・安定・不規則）  
- 事業に理解不能な複雑さはないか？

**Step 2 — Financial Statistics（Defensive 基準の定量面）**  
Graham の代表的スクリーニング基準（詳細は Lesson 010）：

| 指標 | Defensive 基準 |
|---|---|
| 時価総額 | 十分大きい（流動性確保） |
| 流動比率 | ≥ 2.0x |
| 長期負債 | 正味流動資産以下 |
| EPS 安定性 | 過去 10 年 赤字なし |
| 増配実績 | 過去 20 年 継続 |
| EPS 成長 | 10 年で +33%（年率 ~3%） |
| PER | ≤ 15x（過去 3 年平均 EPS） |
| PBR | ≤ 1.5x（PER × PBR ≤ 22.5） |

**Step 3 — Balance Sheet Strength**  
- Net Debt / EBITDA：製造業なら 3x 以下が目安  
- Interest Coverage：EBIT / 利払い ≥ 3x  
- 隠れた負債（オフバランス、年金、偶発債務）を確認

**Step 4 — Dividend Record**  
単なる配当利回りではなく**継続性と成長性**を見る。  
20 年無減配は Graham の最重要定性テストの一つ。

---

### 3. 「分析」vs「投機」の境界線

Graham が繰り返し強調するのは：

> "The security analyst should not attempt to forecast the future. He should focus on **what can be established from the past and present**."

予測ではなく**実績の確認**が素人投資家の武器。  
将来の EPS 予測に頼るほど分析は投機に近づく。

---

### 4. 「安全余裕の地図」として使う

この 4 ステップは Margin of Safety（Lesson 003）を**操作化**したもの。

```
内在価値の推計
  = 過去 3 年平均 EPS × Graham Number の倍率（≤15x）
  + 財務健全性プレミアム

現在株価 << 内在価値推計 → Margin of Safety 有り
```

**Graham Number**（簡易版）：
```
√(22.5 × EPS × BVPS) = Graham Number
株価 < Graham Number なら割安
```

例：EPS = 200円、BVPS = 2,000円  
Graham Number = √(22.5 × 200 × 2,000) = √9,000,000 ≈ **3,000円**

---

## Reo への実用的 application

**FIG バックグラウンドとの接続**  
J.P. Morgan FIG IBD では銀行・保険の財務を扱う。Graham の「Balance Sheet Strength」ステップは FIG 企業では特殊で：  
- 銀行：CET1比率・LCR が「流動比率」の代替  
- 保険：ESR・MCEV が「負債健全性」の代替  
→ Lesson 103–104 でこれを深掘りするが、今日の枠組みを頭に入れておくと繋がりやすい。

**Watchlist 適用（即実践）**  
8393（りそなHD）の直近 10 年 EPS と配当継続性を Graham 基準で追ってみる：  
- EPS：過去 10 年で大きな赤字期なし（2011年以降安定）  
- 配当：2015年以降増配基調  
- PBR：0.7x 前後 → Graham Number と比較する価値あり  

**Camphora / Kaname / AVI の面接で使える切り口**  
「なぜこれを買うか」を聞かれたとき、Step 1-4 の順で説明できると**フレームワーク思考**を示せる。「まず事業を理解し、定量スクリーニングを通過したものを財務健全性で絞り、配当実績で経営規律を確認する」という構造は、アクティビスト系（AVI, Oasis）にも刺さる。

**Schweitzer v6 との接続**  
v6 銘柄の DCF を組む前に、Graham の Step 2/3 スクリーニングを「ゲートウェイチェック」として走らせると、モデルに入る前に明らかなリスクを弾ける。

---

## Self-test（明日説明できるか）

1. **Graham の 4 ステップ分析**を順番に言えるか？各ステップで「何を確認するか」を 1 行で説明できるか？

2. **Graham Number** の計算式を書き、EPS = 300円・BVPS = 3,500円の銘柄の Graham Number を暗算できるか？（ヒント：22.5 × 300 × 3,500 = ?）

3. 自分のウォッチリスト銘柄（例：8393 りそなHD）に Graham の 20 年増配基準を当てはめると通過するか？通過しない場合、それはリスクか・割り引いて考えてよいファクターか、理由とともに説明できるか？

---

## Source

- Benjamin Graham, *The Intelligent Investor* (revised ed. 1973), Chapter 11 "Security Analysis for the Lay Investor: General Approach"
- Jason Zweig commentary (HarperCollins 2003 edition), Chapter 11 コメント
- Graham Number 公式：PER 上限 15x × PBR 上限 1.5x = 22.5 に由来

---

## 次回（Lesson 016）: EPS — Per-share earnings の 3 つの落とし穴

一株利益は最もよく使われ、最も誤解される指標。Graham が警告した「EPS の 3 つの罠」（非経常項目・希薄化・会計選択）と、それを見抜くための調整手法を学ぶ。
