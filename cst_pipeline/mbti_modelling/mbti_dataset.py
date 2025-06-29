from torch.utils.data import Dataset

class MBTIDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, label2id, max_length=256):
        self.texts = texts
        self.labels = [label2id[label] for label in labels]
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encodings = self.tokenizer(
            self.texts[idx], truncation=True, padding='max_length', max_length=self.max_length, return_tensors='pt'
        )
        return {
            'input_ids': encodings['input_ids'].squeeze(),
            'attention_mask': encodings['attention_mask'].squeeze(),
            'labels': self.labels[idx]
        }
