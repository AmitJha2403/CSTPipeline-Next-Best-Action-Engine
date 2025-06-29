# engine/generate_mbti_message.py

def generate_mbti_message(mbti_type, row):
    base_msg = "We truly value your experience. "
    closing = " Let us know if you need anything else."

    style_map = {
        "INTJ": "We've carefully reviewed your concern. Expect a prompt and structured resolution.",
        "ESFP": "Hey there! We're on it and will get this sorted with a smile.",
        "INFP": "We understand how this might feel. Your issue truly matters to us.",
        "ENTP": "We're diving deep into your case and might just find a smarter fix.",
        "ISFJ": "Thanks for your patience. We'll make sure everything works out smoothly for you.",
        "ENTJ": "This will be resolved swiftly. We've assigned our top agents to this.",
        "INFJ": "Your concern is valid, and we appreciate your thoughtful communication.",
        "ESTP": "Let's get this fixed fast. No time wasted!",
    }

    custom_message = style_map.get(mbti_type, "We are here to assist you in the best way possible.")
    return f"{base_msg}{custom_message}{closing}"