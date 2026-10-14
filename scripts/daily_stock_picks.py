#!/usr/bin/env python3
"""Daily 3 interesting stock picks sent to LINE.

Source: Kabutan /disclosures/ (TDnet corporate disclosures)
Logic: Score by presence of interesting keywords (業績修正, TOB, 大量保有, 自社株買い 等),
       then pick top 3 (ties broken by recency).
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from html import unescape

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
    # Capital allocation
    '自社株買い': 7, '自己株式': 6, '増配': 6, '記念配当': 5,
    '株主還元': 6, '配当予想': 5,
    # 増資 / Capital raise
    '第三者割当': 7, '新株予約権': 5, '増資': 5, '転換社債': 4,
    'Issue Price': 4, 'Capital Investment': 3,
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


def send_line(token, user_id, message):
    req = urllib.request.Request(
        'https://api.line.me/v2/bot/message/push',
        data=json.dumps({'to': user_id, 'messages': [{'type': 'text', 'text': message}]}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


def main():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('LINE_USER')
    if not token or not user_id:
        print('ERROR: LINE_TOKEN / LINE_USER env missing')
        sys.exit(1)

    now_jst = datetime.now(JST)
    weekday_jp = ['月', '火', '水', '木', '金', '土', '日'][now_jst.weekday()]
    date_str = now_jst.strftime(f'%m/%d({weekday_jp})')

    try:
        disclosures = fetch_disclosures()
    except Exception as e:
        msg = f'📊 本日 ({date_str}) の 開示注目\n\n⚠️ Kabutan取得エラー: {e}\n\n手動: https://kabutan.jp/disclosures/'
        send_line(token, user_id, msg)
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
        msg = (
            f'📊 本日 ({date_str}) の 開示注目\n\n'
            f'開示データ取得できず (全0件)。\n\n'
            f'手動確認: https://kabutan.jp/disclosures/'
        )
        send_line(token, user_id, msg)
        print('No disclosures at all')
        return

    lines = [f'📊 本日 ({date_str}) の 開示注目3銘柄', '']
    for i, d in enumerate(top3, 1):
        name = d['name'] or '(名称不明)'
        tag = f'[{d["exchange"]}]' if d['exchange'] else ''
        title = d['title'][:70] + ('…' if len(d['title']) > 70 else '')
        time_h = d['time'][11:16] if len(d['time']) >= 16 else ''
        star = '⭐' if d['score'] >= 7 else ''
        lines.append(f'{i}. {star}{d["code"]} {name} {tag}')
        lines.append(f'   {title}')
        meta = []
        if time_h:
            meta.append(time_h)
        if d['score'] > 0:
            meta.append(f'score={d["score"]}')
        if meta:
            lines.append(f'   ({" | ".join(meta)})')
        lines.append('')
    lines.append(f'全開示 (全{len(disclosures)}件): https://kabutan.jp/disclosures/')
    msg = '\n'.join(lines)

    status = send_line(token, user_id, msg)
    try:
        print(f'Sent (status {status}):\n{msg}')
    except UnicodeEncodeError:
        print(f'Sent (status {status}): [msg contains non-encodable chars for console]')


if __name__ == '__main__':
    main()
