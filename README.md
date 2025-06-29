# CSTPipeline-Next-Best-Action-Engine
---
## Problem Statement
Modern customer support teams handle massive volumes of customer conversations every day across social media platforms like Twitter. It is challenging to:

- Understand the intent, sentiment, and urgency of each customer query.
- Prioritize responses efficiently.
- Personalize interactions to match individual customer personalities and preferences.

This project solves this by building an **end-to-end Next-Best-Action (NBA) Engine** that:

1️⃣ Ingests raw customer support conversations from Twitter.  
2️⃣ Cleans, analyzes, and clusters these conversations to understand common support topics and sentiments.  
3️⃣ Predicts each customer’s MBTI personality type using a fine-tuned DistilBERT classifier trained on Reddit data.  
4️⃣ Combines business rules and personality insights to generate **personalized next-best-action recommendations** for each customer.  
5️⃣ Outputs audit logs, result JSONs, and final evaluation CSVs for review.

**Goal:** Enable support teams to **respond faster**, **prioritize better**, and **personalize messages** — improving customer satisfaction and operational efficiency.
---

## Overview

This project builds an end-to-end pipeline for:
- Ingesting and analyzing raw customer support data
- Clustering conversations by topic/intent
- Predicting MBTI personality types for users
- Generating personalized Next-Best-Actions (NBA) using business rules & MBTI traits
- Evaluating results and comparing baseline vs. personalized messages
- The generated results are stored in output folder

## Project Structure
```bash
CSTPipeline-Next-Best-Action-Engine/
├── cst_pipeline/
│   ├── __init__.py
│   ├── main.py
│   ├── ingest.py
│   ├── run_nba.py
│   ├── evaluate_nba.py
│   ├── evaluate_personalized_nba.py
│   ├── mbti_modelling/
│   │   ├── __init__.py
│   │   ├── train_mbti_classifier.py
│   │   ├── tag_cst_users.py
│   │   ├── mbti_dataset.py
│   │   ├── predict_mbti.py
│   ├── conversation_analysis/
│   │   ├── analyze.py
│   │   ├── clustering_features.py
│   │   ├── conversation_clusters.py
│   ├── engine/
│   │   ├── nba_rules.py
│   │   ├── nba_pipeline.py
│   │   ├── utils.py
│   │   ├── generate_mbti_message.py
├── data/
│   ├── raw/
│   │   ├── twcs.csv
│   ├── mbti/
│   │   ├── reddit_post.csv
│   │   ├── unique_author.csv
│   ├── processed/
│   │   ├── conversation_analysis.csv
│   │   ├── cst_mbti_tags.csv
├── output/
│   ├── nba_output.json
│   ├── nba_result_eval.csv
│   ├── mbti_comparison_eval.csv
├── requirements.txt
├── README.md
```
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
  → Download from [Kaggle](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter/data)  
  → Place it in `cst_pipeline/data/raw/`

- **MBTI training data:** Reddit posts & authors  
  → Download `reddit_post.csv` and `unique_author.csv` from [this Kaggle link](https://www.kaggle.com/datasets/minhaozhang1/reddit-mbti-dataset?select=reddit_post.csv)  
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
   ```
3. Add Data
  - Put twcs.csv in cst_pipeline/data/raw/
  - Put reddit_post.csv and unique_author.csv in cst_pipeline/data/mbti/
5. Run the pipeline: 
   ```bash
   pip install -r requirements.txt
   ```
6. Final outputs:
  - nba_output.json — raw NBA predictions
  - nba_result_eval.csv — final evaluated CSV for 1000 customers
  - mbti_comparison_eval.csv — baseline vs. personalized message comparison
