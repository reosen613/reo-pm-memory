#!/usr/bin/env python3
"""Reads latest Weekly PM Status Brief from briefs/buyside/ or reports/ and pushes to Slack #weekly-pm.

Prefers reports/ (new PM agent output) over briefs/buyside/weekly-* (older buyside pipeline).
Env: SLACK_WEBHOOK_URL (= secret SLACK_WEBHOOK_WEEKLY at workflow level)
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
    base = Path(__file__).parent.parent
    # 1st choice: reports/weekly-*.md (new PM agent)
    reports = sorted((base / 'reports').glob('weekly-*.md'), reverse=True) if (base / 'reports').exists() else []
    if reports:
        return reports[0]
    # 2nd: buyside pipeline weekly
    buyside = sorted((base / 'briefs' / 'buyside').glob('weekly-*.md'), reverse=True)
    return buyside[0] if buyside else None


def extract_sections(content: str) -> dict:
    sections = {}
    current = None
    buf = []
    for line in content.split('\n'):
        m = re.match(r'^## \d*\.?\s*(.+?)$', line)
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


def summarize(brief_date: str, content: str, stale_days: int, source: str) -> str:
    sections = extract_sections(content)
    lines = []

    header = f'📅 Weekly PM {brief_date}'
    if stale_days > 10:
        header += f' ⚠️{stale_days}日前'
    lines.append('━' * 14)
    lines.append(header)
    lines.append(f'source: {source}')
    lines.append('━' * 14)
    lines.append('')

    # Headline (if PM agent format)
    headline = sections.get('ヘッドライン') or sections.get('Headline') or sections.get('ヘッドライン / Headline', '')
    if headline:
        lines.append('【ヘッドライン】')
        lines.append(headline[:400])
        lines.append('')

    # Pipeline / project status (PM agent OR buyside)
    pipeline = next((v for k, v in sections.items() if 'Pipeline' in k or 'プロジェクト' in k or 'ステータス' in k or 'Status' in k), '')
    if pipeline:
        lines.append('【ステータス】')
        # Try to extract rows
        rows = []
        for ln in pipeline.split('\n'):
            if ln.strip().startswith('|') and ln.count('|') >= 3 and '---' not in ln:
                rows.append(ln.strip())
        for r in rows[1:5]:  # skip header
            cols = [c.strip() for c in r.strip('|').split('|')]
            if len(cols) >= 2:
                lines.append(f'• {cols[0]}: {cols[1][:80]}')
        lines.append('')

    # 今週の必達 / 注意
    for keyword in ['今週', '必達', '注意', '次のアクション', 'Action', '次アクション']:
        for k, v in sections.items():
            if keyword in k:
                lines.append(f'【{k[:30]}】')
                bullets = re.findall(r'^(?:- |\d+\. )(.+)$', v, re.MULTILINE)
                if not bullets:
                    bullets = [b.strip() for b in v.split('\n') if b.strip()][:3]
                for b in bullets[:5]:
                    b = re.sub(r'\s+', ' ', b)[:200]
                    lines.append(f'• {b}')
                lines.append('')
                break
        else:
            continue
        break

    lines.append('━' * 14)
    file_path = f'reports/{brief_date}' if source == 'reports/' else f'briefs/buyside/weekly-{brief_date}'
    lines.append(f'Full: github.com/reosen613/reo-pm-memory/blob/master/{file_path}.md')

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
        msg = f'📅 Weekly PM ({now_jst.strftime("%m/%d")})\n\n⚠️ reports/weekly-*.md または briefs/buyside/weekly-*.md が見つかりません。'
        send_slack(msg)
        return

    m = re.match(r'weekly-(\d{4}-\d{2}-\d{2})\.md', latest.name)
    if not m:
        print('ERROR: cannot parse date from', latest.name)
        return
    brief_date_str = m.group(1)
    brief_date = datetime.strptime(brief_date_str, '%Y-%m-%d').replace(tzinfo=JST)
    stale_days = (now_jst.date() - brief_date.date()).days

    source = 'reports/' if 'reports' in str(latest) else 'briefs/buyside/'
    content = latest.read_text(encoding='utf-8')
    msg = summarize(brief_date_str, content, stale_days, source)

    status = send_slack(msg)
    try:
        print(f'Sent (status {status}, {len(msg)} chars):\n{msg}')
    except UnicodeEncodeError:
        print(f'Sent (status {status}, {len(msg)} chars)')


if __name__ == '__main__':
    main()
