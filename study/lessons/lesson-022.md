---
title: Lesson 022 — Misleading Artifices — Schilit の precursor
phase: 1
date: 2026-06-24
estimated_reading: ~10 min
---

# Lesson 022 — Misleading Artifices — Schilit の precursor

## 1 行で
Graham が 1934 年に警告した「会計上の誤魔化し」のパターン 5 類型を押さえることで、Schilit（Phase 5）の Financial Shenanigans 全体を構造的に先読みできる。

## なぜ今それをやるか
Lesson 020（Net-Net）・021（Asset-rich）は「安く見える会社」の発見術だった。しかし「安く見えるように**演出された**会社」の識別は、その鏡像として不可欠だ。Graham は *Security Analysis*（1934）と *The Intelligent Investor* の改訂版（1949/1959/1973）で断続的に、管理者が EPS・純資産・稼ぎを人工的に嵩上げする手法を列挙した。これが Schilit（1993）「Financial Shenanigans」の思想的起源であり、Phase 5 の 20 レッスンを深く理解するための地図になる。面接官が「どうやって会計の質を見るか」と聞いてきたとき、「Schilit の 7 つのシェナニガン」を機械的に暗唱するより、**Graham が何十年も前に見抜いた根本ロジック**から語れる方が圧倒的に印象が違う。

---

## Core Content

### 1. Graham の問題意識：「報告利益」は一次情報ではない

Graham の出発点は単純だ。公開企業の経営陣は「好業績を演出する強いインセンティブ」を持ち、会計基準が許す範囲（あるいは少し外れた範囲）でそれを行使する。したがって **アナリストは報告 EPS をそのまま受け取ってはならない** ―― 必ず調整・検証する義務がある。

Graham は主に以下の 5 類型を問題にした。

---

### 2. 5 類型の Misleading Artifices

| # | 類型 | 手口の概要 | Schilit 対応 |
|---|------|-----------|-------------|
| **A** | 非経常利益の経常混入 | 資産売却益・保険金・訴訟和解金を営業利益に含める | Shenanigan 3 |
| **B** | 費用の先送り・資産化 | 本来費用化すべき開発費・修繕費を資産計上し当期費用を圧縮 | Shenanigan 4 |
| **C** | 連結範囲の操作 | 赤字子会社を除外、黒字子会社のみ持分法→連結切替 | Shenanigan 1/2 |
| **D** | 会計方針変更による利益嵩上げ | 在庫評価・減価償却方法の変更で EPS を底上げ | Shenanigan 6 |
| **E** | 引当金・準備金の恣意的取崩 | 景気悪化期に過大積立 → 好況期に取崩して「利益」計上 | Shenanigan 3/6 |

---

### 3. 類型 A の深掘り：非経常利益の経常混入

Graham が最も頻繁に批判したのがこれだ。

**仕組み**：土地・有価証券の売却益（本来「特別利益」）を営業利益の上位に含める、または別の名目（"other income"）で混入させ、繰り返し発生するかのように見せる。

**発見法**：
1. 過去 5 年の「その他収益」の内訳を注記で追う
2. キャッシュフロー計算書の投資 CF（資産売却収入）と P&L の「その他収益」を照合 → CF に出ているのに P&L が膨らんでいれば混入の証拠
3. EBIT margin の年次変動が異常に安定的 → 「調整」の可能性

**日本の典型例**：不動産・エネルギー系の重厚長大企業が含み資産（Lesson 021）を少しずつ売却し、毎年 "その他利益" として計上し続けるケース。いつか資産が尽きると利益は消える。

---

### 4. 類型 B の深掘り：費用の資産化

Graham はこれを「帳簿上の繁栄（paper prosperity）」と呼んだ。

**仕組み**：
- ソフトウェア開発費 → 無形資産（IFRS IAS 38 の開発フェーズのみ）
- 映像・ゲームコンテンツ制作費 → コンテンツ資産
- 顧客獲得費用（CAC）→ 契約獲得コスト（IFRS 15 B94）

これらは適切に使えば正当だが、**技術的に費用要件を満たさない段階から資産化を始める**のが不正だ。

**発見法**：
- 無形資産の急増 × 売上成長率との乖離
- キャッシュ FCF（営業 CF − 投資 CF）が報告純利益を大きく下回る
- 開示注記の「資産化した開発費」の前提を確認（将来の経済的便益が確実か？）

---

