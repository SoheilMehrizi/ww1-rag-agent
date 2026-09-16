"""
Minimal client for the Arvan Cloud AI gateway's chat completions endpoint.

Uses plain `requests` rather than the OpenAI SDK because Arvan's gateway
expects the API key in the Authorization header with an "apikey" scheme,
not the SDK's default "Bearer" scheme.
"""

import requests

import config


def chat_completion(messages: list[dict]) -> str:
    """Send a chat completion request to the Arvan gateway and return the reply text."""
    url = f"{config.ARVAN_ENDPOINT}/chat/completions"
    headers = {
        "Authorization": config.ARVAN_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.ARVAN_MODEL_NAME,
        "messages": messages,
        "temperature": config.LLM_TEMPERATURE,
        "max_tokens": config.LLM_MAX_TOKENS,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=config.LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
