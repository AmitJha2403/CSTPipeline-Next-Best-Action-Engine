# CST Pipeline

This folder contains the **complete Customer Support Twitter (CST) pipeline** for processing raw data, analyzing conversations, training an MBTI personality classifier, running a Next-Best-Action (NBA) engine, and generating final outputs for evaluation.

---

## Folder Structure

### `conversation_analysis/`
Scripts for:
- Ingesting raw Twitter data.
- Cleaning and analyzing conversations.
- Extracting features and clustering similar conversations.
- Generating cluster labels for downstream NBA logic.

---

### `data/`
- **Where your datasets live.**
  - Add `twcs.csv` to `data/raw/`
  - Add `reddit_post.csv` and `unique_author.csv` to `data/mbti/`

---

### `engine/`
Core NBA engine:
- Business rules for deciding the next best action.
- Utilities for time calculations.
- Personalized message generation using MBTI tags.

---

### `mbti_modelling/`
MBTI classification pipeline:
- Fine-tunes a DistilBERT model on Reddit MBTI data.
- Predicts MBTI for each customer.
- Tags your conversation dataset with MBTI labels for personalization.

---

### `output/`
All final outputs:
- Raw NBA JSON results.
- Audit logs.
- Evaluation CSVs for both base NBA and MBTI-personalized NBA.

---

### `prompts/`
(Optional) Any prompt templates for personalized messaging.

---

## 📄 Top-Level Python Files

| File | Purpose |
|------|---------|
| `ingest.py` | Ingests and preprocesses raw Twitter data. |
| `preprocess.py` | (If separate) Handles any extra cleaning steps. |
| `run_nba.py` | Runs the full NBA engine and saves results. |
| `evaluate_nba.py` | Evaluates the base NBA output. |
| `evaluate_personalized_nba.py` | Compares base NBA with MBTI-personalized messaging. |
| `__main__.py` | Main entry point to run the entire pipeline step-by-step. |

---

## Data Requirements

Before running, place these files:
- `twcs.csv` -> `data/raw/`
  - [Download](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter/data)
- `reddit_post.csv` & `unique_author.csv` -> `data/mbti/`
  - [Download](https://www.kaggle.com/datasets/minhaozhang1/reddit-mbti-dataset)

---

## ⚙️ How to Run

Run the **main pipeline**:
```bash
python -m cst_pipeline
```
Or run each step manually:
```
python -m cst_pipeline.ingest
python -m cst_pipeline.conversation_analysis.analyze
python -m cst_pipeline.conversation_analysis.clustering_features
python -m cst_pipeline.conversation_analysis.conversation_clusters
python -m cst_pipeline.mbti_modelling.train_mbti_classifier
python -m cst_pipeline.mbti_modelling.tag_cst_users
python -m cst_pipeline.run_nba
python -m cst_pipeline.evaluate_nba
python -m cst_pipeline.evaluate_personalized_nba
```
