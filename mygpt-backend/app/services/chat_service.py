import os
import httpx
import logging

claude_api_key = os.getenv("CLAUDE_API_KEY")

class ChatService:
    @staticmethod
    def get_answer(question: str) -> str:
        if not claude_api_key:
            logging.error("Claude API key not found")
            return "Claude API key is missing."

        url = "https://api.anthropic.com/v1/messages"

        headers = {
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {"role": "user", "content": question}
            ]
        }

        try:
            response = httpx.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Claude response: {data}")
            return data["content"][0]["text"]
        except httpx.HTTPStatusError as e:
            logging.exception("Claude API returned HTTP error")
            return f"Claude API error: {e.response.status_code}"
        except Exception as e:
            logging.exception("Error calling Claude API")
            return "Claude is temporarily unavailable."
