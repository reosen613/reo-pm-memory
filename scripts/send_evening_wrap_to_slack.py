#!/usr/bin/env python3
"""Reads latest Evening Market Wrap from briefs/buyside/ and pushes to Slack #evening-wrap.

Env: SLACK_WEBHOOK_URL (= secret SLACK_WEBHOOK_EVENING at workflow level)
"""
import os
import re
import json
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
SLACK_MAX_CHARS = 3500


def find_latest():
    briefs_dir = Path(__file__).parent.parent / 'briefs' / 'buyside'
    files = sorted(briefs_dir.glob('evening-*.md'), reverse=True)
    return files[0] if files else None


def extract_sections(content: str) -> dict:
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


def extract_rows(block: str) -> list[str]:
    rows = []
    for ln in block.split('\n'):
        if ln.strip().startswith('|') and ln.count('|') >= 3 and '---' not in ln:
            rows.append(ln.strip())
    return rows[1:] if len(rows) >= 2 else []


def summarize(brief_date: str, content: str, stale_days: int) -> str:
    sections = extract_sections(content)
    lines = []

    header = f'🌆 Evening Wrap {brief_date}'
    if stale_days > 1:
        header += f' ⚠️{stale_days}日前'
    lines.append('━' * 14)
    lines.append(header)
    lines.append('━' * 14)
    lines.append('')

    # Japan Session Close
    jp = next((v for k, v in sections.items() if 'Japan Session' in k or 'Close' in k), '')
    if jp:
        lines.append('【Japan Close】')
        rows = extract_rows(jp)
        for r in rows[:4]:
            lines.append(r)
        drivers = re.search(r'\*\*Key drivers:\*\*(.+?)(?:\n\n|\*\*Top|$)', jp, re.DOTALL)
        if drivers:
            bullets = re.findall(r'^-\s+(.+)$', drivers.group(1), re.MULTILINE)
            for b in bullets[:3]:
                b = re.sub(r'\s+', ' ', b)[:180]
                lines.append(f'• {b}')
        lines.append('')

    # Top gainers/decliners
    gain = next((v for k, v in sections.items() if 'Gainer' in k or 'Decliner' in k or '上昇' in k or '下落' in k), '')
    if not gain:
        # Try to extract from main sections even if not labeled
        for key, val in sections.items():
            if 'Gainer' in val or 'Decliner' in val or '上位' in val:
                gain = val
                break
    if gain:
        # Simple approach: scan for Top 5 Gainers/Decliners in content
        for section_key, section_val in sections.items():
            if 'Top 5 Gainer' in section_val or 'Top 5 Decliner' in section_val:
                for match in re.finditer(r'\*\*Top 5 (Gainers|Decliners).+?\*\*(.+?)(?=\*\*Top 5|\Z)', section_val, re.DOTALL):
                    kind = match.group(1)
                    rows = extract_rows(match.group(2))[:5]
                    if rows:
                        lines.append(f'【Top 5 {kind}】')
                        for r in rows:
                            cols = [c.strip() for c in r.strip('|').split('|')]
                            if len(cols) >= 3:
                                lines.append(f'{cols[0]}. {cols[1]} {cols[2]}')
                        lines.append('')

    # Section 2+ (positions, catalysts, next day prep)
    for key in list(sections.keys())[1:4]:
        content_val = sections[key]
        if content_val.strip():
            lines.append(f'【{key[:40]}】')
            bullets = re.findall(r'^-\s+(.+)$', content_val, re.MULTILINE)[:3]
            for b in bullets:
                b = re.sub(r'\s+', ' ', b)[:150]
                lines.append(f'• {b}')
            if not bullets:
                para = content_val.split('\n\n')[0].strip()[:300]
                para = re.sub(r'\s+', ' ', para)
                if para:
                    lines.append(para)
            lines.append('')

    lines.append('━' * 14)
    lines.append(f'Full: github.com/reosen613/reo-pm-memory/blob/master/briefs/buyside/evening-{brief_date}.md')

    msg = '\n'.join(lines)
    if len(msg) > SLACK_MAX_CHARS:
        msg = msg[:SLACK_MAX_CHARS - 20] + '\n...(truncated)'
    return msg


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
    latest = find_latest()

    if not latest:
        msg = f'🌆 Evening Wrap ({now_jst.strftime("%m/%d")})\n\n⚠️ briefs/buyside/ に evening-*.md が見つかりません。'
        send_slack(msg)
        return

    m = re.match(r'evening-(\d{4}-\d{2}-\d{2})\.md', latest.name)
    if not m:
        print('ERROR: cannot parse date')
        return
    brief_date_str = m.group(1)
    brief_date = datetime.strptime(brief_date_str, '%Y-%m-%d').replace(tzinfo=JST)
    stale_days = (now_jst.date() - brief_date.date()).days

    content = latest.read_text(encoding='utf-8')
    msg = summarize(brief_date_str, content, stale_days)

    status = send_slack(msg)
    try:
        print(f'Sent (status {status}, {len(msg)} chars):\n{msg}')
    except UnicodeEncodeError:
        print(f'Sent (status {status}, {len(msg)} chars)')


if __name__ == '__main__':
    main()
