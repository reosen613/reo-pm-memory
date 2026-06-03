---
title: Lesson 006 — Enterprising Investor: 7 sub-criteria for stock selection
phase: 1
date: 2026-06-03
estimated_reading: ~10 min
---

# Lesson 006 — Enterprising Investor: 7 sub-criteria for stock selection

## 1 行で
Graham の「積極的投資家」は Defensive の受け身 checklist を超え、割安の積極的発掘を 7 つの定量条件で規律する。

## なぜ今それをやるか
Lesson 004 で Defensive と Enterprising の分岐点を確認した。Lesson 005 では Defensive 側の 60/40 allocation ロジックを見た。今夜は Enterprising 側の **銘柄選別ツール** を構築する。Camphora・Kaname 等の日本アクティビスト系ファンドは事実上 Enterprising アプローチ（市場の見落としを拾う）であり、この 7 条件は面接で「Graham 的に割安かどうか」を語る共通言語になる。

---

## Core Content

### Enterprising Investor とは誰か
Graham の定義は「時間・能力・ルール遵守」の 3 要件を満たす投資家。Defensive は市場平均を狙い、Enterprising は **市場平均を上回る** ことを目指す。ただし Graham は「上回るためにはより多くの仕事が必要」と強調し、運だけでは持続しないと釘を刺す。

---

### 7 つの選別条件（_The Intelligent Investor_ Chapter 15 準拠）

| # | 条件 | 数値目安 | 意図 |
|---|------|----------|------|
| 1 | **Financial condition** | 流動比率 ≥ 1.5、長期負債 ≤ 運転資本 | バランスシートの安全性 |
| 2 | **Earnings stability** | 過去 5 年間赤字なし | 周期底でも生存できるか |
| 3 | **Dividend record** | 過去 5 年間配当継続 | 株主還元の継続性（Defensive より要件緩め） |
| 4 | **Earnings growth** | 過去 3 年平均 EPS ≥ 過去 3 年平均 EPS の前 3 年比でプラス | 構造的成長or安定 |
| 5 | **P/E ratio** | ≤ 10× （直近 EPS ベース） | 過剰なグロース期待を排除 |
| 6 | **P/BV ratio** | P/BV × P/E ≤ 22（Graham Number 派生） | 価格と資産の合成チェック |
| 7 | **Total size** | 時価総額 ≥ 一定水準（流動性確保） | 小型過ぎて流動性リスクが出ないか |

> **Graham Number の公式**：`√(22.5 × EPS × BVPS)`  
> これは「P/E ≤ 15、P/BV ≤ 1.5 の積」として導かれる。PBR 1 倍割れが多い TSE において特に有効な第一フィルター。

---

### Defensive との比較

| 項目 | Defensive | Enterprising |
|------|-----------|--------------|
| P/E 上限 | 15× | 10× |
| 配当継続要件 | 20 年連続 | 5 年継続（緩め） |
| 赤字許容 | ゼロ (10 年) | ゼロ (5 年) |
| 時間コスト | 低い | 高い（調査必要） |
| 目標リターン | 市場並み + α | 市場超過 |

Enterprising は **より安く買う代わりに調査の手間を自分で引き受ける** 契約だと理解すること。

---

### 具体例：TSE PBR スクリーニングへの適用

2023 年 3 月の TSE「資本コスト経営」要請以降、多くの日本株が PBR < 1 から改善途上にある。Graham 的 Enterprising フィルターを Japan Universe に当てると：

- **流動比率 ≥ 1.5**：製造業・建設業の多くが通過
- **P/E ≤ 10**：TSE Prime の中央値が約 15×（2026 年頭）なので、絞り込みが効く
- **Graham Number との乖離**：株価が Graham Number を 20% 以上下回る銘柄は "Enterprising 候補"

これが Camphora や Strategic Capital が用いる定量フィルターの原型に近い。

---

## Reo への実用的 application

**Schweitzer v6 作業との接続**  
v6 ポートフォリオの Long 側（8864・5451・1969 等）は Enterprising 条件をいくつ通過しているか確認するだけで、投資仮説の **Graham 的根拠** を即座に語れる。面接でバリュエーション根拠を聞かれたとき「Graham Number vs 現在株価で X% ディスカウント」と言えると具体性が増す。

**ウォッチリスト Quick Check**

| Ticker | 業種 | Graham Condition 初期判断 |
|--------|------|--------------------------|
| 8864 太平洋興発 | 不動産 | PBR 低、配当あり → 4–6 条件通過可能性高 |
| 5451 淀川製鋼所 | 鉄鋼 | P/E 低め、流動比率良好 → Enterprising 候補 |
| 1969 高砂熱学 | 建設設備 | 安定配当、収益安定 → 3–4 条件クリアか |
| 6440 JUKI | 産業機械 | 景気敏感・収益変動あり → Condition 2 (安定性) 要確認 |

**Kaname / Camphora 面接想定 Q&A**  
「Graham の Enterprising 条件から見て今の日本株で最も魅力的なセクターは？」  
→ 「流動比率が高く PBR が依然 < 1 の建設・素材セクター。TSE 改革圧力で ROE 改善余地があり、Graham Number 対比で 20-30% ディスカウントが残る銘柄が複数存在する」と答えられると面接官に刺さる。

---

## Self-test（明日説明できるか）

1. Graham の Enterprising Investor 7 条件を、Defensive との数値の違いに触れながら 3 条件以上言えるか？
2. Graham Number の計算式を導け。P/E 15× かつ P/BV 1.5× という 2 つの条件からどう√式が来るか説明せよ。
3. Reo のウォッチリスト（8864・5451・1969 のいずれか）について、上記 7 条件のうちどの条件が通過しやすく、どの条件が懸念点になりうるか仮説を述べよ。

---

## Source
- Graham, Benjamin. *The Intelligent Investor*, Rev. Ed. (1973), Chapter 15 — "Stock Selection for the Enterprising Investor"
- Jason Zweig commentary, same chapter (HarperCollins 2003 ed.)
- TSE「資本コストや株価を意識した経営の実現に向けた対応について」2023年3月

---

## 次回（Lesson 007）: The Investor and Inflation — 1971 と 2026 の比較
インフレが株式・債券・不動産にどう影響するか、Graham が書いた 1973 年版の論点を 2026 年の日本（日銀政策正常化・円安）文脈で再検討する。
