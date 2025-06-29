# CSTPipeline-Next-Best-Action-Engine

## Overview

This project builds an end-to-end pipeline for:
- Ingesting and analyzing raw customer support data
- Clustering conversations by topic/intent
- Predicting MBTI personality types for users
- Generating personalized Next-Best-Actions (NBA) using business rules & MBTI traits
- Evaluating results and comparing baseline vs. personalized messages

---

## Project Structure

- `cst_pipeline/ingest.py` — loads and cleans raw data.
- `cst_pipeline/conversation_analysis/` — NLP analysis, feature extraction, clustering.
- `cst_pipeline/mbti_modelling/` — MBTI classifier training and tagging.
- `cst_pipeline/engine/` — NBA rules engine and utilities.
- `cst_pipeline/run_nba.py` — main NBA pipeline runner.
- `cst_pipeline/evaluate_nba.py` — evaluates NBA results.
- `cst_pipeline/evaluate_personalized_nba.py` — evaluates MBTI-personalized NBA messages.
- `cst_pipeline/main.py` — runs the full pipeline in sequence.

---

## Data Assumptions

- **Input:** CSV of cleaned customer support tweets (`conversation_analysis.csv`)
- MBTI classifier uses `reddit_post.csv` (Reddit posts labeled with MBTI types).
- Output: JSON + CSV files in `cst_pipeline/output/`

- **Main input:** Customer support tweets from Twitter — `twcs.csv`  
  → 📥 Download from [Kaggle](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter/data)  
  → Place it in `cst_pipeline/data/raw/`

- **MBTI training data:** Reddit posts & authors  
  → 📥 Download `reddit_post.csv` and `unique_author.csv` from [this Kaggle link](https://www.kaggle.com/datasets/minhaozhang1/reddit-mbti-dataset?select=reddit_post.csv)  
  → Place both files in `cst_pipeline/data/mbti/`


---

## Design Decisions

- Uses **Hugging Face Transformers** (`DistilBERT`) for MBTI classification.
- Clustering done with standard NLP embeddings.
- NBA rules coded in `nba_rules.py` — these map clusters + sentiment + urgency to channel & message.
- MBTI personalization hooks customize messages using simple templates.
- Relative imports are used to keep code modular and package-safe.
- Logs & intermediate files are versioned for traceability.

---

## How to Run

1. Clone repo & set up virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the pipeline:
   ```bash
   python -m cst_pipeline
4. Final outputs:
  - nba_output.json — raw NBA predictions
  - nba_result_eval.csv — final evaluated CSV for 1000 customers
  - mbti_comparison_eval.csv — baseline vs. personalized message comparison

