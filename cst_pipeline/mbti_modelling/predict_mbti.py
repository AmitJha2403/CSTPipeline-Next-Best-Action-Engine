from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Load model
MODEL_DIR = "cst_pipeline/mbti_model/model"
model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
tokenizer = DistilBertTokenizer.from_pretrained(os.path.join(MODEL_DIR, "tokenizer"))
model.eval()

id2label = model.config.id2label

def predict_mbti(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return "UNKNOWN"
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_id = outputs.logits.argmax(dim=-1).item()
        return id2label[predicted_id]
