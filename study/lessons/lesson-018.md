---
title: Lesson 018 — Stock Selection for the Defensive Investor (full guidance)
phase: 1
date: 2026-06-17
estimated_reading: ~10 min
---

# Lesson 018 — Stock Selection for the Defensive Investor (full guidance)

## 1 行で
Graham の Defensive Investor 株式選択とは、**7 つの定量基準を全クリアした「退屈で安全な株」だけを等分に持つ** という徹底した規律であり、2026 年の日本市場でも有効な枠組みとして残る。

---

## なぜ今それをやるか

Lesson 010 で 7 つの統計的テストを概要として学んだ。Lesson 016・017 では EPS の質と横断比較の方法論を学んだ。Lesson 018 はその総合版：Graham が *The Intelligent Investor* Ch. 14 で示した「守り型投資家のための完全な株式選択フレームワーク」を、条件・理由・日本市場への翻訳込みで体系化する。Lesson 019（Enterprising Investor 版）との対比の起点にもなる。

---

## Core Content

### Defensive Investor とは何者か（復習）

Graham の定義：「時間・能力・意欲のいずれかが不足し、**アクティブな証券分析に従事できない** 投資家」。目標は最大リターンではなく、**最小努力での合理的リターン**。

> "The defensive investor must confine himself to the shares of important companies with a long record of profitable operations and in strong financial condition."

---

### 7 つの基準（Graham Ch. 14 完全版）

| # | 基準 | 数値閾値（Graham原典） | なぜその数値か |
|---|------|-----------------------|----------------|
| 1 | **企業規模（Adequate Size）** | 製造業：売上高 ≥ $1億 / 公益：総資産 ≥ $5,000万（1972年ドル基準） | 小型株は情報非対称性・流動性リスクが高い |
| 2 | **財務強度（Financial Strength）** | 流動比率 ≥ 2.0×、長期負債 ≤ 純流動資産 | 短期支払能力と中長期ソルベンシーの二重確認 |
| 3 | **利益の継続性（Earnings Stability）** | 過去 10 年間、赤字ゼロ | 1 度の大赤字は稼得力の不確実性を示す |
| 4 | **配当の継続性（Dividend Record）** | 過去 20 年間、無配なし | 配当はキャッシュの実在を示す最も誠実なシグナル |
| 5 | **利益成長（Earnings Growth）** | 過去 10 年で EPS +33% 以上（3 年平均比較） | インフレ分程度の実質成長を担保 |
| 6 | **妥当な株価収益率（Moderate P/E）** | PER ≤ 15× （過去 3 年平均 EPS 基準） | 割高バイアスへの定量的歯止め |
| 7 | **妥当な株価純資産倍率（Moderate P/B）** | PBR ≤ 1.5× ／ PER × PBR ≤ 22.5 が目安 | 純資産割れリスクの回避と PER との整合性 |

**Graham の補足（P/E × P/B ≤ 22.5 ルール）：**

- PER = 15, PBR = 1.5 のとき積は 22.5 → 許容上限
- PBR が低ければ PER を 15 超に引き上げる余地がある（例：PBR 1.0 なら PER 22.5 まで許容）
- 逆もしかり

---

### なぜ「等分保有（diversified list）」か

Graham は 10〜30 銘柄の等分保有を推奨する。理由：

1. **個別銘柄の予測不能性** — どの銘柄が最大リターンを出すか事前に知る方法はない
2. **規律の保持** — 比重を変えると情動的バイアスが入る
3. **取引コスト削減** — リバランスを最小化

> 「Defensive Investor が本質的価値の計算に時間を使うべきでない。Graham の 7 基準を満たす株の中から分散投資するだけで十分。」

---

### 日本市場 2026 への翻訳

