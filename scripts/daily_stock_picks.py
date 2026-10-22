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

# Noise to downrank/filter (routine filings + marketing fluff)
NOISE_KEYWORDS = {
    # Routine filings
    '四半期報告書': -10, '有価証券報告書': -8, '半期報告書': -8,
    'Financial Results Briefing': -8, 'Integrated Report': -8,
    'Corporate Governance Report': -8, 'コーポレート・ガバナンス': -8,
    '定時株主総会': -5, '基準日': -3,
    # IR / Marketing fluff
    '説明会のお知らせ': -8, '説明会': -5, 'IRTV': -8,
    'セミナー': -5, 'ウェビナー': -5, 'Live': -3,
    '個人投資家向け': -5,
    # PR / Awards
    '受賞': -8, 'Award': -8, '認定': -5, '表彰': -5, 'Leader': -3,
    # Reports (not actionable)
    '提言': -8, 'シナリオ': -5, 'シナリオレポート': -8, 'レポート': -3,
    # Platform/subsidiary news
    'サブスク': -3, 'ラインナップ拡充': -5,
}

# Hard filter: score below this is suppressed (never shown as pick)
MIN_SCORE_TO_SHOW = 3


def fetch_company_hp(code: str) -> str | None:
    """Scrape company HP URL from Kabutan stock page. Return None on failure."""
    try:
        req = urllib.request.Request(
            f'https://kabutan.jp/stock/?code={code}',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode('utf-8', errors='replace')
        # Look for external links that match corporate HP pattern (not minkabu/kabutan/ads)
        exclusions = ('kabutan.jp', 'minkabu.jp', 'google', 'twitter', 'facebook',
                      'line.me', 'doubleclick', 'cdnjs', 'cloudflare', 'yahoo',
                      'rakuten.co.jp', 'adserver', 'japannext.co.jp', 'ebis.ne.jp')
        for m in re.finditer(r'href="(https?://[^"]+)"', html):
            url = m.group(1)
            if any(x in url.lower() for x in exclusions):
                continue
            # Must look like a corporate HP (short-ish, no query, likely .co.jp/.com/.jp)
            if any(url.lower().endswith(ext) or url.lower().endswith(ext + '/') for ext in ['.co.jp', '.com', '.jp', '.io']) \
               and len(url) < 100 and '?' not in url and '&' not in url:
                return url
        return None
    except Exception:
        return None


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://kabutan.jp/',
}


# --- どういう会社か（毎回の通知に入れる。Reo 2026-10-21/22「毎回どういう会社か入るようにして」） ---
_BASICS = None


def load_basics() -> dict:
    """data/company_basics.json: 全上場3,707社の業種・市場・時価総額・四季報2026秋の見出しとコメント（銘柄研究帳 universe.json から生成）。無ければ空。"""
    global _BASICS
    if _BASICS is None:
        try:
            import json as _json
            _BASICS = _json.loads((Path(__file__).parent.parent / 'data' / 'company_basics.json').read_text(encoding='utf-8'))
        except Exception:
            _BASICS = {}
    return _BASICS


