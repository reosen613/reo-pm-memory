#!/usr/bin/env python3
"""Reads latest Buy-side Morning Brief from briefs/buyside/ and pushes to Slack #morning-brief.

Mobile-optimized summary: watched names + catalysts + macro + today's calendar.
If brief is older than 24h, warns about stale data.
Env: SLACK_WEBHOOK_URL (= secret SLACK_WEBHOOK_MORNING at workflow level)
"""
import os
import re
import json
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from slack_push import send_slack_blocks, header, section, divider, context

JST = timezone(timedelta(hours=9))
SLACK_MAX_CHARS = 3500


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


def build_takeaway(sections: dict, content: str) -> str:
    """Extract 1-3 bullet takeaway from the brief's own highlighted content."""
    lines = []

    # 1. Flagged items (brief's own highlight marker)
    flagged = re.findall(r'\*\*Flagged[:：]?\s*(.+?)\*\*', content)
    for f in flagged[:2]:
        txt = re.sub(r'\s+', ' ', f).strip()[:180]
        lines.append(f'🚩 {txt}')

    # 2. Watched Names with strong implications (short/long thesis change)
    wn = next((v for k, v in sections.items() if 'Watched Names' in k or '銘柄' in k), '')
    if wn:
        for ln in wn.split('\n'):
            if 'SHORT' in ln and ('challenge' in ln.lower() or '棄損' in ln or '崩壊' in ln or '弱' in ln):
                m = re.search(r'(\d{4})\s*(?:\|)?\s*([^\|]+?)\s*\|.*?\|\s*(.+?)(?:\||$)', ln)
                if m:
                    lines.append(f'⚠️ Short thesis: {m.group(1)} {m.group(2).strip()[:30]} — {m.group(3).strip()[:100]}')
                    break
            if 'LONG' in ln and ('challenge' in ln.lower() or 'headwind' in ln.lower() or '棄損' in ln):
                m = re.search(r'(\d{4})\s*(?:\|)?\s*([^\|]+?)\s*\|.*?\|\s*(.+?)(?:\||$)', ln)
                if m:
                    lines.append(f'⚠️ Long headwind: {m.group(1)} {m.group(2).strip()[:30]} — {m.group(3).strip()[:100]}')
                    break

    # 3. US overnight dominant driver (first sentence of key drivers)
    us = next((v for k, v in sections.items() if 'Overnight' in k or 'US Close' in k), '')
    if us:
        drivers = re.search(r'\*\*Key drivers:\*\*\s*(.+?)(?:[。.]|\n)', us, re.DOTALL)
        if drivers and not lines:  # only add if we have nothing else
            lines.append(f'📰 US: {re.sub(r"\s+", " ", drivers.group(1)).strip()[:150]}')

    if not lines:
        return '本日の brief は routine 内容。 Watched Names section を各自 scan 推奨。'
    return '\n'.join(f'• {l}' for l in lines[:3])


def build_blocks(brief_date: str, content: str, stale_days: int) -> list:
    sections = extract_sections(content)
    blocks = []

    title = f'🌅 Morning Brief — {brief_date}'
    if stale_days > 1:
        title += f' ⚠️ {stale_days}日前'
    blocks.append(header(title))

    # Takeaway at top
    takeaway = build_takeaway(sections, content)
    blocks.append(section(f'💡 *Today\'s Takeaway*\n{takeaway}'))

    # Overnight US
    us = next((v for k, v in sections.items() if 'Overnight' in k or 'US Close' in k), '')
    if us:
        drivers = re.search(r'\*\*Key drivers:\*\*\s*(.+?)(?:\n\n|\*\*Flagged|$)', us, re.DOTALL)
        if drivers:
            txt = re.sub(r'\s+', ' ', drivers.group(1).strip())[:600]
            blocks.append(divider())
            blocks.append(section(f'*🌙 Overnight US*\n{txt}'))

    # Japan Pre-Market
    jp = next((v for k, v in sections.items() if 'Japan Pre-Market' in k or ('Japan' in k and 'Signal' in k)), '')
    if jp:
        bullets = re.findall(r'^-\s+(.+)$', jp, re.MULTILINE)[:3]
        if bullets:
            body = '\n'.join(f'• {b.strip()[:200]}' for b in bullets)
            blocks.append(divider())
            blocks.append(section(f'*🇯🇵 Japan Pre-Market*\n{body}'))

    # Watched Names
    wn = next((v for k, v in sections.items() if 'Watched Names' in k or '銘柄' in k), '')
    if wn:
        rows = extract_rows_from_table(wn)
        if rows:
            blocks.append(divider())
            blocks.append(section('*📌 注目銘柄*'))
            for r in rows[:4]:
                cols = [c.strip() for c in r.strip('|').split('|')]
                if len(cols) >= 5:
                    ticker, name, headline, _, implication = cols[0], cols[1], cols[2], cols[3], cols[4]
                    body = f'*{ticker} {name}*\n{headline[:150]}'
                    if implication:
                        body += f'\n→ _{implication[:120]}_'
                    blocks.append(section(body))

    # Today's Calendar
    cal = next((v for k, v in sections.items() if 'Calendar' in k or '予定' in k), '')
    if cal:
        rows = extract_rows_from_table(cal)
        if rows:
            cal_lines = []
            for r in rows[:3]:
                cols = [c.strip() for c in r.strip('|').split('|')]
                if len(cols) >= 2:
                    cal_lines.append(f'• *{cols[0]}* — {cols[1][:120]}')
            if cal_lines:
                blocks.append(divider())
                blocks.append(section('*📅 Today Calendar*\n' + '\n'.join(cal_lines)))

    # EDINET
    ed = next((v for k, v in sections.items() if 'EDINET' in k or 'Activist' in k), '')
    if ed:
        first_line = next((l for l in ed.split('\n') if l.strip() and not l.startswith('#')), '')
        if first_line:
            blocks.append(divider())
            blocks.append(section(f'*🔍 EDINET*\n{first_line.strip()[:250]}'))

    blocks.append(divider())
    blocks.append(context([f'<https://github.com/reosen613/reo-pm-memory/blob/master/briefs/buyside/morning-{brief_date}.md|Full brief on GitHub>']))

    return blocks


def send_slack(message: str) -> int:
    url = os.environ.get('SLACK_WEBHOOK_URL')
    if not url:
        print('ERROR: SLACK_WEBHOOK_URL env missing')
        sys.exit(1)
    req = urllib.request.Request(
        url,
        data=json.dumps({'text': message, 'mrkdwn': True}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


def main():
    now_jst = datetime.now(JST)
    latest = find_latest_morning_brief()

    if not latest:
        msg = (
            f'🌅 Morning Brief ({now_jst.strftime("%m/%d")})\n\n'
            f'⚠️ briefs/buyside/ に morning-*.md が見つかりません。\n'
            f'cronが停止している可能性。'
        )
        send_slack(msg)
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
    blocks = build_blocks(brief_date_str, content, stale_days)

    status = send_slack_blocks(blocks, fallback_text=f'🌅 Morning Brief {brief_date_str}')
    print(f'Sent (status {status}, {len(blocks)} blocks)')


if __name__ == '__main__':
    main()
