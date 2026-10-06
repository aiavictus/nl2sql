import httpx

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

AVAILABLE_MODELS = {
    "llama3.2": "llama3.2:3b",
###    "qwen3": "qwen3:4b",
    "gemma3": "gemma3:4b",
}

DEFAULT_MODEL = "gemma3"


def ask_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    if model not in AVAILABLE_MODELS:
        raise ValueError(
            f"Unknown model '{model}'. "
            f"Available models: {', '.join(AVAILABLE_MODELS)}"
        )

    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": AVAILABLE_MODELS[model],
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 300,
            },
            "think": False,
        },
        timeout=60,
    )

    response.raise_for_status()
    return response.json()["message"]["content"]


if __name__ == "__main__":
    print(ask_llm("Reply with exactly: LOCAL_LLM_OK"))