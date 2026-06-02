---
title: Lesson 005 — Defensive Investor: 60/40 stock-bond の論理
phase: 1
date: 2026-06-02
estimated_reading: ~10 min
---

# Lesson 005 — Defensive Investor: 60/40 stock-bond の論理

## 1 行で
Graham の Defensive Investor は「株 50-75% / 債券 25-50%」のバンドで感情をルール化し、リバランスによって意図せず逆張りを実装する。

---

## なぜ今それをやるか

Lesson 004 で Defensive と Enterprising の二項分類を学んだ。今日はその Defensive 側の具体的な**アセット・アロケーション原則**を深掘りする。"60/40" は現代でも年金・ファミリーオフィス・マルチアセットファンドのデフォルト設定であり、Camphora・Schweitzer のようなロング中心のファンドが bond proxy 株に付けるバリュエーションプレミアムの根拠とも直結する。

---

## Core Content

### 1. Graham の原則：50/50 ≒ ルールの本質

Graham が *The Intelligent Investor* (1949, rev. 1973) の第 4 章で示したのは、厳密な "60/40" ではなく **「株式は最小 25%、最大 75%、残りは債券」** という可変バンドだ。中立点として 50/50 を推奨し、以下の調整ルールを設けた。

| 市場環境 | 推奨株比率 | 判断基準 |
|----------|-----------|----------|
| 株価が "割高" に見える | 25% まで下げる | Dow の P/E や配当利回り |
| 株価が "割安" に見える | 75% まで上げる | 配当利回り > 社債利回り |
| 判断がつかない | 50/50 で維持 | デフォルト |

ポイントは **「いつ変えるかのルールを事前に決める」** こと。感情トリガーではなくバリュエーション指標でリバランスする。

---

### 2. 50/50 ルールが「意図せぬ逆張り」になる理由

株が上がると株比率が 50% を超える → 株を売って債券を買うリバランス  
株が下がると株比率が 50% を割る → 株を買って債券を売るリバランス

これは機械的な **買い安く・売り高く** の実装だ。Graham はこれを "a form of automatic market-timing without forecasting" と表現した。心理的な強みは「安いときに買う根拠がルールにある」こと。

---

### 3. 債券サイドのロジック

Graham が債券を組む目的は **リターン最大化ではなく心理的安定材料**。

- 株が -30% でも bond が +5% なら portfolio 全体の損は -12.5%（50/50 仮定）
- 損失の数字が小さくなることで投資家は**パニック売りをしない**
- Graham は "the bond component is the investor's defense against his own nervous system" と言った

現代文脈：60/40 の "40" は国債だけでなく IG 社債・短期債・キャッシュで構成されることが多い。日銀 YCC 撤廃後の JGB は 2023年以降、防衛役として再機能し始めた（10年 1.5-1.7% 台, 2026年初時点）。

---

### 4. "60/40 は死んだ" 議論との向き合い方

2022年のインフレ・利上げ局面では、株も債券も同時下落し 60/40 が機能不全に陥った。批判の要点は「株と債券の相関がプラスに転じた」こと。

しかし Graham の真意は「債券のリターンが高いから買う」ではなく「**確実性のある資産を持つことで心理的土台を作る**」。相関が崩れる局面でもルールベースのリバランスを貫く投資家だけが、底値付近で買い増しできた。

---

### 5. 現代のファミリーオフィス・ロングオンリーへの翻訳

| Graham 原則 | 現代 FO / Concentrated Long |
|------------|------------------------------|
| 株 25-75% | ポートフォリオ集中度（Top 10 holdings ≤75%? ） |
| 债券 25-75% | Cash buffer / IG bond / MMF |
| リバランストリガー | 個別銘柄ウェイト上限（例：単一銘柄 ≤20%） |
| 感情排除ルール | Investment policy statement (IPS) |

Camphora・Kaname のようなエンゲージメントファンドは、株式 100% に近い構成だが、代わりに**キャッシュポジションと購入価格ルール（MoS）**で Graham の "defensive floor" を代替している。

---

## Reo への実用的 application

**Schweitzer v6 ポートフォリオ:**  
Schweitzer がロング中心の日本株集中戦略をとる場合、60/40 の "40" は直接使わないかもしれないが、リスク管理として「保有銘柄の平均 upside/downside 比率を常に 2:1 以上維持する」という MoS ルールが Graham の債券枠と機能的に同値だ。v6 の pitch で "downside protection logic" を問われたとき、Graham の 50/50 リバランス原則を引いて「感情でなくルールで守る」と答えられる。

**Watchlist 適用:**  
- **8393（佐賀銀行）** のような低 PBR 日本銀行株は、Graham 的には "bond-like dividend yield + embedded optionality" と見なせる。配当利回りが JGB 10年 +200bp 以上あれば、defensive floor として機能しうる。
- **6440（JUKI）、7282（豊田合成）** のシクリカルは株比率を下げるべき局面（業績ピーク）で Graham 基準 25% ゾーンに入る可能性がある。

**面接スクリプト（Camphora / Oasis 向け）:**  
「Graham の 50/50 に学ぶ点は、ルールが感情を凌駕する構造設計です。私が銘柄 X を保有する際も、事前に "何が起きたら売るか" を文書化し、下落時に感情でなくファンダメンタルズで判断できるよう IPS を設定しています。」

---

## Self-test（明日説明できるか）

1. **Graham の Defensive Investor のアセット・アロケーション・バンドを具体的に示し、「株 60%・债券 40%」という固定値が正確でない理由を説明せよ。**
2. **50/50 リバランスが "意図せぬ逆張り" になるメカニズムを、2つのシナリオ（株高 / 株安）で説明せよ。**
3. **Schweitzer v6 のようなロング集中型ファンドにおいて、Graham の "债券フロア" に機能的に相当するリスク管理手法を1つ挙げよ。**

---

## Source
- Benjamin Graham, *The Intelligent Investor* (rev. ed. 1973), Ch. 4 "General Portfolio Policy: The Defensive Investor"
- Jason Zweig commentary (2003 edition), Ch. 4 margin notes on 60/40 origins
- 日銀 YCC 撤廃後の JGB イールド推移: Bloomberg consensus (2026年初時点)

---

## 次回（Lesson 006）: Enterprising Investor — 7 sub-criteria for stock selection
Graham が Enterprising（積極型）投資家に課す 7 つのスクリーニング条件を学ぶ。Defensive の "安全第一" から一歩踏み込んで、バーゲン株の定量的な発掘条件を習得する。
