import os

try:
    import anthropic as _anthropic
except ImportError:
    _anthropic = None

try:
    from llm import OpenAI
except ImportError:
    OpenAI = None


def generate_text(prompt: str, max_tokens: int = 600) -> str:
    if _anthropic is not None and os.getenv('ANTHROPIC_API_KEY'):
        model_name = os.getenv('ANTHROPIC_MODEL', 'claude-haiku-4-5-20251001')
        client = _anthropic.Anthropic()
        message = client.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return message.content[0].text

    if os.getenv('OPENAI_API_KEY') and OpenAI is not None:
        model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        client = OpenAI(model=model_name)
        return client(prompt)

    raise RuntimeError(
        'No LLM backend configured. Set ANTHROPIC_API_KEY in your environment or a .env file in the project root.'
    )
