import pandas as pd
import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from preprocess import preprocess_dataframe  

# --- Configuration ---
BATCH_MODE = "daily"  # Change to "hourly" if needed
RAW_CSV = "cst_pipeline/data/raw/twcs.csv"

# Storage mode: "csv", "sqlite", or "cloud"
STORAGE_MODE = "csv"

# CSV paths
PROCESSED_CSV = "cst_pipeline/data/processed/cst_ingested.csv"
STATE_FILE = "cst_pipeline/data/logs/last_ingested.json"

# SQLite config
SQLITE_DB = "cst_pipeline/data/processed/cst_ingested.db"
SQLITE_TABLE = "tweets"

# Twitter's datetime format
DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"

# --- State management ---
def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_processed_time": "2000-01-01T00:00:00+0000"}
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

# --- Storage Abstraction ---
def save_data(data):
    if STORAGE_MODE == "csv":
        data.to_csv(PROCESSED_CSV, index=False)
    elif STORAGE_MODE == "sqlite":
        engine = create_engine(f"sqlite:///{SQLITE_DB}")
        data.to_sql(SQLITE_TABLE, con=engine, if_exists='replace', index=False)
    elif STORAGE_MODE == "cloud":
        raise NotImplementedError("Cloud storage not implemented.")
    else:
        raise ValueError(f"Unsupported STORAGE_MODE: {STORAGE_MODE}")

def load_existing_data():
    if STORAGE_MODE == "csv":
        if os.path.exists(PROCESSED_CSV):
            return pd.read_csv(PROCESSED_CSV, parse_dates=['created_at'], date_parser=pd.to_datetime)
        else:
            return pd.DataFrame()
    elif STORAGE_MODE == "sqlite":
        engine = create_engine(f"sqlite:///{SQLITE_DB}")
        try:
            return pd.read_sql(SQLITE_TABLE, con=engine, parse_dates=['created_at'])
        except Exception:
            return pd.DataFrame()
    elif STORAGE_MODE == "cloud":
        raise NotImplementedError("Cloud storage not implemented.")
    else:
        raise ValueError(f"Unsupported STORAGE_MODE: {STORAGE_MODE}")

# --- Ingestion pipeline ---
def ingest():
    # Load raw data
    df = pd.read_csv(RAW_CSV)

    # Parse Twitter datetime format
    df['created_at'] = pd.to_datetime(df['created_at'], format=DATE_FORMAT, errors='coerce')
    df.dropna(subset=['created_at'], inplace=True)

    # Load ingestion state
    state = load_state()
    last_ingested_time = pd.to_datetime(state["last_processed_time"])

    # Filter new records
    new_data = df[df['created_at'] > last_ingested_time].copy()
    if new_data.empty:
        print("No new records to ingest.")
        return

    # Deduplicate new batch
    new_data.drop_duplicates(subset=['tweet_id'], inplace=True)

    # Load and combine with previous data
    old_data = load_existing_data()
    if not old_data.empty:
        combined = pd.concat([old_data, new_data], ignore_index=True)
        combined.drop_duplicates(subset=['tweet_id'], inplace=True)
    else:
        combined = new_data

    # Preprocess full dataset
    combined = preprocess_dataframe(combined)

    # Sort for time order
    combined.sort_values(by='created_at', inplace=True)

    # Save to target storage
    save_data(combined)

    # Update last timestamp
    max_time = combined['created_at'].max().strftime("%Y-%m-%dT%H:%M:%S%z")
    save_state({"last_processed_time": max_time})

    print(f"Ingested {len(new_data)} new records. Last timestamp: {max_time}")

# Run pipeline
if __name__ == "__main__":
    ingest()

