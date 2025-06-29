# `conversation_analysis` Folder

This folder contains all the scripts related to analyzing, processing, clustering, and interpreting customer conversations.

---

## Files Explained

### `analyze.py`
- **Purpose:**  
  Loads the raw `twcs.csv` dataset, cleans the text, and runs sentiment or emoji analysis.
- **Output:**  
  Creates a processed CSV file: `conversation_analysis.csv` in `data/processed/`.
- **Key Tasks:**  
  - Cleans raw tweets.
  - Extracts useful features (e.g., sentiment, cleaned text).

---

### `clustering_features.py`
- **Purpose:**  
  Generates numerical features for clustering customer conversations.
- **Output:**  
  Updates or generates additional cluster feature columns in the processed data.
- **Key Tasks:**  
  - Computes conversation-level statistics (number of turns, message ratios, etc.).
  - Prepares vectors for clustering.

---

### `conversation_clusters.py`
- **Purpose:**  
  Performs clustering on the processed conversation features to group similar customer conversations.
- **Output:**  
  Adds cluster labels to each conversation in the processed dataset.
- **Key Tasks:**  
  - Runs a clustering algorithm (e.g., KMeans).
  - Labels each conversation with its cluster.
  - Helps segment customers for downstream Next-Best-Action.

---

## Data Flow

`twcs.csv` → `analyze.py` → `clustering_features.py` → `conversation_clusters.py`  
Processed results are stored in:  
```bash
data/processed/conversation_analysis.csv
```


