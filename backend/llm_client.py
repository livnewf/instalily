import os

try:
    import anthropic as _anthropic
except ImportError:
    _anthropic = None

try:
    from llm import OpenAI
except ImportError:
    OpenAI = None

try:
    from transformers import pipeline
except ImportError:
    pipeline = None


def _needs_trust_remote_code(model_name: str) -> bool:
    return 'qwen' in model_name.lower()


def generate_text(prompt: str, max_tokens: int = 200) -> str:
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

    if pipeline is not None:
        model_name = os.getenv('LOCAL_MODEL', 'gpt2')
        use_trust_remote_code = _needs_trust_remote_code(model_name)

        try:
            text_generator = pipeline(
                'text-generation',
                model=model_name,
                trust_remote_code=use_trust_remote_code,
                max_new_tokens=max_tokens,
                do_sample=False,
                return_full_text=False,
            )
            result = text_generator(prompt)
            text = result[0]['generated_text']

            if text.startswith(prompt):
                text = text[len(prompt):].strip()

            return text
        except Exception as exc:
            error_message = str(exc)
            if 'transformers_stream_generator' in error_message or 'DisjunctiveConstraint' in error_message:
                fallback_model = 'gpt2'
                try:
                    fallback_generator = pipeline(
                        'text-generation',
                        model=fallback_model,
                        max_new_tokens=max_tokens,
                        do_sample=False,
                        return_full_text=False,
                    )
                    result = fallback_generator(prompt)
                    text = result[0]['generated_text']
                    if text.startswith(prompt):
                        text = text[len(prompt):].strip()
                    return text
                except Exception as fallback_exc:
                    raise RuntimeError(
                        f"Transformers local model {model_name} requires transformers_stream_generator or a compatible transformers version, "
                        f"and fallback model {fallback_model} also failed: {fallback_exc}. "
                        "Set OPENAI_API_KEY to use OpenAI or install a compatible local model."
                    ) from exc

            raise RuntimeError(
                f"Transformers pipeline failed: {exc}. "
                "Install missing transformer runtime packages like einops, "
                "or set OPENAI_API_KEY to use OpenAI instead."
            )

    raise RuntimeError(
        'No valid LLM backend available. Install `llm` or `transformers` and set OPENAI_API_KEY or LOCAL_MODEL.'
    )
