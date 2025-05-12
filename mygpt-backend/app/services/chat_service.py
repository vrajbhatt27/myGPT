import logging
import os

import anthropic
from app.services.rag.claude_prompter import build_claude_prompt
from app.services.rag.query_pinecone import query_top_k_chunks

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))


class ChatService:
    def __call_claude(self, prompt: str) -> str:
        try:
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=512,
                temperature=0.5,
                system='You are a helpful medical research assistant. Your job is to answer questions using only the information provided in the context below. Do not rely on external knowledge or make assumptions beyond what the context supports. You may synthesize and paraphrase information if it appears in the form of bullet points, summaries, or fragmented text, as long as the meaning is clear. If the context does not contain enough relevant information, respond with:"I don\'t know based on the provided context."',
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
            )
            return message.content[0].text

        except anthropic.APIStatusError as e:
            logging.exception("Claude API error")
            return f"Claude API error: {e.status_code}"
        except Exception:
            logging.exception("Error calling Claude API")
            return "Claude is temporarily unavailable."

    @classmethod
    def get_answer(cls, question: str, namespace: str = "default") -> str:
        chunks = query_top_k_chunks(question, namespace=namespace, top_k=3)
        top_texts = [chunk["chunk_text"] for chunk in chunks]

        prompt = build_claude_prompt(question, top_texts)

        instance = cls()
        return instance.__call_claude(prompt)
