#!/usr/bin/env python3
"""Reads latest Buy-side Morning Brief from briefs/buyside/ and pushes to LINE.

Mobile-optimized summary: watched names + catalysts + macro + today's calendar.
If brief is older than 24h, warns about stale data.
"""
import os
import re
import json
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
LINE_MAX_CHARS = 4800


def find_latest_morning_brief():
    """Find the most recent briefs/buyside/morning-*.md file."""
    briefs_dir = Path(__file__).parent.parent / 'briefs' / 'buyside'
    files = sorted(briefs_dir.glob('morning-*.md'), reverse=True)
    return files[0] if files else None


def extract_sections(content: str) -> dict:
    """Parse markdown brief into named sections."""
    sections = {}
    current = None
    buf = []
    for line in content.split('\n'):
        m = re.match(r'^## \d+\.\s+(.+?)$', line)
        if m:
            if current:
                sections[current] = '\n'.join(buf).strip()
            current = m.group(1).strip()
            buf = []
        elif current:
            buf.append(line)
    if current:
        sections[current] = '\n'.join(buf).strip()
    return sections


def extract_rows_from_table(block: str) -> list[str]:
    """Pull data rows from a markdown table (skip header + separator)."""
    rows = []
    for ln in block.split('\n'):
        if ln.strip().startswith('|') and ln.count('|') >= 3 and '---' not in ln:
            rows.append(ln.strip())
    return rows[1:] if len(rows) >= 2 else []


def summarize_for_line(brief_date: str, content: str, stale_days: int) -> str:
    sections = extract_sections(content)
    lines = []

    header = f'🌅 Morning Brief {brief_date}'
    if stale_days > 1:
        header += f' ⚠️{stale_days}日前'
    lines.append('━' * 14)
    lines.append(header)
    lines.append('━' * 14)
    lines.append('')

    # Overnight US (top line + key drivers 1-2 sentences)
    us = sections.get('Overnight US Close (Mon Jun 22)') or next(
        (v for k, v in sections.items() if 'Overnight' in k or 'US Close' in k), ''
    )
    if us:
        lines.append('【Overnight US】')
        drivers = re.search(r'\*\*Key drivers:\*\*\s*(.+?)(?:\n\n|\*\*Flagged|$)', us, re.DOTALL)
        if drivers:
            txt = drivers.group(1).strip()
            txt = re.sub(r'\s+', ' ', txt)[:400]
            lines.append(txt)
        else:
            table_rows = extract_rows_from_table(us)[:3]
            for r in table_rows:
                lines.append(r)
        lines.append('')

    # Japan Pre-Market
    jp = next((v for k, v in sections.items() if 'Japan Pre-Market' in k or 'Japan' in k and 'Signals' in k), '')
    if jp:
        lines.append('【Japan Pre-Market】')
        bullets = re.findall(r'^-\s+(.+)$', jp, re.MULTILINE)
        for b in bullets[:3]:
            lines.append(f'• {b.strip()[:150]}')
        lines.append('')

    # Watched Names (most actionable section)
    wn = next((v for k, v in sections.items() if 'Watched Names' in k or '銘柄' in k), '')
    if wn:
        lines.append('【注目銘柄】')
        rows = extract_rows_from_table(wn)
        for r in rows[:4]:
            cols = [c.strip() for c in r.strip('|').split('|')]
            if len(cols) >= 5:
                ticker, name, headline, _, implication = cols[0], cols[1], cols[2], cols[3], cols[4]
                lines.append(f'▸ {ticker} {name}')
                lines.append(f'  {headline[:120]}')
                if implication:
                    lines.append(f'  → {implication[:100]}')
        lines.append('')

    # Today's Calendar
    cal = next((v for k, v in sections.items() if 'Calendar' in k or '予定' in k), '')
    if cal:
        lines.append('【Today Calendar】')
        rows = extract_rows_from_table(cal)
        for r in rows[:3]:
            cols = [c.strip() for c in r.strip('|').split('|')]
            if len(cols) >= 2:
                lines.append(f'• {cols[0]}: {cols[1][:100]}')
        lines.append('')

    # EDINET / Activist Filings (brief)
    ed = next((v for k, v in sections.items() if 'EDINET' in k or 'Activist' in k), '')
    if ed:
        first_line = next((l for l in ed.split('\n') if l.strip() and not l.startswith('#')), '')
        if first_line:
            lines.append('【EDINET】')
            lines.append(first_line.strip()[:200])
            lines.append('')

    lines.append('━' * 14)
    lines.append(f'Full: github.com/reosen613/reo-pm-memory/blob/master/briefs/buyside/morning-{brief_date}.md')

    msg = '\n'.join(lines)
    if len(msg) > LINE_MAX_CHARS:
        msg = msg[:LINE_MAX_CHARS - 20] + '\n...(truncated)'
    return msg


def send_line(token: str, user_id: str, message: str) -> int:
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
    latest = find_latest_morning_brief()

    if not latest:
        msg = (
            f'🌅 Morning Brief ({now_jst.strftime("%m/%d")})\n\n'
            f'⚠️ briefs/buyside/ に morning-*.md が見つかりません。\n'
            f'cronが停止している可能性。'
        )
        send_line(token, user_id, msg)
        return

    # Parse brief date from filename
    m = re.match(r'morning-(\d{4}-\d{2}-\d{2})\.md', latest.name)
    if not m:
        print('ERROR: cannot parse brief date from', latest.name)
        return
    brief_date_str = m.group(1)
    brief_date = datetime.strptime(brief_date_str, '%Y-%m-%d').replace(tzinfo=JST)
    stale_days = (now_jst.date() - brief_date.date()).days

    content = latest.read_text(encoding='utf-8')
    msg = summarize_for_line(brief_date_str, content, stale_days)

    status = send_line(token, user_id, msg)
    try:
        print(f'Sent (status {status}, {len(msg)} chars):\n{msg}')
    except UnicodeEncodeError:
        print(f'Sent (status {status}, {len(msg)} chars): [non-ASCII]')


if __name__ == '__main__':
    main()
