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


# Block builders (shorthand)
def header(text: str) -> dict:
    return {'type': 'header', 'text': {'type': 'plain_text', 'text': text[:150], 'emoji': True}}


def section(text: str) -> dict:
    return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text[:3000]}}


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
