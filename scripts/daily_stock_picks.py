#!/usr/bin/env python3
"""Daily 3 interesting stock picks sent to Slack #stock-picks.

Source: Kabutan /disclosures/ (TDnet corporate disclosures)
Logic: Score by presence of interesting keywords (業績修正, TOB, 大量保有, 自社株買い 等),
       then pick top 3 (ties broken by recency).
Env: SLACK_WEBHOOK_URL (= secret SLACK_WEBHOOK_STOCKS at workflow level)
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from slack_push import send_slack, send_slack_blocks, header, section, section_fields, divider, context

JST = timezone(timedelta(hours=9))

# Weighted keywords by Reo's edge (activist/event-driven + value + 業績 catalyst).
# Higher weight = more interesting.
KEYWORD_WEIGHTS = {
    # Event-driven (TOB, M&A)
    'TOB': 10, '公開買付': 10, '非公開化': 10, 'MBO': 10, 'LBO': 10,
    'Tender': 9, 'Acquisition': 8, '買付': 7, '買収': 8,
    '合併': 7, '完全子会社化': 8, '株式交換': 7, '株式併合': 7,
    # Activist / 持ち分 changes
    '大量保有': 9, '活動方針': 9, '重要提案': 9, '共同保有': 8,
    '5%': 7, '株券等': 5,
    # Earnings catalyst
    '上方修正': 9, '下方修正': 8, '業績予想': 6, '最高益': 7,
    '増益': 5, '通期予想': 4, '営業利益': 3,
    'Earnings': 4, 'Upward Revision': 8, 'Downward Revision': 8,
    # Capital allocation
    '自社株買い': 7, '自己株式': 6, '増配': 6, '記念配当': 5,
    '株主還元': 6, '配当予想': 5,
    'Share Buyback': 7, 'Dividend': 4, 'Treasury Stock': 5,
    # 増資 / Capital raise
    '第三者割当': 7, '新株予約権': 5, '増資': 5, '転換社債': 4,
    'Issue Price': 5, 'Selling Price': 5, 'Capital Investment': 4,
    # Governance / 不正 (short candidates)
    '不正': 9, '疑義': 9, '意見不表明': 9, '限定付適正意見': 8,
    '不適切': 8, '特別調査委員会': 8, '過年度訂正': 7,
    '特別注意': 8, '監理銘柄': 7, '上場廃止': 8,
    # Partnership / 業務提携
    '資本業務提携': 7, '資本提携': 6, '業務提携': 5, '出資': 5,
    # Insider / 役員
    '社長交代': 6, '代表取締役異動': 5, '辞任': 4,
    # Special
    'ToSTNeT': 6, 'PBR': 4, 'ROE': 3,
}

# Noise to downrank (routine filings)
NOISE_KEYWORDS = {
    '四半期報告書': -5, '有価証券報告書': -3, '半期報告書': -3,
    'Financial Results Briefing': -3, 'Integrated Report': -3,
    'Corporate Governance Report': -3, 'コーポレート・ガバナンス': -3,
    '定時株主総会': -3, '基準日': -2,
}


def fetch_disclosures():
    """Fetch and parse Kabutan disclosures page."""
    req = urllib.request.Request(
        'https://kabutan.jp/disclosures/',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8', errors='replace')

    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    results = []
    for row in rows:
        code_m = re.search(r'/stock/\?code=(\d{4})', row)
        if not code_m:
            continue
        code = code_m.group(1)
        if code == '0000':
            continue

        # Extract stock name (first <th class="tal"> after code)
        name_m = re.search(r'<th\s+scope="row"\s+class="tal">([^<]+)</th>', row)
        name = unescape(name_m.group(1).strip()) if name_m else ''

        # Extract disclosure title (link text to PDF)
        title_m = re.search(r'target="pdf">([^<]+)(?:<img|</a>)', row)
        title = unescape(title_m.group(1).strip()) if title_m else ''
        # Clean up trailing numbers like "2026"
        title = re.sub(r'\s*20\d\d\s*$', '', title)

        # Extract timestamp
        time_m = re.search(r'<time[^>]*datetime="([^"]+)"', row)
        time_iso = time_m.group(1) if time_m else ''

        # Exchange & category (optional)
        exch_m = re.search(r'<td\s+class="tac">([東名福札]証?[PGSNPro]+)</td>', row)
        exchange = exch_m.group(1) if exch_m else ''

        results.append({
            'code': code, 'name': name, 'title': title,
            'time': time_iso, 'exchange': exchange,
        })

    return results


def score_disclosure(d):
    """Score higher = more interesting."""
    title = d['title']
    score = 0
    for kw, w in KEYWORD_WEIGHTS.items():
        if kw in title:
            score += w
    for kw, w in NOISE_KEYWORDS.items():
        if kw in title:
            score += w  # negative
    return score


def categorize(title):
    """Return (category_tag, trade_angle). Trade angle = what Reo should do/watch."""
    t = title
    # Event-driven (TOB/M&A)
    if any(k in t for k in ['TOB', '公開買付', '非公開化', 'MBO', 'LBO', 'Tender']):
        if '条件等の変更' in t or '価格の変更' in t or 'Amendment' in t:
            return ('🤝 TOB条件変更', '価格up・期限延長の可能性 → 現在株価と比較してarb spread残っているか即check、残っていれば entry 検討')
        if '応募' in t or '下限' in t:
            return ('🤝 TOB応募状況', '応募率で成立確度判定 → 下限超えてれば決済織込みで arb spread 縮小')
        return ('🤝 TOB発表', 'event-driven核心案件 → premium/discount分析、同業他社の next target 推定')
    if '完全子会社化' in t or '株式交換' in t:
        return ('🤝 子会社化', '同業・親子上場解消 → +45-50%プレミアム法則の pattern (レオパレス/フェローテク等と比較)')
    if '合併' in t:
        return ('🤝 合併', 'シナジー数字 + 新会社の時価総額 + 株式比率で arb check')
    # Activist
    if '大量保有' in t or '活動方針' in t or '重要提案' in t:
        if '5%' in t or '新規' in t:
            return ('⚔️ Activist新規', '5%超の新規保有 → Day 0 候補、翌営業日の板で初期反応確認、活動方針欄で「重要提案」有無check')
        return ('⚔️ Activist変動', '保有pt変化で意図 (ラダー買増 or 利確) → 直前の%と増減幅で判定')
    # Earnings
    if '上方修正' in t or '最高益' in t:
        return ('📈 業績上振れ', 'OP 修正率と要因 (需要/値上げ/コスト) check → 既存 short の thesis challenge 可能性、同業への spillover')
    if '下方修正' in t:
        return ('📉 業績下振れ', 'OP 下方率と要因 → 既存 long の thesis 棄損、同業連鎖で short pair 候補')
    if '業績予想' in t:
        return ('📊 業績予想', '通期・四半期予想修正 → 市場想定とのdeviation check')
    # Capital allocation
    if '自社株買い' in t or '自己株式' in t:
        return ('💰 自社株買い', '上限枚数・金額・期間 → 時価総額比%で demand 影響評価、PBR<1なら特に effective')
    if '増配' in t or '記念配当' in t:
        return ('💰 増配', '配当方針 shift → 利回り再計算、株主還元強化トレンド銘柄 scan')
    # Governance red
    if '意見不表明' in t or '限定付適正意見' in t:
        return ('🚨 監査問題', 'Big4 意見不表明 → 特別注意銘柄行きの前兆 (Schilit三点セット候補)、short entry検討')
    if '不正' in t or '不適切' in t or '疑義' in t:
        return ('🚨 不正疑義', '会計不正・疑義 → short candidate (エア・ウォーター/電気興業 pattern)、第三者委委員 lineup check')
    if '特別調査委員会' in t or '過年度訂正' in t:
        return ('🚨 第三者委', '不正調査開始 → 訂正発表までの期間で短期ショート、監査法人交代と重なれば three-strike')
    if '特別注意' in t or '監理銘柄' in t or '上場廃止' in t:
        return ('🚨 制裁', 'JPX制裁 → 上場廃止までのタイムライン確認、活動方針変更の持ち分変動と連動check')
    # Capital raise
    if '第三者割当' in t or '新株予約権' in t:
        return ('💵 増資', '発行価格と割引率 → 既存株主希薄化率、調達資金使途が M&A か 事業資金か')
    # Partnership
    if '資本業務提携' in t or '資本提携' in t:
        return ('🤝 資本提携', '出資比率・金額 → 将来の TOB 発展可能性 (伊藤忠×電通総研 pattern)')
    # English fallbacks
    if 'Issue Price' in t or 'Selling Price' in t:
        return ('💵 公募価格決定', '公募・売出 price fix → ディスカウント率と需給 impact')
    if 'Capital Investment' in t or '設備投資' in t:
        return ('🏭 設備投資', '追加投資額・増産率 → 業界 capex サイクルの位置')
    if 'Share Buyback' in t or 'Buyback' in t:
        return ('💰 自社株買い (EN)', '英語開示自社株買い → 国内開示 cross check')
    if 'Dividend' in t:
        return ('💰 配当関連 (EN)', '英語配当開示 → 利回り再計算')
    if 'Acquisition' in t:
        return ('🤝 Acquisition (EN)', '英語M&A → 国内公式開示 cross check')
    if 'Earnings' in t or 'Financial Results' in t:
        return ('📊 決算 (EN)', '英語決算 → 日本語版の数字 cross check')
    # Default
    return ('📄 開示', '事務的開示 → 他 pick が強ければ skip 可')


def build_takeaway(top3: list, total: int) -> str:
    """Generate a 1-2 sentence takeaway summarizing today's themes."""
    categories = [categorize(d['title'])[0] for d in top3]
    themes = []
    tob_count = sum(1 for c in categories if 'TOB' in c or '子会社' in c or '合併' in c)
    activist_count = sum(1 for c in categories if 'Activist' in c)
    earnings_count = sum(1 for c in categories if '業績' in c)
    gov_count = sum(1 for c in categories if '🚨' in c)
    capital_count = sum(1 for c in categories if '自社株' in c or '増配' in c or '💵' in c)

    if tob_count >= 2:
        themes.append(f'TOB/M&A再編 {tob_count}件 (arb機会)')
    if activist_count >= 1:
        themes.append(f'Activist動き {activist_count}件 (Day 0 entry候補)')
    if gov_count >= 1:
        themes.append(f'ガバナンス red flag {gov_count}件 (short candidate)')
    if earnings_count >= 2:
        themes.append(f'業績修正 {earnings_count}件 (thesis再評価)')
    if capital_count >= 2:
        themes.append(f'資本政策 {capital_count}件 (需給 catalyst)')

    high_score = top3[0]['score'] if top3 else 0
    if high_score >= 15:
        headline = f'⭐ 高score pick あり (score {high_score}) → #1 を優先深掘り'
    elif high_score >= 7:
        headline = f'中score picks → #1 の trade angle 確認推奨'
    else:
        headline = f'大型 catalyst 乏しい日 → routine filings 中心'

    takeaway = headline
    if themes:
        takeaway += '。 本日のテーマ: ' + ' / '.join(themes)
    takeaway += f' (全{total}開示)'
    return takeaway


