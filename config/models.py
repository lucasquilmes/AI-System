from typing import Dict, Any

# Keys are the model names you pass via --model
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    # --- Local / open-source via Ollama ---
    "llama3:8b": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "qwen2.5": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "qwen3:8b": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "deepseek-r1": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "mistral:7b": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "kimi-k2.5:cloud": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },

    # --- OpenAI ---
    "gpt-4o-mini": {
        "provider": "openai",
        "temperature": 0.0,
        "seed": 42,
    },
    "gpt-4o": {
        "provider": "openai",
        "temperature": 0.0,
        "seed": 42,
    },

    # --- Anthropic ---
    "claude-3-5-sonnet-20241022": {
        "provider": "anthropic",
        "temperature": 0.0,
    },
    "claude-3-opus-20250219": {
        "provider": "anthropic",
        "temperature": 0.0,
    },

    # --- Google ---
    "gemini-1.5-pro": {
        "provider": "google",
        "temperature": 0.0,
    },
    "gemini-2.0-flash": {
        "provider": "google",
        "temperature": 0.0,
    },
}
