"""Shared Slack push helper. Posts a text message to the Slack Incoming Webhook URL
specified by the environment variable SLACK_WEBHOOK_URL.
"""
import os
import sys
import json
import urllib.request


def send_slack(text: str, webhook_url: str | None = None) -> int:
    url = webhook_url or os.environ.get('SLACK_WEBHOOK_URL')
    if not url:
        print('ERROR: SLACK_WEBHOOK_URL not set', file=sys.stderr)
        sys.exit(1)
    payload = {'text': text, 'mrkdwn': True}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status
