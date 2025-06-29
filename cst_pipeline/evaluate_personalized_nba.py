import pandas as pd
from cst_pipeline.engine.nba_rules import decide_nba_action
from datetime import datetime, timezone
import os

from cst_pipeline.engine.generate_mbti_message import generate_mbti_message

# Paths
DATA_DIR = os.path.join("cst_pipeline", "data", "processed")
OUTPUT_PATH = os.path.join("cst_pipeline", "output", "mbti_comparison_eval.csv")

# Load conversation and MBTI data
conv_df = pd.read_csv(os.path.join(DATA_DIR, "conversation_analysis.csv"))
mbti_df = pd.read_csv(os.path.join(DATA_DIR, "cst_mbti_tags.csv"))

# Merge MBTI tags
conv_df = conv_df.merge(mbti_df, on="author_id", how="left")
conv_df["predicted_mbti"] = conv_df["predicted_mbti"].fillna("")

# Convert date
conv_df['created_at'] = pd.to_datetime(conv_df['created_at'], utc=True)
now = datetime.now(timezone.utc)
conv_df['minutes_since_last_reply'] = (now - conv_df['created_at']).dt.total_seconds() / 60
urgency_cutoff = conv_df['minutes_since_last_reply'].quantile(0.75)

# Sample 10–20 users for evaluation
sample_df = conv_df.sample(n=15, random_state=42)

results = []

for _, row in sample_df.iterrows():
    row_dict = row.to_dict()

    # Run base NBA (no MBTI personalization)
    nba_base = decide_nba_action(row_dict, urgency_cutoff)
    base_message = nba_base["message"]

    # Run MBTI-personalized NBA (hook in generate_mbti_message)
    if row_dict.get("predicted_mbti"):
        personalized_msg = generate_mbti_message(row_dict["predicted_mbti"], row_dict)
    else:
        personalized_msg = base_message

    results.append({
        "customer_id": row_dict["author_id"],
        "mbti_type": row_dict.get("predicted_mbti", ""),
        "channel": nba_base["channel"],
        "baseline_message": base_message,
        "personalized_message": personalized_msg,
        "reasoning": nba_base["reasoning"]
    })

# Save comparison output
result_df = pd.DataFrame(results)
result_df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved MBTI comparison output to: {OUTPUT_PATH}")
