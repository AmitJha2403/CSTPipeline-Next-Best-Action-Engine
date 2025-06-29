from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from .mbti_dataset import MBTIDataset
import pandas as pd
import torch
import os
os.environ["WANDB_DISABLED"] = "true"

# Define all 16 MBTI types
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Load and preprocess
df = pd.read_csv("cst_pipeline/data/mbti/reddit_post.csv")
df = df.sample(n=1000, random_state=42)
df = df[df['mbti'].isin(MBTI_TYPES)]  # Filter valid labels
texts = df['body'].astype(str).tolist()
labels = df['mbti'].tolist()

# Encode labels
MBTI_TYPES = sorted(df['mbti'].unique().tolist())
label2id = {label: i for i, label in enumerate(MBTI_TYPES)}
id2label = {i: label for label, i in label2id.items()}

# Train-test split
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.1, random_state=42)

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
train_dataset = MBTIDataset(train_texts, train_labels, tokenizer, label2id)
val_dataset = MBTIDataset(val_texts, val_labels, tokenizer, label2id)

# Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=len(MBTI_TYPES), id2label=id2label, label2id=label2id
)

training_args = TrainingArguments(
    output_dir="cst_pipeline/mbti_model/model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    logging_dir="logs",
    logging_steps=10,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
)

trainer.train()
model.save_pretrained("cst_pipeline/mbti_model/model")
tokenizer.save_pretrained("cst_pipeline/mbti_model/model/tokenizer")
