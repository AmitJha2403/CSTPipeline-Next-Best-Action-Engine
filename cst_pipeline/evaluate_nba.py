# evaluate_nba.py
import pandas as pd
import json
import os
from datetime import datetime
from collections import defaultdict
import random

# Load NBA results from existing output
nba_output_path = os.path.join("cst_pipeline","output", "nba_output.json")
with open(nba_output_path, "r") as f:
    nba_results = json.load(f)

print(f"Loaded {len(nba_results)} NBA results")

# Load conversation data to generate chat logs
conv_df = pd.read_csv(os.path.join("cst_pipeline", "data", "processed", "conversation_analysis.csv"), parse_dates=["created_at"])

# Filter to top 1000 customers
top_n = 1000
filtered_results = random.sample(nba_results, min(top_n, len(nba_results)))

# Build mapping for tweet -> author and messages
chat_logs = defaultdict(list)
for _, row in conv_df.iterrows():
    convo_id = row["conversation_id"]
    sender = "Customer" if row["inbound"] else "Support_agent"
    text = row["text"]
    chat_logs[convo_id].append((row["created_at"], sender, text))

# Helper: generate plain-text chat log
def format_chat_log(chat_data):
    chat_data = sorted(chat_data, key=lambda x: x[0])  # Sort by timestamp
    return "\n".join([f"{sender}: {text}" for _, sender, text in chat_data])

# Define logic to assign issue_status
def predict_issue_status(channel):
    if channel == "email_reply":
        return "resolved"
    elif channel == "scheduling_phone_call":
        return "escalated"
    elif channel == "twitter_dm_reply":
        return "pending_customer_response"
    return "pending_customer_response"

# Assemble final dataframe
rows = []
for entry in filtered_results:
    convo_id = entry["conversation_id"]
    row = {
        "customer_id": entry.get("customer_id") or entry.get("author_id"),
        "chat_log": format_chat_log(chat_logs[convo_id]),
        "channel": entry["channel"],
        "message": entry["message"],
        "send_time": entry["send_time"],
        "reasoning": entry["reasoning"],
        "issue_status": predict_issue_status(entry["channel"])
    }
    rows.append(row)

result_df = pd.DataFrame(rows)

# Save as CSV in output folder
output_csv_path = os.path.join("cst_pipeline","output", "nba_result_eval.csv")
result_df.to_csv(output_csv_path, index=False)
print(f"Evaluation CSV saved at: {output_csv_path}")
