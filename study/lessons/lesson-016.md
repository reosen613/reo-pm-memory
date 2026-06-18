---
title: Lesson 016 — EPS — Per-share earnings の 3 つの落とし穴
phase: 1
date: 2026-06-18
estimated_reading: ~10 min
---

# Lesson 016 — EPS — Per-share earnings の 3 つの落とし穴

## 1 行で
「1株当たり利益」はそのまま使うと嘘をつく——単年・非経常・希薄化という3層のノイズを除去してはじめて比較可能な数字になる。

## なぜ今それをやるか
Lesson 015（General Approach to Security Analysis）で「EPSを分析の起点にするな、まず分母(株数)と分子(利益の質)を疑え」という考え方を学んだ。016ではそれを実務レベルに落とす。Graham 第12章 "Things to Consider About Per-Share Earnings" は、今日のbuyside面接でも「EPSの質をどう見るか」と問われたとき直接使えるフレームワーク。

---

## Core Content

### 落とし穴①：単年 EPS への依存

Graham が最初に警告するのは「直近1年のEPSで株価を評価すること」。景気サイクル・季節性・一時的な業況変動で利益は激しく振れる。

**Graham の処方箋：7〜10年平均 EPS を使う**

| 指標 | 使い方 |
|------|--------|
| 直近1年 EPS | 市場のモメンタム参考のみ |
| 過去7年平均 EPS | Graham 流 P/E の分母 |
| サイクルピーク/トラフ比較 | 景気感応度チェック |

例：6440（IDEC）は製造業向け FA 部品メーカーで、設備投資サイクルに連動してEPSが±40%変動する。単年EPSでバリュエーションすると天井で割安に、底で割高に見えるという逆転が起きる。

---

### 落とし穴②：非経常項目の混入

企業は「特別損益」「一過性費用」として様々な項目を経常利益の外に押し込む。しかし Graham は「毎年発生する一過性費用はもはや経常費用」と喝破した。

**よく見る非経常項目の分類**

| 項目 | 方向 | 見方 |
|------|------|------|
| 工場閉鎖・リストラ費用 | EPS 押し下げ | 毎年計上なら実質コスト |
| 投資有価証券売却益 | EPS 押し上げ | 繰り返し不可——除外 |
| のれん減損 | EPS 押し下げ | 過去M&Aの失敗の認識 |
| 退職給付数理差異 | 双方向 | OCI経由でも実質は費用 |

日本固有の注意：**政策保有株の売却益**は2024〜2026年の株式解消圧力で多くの企業に発生。例えば 8393（りそな）や FIG 系は毎期数十億円規模の売却益が「投資有価証券売却益」として特別利益に計上される。これを含めた EPS は持続可能でない。

Graham の手順：5年間の P/L を並べ、非経常項目を**恒常的に発生するか否か**で振り分け、恒常的なものは経常利益に戻す「正常化 EPS（Normalized EPS）」を計算する。

---

### 落とし穴③：希薄化（Dilution）

報告されるのは **Basic EPS**（発行済み株数ベース）だが、ストックオプション・転換社債・新株予約権が行使されると株数が増える。**Diluted EPS** を使わない限り、潜在的な希薄化を見落とす。

**Treasury Stock Method（TSM）の骨格**

```
希薄化後株数
 = 基本株数
 + インザマネーのオプション行使株数
 - 行使代金で自社株買い戻せる株数（≒ 行使株数 × 行使価格 / 株価）
```

例：4477（BASE）はグロース期に大量のストックオプションを発行。Basic EPS と Diluted EPS の乖離が最大 15%超になった時期がある。グロース株の shorting 時は Diluted EPS を分母にしないとバリュエーションが甘くなる。

**日本特有のポイント：転換社債（CB）**  
近年 J-REIT や新興企業は CB を多用。CB 転換時の株数増加は Diluted EPS に反映されるが、発行条件（転換価格 = 時価の 90〜100%）で希薄化インパクトが変わる。有報の「潜在株式による影響」欄を必ず確認する。

---

### 3つをまとめると：Normalized Diluted EPS

```
Normalized Diluted EPS
 = (7〜10年平均 経常利益 ± 非経常項目の正規化調整)
   ÷ 完全希薄化後株数
```

これが Graham の言う「真の稼ぎ」。市場は通常 "next 12-month Basic EPS" を材料に動くので、両者の乖離がそのまま**ミスプライシングの発生源**になる。

---

## Reo への実用的 application

**Schweitzer v6 ポートフォリオ点検チェックリスト（EPS 品質）**

1. **6594（日本電産 / Nidec）**：M&A連続で取得のれんが累積。のれん減損リスクが顕在化した期の EPS は要正規化。
2. **5032（ANYCOLOR）**：ストックオプション大量発行。Basic vs Diluted の乖離を確認——Lesson 140 の M-Score 分析の前提。
3. **8393（りそな HG）**：政策保有株売却益が毎期混入。Long 銘柄として持つ場合でも EPS の質を整理してPitch に組み込む。
4. **4661（オリエンタルランド / OLC）**：コロナ回復後に非経常の補助金・損失が消えた。2023〜2025 の EPS ジャンプが正常化後に維持可能か確認。

**面接想定 Q&A**
- *"How do you think about earnings quality when looking at a Japanese company?"*  
→「まず正規化 EPS（非経常除去）→ 希薄化後株数で割る→ 7年平均と直近の乖離をチェックし、乖離が大きい銘柄を精査します」

---

## Self-test（明日説明できるか）

1. Graham が P/E の分母に直近 1 年 EPS を使わず 7〜10 年平均を使う理由を 2 文で説明せよ。
2. 日本企業の政策保有株売却益が EPS に与える影響と、それを正規化する手順を述べよ。
3. 自分のウォッチリストから 1 銘柄を選び、Basic EPS と Diluted EPS の差が生じうる要因を挙げよ。

---

## Source
- Graham, *The Intelligent Investor*, Chapter 12 "Things to Consider About Per-Share Earnings" (Rev. ed., Harper, 2003)
- Zweig commentary, same chapter（現代企業への適用注釈）
- IFRS IAS 33 "Earnings per Share"（希薄化計算の国際基準）

---

## 次回（Lesson 017）：A Comparison of Four Listed Companies — Graham 比較分析手法
Graham が同業4社を並べて行う横断比較の方法論。単純な数値比較ではなく「なぜ差が生まれるか」を問う構造分析の原型——Schweitzer v6 の peer comparison 作成に直結する。
