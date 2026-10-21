#!/usr/bin/env python3
"""briefs/reosen/morning-YYYY-MM-DD.md（claude.ai のクラウドルーティンが書く Reosen Equity の朝のまとめ）を
Slack #銘柄研究帳 に送る。PC が寝ていても届くようにするための経路。

Env: SLACK_WEBHOOK_URL（= secret SLACK_WEBHOOK_KENKYU。無ければ SLACK_WEBHOOK_MORNING にフォールバック）
"""
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from slack_push import send_slack, mdfix

JST = timezone(timedelta(hours=9))
MAX = 3800


def find_latest():
    d = Path(__file__).parent.parent / 'briefs' / 'reosen'
    files = sorted(d.glob('morning-*.md'), reverse=True) if d.exists() else []
    return files[0] if files else None


def main():
    p = find_latest()
    if not p:
        print('no brief found'); return 0
    date = p.stem.replace('morning-', '')
    today = datetime.now(JST).date().isoformat()
    body = p.read_text(encoding='utf-8').strip()
    if date != today:
        body = f'⚠ このまとめは {date} 分（今日の分がまだ無い）\n\n' + body
    text = '[Claude] ' + mdfix(body)
    if len(text) > MAX:
        text = text[:MAX - 40] + '\n…（続きは GitHub の briefs/reosen/ に）'
    status = send_slack(text)
    print('Sent', status, p.name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
