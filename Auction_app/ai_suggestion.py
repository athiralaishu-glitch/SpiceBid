import requests
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def suggest_next_bid_openrouter(current_bid, min_increment, auction_history=None, user_behavior=None):
    print("Using API KEY:", settings.OPENROUTER_API_KEY)
    prompt = f"""
    You are an expert auction assistant.
    Current highest bid: {current_bid}
    Minimum increment: {min_increment}
    Auction history: {auction_history}
    User past behavior: {user_behavior}

    Suggest a reasonable next bid ONLY as a number.
    """
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
         "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 50
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)
        response.raise_for_status()
        result = response.json()
        logger.info("OpenRouter Response: %s", result)  # debug log
        suggestion = result['choices'][0]['message']['content'].strip()
        return suggestion
    except Exception as e:
        logger.error("OpenRouter AI error: %s", e)
        return None