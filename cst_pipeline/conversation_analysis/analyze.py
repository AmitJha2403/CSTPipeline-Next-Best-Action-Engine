import pandas as pd
import os
from tqdm import tqdm
from transformers import pipeline

from .thread_builder import build_conversations
from .sentiment_analysis import get_vader_sentiment
from .resolver import is_resolved

print("analyze at work")

DATA_PATH = os.path.join("cst_pipeline", "data", "processed", "cst_ingested.csv")
OUTPUT_PATH = os.path.join("cst_pipeline", "data", "processed", "conversation_analysis.csv")

SUBSET_SIZE = 5000
BATCH_SIZE = 32

LABELS = [
    "flight booking", "baggage issue", "cancellation", "payment problem",
    "account login", "technical issue", "general query", "positive feedback", "complaint"
]

def analyze():
    df = pd.read_csv(DATA_PATH, parse_dates=['created_at'])

    # Use only a random subset for speed during development
    df = df.sample(n=SUBSET_SIZE, random_state=42).sort_values(by="created_at")
    print("a: subset loaded")

    # Add sentiment (VADER)
    df['text_sentiment'] = df['text_clean'].apply(get_vader_sentiment)
    print("b: sentiment done")

    # Zero-shot classification on only inbound tweets with non-empty text_clean
    inbound_df = df[df["inbound"]].copy()
    inbound_df = inbound_df.dropna(subset=["text_clean"])
    inbound_df = inbound_df[inbound_df["text_clean"].str.strip().astype(bool)]

    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    print("c: classifier loaded")

    results = []
    texts = inbound_df["text_clean"].tolist()

    print("c: starting classification")

    for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Zero-shot classification"):
        batch_texts = texts[i:i + BATCH_SIZE]
        try:
            preds = classifier(batch_texts, LABELS, multi_label=True)
            batch_labels = [pred["labels"][0] if isinstance(pred, dict) else "unknown" for pred in preds]
        except Exception as e:
            print(f"Batch failed at index {i}: {e}")
            batch_labels = ["unknown"] * len(batch_texts)

        results.extend(batch_labels)

    # Assign results and merge into main df
    inbound_df = inbound_df.iloc[:len(results)].copy()
    inbound_df["nature_of_support_request"] = results

    df = df.merge(
        inbound_df[["tweet_id", "nature_of_support_request"]],
        on="tweet_id", how="left"
    )
    df["nature_of_support_request"].fillna("agent_response", inplace=True)
    print("d: request classification done")

    # Thread tagging
    threads = build_conversations(df)
    print("e: threads built")

    # Assign conversation_id (i.e., root tweet ID) to every tweet
    tweet_to_convo = {}
    for root, thread in threads.items():
        for tid in thread:
            tweet_to_convo[tid] = root

    df["conversation_id"] = df["tweet_id"].map(tweet_to_convo)


    # Determine resolution status
    thread_status = {
        root: "resolved" if is_resolved(thread, df) else "open"
        for root, thread in threads.items()
    }

    df['ticket_status'] = df['tweet_id'].apply(lambda tid: thread_status.get(tid, "ambiguous"))
    print("f: resolution tagged")

    # Save final output
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved analyzed data to {OUTPUT_PATH}")

if __name__ == "__main__":
    analyze()
