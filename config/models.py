from typing import Dict, Any

# Keys are the model names you pass via --model
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    # --- Local / open-source via Ollama ---
    # Modelos verificados con: ollama list
    "llama3.1:8b": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "mistral-nemo": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "command-r": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "gemma2:27b": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "mixtral": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "llama3.3": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "qwen2.5:32b": {
        "provider": "ollama",
        "temperature": 0.0,
        "num_ctx": 8192,
        "seed": 42,
    },
    "aya-expanse:32b": {
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
