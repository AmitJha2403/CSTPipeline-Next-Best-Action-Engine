# DEPRECATED: Logic now exists in nba_rules.py. Do not use this file.

def select_channel(label):
    if label == "quick_positive_resolution":
        return None
    elif label == "unresponsive_user":
        return "twitter_dm_reply"
    elif label in ["frustrated_escalation", "long_negative_thread"]:
        return "scheduling_phone_call"
    elif label == "high_effort_positive":
        return "email_reply"
    else:
        return "email_reply"
