# nba_rules.py
from datetime import datetime, timedelta, timezone
from .utils import compute_send_time, parse_datetime
from .generate_mbti_message import generate_mbti_message

def decide_nba_action(row, urgency_cutoff):
    customer_id = str(row['author_id'])
    text_clean = str(row.get('text_clean', '')).lower()
    sentiment = str(row.get('dominant_sentiment', '')).lower()
    support_type = str(row.get('request_type', '')).lower()
    ticket_status = str(row.get('ticket_status', '')).lower()
    cluster_label = str(row.get('label', '')).lower()
    created_at_raw = row.get('created_at', '')

    minutes_since = float(row.get("minutes_since_last_reply", 0))

    if ticket_status == 'open':
        if minutes_since > urgency_cutoff:
            channel = 'scheduling_phone_call'  # Escalate old tickets
        elif sentiment == 'negative' and support_type in [
            "complaint", "baggage issue", "flight booking", "technical issue", "account login"
        ]:
            channel = 'scheduling_phone_call'
        elif sentiment == 'positive' and cluster_label == 'unresponsive_user':
            channel = 'email_reply'
        elif 'dm' in text_clean or 'direct message' in text_clean:
            channel = 'twitter_dm_reply'
        else:
            channel = 'email_reply'
    else:
        channel = 'email_reply'



    # Customize message
    if channel == 'scheduling_phone_call':
        message = "Hi, we're sorry you've had trouble reaching us. We've scheduled a callback to assist you personally."
    elif channel == 'twitter_dm_reply':
        message = "Hi, thanks for your message. Please check your DMs for further assistance!"
    else:
        message = "Thanks for reaching out. We're reviewing your request and will get back to you soon via email."

    # Use MBTI-aware message if available
    if row.get("mbti_type"):
        message = generate_mbti_message(row["mbti_type"], message)
    else:
        message = message

    # Reasoning
    reasoning = (
        f"Customer showed {sentiment or 'neutral'} sentiment on a '{support_type or 'general'}' issue. "
        f"Cluster behavior is '{cluster_label or 'unknown'}', so the system selected '{channel}' "
        f"as the optimal channel for resolution."
    )

    try:
        created_at_dt = parse_datetime(created_at_raw)
    except Exception:
        created_at_dt = datetime.now(timezone.utc)
    send_time = compute_send_time(created_at_dt)

    return {
        "customer_id": customer_id,
        "channel": channel,
        "send_time": send_time,
        "message": message,
        "reasoning": reasoning,
        "minutes_since_last_reply": minutes_since,
        "mbti_type": row.get("mbti_type", None),
        "personalized": bool(row.get("mbti_type"))
    }
