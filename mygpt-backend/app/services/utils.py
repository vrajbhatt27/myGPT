import re


def normalize_question(q: str) -> str:
    # Remove emojis & special characters
    q = re.sub(r"[^\w\s\?\.,]", "", q)

    # Lowercase and strip polite prefixes
    q = q.lower().strip()
    q = re.sub(
        r"^(can you|could you|would you|please|i need|i want|help me with)\b.*?\b",
        "",
        q,
    )

    return q.strip()
