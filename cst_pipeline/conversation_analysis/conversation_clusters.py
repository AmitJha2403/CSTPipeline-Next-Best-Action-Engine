import pandas as pd
import os

input_path = os.path.join("cst_pipeline", "data", "processed", "conversation_clusters.csv")
df = pd.read_csv(input_path)

# Aggregate stats by cluster
cluster_profiles = df.groupby('cluster').agg({
    'num_turns': 'mean',
    'duration_min': 'mean',
    'initial_sentiment_enc': 'mean',
    'request_type_enc': lambda x: x.mode()[0],
    'author_id': 'count'
}).rename(columns={'author_id': 'num_samples'}).reset_index()

# Add interpretation rule
def interpret_cluster(row):
    if row['num_turns'] <= 2 and row['initial_sentiment_enc'] >= 1.5:
        return "quick_positive_resolution"
    elif row['num_turns'] > 5 and row['initial_sentiment_enc'] < 1:
        return "frustrated_escalation"
    elif row['duration_min'] < 1 and row['num_turns'] <= 1:
        return "unresponsive_user"
    elif row['num_turns'] >= 4 and row['initial_sentiment_enc'] >= 1:
        return "high_effort_positive"
    elif row['initial_sentiment_enc'] < 1 and row['duration_min'] > 5:
        return "long_negative_thread"
    else:
        return "neutral_support"

def select_channel(cluster_label):
    if cluster_label == "quick_positive_resolution":
        return None  # Already resolved
    elif cluster_label == "unresponsive_user":
        return "twitter_dm_reply"
    elif cluster_label == "frustrated_escalation":
        return "scheduling_phone_call"
    elif cluster_label == "long_negative_thread":
        return "scheduling_phone_call"
    elif cluster_label == "high_effort_positive":
        return "email_reply"
    else:
        return "email_reply"

cluster_profiles["label"] = cluster_profiles.apply(interpret_cluster, axis=1)

# Save if needed
output_path = os.path.join("cst_pipeline", "data", "processed", "interpreted_clusters.csv")
cluster_profiles.to_csv(output_path, index=False)
print(cluster_profiles)
