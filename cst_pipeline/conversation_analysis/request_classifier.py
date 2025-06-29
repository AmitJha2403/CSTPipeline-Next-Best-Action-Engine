from transformers import pipeline
print("request_classifier at work")
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

CANDIDATE_LABELS = [
    "flight booking problem",
    "refund or cancellation",
    "product or service feedback",
    "pricing or fare query",
    "general question",
    "non-support message"
]

def classify_request(text):
    if not isinstance(text, str) or text.strip() == "":
        return "non-support message"
    result = classifier(text, candidate_labels=CANDIDATE_LABELS)
    return result['labels'][0]