def _fetch_minkabu_profile(code: str) -> str | None:
    """みんかぶの銘柄ページの description から事業の1行を拾う（取れなければ None）。"""
    try:
        req = urllib.request.Request(f'https://minkabu.jp/stock/{code}', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode('utf-8', errors='replace')
        m = re.search(r'<meta name="description" content="([^"]{20,400})"', html)
        if m:
            t = re.sub(r'\s+', ' ', m.group(1)).strip()
            return t[:160]
    except Exception:
        pass
    return None


def company_overview(code: str) -> str:
    """Slack に出す『どういう会社か』: 業種・市場・時価総額、四季報の見出しとコメント（前半）、予想PER・EPS・配当。"""
    b = load_basics().get(code) or {}
    parts = []
    mc = (b.get('mcap') or 0) * 100  # universe.json の mcap は百億円単位
    head = ' / '.join(x for x in [b.get('s33'), b.get('mkt'), (f"時価総額{mc:,.0f}億" if mc >= 10 else (f"時価総額{mc:.1f}億" if mc > 0 else None))] if x)
    if head:
        parts.append(head)
    if b.get('hd') or b.get('cm'):
        cm = (b.get('cm') or '')[:110]
        parts.append(f"四季報: {cm}" if cm.startswith('【') else f"四季報: 【{b.get('hd') or '-'}】{cm}")
    nums = []
    if b.get('per'):
        nums.append(f"予想PER {b['per']}倍")
    if b.get('eps'):
        nums.append(f"予想EPS {b['eps']:,.0f}円")
    if b.get('dps'):
        nums.append(f"配当 {b['dps']:,.0f}円")
    if nums:
        parts.append('・'.join(nums))
    if not parts:
        mk = _fetch_minkabu_profile(code)
        parts.append(mk or '概要を取得できず（株探・みんかぶのリンクから確認）')
    return '\n'.join(parts)


def _fetch_kabutan():
    """Kabutan disclosures page (blocked with 405 from some datacenter IPs)."""
    req = urllib.request.Request('https://kabutan.jp/disclosures/', headers=HEADERS)
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
        name_m = re.search(r'<th\s+scope="row"\s+class="tal">([^<]+)</th>', row)
        name = unescape(name_m.group(1).strip()) if name_m else ''
        title_m = re.search(r'target="pdf">([^<]+)(?:<img|</a>)', row)
        title = unescape(title_m.group(1).strip()) if title_m else ''
        title = re.sub(r'\s*20\d\d\s*$', '', title)
        time_m = re.search(r'<time[^>]*datetime="([^"]+)"', row)
        time_iso = time_m.group(1) if time_m else ''
        exch_m = re.search(r'<td\s+class="tac">([東名福札]証?[PGSNPro]+)</td>', row)
        exchange = exch_m.group(1) if exch_m else ''
        results.append({'code': code, 'name': name, 'title': title, 'time': time_iso, 'exchange': exchange})
    return results


def _fetch_tdnet_day(day):
    """TDnet (JPX) daily list: I_list_001_YYYYMMDD.html ... (100 rows per page)."""
    out = []
    for page in range(1, 15):
        url = f'https://www.release.tdnet.info/inbs/I_list_{page:03d}_{day:%Y%m%d}.html'
        req = urllib.request.Request(url, headers={**HEADERS, 'Referer': 'https://www.release.tdnet.info/inbs/I_main_00.html'})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                html = r.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break
            raise
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
        n = 0
        for row in rows:
            code_m = re.search(r'class="[^"]*kjCode"[^>]*>\s*(\d{4})\d?\s*<', row)
            if not code_m:
                continue
            name_m = re.search(r'class="[^"]*kjName"[^>]*>([^<]*)<', row)
            title_m = re.search(r'class="[^"]*kjTitle"[^>]*>\s*<a[^>]*>([^<]+)</a>', row)
            time_m = re.search(r'class="[^"]*kjTime"[^>]*>\s*(\d{1,2}:\d{2})', row)
            place_m = re.search(r'class="[^"]*kjPlace"[^>]*>([^<]*)<', row)
            out.append({
                'code': code_m.group(1),
                'name': unescape(name_m.group(1)).strip() if name_m else '',
                'title': unescape(title_m.group(1)).strip() if title_m else '',
                'time': f'{day:%Y-%m-%d}T{time_m.group(1)}' if time_m else f'{day:%Y-%m-%d}',
                'exchange': (place_m.group(1).strip() if place_m else ''),
            })
            n += 1
        if n == 0 or not re.search(rf'I_list_{page + 1:03d}_', html):
            break
    return out


def fetch_disclosures():
    """Kabutan first; if it is blocked (405 etc.), fall back to TDnet (today + previous business day)."""
    try:
        res = _fetch_kabutan()
        if res:
            return res
    except Exception as e:
        print('kabutan failed, falling back to TDnet:', e)
    now = datetime.now(JST)
    days = [now.date()]
    prev = now.date() - timedelta(days=1)
    while prev.weekday() >= 5:
        prev -= timedelta(days=1)
    days.append(prev)
    results = []
    for d in days:
        results.extend(_fetch_tdnet_day(d))
    if not results:
        raise RuntimeError('TDnet からも取得できませんでした')
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

    # Score all, dedup by code
    for d in disclosures:
        d['score'] = score_disclosure(d)
    disclosures.sort(key=lambda x: (-x['score'], x['time']), reverse=False)
    seen = {}
    for d in disclosures:
        if d['code'] not in seen or seen[d['code']]['score'] < d['score']:
            seen[d['code']] = d
    unique = list(seen.values())
    unique.sort(key=lambda x: (-x['score'], x['time']), reverse=False)

    # Apply hard filter: only picks with score >= MIN_SCORE_TO_SHOW
    qualified = [d for d in unique if d['score'] >= MIN_SCORE_TO_SHOW]
    top3 = qualified[:3]

    # If < 3 qualified, send "quiet day" message with context + alternative sources
    if len(top3) < 3:
        quiet_hour = now_jst.hour < 15  # early in day = probably just slow
        header_txt = f'📊 開示注目 — {date_str}'
        if not top3:
            msg_text = (
                f'🔇 *静かな日* — 全{len(disclosures)}開示 のうち、 本日の trade angle に値する catalyst なし。\n\n'
                f'大半 が 事務的 開示 (四半期報告書 / IR説明会 / 受賞 / レポート 等)。\n\n'
                f'{"午前中なので 15:30 の 2回目 push で 後場 の 開示 (業績修正・TOB 発表 等) を 待つ。" if quiet_hour else "本日 は 大型 catalyst 乏しい の で、 他 source に 移動 推奨。"}'
            )
        else:
            msg_text = (
                f'🔇 *静かな日* — 全{len(disclosures)}開示 のうち、 有意な picks は {len(top3)}件 のみ。'
            )

        blocks = [
            header(header_txt),
            section(msg_text),
            divider(),
            section(
                '*🔍 代替 scan 推奨 source*:\n'
                '• <https://kabutan.jp/warning/|Kabutan 警告・ストップ高/急騰>\n'
                '• <https://maonline.jp/|M&A Online 大量保有>\n'
                '• <https://www.jpx.co.jp/listing/measures/alert/index.html|JPX 特別注意銘柄>\n'
                '• <https://kabutan.jp/disclosures/|Kabutan 全開示>'
            ),
        ]
        # Show the few that qualified (even if < 3) with full angle
        for i, d in enumerate(top3):
            name = d['name'] or '(名称不明)'
            cat, trade_angle = categorize(d['title'])
            title = d['title'][:150] + ('…' if len(d['title']) > 150 else '')
            time_h = d['time'][11:16] if len(d['time']) >= 16 else ''
            star = '⭐ ' if d['score'] >= 15 else ''
            rank = ['①', '②', '③'][i]

            blocks.append(divider())
            blocks.append(section(f'{rank} *{star}{d["code"]} {name}*\n{cat}'))
            blocks.append(section(f'🏢 *どういう会社*\n{company_overview(d["code"])}'))
            if trade_angle:
                blocks.append(section(f'🎯 *Trade Angle*\n{trade_angle}'))
            blocks.append(section(f'📰 {title}'))
            meta = [f'🕐 {time_h}'] if time_h else []
            if d['score'] > 0:
                meta.append(f'📊 score {d["score"]}')
            link_parts = [
                f'<https://kabutan.jp/stock/?code={d["code"]}|📊 Kabutan>',
                f'<https://minkabu.jp/stock/{d["code"]}|📘 Minkabu>',
                f'<https://irbank.net/{d["code"]}/|📈 IRBANK>',
            ]
            hp = fetch_company_hp(d['code'])
            if hp:
                link_parts.append(f'<{hp}|🏢 公式HP>')
            meta.append(' / '.join(link_parts))
            blocks.append(context(meta))

        send_slack_blocks(blocks, fallback_text=f'📊 {date_str} 静かな日')
        print(f'Quiet day: {len(qualified)} qualified of {len(disclosures)}')
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
        blocks.append(section(f'🏢 *どういう会社*\n{company_overview(d["code"])}'))

        # Trade angle (the "why Reo should care" part)
        if trade_angle:
            blocks.append(section(f'🎯 *Trade Angle*\n{trade_angle}'))

        # Original disclosure (raw title)
        blocks.append(section(f'📰 {title}'))

        # Meta context (links to multiple sources)
        meta_elems = []
        if time_h:
            meta_elems.append(f'🕐 {time_h}')
        if d['score'] > 0:
            meta_elems.append(f'📊 score {d["score"]}')
        # Standard sources
        link_parts = [
            f'<https://kabutan.jp/stock/?code={d["code"]}|📊 Kabutan>',
            f'<https://minkabu.jp/stock/{d["code"]}|📘 Minkabu>',
            f'<https://irbank.net/{d["code"]}/|📈 IRBANK>',
        ]
        # Try to fetch company HP
        hp = fetch_company_hp(d['code'])
        if hp:
            link_parts.append(f'<{hp}|🏢 公式HP>')
        meta_elems.append(' / '.join(link_parts))
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
