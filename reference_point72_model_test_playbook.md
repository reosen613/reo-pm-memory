---
name: Point72 モデルテスト Playbook（アーカイブ）
description: Point72 45分3表モデリングテストの63ステップ手順書 — 2026-04-05合格済、参照用アーカイブ
type: reference
---

## ステータス: アーカイブ（2026-04-05合格済）

このプレイブックは過去のテスト準備で使用した完成版手順。現役の作業対象ではないが、将来同種のテストを受ける／後輩に教える／モデリング論点を確認する際の参照用として保持。

## テスト概要
- Point72の45分タイムドモデルテスト（アナリストポジション）
- 日本の自動車部品メーカー
- 実績: 2018A-2022A、予測: 2023E-2026E
- 一枚シート完結、partially completedモデルの黄色セルを埋める
- 最重要目標: **Balance Check = 0**
- Vera（Point72テストプラットフォーム）を使用、Claude Code使用不可

## Demoテスト結果
- Demo_Blank_RA2で全セル正解（丸め誤差のみ、ロジックエラーゼロ）
- Balance Check = 0 全年度達成

## 本番手順（63ステップ、Phase 0-10）

### Phase 0: 全体把握（0:00-2:00）
- シート全体スクロール、コストドライバー確認（COGS%あるか？ブリッジ型か？）

### Phase 1: 売上分析（2:00-7:00）
- Row 18: 売上=Row12リンク
- Row 19: 成長率=(当年-前年)/前年
- Row 20: $変動=当年-前年
- Row 21: 数量効果=ΔVol×前年ASP/1M
- Row 22: 価格効果=Row20-Row21

### Phase 2: GP→COGS（7:00-12:00）
- Row 27: GP増分(数量)=Row21×0.2
- Row 29: GP増分(価格)=Row22×0.7
- Row 24: COGS=Rev-(前年GP+Row27+Row29) ※COGS%明示ならRev×COGS%
- Row 26: 粗利率=Row25/Rev

### Phase 3: IS中盤（12:00-15:00）
- Row 32: SG&A=Rev×Row57
- Row 33: D&A=Rev×Row58
- Row 34: 営業利益=Row25-Row32-Row33
- Row 35: 営業利益率=Row34/Rev

### Phase 4: Debt確定→IS完成（15:00-22:00）
- Row 82: LT Debt=前年+Row128
- Row 37: 利息=Row82(当年末LT Debt)×Row59
- Row 38-40: 税引前→税→NI
- Row 45: EPS=Row40/Row43(希薄化後)
- Row 130: 配当=-(Row46×Row42(基本))
- Row 112: SBC=Rev×Row142

### Phase 5: 調整後指標（22:00-24:00）
- Row 51: Adj EBITDA=Row34+Row33+Row49
- Row 54: Adj EPS=(Row40+Row49)/Row43

### Phase 6: BS WC+固定資産（24:00-28:00）
- Row 68: AR=Rev×DSO/365
- Row 69: Inv=COGS×DIO/365
- Row 78: AP=COGS×DPO/365
- Row 121: CapEx=Rev×Row141(負)
- Row 72: PP&E=前年-Row121(負)-Row33

### Phase 7: CF（28:00-34:00）
- Row 110-112: NI+D&A+SBC
- Row 115: ΔAR=前年-当年（増→マイナス）
- Row 116: ΔInv=前年-当年（増→マイナス）
- Row 117: ΔAP=当年-前年（増→プラス）
- Row 118: 営業CF合計
- Row 136: 現金純増減=営業+投資+財務+為替
- Row 138: 期末Cash=期首+純増減
- Row 139: FCF=Row118+Row121

### Phase 8: BS完成（34:00-38:00）
- Row 67: Cash=Row138
- Row 86: 純資産=前年+NI+配当(負)+SBC ★SBC忘れない
- Row 88: Balance Check=0

### Phase 9: 比率（38:00-42:00）
- Row 97: NetDebt/EBITDA=(Row82-Row67)/Row51 ★LT Debtのみ
- Row 101: ROE=NI/Avg Equity ★÷2忘れない
- Row 103: ROIC=EBIT×(1-税率)/Avg IC ★分子はNOPAT

### Phase 10: バリュエーション（42:00-45:00）
- Row 146: 時価総額=株価×Row43(希薄化後)
- Row 147: EV=時価総額+Row82-Row67
- Row 149-151: PER, EV/EBITDA, FCF Yield

## 間違えやすい5つ
1. COGS%直接ではなくGPブリッジ→COGS逆算（COGS%明示ならそっち）
2. 利息=LT Debt当年末×金利（Total Debtではない）
3. PP&E: CapExはマイナス値→Prior-Row121(負)-D&A
4. 純資産: Prior+NI+配当(負)+SBC ★SBC忘れない
5. ROIC分子=EBIT×(1-税率) ★NIではない

## 株数の使い分け
- 配当(Row130): 基本株数(Row42)
- EPS/Adj EPS/時価総額: 希薄化後(Row43)

## BSデバッグ順
1. SBC漏れ(≈7) 2. PP&E符号 3. Cash≠CF期末 4. WC符号 5. 配当符号

## 本番テスト結果（2026-04-05）
- 本番テスト完了・提出済み・**合格**
- BS Balance = 0 達成、FCF修正済み（プラス転換）
- 3表リンク正常、Valuation妥当
