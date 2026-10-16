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

sys.path.insert(0, str(Path(__file__).parent))
from slack_push import send_slack_blocks, header, section, divider, context

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


def _build_weekly_takeaway(content: str) -> str:
    """Extract HIGH risk, blockers, and top action from PM/pipeline brief."""
    lines = []

    # 1. First HIGH risk item (buyside pipeline format)
    high = re.search(r'(?:🔴|HIGH|高)\s*(?:Stuck|停滞)?.+?\|\s*([^|]+?)\s*\|', content[:3000])
    if high:
        lines.append(f'🔴 HIGH risk: {high.group(1).strip()[:120]}')

    # 2. ヘッドライン (PM agent format)
    headline_match = re.search(r'##\s*ヘッドライン\s*\n+(.+?)(?:\n\n|##)', content, re.DOTALL)
    if headline_match:
        txt = re.sub(r'\s+', ' ', headline_match.group(1)).strip()[:200]
        if txt and not any(txt in l for l in lines):
            lines.append(f'📌 Headline: {txt}')

    # 3. 今週の必達 - first item
    week_match = re.search(r'(?:今週の必達|Priority)[^\n]*\n+(?:\d+\.|-)\s*(.+?)(?:\n|$)', content)
    if week_match:
        txt = re.sub(r'[\*_]', '', week_match.group(1))[:150]
        lines.append(f'🎯 最優先: {txt.strip()}')

    if not lines:
        return 'ヘッドライン抽出失敗。 詳細は本文 scan 推奨。'
    return '\n'.join(f'• {l}' for l in lines[:3])


def _wrap_as_blocks(brief_date: str, stale_days: int, source: str, text_msg: str, content: str) -> list:
    title = f'📅 Weekly PM — {brief_date}'
    if stale_days > 10:
        title += f' ⚠️ {stale_days}日前'
    body = re.sub(r'━+\n', '', text_msg)
    body_lines = [l for l in body.split('\n') if l.strip() and not l.startswith('📅') and not l.startswith('source:')]
    sections_split = re.split(r'(【[^】]+】)', '\n'.join(body_lines))
    blocks = [header(title)]
    blocks.append(context([f'source: `{source}`']))
    # Takeaway at top
    takeaway = _build_weekly_takeaway(content)
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
    file_path = f'reports/{brief_date}' if source == 'reports/' else f'briefs/buyside/weekly-{brief_date}'
    blocks.append(divider())
    blocks.append(context([f'<https://github.com/reosen613/reo-pm-memory/blob/master/{file_path}.md|Full brief on GitHub>']))
    return blocks


def main():
    now_jst = datetime.now(JST)
    latest = find_latest()

    if not latest:
        send_slack_blocks([
            header(f'📅 Weekly PM — {now_jst.strftime("%m/%d")}'),
            section('⚠️ reports/weekly-*.md または briefs/buyside/weekly-*.md が見つかりません。'),
        ], fallback_text='Weekly PM missing')
        return

    m = re.match(r'weekly-(\d{4}-\d{2}-\d{2})\.md', latest.name)
    if not m:
        print('ERROR: cannot parse date from', latest.name)
        return
    brief_date_str = m.group(1)
    brief_date = datetime.strptime(brief_date_str, '%Y-%m-%d').replace(tzinfo=JST)
    stale_days = (now_jst.date() - brief_date.date()).days

    source = 'reports/' if 'reports' in str(latest) else 'briefs/buyside/'
    if stale_days > 10:
        # 古いレポートを毎回流さない（2026-10-16 Reo: 6/22 のフジクラの話が毎日出ていた）
        send_slack_blocks([
            header(f'📅 Weekly PM — {now_jst.strftime("%m/%d")}'),
            section(f'新しい週次レポートがありません（最新は {brief_date_str}、{stale_days}日前）。週次PMの定期実行が止まっている可能性があるので、Claude アプリの「ルーティン」を確認してください。'),
            context([f'<https://github.com/reosen613/reo-pm-memory/blob/master/{source}weekly-{brief_date_str}.md|最新のレポート>']),
        ], fallback_text=f'Weekly PM: 新しいレポートなし（最新 {brief_date_str}）')
        print(f'stale ({stale_days}d): sent short notice only')
        return
    content = latest.read_text(encoding='utf-8')
    text_msg = summarize(brief_date_str, content, stale_days, source)
    blocks = _wrap_as_blocks(brief_date_str, stale_days, source, text_msg, content)

    status = send_slack_blocks(blocks, fallback_text=f'📅 Weekly PM {brief_date_str}')
    print(f'Sent (status {status}, {len(blocks)} blocks)')


if __name__ == '__main__':
    main()