def main():
    now_jst = datetime.now(JST)
    weekday_jp = ['月', '火', '水', '木', '金', '土', '日'][now_jst.weekday()]
    date_str = now_jst.strftime(f'%m/%d({weekday_jp})')

    try:
        disclosures = fetch_disclosures()
    except Exception as e:
        blocks = [
            header(f'📊 開示注目 — {date_str}'),
            section(f'⚠️ *Kabutan取得エラー*: {e}\n\n<https://kabutan.jp/disclosures/|手動で開示一覧を確認>'),
        ]
        send_slack_blocks(blocks, fallback_text=f'開示注目エラー {date_str}')
        print('Error path:', e)
        return

    # Score all, sort by score (interesting first), fallback to most recent
    for d in disclosures:
        d['score'] = score_disclosure(d)
    disclosures.sort(key=lambda x: (-x['score'], x['time']), reverse=False)

    # Dedup by code (keep highest-scored per code; English/Japanese pairs for same stock)
    seen = {}
    for d in disclosures:
        if d['code'] not in seen or seen[d['code']]['score'] < d['score']:
            seen[d['code']] = d
    unique = list(seen.values())
    unique.sort(key=lambda x: (-x['score'], x['time']), reverse=False)
    top3 = unique[:3]

    if not top3:
        blocks = [
            header(f'📊 開示注目 — {date_str}'),
            section('開示データ取得できず (全0件)。\n<https://kabutan.jp/disclosures/|手動確認>'),
        ]
        send_slack_blocks(blocks, fallback_text=f'開示注目 {date_str} (データなし)')
        print('No disclosures at all')
        return

    blocks = [
        header(f'📊 開示注目3銘柄 — {date_str}'),
        section(f'💡 *Today\'s Takeaway*\n{build_takeaway(top3, len(disclosures))}'),
    ]
    for i, d in enumerate(top3):
        name = d['name'] or '(名称不明)'
        tag = f'`{d["exchange"]}`' if d['exchange'] else ''
        title = d['title'][:150] + ('…' if len(d['title']) > 150 else '')
        time_h = d['time'][11:16] if len(d['time']) >= 16 else ''
        cat, trade_angle = categorize(d['title'])
        star = '⭐ ' if d['score'] >= 15 else ''
        rank = ['①', '②', '③'][i]

        # Headline block: ranking + ticker + category
        headline_md = f'{rank} *{star}{d["code"]} {name}* {tag}\n{cat}'
        blocks.append(divider())
        blocks.append(section(headline_md))

        # Trade angle (the "why Reo should care" part)
        if trade_angle:
            blocks.append(section(f'🎯 *Trade Angle*\n{trade_angle}'))

        # Original disclosure (raw title)
        blocks.append(section(f'📰 {title}'))

        # Meta context
        meta_elems = []
        if time_h:
            meta_elems.append(f'🕐 {time_h}')
        if d['score'] > 0:
            meta_elems.append(f'📊 score {d["score"]}')
        meta_elems.append(f'<https://kabutan.jp/stock/?code={d["code"]}|{d["code"]} 個別ページ>')
        blocks.append(context(meta_elems))

    blocks.append(divider())
    blocks.append(context([f'全{len(disclosures)}件: <https://kabutan.jp/disclosures/|kabutan.jp/disclosures/>']))

    status = send_slack_blocks(blocks, fallback_text=f'📊 開示注目3銘柄 {date_str}')
    msg = f'Blocks sent ({len(blocks)} blocks)'
    try:
        print(f'Sent (status {status}):\n{msg}')
    except UnicodeEncodeError:
        print(f'Sent (status {status}): [msg contains non-encodable chars for console]')


if __name__ == '__main__':
    main()