| Graham 基準 | 日本版の読み替え | 注意点 |
|-------------|----------------|--------|
| 企業規模 | TOPIX 500 構成銘柄 or 時価総額 ≥ 500 億円 | 流動性・情報開示の観点 |
| 財務強度 | 流動比率 ≥ 1.5×（日本製造業の実態に合わせ緩和）、D/E ≤ 0.5× | 日本企業は自己資本比率が高い傾向 |
| 利益継続性 | 過去 10 年、営業赤字ゼロ | GAAP 純利益より営業利益で確認（特損に歪められにくい） |
| 配当継続性 | 過去 10 年、減配 or 無配なし | 20 年は厳しすぎる（2008 GFC で多くが一時減配） |
| 利益成長 | 過去 10 年で営業利益 +20% 以上 | デフレ期を考慮し閾値を下げる |
| P/E | PER ≤ 15× (12M trailing) | TSE PBR<1 改革で割安銘柄が増加中 |
| P/B | PBR ≤ 1.2× ／ PER × PBR ≤ 18.0 | 日本市場の PBR 水準を反映 |

---

### 何を**除外**するか（Graham の警告再掲）

Lesson 012 と連動：

- **新規公開株 (IPO)** — 過去 10 年の記録を持たない
- **ホットセクター株** — 高成長 = 高 PER → 基準 ⑥ 違反
- **無配・累積赤字企業** — 基準 ③④ 違反
- **財務レバレッジ過大企業** — 基準 ② 違反
- **予想 EPS に依存した銘柄** — 「将来 2 年で黒字化予定」は Defensive の対象外

---

### 現実的なスクリーニング（Reo が今すぐできる）

```
Filter set（Bloomberg/Capital IQ）:
  Market Cap  ≥ ¥500bn
  Current Ratio ≥ 1.5
  Net Debt/EBITDA ≤ 2.0
  10yr trailing: no operating loss year
  Div History: no cut/omission in 10yr
  PER (3yr avg EPS) ≤ 15
  PBR ≤ 1.5
```

このフィルターを通過する TSE Prime 銘柄は現在 30〜50 社程度。Graham の言う「退屈だが安全」な企業群。

---

## Reo への実用的 application

### Schweitzer v6 ロングポジション照合

ウォッチリスト Long（8864/5451/1969/6440/7282/4204/1928/1605/4540/8393）の各銘柄に今夜の 7 基準を当てはめてみる。**全条件クリアの銘柄 = Defensive Investor 観点でも安全** という確認が Schweitzer への説明で使える（「これは Graham Defensive 基準を 7/7 クリアしています」）。

### ファンドインタビュー活用

Camphora・Kaname は「エンゲージメント後の企業価値向上」を狙うが、**スクリーニング入口として Defensive 基準を使う**。財務安定 + 低 PBR + 利益継続 = 「本来の価値があるのに評価されていない」企業を発見するための最初のフィルター。

> 「なぜその銘柄に注目しましたか？」への回答：「Graham の 7 基準を全クリアしながら PBR が 0.7× 台にあり、TSE のガバナンス改革の波及で再評価余地がある、と判断しました」

### FIG 文脈（8393 池田泉州 HD）

銀行株は「流動比率」の概念が適用しにくい（預金 = 短期負債のため）。Graham も金融株には別基準を設けており、**Lesson 103（Banks DDM P/TBV）** で改めて扱う。今は「金融を除いた事業会社」への適用に集中する。

---

## Self-test（明日説明できるか）

1. **Graham の 7 基準を番号なしで全部言えるか（30 秒以内）。各基準に数値を付けよ。**

2. **PER 20× ・PBR 1.0× の銘柄は Graham の基準を満たすか。PER × PBR ルールで判定せよ。**

3. **ウォッチリストの 1928（積水ハウス）を Graham の 7 基準に照らして評価してみよ。何基準クリアできそうか？（暗記不要、論法の型を練習）**

---

## Source

- Benjamin Graham, *The Intelligent Investor* (revised ed. with Zweig commentary), **Chapter 14**: "Stock Selection for the Defensive Investor" — 7 基準の直接出典
- Graham & Dodd, *Security Analysis* 6th ed., Chapter 43: Financial Condition in Stock Selection
- 個人的注記：日本市場への翻訳（流動比率・配当継続年数の調整）は Reo の judgment であり Graham 原典にない

---

## 次回（Lesson 019）：Stock Selection for the Enterprising Investor (full guidance)

Defensive の 7 基準をベースに、**Enterprising 版の緩和・追加基準**（割安 bargain issue、Net-Net、特殊状況）を学ぶ。Reo のショートウォッチリスト分析への接続点でもある。
