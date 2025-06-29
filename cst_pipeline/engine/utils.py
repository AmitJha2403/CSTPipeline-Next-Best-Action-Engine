# utils.py
from datetime import datetime, timedelta

def compute_send_time(created_at):
    if created_at.hour < 16:
        return (created_at + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        next_day = created_at + timedelta(days=1)
        return next_day.replace(hour=10, minute=0, second=0).strftime('%Y-%m-%dT%H:%M:%SZ')

def parse_datetime(dt_str):
    return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
