#!/usr/bin/env python3
"""LINE reminder sender. Fires on GitHub Actions cron.
Reads data/reminders.yaml, matches current JST hour, sends matched message.
"""
import os, sys, json, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
import yaml

JST = timezone(timedelta(hours=9))


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
    key = now_jst.strftime('%Y-%m-%d %H:00')
    print(f'Current JST: {now_jst.isoformat()} / match key: {key}')

    data_path = Path(__file__).parent.parent / 'data' / 'reminders.yaml'
    with data_path.open('r', encoding='utf-8') as f:
        reminders = yaml.safe_load(f) or []

    sent = 0
    for r in reminders:
        if r.get('when') == key:
            print(f'→ sending: {r.get("title", "")}')
            try:
                status = send_line(token, user_id, r['message'])
                print(f'  LINE status: {status}')
                sent += 1
            except urllib.error.HTTPError as e:
                print(f'  HTTPError: {e.code} {e.read().decode()}')
            except Exception as e:
                print(f'  Error: {e}')

    if sent == 0:
        print(f'No reminders matched for {key}')


if __name__ == '__main__':
    main()
