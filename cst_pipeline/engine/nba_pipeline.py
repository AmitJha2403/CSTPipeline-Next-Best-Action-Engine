# nba_pipeline.py
import pandas as pd
from engine.llm_reasoner import get_llm_nba_decision
from engine.nba_rules import decide_nba_action
from datetime import datetime, timezone
import os
from engine.utils import compute_send_time
from tqdm import tqdm

def run_pipeline(use_tqdm=True, limit=None, use_llm=False):
    # Paths
    DATA_DIR = os.path.join("cst_pipeline", "data", "processed")

    # Load all three datasets
    conv_df = pd.read_csv(os.path.join(DATA_DIR, "conversation_analysis.csv"))

    # Compute minutes since last tweet for each row
    now = datetime.now(timezone.utc)
    conv_df['created_at'] = pd.to_datetime(conv_df['created_at'], utc=True)
    conv_df['minutes_since_last_reply'] = (now - conv_df['created_at']).dt.total_seconds() / 60
    urgency_cutoff = conv_df['minutes_since_last_reply'].quantile(0.75)

    cluster_df = pd.read_csv(os.path.join(DATA_DIR, "conversation_clusters.csv"))
    label_df = pd.read_csv(os.path.join(DATA_DIR, "interpreted_clusters.csv"))

    conv_df['conversation_id'] = conv_df['conversation_id'].fillna(-1).astype(int)
    cluster_df['author_id'] = cluster_df['author_id'].astype(str)
    label_df['cluster'] = label_df['cluster'].astype(int)

    # Merge on 'author_id'
    merged_df = conv_df.merge(cluster_df, on="conversation_id", how="left")
    
    # Merge with cluster interpretation
    merged_df['cluster'] = merged_df['cluster'].fillna(-1).astype(int)
    merged_df = merged_df.merge(label_df[['cluster', 'label']], on="cluster", how="left")

    # Rename to expected names for NBA rule engine
    merged_df["author_id"] = merged_df["author_id_x"]
    merged_df["ticket_status"] = merged_df["ticket_status_x"]
    

    # Ensure 'cluster' type match for label join
    # Safer NaN handling: only fill strings with '', and numeric with a default
    string_cols = merged_df.select_dtypes(include=['object']).columns
    merged_df[string_cols] = merged_df[string_cols].fillna('')

    nba_outputs = []
    log_rows = []
    
    #If your code is running slow 
    # if limit:
    #     merged_df = merged_df.head(limit)

    print(f"Total rows in merged_df: {len(merged_df)}")
    print("Columns available:", merged_df.columns.tolist())
    print("Sample row:")
    print(merged_df.iloc[0].to_dict())

    iterable = tqdm(merged_df.iterrows(), total=len(merged_df)) if use_tqdm else merged_df.iterrows()


    for _, row in iterable:
        try:
            if row["ticket_status"] not in ["open", "pending"]:
                continue

            row_dict = row.to_dict()

            if use_llm:
                nba_json = get_llm_nba_decision(row_dict)
            else:
                nba_json = decide_nba_action(row_dict, urgency_cutoff)

            nba_json["customer_id"] = str(row["author_id"])
            nba_json["send_time"] = compute_send_time(row.get("created_at"))
            nba_json["conversation_id"] = row["conversation_id"]
            nba_outputs.append(nba_json)

            log_rows.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "conversation_id": row["conversation_id"],
                "customer_id": row["author_id"],
                "channel": nba_json.get("channel", ""),
                "send_time": nba_json.get("send_time", ""),
                "message": nba_json.get("message", ""),
                "reasoning": nba_json.get("reasoning", "")
            })

        except Exception as e:
            print(f"Skipping row due to error: {e}")

    # Save audit CSV
    audit_path = os.path.join("cst_pipeline", "output", "nba_audit_log.csv")
    pd.DataFrame(log_rows).to_csv(audit_path, index=False)
    print(f"Audit log written to {audit_path}")


    return nba_outputs
