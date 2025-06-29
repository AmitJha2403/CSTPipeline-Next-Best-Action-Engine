# clustering_features.py
import pandas as pd
import numpy as np
from cst_pipeline.conversation_analysis.analyze import build_conversations
from sklearn.preprocessing import LabelEncoder, StandardScaler
from collections import Counter
from datetime import timedelta
import hdbscan
import matplotlib.pyplot as plt
import seaborn as sns
import os

def extract_conversation_features(df, threads):
    rows = []
    seen_tweet_ids = set()  # Track tweets already assigned

    for root_id, tweet_ids in threads.items():
        # If thread overlaps with any seen tweets, skip it
        if any(tid in seen_tweet_ids for tid in tweet_ids):
            continue

        convo = df[df["tweet_id"].isin(tweet_ids)].sort_values("created_at")
        if convo.empty:
            continue

        # Mark all tweets as processed
        seen_tweet_ids.update(tweet_ids)

        # Ignore if resolved
        if convo[convo["tweet_id"] == root_id]["ticket_status"].values[0] == "resolved":
            continue

        author_id = convo[convo["tweet_id"] == root_id]["author_id"].values[0]
        created_times = convo["created_at"]
        duration = (created_times.max() - created_times.min()).total_seconds() / 60  # in minutes

        user_msgs = convo[convo["inbound"]]
        agent_msgs = convo[~convo["inbound"]]

        sentiments = user_msgs["text_sentiment"].values
        dominant_sentiment = Counter(sentiments).most_common(1)[0][0] if len(sentiments) > 0 else "neutral"

        rows.append({
            "conversation_id": root_id,
            "author_id": author_id,
            "num_turns": len(convo),
            "num_user_msgs": len(user_msgs),
            "num_agent_msgs": len(agent_msgs),
            "duration_min": duration,
            "initial_sentiment": sentiments[0] if len(sentiments) > 0 else "neutral",
            "dominant_sentiment": dominant_sentiment,
            "request_type": convo[convo["tweet_id"] == root_id]["nature_of_support_request"].values[0],
            "ticket_status": convo[convo["tweet_id"] == root_id]["ticket_status"].values[0]
        })

    convo_df = pd.DataFrame(rows)

    # Encode categorical features
    le_sent = LabelEncoder()
    le_type = LabelEncoder()

    convo_df["initial_sentiment_enc"] = le_sent.fit_transform(convo_df["initial_sentiment"])
    convo_df["dominant_sentiment_enc"] = le_sent.transform(convo_df["dominant_sentiment"])
    convo_df["request_type_enc"] = le_type.fit_transform(convo_df["request_type"])

    return convo_df

def run_clustering():
    # Load processed data
    input_path = os.path.join("cst_pipeline", "data", "processed", "conversation_analysis.csv")
    df = pd.read_csv(input_path, parse_dates=["created_at"])
    # Build threads again
    threads = build_conversations(df)
    print("Threads rebuilt")

    # Extract conversation-level features
    convo_df = extract_conversation_features(df, threads)
    print("Features extracted")

    # Prepare features for clustering
    feature_cols = [
        "num_turns", "num_user_msgs", "num_agent_msgs", "duration_min",
        "initial_sentiment_enc", "dominant_sentiment_enc", "request_type_enc"
    ]
    X = convo_df[feature_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Run HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=20, prediction_data=True)
    convo_df["cluster"] = clusterer.fit_predict(X_scaled)

    print("Clustering complete")
    print(convo_df["cluster"].value_counts())

    # Save cohort info
    cluster_path = os.path.join("cst_pipeline", "data", "processed", "conversation_clusters.csv")
    convo_df.to_csv(cluster_path, index=False)
    print("Saved clusters to conversation_clusters.csv")

    # Visualize with pairplot
    plot_cols = ["num_turns", "duration_min", "initial_sentiment_enc", "request_type_enc", "cluster"]
    sns.pairplot(convo_df[plot_cols], hue="cluster", corner=True, palette="tab10")
    plt.suptitle("Conversation Cohorts by Cluster", y=1.02)
    plt.tight_layout()
    plot_path = os.path.join("cst_pipeline", "data", "processed", "convo_clusters_plot.png")
    plt.savefig(plot_path)
    # plt.show()

if __name__ == "__main__":
    run_clustering()