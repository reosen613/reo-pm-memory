"""Fetch major global market indices via Yahoo Finance Chart API (no key, no deps).

Returns a dict of {category: [(symbol, name_jp, close, change, pct)]} suitable for
Block Kit section_fields display on Slack.

Reference: sekai-kabuka.com style — US / 日本 / Asia / 欧州 / FX / 商品 / 金利 in one glance.
"""
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor


# Symbol -> (display_name_jp, category)
SYMBOLS = [
    # US equity
    ('^DJI',   'ダウ',           'US'),
    ('^GSPC',  'S&P500',          'US'),
    ('^IXIC',  'NASDAQ',          'US'),
    ('^SOX',   'SOX (半導体)',    'US'),  # may not resolve, try
    ('^VIX',   'VIX',             'US'),
    # Japan
    ('^N225',  '日経225',          'JP'),
    ('^TPX',   'TOPIX',           'JP'),  # may be ^TOPX
    # Europe
    ('^FTSE',  '英 FTSE100',      'EU'),
    ('^GDAXI', '独 DAX',          'EU'),
    ('^FCHI',  '仏 CAC40',        'EU'),
    # Asia
    ('^HSI',   '香港 ハンセン',    'ASIA'),
    ('000001.SS', '上海総合',     'ASIA'),
    ('^KS11',  '韓国 KOSPI',      'ASIA'),
    # FX
    ('JPY=X',  'USD/JPY',         'FX'),
    ('EURJPY=X', 'EUR/JPY',       'FX'),
    ('EURUSD=X', 'EUR/USD',       'FX'),
    # Commodities
    ('CL=F',   'WTI 原油',        'COM'),
    ('GC=F',   'Gold',            'COM'),
    ('SI=F',   'Silver',          'COM'),
    # Yields
    ('^TNX',   '米10年',          'YIELD'),
]


def fetch_one(sym: str, display: str, cat: str) -> dict | None:
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=5d'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.load(r)
        result = data.get('chart', {}).get('result', [{}])[0]
        meta = result.get('meta', {})
        close = meta.get('regularMarketPrice')
        # Use actual previous day close from the series (not chartPreviousClose, which is 5-day lookback)
        closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])
        prev = None
        if len(closes) >= 2:
            # Last valid close before today
            for v in reversed(closes[:-1]):
                if v is not None:
                    prev = v
                    break
        if prev is None:
            prev = meta.get('chartPreviousClose')
        if close is None or prev is None:
            return None
        chg = close - prev
        pct = (chg / prev * 100) if prev else 0.0
        return {
            'symbol': sym, 'name': display, 'category': cat,
            'close': close, 'change': chg, 'pct': pct,
        }
    except Exception:
        return None


def fetch_all() -> dict:
    """Returns {category: [snapshot...]} with None entries filtered."""
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(fetch_one, s, n, c) for s, n, c in SYMBOLS]
        for f in futs:
            r = f.result()
            if r is None:
                continue
            results.setdefault(r['category'], []).append(r)
    return results


def fmt_snapshot(s: dict) -> str:
    """Format one snapshot as 1-line Slack mrkdwn."""
    pct = s['pct']
    arrow = '🟢' if pct > 0.1 else '🔴' if pct < -0.1 else '⚪'
    close_fmt = f'{s["close"]:,.2f}' if s['close'] < 10000 else f'{s["close"]:,.0f}'
    return f'{arrow} *{s["name"]}* `{close_fmt}` ({pct:+.2f}%)'


CATEGORY_LABELS = {
    'US': '🇺🇸 米国株',
    'JP': '🇯🇵 日本株',
    'EU': '🇪🇺 欧州株',
    'ASIA': '🌏 アジア株',
    'FX': '💱 FX',
    'COM': '🛢️ 商品',
    'YIELD': '📊 金利',
}

CATEGORY_ORDER = ['US', 'JP', 'EU', 'ASIA', 'FX', 'COM', 'YIELD']


def build_market_blocks(title_prefix: str = '📈 市場概観') -> list:
    """Build a list of Slack Block Kit items for the full market snapshot."""
    from slack_push import header, section, divider

    data = fetch_all()
    blocks = []
    for cat in CATEGORY_ORDER:
        items = data.get(cat, [])
        if not items:
            continue
        label = CATEGORY_LABELS[cat]
        lines = [fmt_snapshot(s) for s in items]
        blocks.append(section(f'*{label}*\n' + '\n'.join(lines)))
    return blocks


if __name__ == '__main__':
    data = fetch_all()
    for cat in CATEGORY_ORDER:
        items = data.get(cat, [])
        if not items:
            continue
        print(f'=== {CATEGORY_LABELS[cat]} ===')
        for s in items:
            print(fmt_snapshot(s))
        print()
