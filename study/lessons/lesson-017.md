---
title: Lesson 017 — A Comparison of Four Listed Companies — Graham 比較分析手法
phase: 1
date: 2026-06-19
estimated_reading: ~10 min
---

# Lesson 017 — A Comparison of Four Listed Companies — Graham 比較分析手法

## 1 行で
Graham は 4 社の財務数値を横並びにすることで、「何が安いか」でなく「何が安全か」という問いを定量化した。

---

## なぜ今それをやるか

前回（Lesson 016）では EPS の 3 つの落とし穴を学んだ。しかし単体の EPS は危険だ——歴史的文脈も、財務強度の比較も、業界ポジションも見えない。

Graham は *The Intelligent Investor* 第 13 章でこの罠を鮮やかに示す。DJIA 構成 4 社（1970 年）を「比較表」で分析し、最安値に見える株が実は最危険であることを論証した。これがバイサイドで言う **comparative analysis（比較分析）** の原型であり、Schweitzer v6 や Camphora・Pantheum 面接での pitch「なぜ *このバリュエーション* で *この株* を選ぶか」に直結する思考法だ。

---

## Core Content

### Graham が用いた 4 社の比較軸（1970 年 DJIA より）

Graham は以下のカテゴリーで 4 社を並べた。Reo がバイサイドで使う軸に再整理する：

| 比較軸 | Graham の問い | 現代バイサイドでの相当 |
|---|---|---|
| **Price / Book** | 純資産に対して何倍払うか | P/B、PBR |
| **Price / Earnings (trailing)** | 過去利益の何倍か | Trailing P/E |
| **EPS growth (past 7yr)** | 利益の方向性と安定性 | CAGR、EPS trend |
| **Dividend yield** | 株主への還元持続性 | DY |
| **Financial soundness** | 流動比率、負債比率 | Net Debt / EBITDA、CR |
| **Book value per share** | 清算価値の代理 | BVPS |

#### 1970 年の 4 社：何が起きたか

| 会社 | P/E | PBR | 財務安全性 | Graham の判定 |
|---|---|---|---|---|
| ELTRA Corp | 約 7x | 1.0x | 健全 | **買い候補（防衛型）** |
| Emerson Electric | 約 26x | 5.4x | 健全 | 割高・過去の成長が織り込み済み |
| Emery Air Freight | 約 45x | 7.8x | 許容 | 高成長だが価格はその成長を何年先まで割引するか |
| Eltra vs Emery | 6x差 | 8x差 | 同等 | **同等のリスクで 6-8 倍安い** |

Graham の結論：「Emery の株価は、今後も高成長が続く、という *賭け* を含んでいる。Eltra の株価は、*そんな賭けを一切しない* 投資家向けだ」

### Graham 比較分析の 3 ステップ

```
Step 1 — スクリーニング軸を揃える（apple to apple）
  ・同一時点の数値（期末 or TTM）
  ・EPS は normalized（一過性除く） ← Lesson 016 の実践
  ・BV は goodwill, intangibles を明記して扱う

Step 2 — Safety First（守りの評価）
  ・流動比率 > 2x（製造業）、負債比率が業界平均以下
  ・連続 20 年の黒字（理想）、最低 7 年
  ・Dividend: 過去 20 年継続（防衛型）

Step 3 — Price Check（攻めの評価）
  ・P/E < 15x（Graham の上限）
  ・P/B < 1.5x、または P/E × P/B < 22.5
  ・「安さ」ではなく「Safety margin = 内在価値との乖離」
```

### Graham の核心：価格比較 ≠ 価値比較

最も安い株（低 P/E）≠ 最も良い買い。重要なのは：

**Margin of Safety = 内在価値（IV） − 株価**

IV の代理変数として Graham は「正常化 EPS × 適正倍率（≈ 15x）」を使うが、比較分析では **相対的な財務強度と価格の不均衡** を探す。同程度の品質の企業群の中で、なぜかディスカウントされている 1 社が狙い目だ。

### 日本への応用：TSE Prime 比較

| 軸 | 8864 タス (Long) | 業種平均 | 割安根拠 |
|---|---|---|---|
| P/B | 0.6x | 1.2x | 純資産より 40% 安い |
| P/E | 8x | 14x | 低い成長期待が織り込まれている |
| Net Debt | ネットキャッシュ | D/E 0.4x | 財務強度は業界上位 |
| DY | 3.2% | 1.8% | 還元意欲あり |

→ Graham の視点では、「Eltra 型」の投資候補。財務的に健全で、価格が安い。リスクは *成長しないこと* だが、その成長リスクを価格が既に割引している。

---

## Reo への実用的 application

**Schweitzer v6 pitch での活用：**  
ファンドに 1 銘柄を提案する際、比較表（3〜5 社横並び）を作り、「なぜ *この* 銘柄がこの集合の中で最も Margin of Safety が大きいか」を示す。Pantheum・Oasis 面接では「アイデアの差別化」を問われる——Graham 式の比較フォーマットは、直感ではなく *数値のロジック* で差別化を語る枠組みになる。

**ショート side（6594 日本電産 / 4661 OLC 等）への応用：**  
比較分析は割安探しだけでなく「なぜこの株は高すぎるか」の論拠にもなる。OLC（4661）の P/E が同業比 2-3x 高い場合、「期待成長率が正当化する水準を超えているか？」を Graham の 15x 上限で反証する。

**FIG バックグラウンドとの接続：**  
銀行（8393 りそな等）の比較では PBR + ROE が主軸。Graham の P/B 1.5x 上限は、J-REIT を除く銀行の正常化 ROE が低いことを考えると納得感がある。

---

## Self-test（明日説明できるか）

1. **Graham の比較分析で必ず並べる 6 つの軸は何か。そのうち "Safety" に属するのはどれか。**

2. **「P/E が低いから割安」という主張の何が間違いか。Graham の視点で 2 点挙げよ。**

3. **自分のロングウォッチリスト（例：1605 INPEX）について、同業 2 社と Graham 式比較表を作るとしたら、どの軸を最初に揃えるか。BV の調整で考慮すべき点は？**

---

## Source

- Benjamin Graham, *The Intelligent Investor*, Chapter 13「A Comparison of Four Listed Companies」(1973 revised edition, HarperCollins)
- Commentary: Jason Zweig の脚注（2003 revised edition） pp. 336-352
- 日本株応用部分は Reo のウォッチリストへの著者（Reo Study Bot）による演繹

---

## 次回（Lesson 018）: Stock Selection for the Defensive Investor（full guidance）

Graham が防衛型投資家向けに提示した 7 statistical tests をフルに展開する。Schweitzer v6 のスクリーニング条件との対応関係を整理し、実際に日本株 1 社でテストを走らせる。
