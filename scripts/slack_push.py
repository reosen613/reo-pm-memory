"""Shared Slack push helper. Posts to the Slack Incoming Webhook URL
specified by env SLACK_WEBHOOK_URL. Supports both plain text (send_slack)
and Block Kit (send_slack_blocks) formats.
"""
import os
import sys
import json
import urllib.request


def _post(payload: dict, webhook_url: str | None = None) -> int:
    url = webhook_url or os.environ.get('SLACK_WEBHOOK_URL')
    if not url:
        print('ERROR: SLACK_WEBHOOK_URL not set', file=sys.stderr)
        sys.exit(1)
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


def send_slack(text: str, webhook_url: str | None = None) -> int:
    return _post({'text': text, 'mrkdwn': True}, webhook_url)


def send_slack_blocks(blocks: list, fallback_text: str = '', webhook_url: str | None = None) -> int:
    payload = {'blocks': blocks}
    if fallback_text:
        payload['text'] = fallback_text  # notification preview
    return _post(payload, webhook_url)


import re as _re


def mdfix(text: str) -> str:
    """Convert GitHub/standard markdown to Slack mrkdwn:
    - **bold** → *bold*
    - 2+ consecutive markdown table rows → wrapped in ``` code block (aligned columns)
    - single table rows → `cells joined with " | "`
    - skip --- separator rows
    """
    if not text:
        return text
    # ** → * (Slack bold)
    text = _re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)

    lines = text.split('\n')
    # First pass: parse table rows into cell arrays
    def _is_table_row(ln: str) -> bool:
        s = ln.strip()
        return s.startswith('|') and s.count('|') >= 2 and '---' not in s

    # Collect consecutive table-row runs
    out = []
    i = 0
    while i < len(lines):
        if _is_table_row(lines[i]):
            run = []
            while i < len(lines) and (_is_table_row(lines[i]) or '---' in lines[i]):
                if '---' not in lines[i]:
                    cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                    cells = [c for c in cells if c]
                    if cells:
                        run.append(cells)
                i += 1
            if len(run) >= 2:
                # Wrap in code block with aligned columns
                n_cols = max(len(r) for r in run)
                # Normalize: pad shorter rows
                for r in run:
                    while len(r) < n_cols:
                        r.append('')
                # Column widths
                col_w = [max(len(r[c]) for r in run) for c in range(n_cols)]
                aligned = ['  '.join(r[c].ljust(col_w[c]) for c in range(n_cols)) for r in run]
                out.append('```\n' + '\n'.join(aligned) + '\n```')
            elif len(run) == 1:
                out.append(' | '.join(run[0]))
        else:
            out.append(lines[i])
            i += 1
    return '\n'.join(out)


# Block builders (shorthand)
def header(text: str) -> dict:
    return {'type': 'header', 'text': {'type': 'plain_text', 'text': text[:150], 'emoji': True}}


def section(text: str) -> dict:
    return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': mdfix(text)[:3000]}}


def section_fields(fields: list[str]) -> dict:
    """Each field is a mrkdwn string. Max 10 fields, displayed in 2 cols."""
    return {
        'type': 'section',
        'fields': [{'type': 'mrkdwn', 'text': f[:2000]} for f in fields[:10]],
    }


def divider() -> dict:
    return {'type': 'divider'}


def context(elements: list[str]) -> dict:
    """Small text under a section. Each element is a mrkdwn string."""
    return {
        'type': 'context',
        'elements': [{'type': 'mrkdwn', 'text': e[:150]} for e in elements[:10]],
    }
