import pandas as pd
import re
import hashlib
import emoji

# Simple emoji sentiment score (naive rule-based)
EMOJI_POSITIVE = {'🙂', '😀', '😄', '😍', '❤️', '👍', '😊'}
EMOJI_NEGATIVE = {'😠', '😡', '💢', '😞', '👎', '😤', '😭'}

def extract_emoji_sentiment(text):
    found = set(c for c in text if c in emoji.EMOJI_DATA)
    if found & EMOJI_POSITIVE:
        return 'positive'
    elif found & EMOJI_NEGATIVE:
        return 'negative'
    elif found:
        return 'neutral'
    return 'none'

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)      # remove URLs
    text = re.sub(r"@\w+", "", text)         # remove mentions
    text = re.sub(r"[^\w\s]", "", text)      # remove punctuation/symbols
    text = re.sub(r"\s+", " ", text).strip() # normalize whitespace
    return text

def preprocess_dataframe(df):
    df = df.copy()

    # Clean text
    df['text_clean'] = df['text'].apply(clean_text)

    #Emoji sentiment extraction
    df['emoji_sentiment'] = df['text'].apply(extract_emoji_sentiment)


    # Convert inbound to boolean
    df['inbound'] = df['inbound'].astype(str).str.upper().eq('TRUE')

    # Author ID as string
    df['author_id'] = df['author_id'].astype(str)

    # Extract UTC hour of tweet for time pattern analysis
    df['created_hour_utc'] = df['created_at'].dt.hour
    
    # Response chain cleaning
    df['in_response_to_tweet_id'] = pd.to_numeric(df['in_response_to_tweet_id'], errors='coerce')
    df['response_tweet_id'] = pd.to_numeric(df['response_tweet_id'], errors='coerce')

    return df
