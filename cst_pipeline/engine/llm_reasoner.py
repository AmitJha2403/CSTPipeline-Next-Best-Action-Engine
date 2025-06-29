# llm_reasoner.py
import subprocess
import json

def get_llm_nba_decision(row):
    prompt = f"""
    You are a support AI assistant. Based on the following user data, suggest the best channel (email_reply, twitter_dm_reply, or scheduling_phone_call),
    an empathetic message tailored to their MBTI personality type, and a justification.
    
    User Info:
    - MBTI: {row.get('predicted_mbti', 'Unknown')}
    - Sentiment: {row.get('dominant_sentiment', 'neutral')}
    - Request Type: {row.get('request_type', '')}
    - Cleaned Chat Log: {row.get('text_clean', '')}
    - Minutes Since Last Reply: {row.get('minutes_since_last_reply', 0)}
    
    Respond in JSON with keys: channel, message, reasoning.
    """

    # Call local Ollama model (assumes `ollama run llama3` is working)
    result = subprocess.run(
        ['ollama', 'run', 'llama3'],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE
    )
    
    try:
        # Extract and clean the first JSON from the output
        output = result.stdout.decode('utf-8')
        json_str = output[output.find('{'):output.rfind('}')+1]
        response = json.loads(json_str)
        return response
    except Exception as e:
        print("LLM parsing failed, falling back:", e)
        return {
            "channel": "email_reply",
            "message": "Thanks for reaching out. We'll follow up soon.",
            "reasoning": "Fallback message due to parsing error."
        }
