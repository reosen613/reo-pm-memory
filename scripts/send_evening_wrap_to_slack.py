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

sys.path.insert(0, str(Path(__file__).parent))
from slack_push import send_slack_blocks, header, section, divider, context

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


def _build_evening_takeaway(content: str) -> str:
    """Extract key drivers + themes from evening wrap."""
    lines = []

    # 1. First bullet of Key drivers
    drivers_match = re.search(r'\*\*Key drivers:\*\*(.+?)(?:\n\n|\*\*Top)', content, re.DOTALL)
    if drivers_match:
        first_bullet = re.search(r'^-\s+(.+?)$', drivers_match.group(1), re.MULTILINE)
        if first_bullet:
            txt = re.sub(r'\s+', ' ', first_bullet.group(1))[:200]
            txt = re.sub(r'\*\*', '', txt)  # strip markdown bold
            lines.append(f'📰 {txt}')

    # 2. Index Nikkei change
    nikkei_match = re.search(r'Nikkei\s*225\s*\|\s*([\d,]+(?:\.\d+)?)\s*\|\s*([−\-+][\d,.]+)\s*\|\s*\*?\*?([−\-+]\d+\.\d+%)', content)
    if nikkei_match:
        lines.append(f'📈 Nikkei {nikkei_match.group(1)} ({nikkei_match.group(3)})')

    # 3. Top decliner (first entry)
    decliner_section = re.search(r'\*\*Top 5 Decliner.+?\*\*(.+?)(?:\*\*|\n\n)', content, re.DOTALL)
    if decliner_section:
        rows = [l for l in decliner_section.group(1).split('\n') if l.strip().startswith('|') and '---' not in l]
        if len(rows) >= 2:
            cols = [c.strip() for c in rows[1].strip('|').split('|')]
            if len(cols) >= 4:
                lines.append(f'📉 Top decliner: {cols[1]} ({cols[2]}) — {cols[3][:100]}')

    if not lines:
        return 'routine market close。 詳細セクション scan 推奨。'
    return '\n'.join(f'• {l}' for l in lines[:3])


def _wrap_as_blocks(brief_date: str, stale_days: int, text_msg: str, content: str) -> list:
    """Wrap plain-text summary into Block Kit for Slack rich display."""
    title = f'🌆 Evening Wrap — {brief_date}'
    if stale_days > 1:
        title += f' ⚠️ {stale_days}日前'
    # Strip existing separator lines from text_msg
    body = re.sub(r'━+\n', '', text_msg)
    # Remove the first line (the title header duplicated)
    body_lines = [l for l in body.split('\n') if l.strip() and not l.startswith('🌆')]
    sections_split = re.split(r'(【[^】]+】)', '\n'.join(body_lines))
    blocks = [header(title)]
    # Takeaway at top
    takeaway = _build_evening_takeaway(content)
    blocks.append(section(f'💡 *Today\'s Takeaway*\n{takeaway}'))
    buf = ''
    for part in sections_split:
        if part.startswith('【'):
            if buf.strip():
                blocks.append(section(buf.strip()[:2900]))
            blocks.append(divider())
            buf = f'*{part}*\n'
        else:
            buf += part
    if buf.strip():
        blocks.append(section(buf.strip()[:2900]))
    blocks.append(divider())
    blocks.append(context([f'<https://github.com/reosen613/reo-pm-memory/blob/master/briefs/buyside/evening-{brief_date}.md|Full brief on GitHub>']))
    return blocks


def main():
    now_jst = datetime.now(JST)
    latest = find_latest()

    if not latest:
        send_slack_blocks([
            header(f'🌆 Evening Wrap — {now_jst.strftime("%m/%d")}'),
            section('⚠️ briefs/buyside/ に evening-*.md が見つかりません。'),
        ], fallback_text='Evening Wrap missing')
        return

    m = re.match(r'evening-(\d{4}-\d{2}-\d{2})\.md', latest.name)
    if not m:
        print('ERROR: cannot parse date')
        return
    brief_date_str = m.group(1)
    brief_date = datetime.strptime(brief_date_str, '%Y-%m-%d').replace(tzinfo=JST)
    stale_days = (now_jst.date() - brief_date.date()).days

    content = latest.read_text(encoding='utf-8')
    text_msg = summarize(brief_date_str, content, stale_days)
    blocks = _wrap_as_blocks(brief_date_str, stale_days, text_msg, content)

    status = send_slack_blocks(blocks, fallback_text=f'🌆 Evening Wrap {brief_date_str}')
    print(f'Sent (status {status}, {len(blocks)} blocks)')


if __name__ == '__main__':
    main()
