# `mbti_modelling` Folder

This folder contains all scripts for training, predicting, and tagging MBTI personality types for customers.

---

## Files Explained

### `train_mbti_classifier.py`
- **Purpose:**  
  Fine-tunes a DistilBERT model to classify text into one of 16 MBTI personality types.
- **Inputs:**  
  - `reddit_post.csv` (MBTI-labeled Reddit posts)
- **Outputs:**  
  - Saves trained model to `mbti_modeling/model/`
- **Special Note:**  
  Uses `wandb` for logging. Make sure to handle any `wandb` login needs.

---

### `tag_cst_users.py`
- **Purpose:**  
  Tags each customer in your conversation dataset with a predicted MBTI type.
- **Inputs:**  
  - `conversation_analysis.csv`
  - Trained MBTI model
- **Outputs:**  
  - `cst_mbti_tags.csv` in `data/processed/`

---

### `mbti_dataset.py`
- **Purpose:**  
  Defines a custom PyTorch `Dataset` for tokenizing text and preparing it for training.
- **Usage:**  
  Imported by `train_mbti_classifier.py` to prepare data batches.

---

### `predict_mbti.py`
- **Purpose:**  
  Loads the saved MBTI model to predict a personality type for a given text.
- **Usage:**  
  Called by `tag_cst_users.py` and other modules that need MBTI predictions.

---

## Data Flow

1️ `reddit_post.csv` → `train_mbti_classifier.py` → saved model  
2️ `conversation_analysis.csv` + model → `tag_cst_users.py` → `cst_mbti_tags.csv`

---

## Usage

Run these steps:
```bash
python -m cst_pipeline.mbti_modelling.train_mbti_classifier
python -m cst_pipeline.mbti_modelling.tag_cst_users
