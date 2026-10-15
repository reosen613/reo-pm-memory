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
    # Yields (US Treasuries)
    ('^IRX',   '米3M (短期)',      'YIELD'),
    ('^FVX',   '米5年',            'YIELD'),
    ('^TNX',   '米10年',           'YIELD'),
    ('^TYX',   '米30年',           'YIELD'),
    # 日本10年国債 yield は Yahoo API 対応なし → _append_jgb_note() で別途notice
]


def _sparkline(values: list[float]) -> str:
    """Convert list of values to 8-char unicode sparkline."""
    chars = '▁▂▃▄▅▆▇█'
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return '      '  # 6 spaces
    lo, hi = min(vals), max(vals)
    rng = hi - lo
    if rng == 0:
        return chars[3] * len(vals)
    out = []
    for v in values:
        if v is None:
            out.append(' ')
        else:
            idx = int((v - lo) / rng * (len(chars) - 1))
            out.append(chars[idx])
    return ''.join(out)


def fetch_one(sym: str, display: str, cat: str) -> dict | None:
    # 30d range for better sparkline trend context
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1mo'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.load(r)
        result = data.get('chart', {}).get('result', [{}])[0]
        meta = result.get('meta', {})
        close = meta.get('regularMarketPrice')
        # Use actual previous day close from the series (not chartPreviousClose which can be 5-day lookback)
        closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])
        prev = None
        if len(closes) >= 2:
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
        # Sparkline from last ~20 valid closes
        valid_closes = [c for c in closes if c is not None][-20:]
        spark = _sparkline(valid_closes) if len(valid_closes) >= 5 else ''
        # 1-month change for context
        pct_1mo = None
        if len(valid_closes) >= 2:
            pct_1mo = (valid_closes[-1] - valid_closes[0]) / valid_closes[0] * 100
        return {
            'symbol': sym, 'name': display, 'category': cat,
            'close': close, 'change': chg, 'pct': pct,
            'spark': spark, 'pct_1mo': pct_1mo,
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


def _display_width(s: str) -> int:
    """Approximate display width (CJK chars = 2, others = 1)."""
    w = 0
    for ch in s:
        # Common full-width ranges (CJK, Hiragana, Katakana, full-width punct)
        if (0x3000 <= ord(ch) <= 0x9FFF) or (0xFF00 <= ord(ch) <= 0xFFEF):
            w += 2
        else:
            w += 1
    return w


def _pad(s: str, width: int) -> str:
    """Pad string with spaces to visual width."""
    cur = _display_width(s)
    if cur >= width:
        return s
    return s + ' ' * (width - cur)


def _format_table_block(items: list) -> str:
    """Format category items as aligned monospace table with trend sparkline.
    Format: name (padded) | close (right) | 🟢▲+X.XX% / 🔴▼-X.XX% | sparkline (1mo) | 1mo%
    """
    lines = []
    name_w = max((_display_width(s['name']) for s in items), default=10)
    name_w = max(name_w, 12)

    for s in items:
        pct = s['pct']
        if pct > 0.1:
            marker = '🟢▲'
            sign = '+'
        elif pct < -0.1:
            marker = '🔴▼'
            sign = ''
        else:
            marker = '⚪━'
            sign = '+' if pct >= 0 else ''
        if s['close'] >= 10000:
            close_fmt = f'{s["close"]:>10,.0f}'
        elif s['close'] >= 100:
            close_fmt = f'{s["close"]:>10,.2f}'
        else:
            close_fmt = f'{s["close"]:>10,.3f}'
        pct_fmt = f'{sign}{pct:.2f}%'
        spark = s.get('spark', '')
        pct_1mo = s.get('pct_1mo')
        mo_fmt = f'  1m: {pct_1mo:+5.1f}%' if pct_1mo is not None else ''
        line = f'{_pad(s["name"], name_w)}  {close_fmt}  {marker} {pct_fmt:>8s}  {spark}{mo_fmt}'
        lines.append(line)
    return '\n'.join(lines)


def build_market_blocks(title_prefix: str = '📈 市場概観') -> list:
    """Build Slack Block Kit items: category sections with monospace code block."""
    from slack_push import section

    data = fetch_all()
    blocks = []
    for cat in CATEGORY_ORDER:
        items = data.get(cat, [])
        if not items:
            continue
        label = CATEGORY_LABELS[cat]
        table = _format_table_block(items)
        # Use ```code``` for monospace alignment
        blocks.append(section(f'*{label}*\n```\n{table}\n```'))
    return blocks


def fmt_snapshot(s: dict) -> str:
    """Legacy inline format (kept for test / debug use)."""
    pct = s['pct']
    arrow = '🟢' if pct > 0.1 else '🔴' if pct < -0.1 else '⚪'
    close_fmt = f'{s["close"]:,.2f}' if s['close'] < 10000 else f'{s["close"]:,.0f}'
    return f'{arrow} *{s["name"]}* `{close_fmt}` ({pct:+.2f}%)'


if __name__ == '__main__':
    data = fetch_all()
    for cat in CATEGORY_ORDER:
        items = data.get(cat, [])
        if not items:
            continue
        print(f'=== {CATEGORY_LABELS[cat]} ===')
        print(_format_table_block(items))
        print()