### 5. 類型 E の深掘り：引当金の Big Bath と Cookie Jar

Graham の時代から経営者がよく使うのが **Big Bath** と **Cookie Jar** のセットだ。

| 局面 | 操作 | 効果 |
|------|------|------|
| **業績悪化期（社長交代時）** | 前経営陣のせいにして過大損失計上（Big Bath） | 翌年以降の比較基準を下げる |
| **業績回復期** | 過大計上した引当金を取崩し（Cookie Jar） | 努力なく「利益増」が出現 |

日本で典型的なのは **のれん一括減損**（新 CEO 就任直後）→ 翌年から減損費用ゼロで利益改善、というパターン。**見抜くには前 CEO 退任・社長交代の時期と大型特損の時期を照合する**。

---

### 6. Graham → Schilit の知識地図

```
Graham (1934-1973)           Schilit (1993-2018)
─────────────────            ───────────────────────────────────
類型 A: 非経常混入       →   Shenanigan 3: Boosting income with one-time gains
類型 B: 費用の先送り     →   Shenanigan 4: Shifting current expenses to later
類型 C: 連結操作         →   Shenanigan 1: Recording revenue too soon
類型 D: 会計方針変更     →   Shenanigan 6: Shifting current income to later
類型 E: 引当金操作       →   Shenanigan 3 + 6 の複合
```

Phase 5（Lesson 121-140）ではこの各枝を一つずつ深掘りする。今日の目標は **幹を理解すること**。

---

## Reo への実用的 application

### ショートサイドへの直接応用

Reo のショートウォッチリスト（4661・5032・4911・5803・4062・4477・6027・6594）の中でこの観点が特に鋭いのは次の 2 銘柄だ。

**5032 ANYCOLOR（ショート仮説）**
VTuber 事業の会計は以下の論点を持つ：
- タレント向け初期制作費（3D モデル、配信システム）の **資産化 vs 費用化** — 資産化すれば当期費用が圧縮され利益が嵩上げ
- ライブ配信チケット・グッズ売上の **収益認識タイミング**（IFRS 15 ステップ 5：履行義務の充足）
- 所属タレント離脱時の **コンテンツ資産の減損テスト** が適切か
→ M-Score（Lesson 133）の DSRI（Day's Sales Receivable Index）と AQI（Asset Quality Index）を計算すれば仮説が定量化できる

**4911 資生堂（ショート仮説）**
構造改革期（2023-2025）に大型特損を計上中 → **Big Bath 後の Cookie Jar 相場** に入っていないか、引当金取崩しの有無を次の決算で要確認。

### FIG 出身の視点で追加すること
銀行・保険の引当金（貸倒引当金・責任準備金）は、一般事業会社より格段に経営者裁量が大きい。Reo の JPM FIG IBD 経験は「どの水準で引当を切るかは経営判断」という肌感覚があるはず ―― その感覚を株式分析に転用することが他の受験者との差別化になる。

---

## Self-test（明日説明できるか）

1. **「非経常利益の経常混入」を発見するためにキャッシュフロー計算書の投資セクションを見るのはなぜか？ P&L だけ見ていると何を見落とすか？**

2. **Big Bath と Cookie Jar のセットがなぜ有害か、"利益の平準化（earnings smoothing）"との違いも含めて説明せよ。**

3. **5032 ANYCOLOR の VTuber 事業において、Graham が批判する「費用の資産化（類型 B）」が発生しうる具体的な勘定科目を 2 つ挙げ、それを発見するために有報のどこを確認するか述べよ。**

---

## Source

- Graham, B. & Dodd, D. (1951). *Security Analysis*, 3rd ed., Chapter 32「Misleading Artifices in the Income Account」
- Graham, B. (1973). *The Intelligent Investor*, 4th ed., Chapter 12「Things to Consider About Per-Share Earnings」（特に「Artifices in the Presentation of Income Account Figures」節）
- Schilit, H. & Perler, J. (2018). *Financial Shenanigans*, 4th ed. — 上記との対応は著者独自マッピング
- IFRS IAS 38（無形資産）・IFRS 15（収益認識）— 費用資産化・収益認識の現代的基準

---

## 次回 (Lesson 023): Per-Share Earnings — non-recurring の真偽

EPS の計算で「一過性項目」を除外すべきか含めるべきか、Graham の判断基準と現代の「調整 EPS」問題を接続する。5032・4661 等の「Non-GAAP 利益」開示の読み方を演習する。
