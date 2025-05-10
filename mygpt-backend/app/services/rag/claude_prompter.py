# app/services/rag/claude_prompter.py


def build_claude_prompt(question: str, context_chunks: list[str]) -> str:
    """
    Builds the user message to send to Claude with contextual chunks and the question.
    Assumes Claude's behavior is set via the system prompt.
    """
    prompt = "### CONTEXT ###\n"
    for i, chunk in enumerate(context_chunks):
        prompt += f"Chunk {i + 1}:\n{chunk.strip()}\n\n"

    prompt += "### QUESTION ###\n"
    prompt += question.strip()
    prompt += "\n\n### ANSWER ###\n"

    return prompt
