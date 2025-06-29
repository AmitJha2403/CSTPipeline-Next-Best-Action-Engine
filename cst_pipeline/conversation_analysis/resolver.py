print("resolver at work")

def is_resolved(thread, df):
    """
    Rule: If company replies and no follow-up from user within N hours (e.g., 24), it's resolved.
    """
    thread_df = df[df['tweet_id'].isin(thread)].sort_values(by='created_at')

    for idx, row in thread_df.iterrows():
        if not row['inbound']:  # Agent response
            after_agent = thread_df[(thread_df['created_at'] > row['created_at']) & (thread_df['inbound'])]
            if after_agent.empty:
                return True  # No user follow-up after agent reply
    return False
