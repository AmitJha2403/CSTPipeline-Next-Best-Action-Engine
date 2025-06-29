import pandas as pd
print("thread_builder at work")
def build_conversations(df):
    """
    Returns a dict: {root_tweet_id: [ordered conversation thread]}
    """
    threads = {}
    df = df.sort_values(by="created_at")

    tweet_map = df.set_index('tweet_id').to_dict(orient='index')

    for tweet_id, row in tweet_map.items():
        if row['inbound']:  # Start only from inbound messages (customer)
            thread = [tweet_id]
            current = tweet_id
            while tweet_map.get(current) and tweet_map[current]['response_tweet_id'] in tweet_map:
                next_id = tweet_map[current]['response_tweet_id']
                thread.append(next_id)
                current = next_id
            threads[tweet_id] = thread

    return threads
