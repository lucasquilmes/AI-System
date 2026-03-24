from pathlib import Path

# General registry to map task names to their configuration
# No schema needed - just raw LLM output
GENERAL_REGISTRY = {
    "classification": {
        "name": "classification",
        "system_prompt": Path("prompts/classification_system.txt"),
        "user_prompt": Path("prompts/classification_user.txt"),
        "output_prefix": "classification",
    },

    "extraction": {
        "name": "extraction",
        "system_prompt": Path("prompts/extraction_system.txt"),
        "user_prompt": Path("prompts/extraction_user.txt"),
        "output_prefix": "extraction",
    },

    "sentiment": {
        "name": "sentiment",
        "system_prompt": Path("prompts/sentiment_system.txt"),
        "user_prompt": Path("prompts/sentiment_user.txt"),
        "output_prefix": "sentiment",
    },

    "custom": {
        "name": "custom",
        "system_prompt": Path("prompts/custom_system.txt"),
        "user_prompt": Path("prompts/custom_user.txt"),
        "output_prefix": "custom",
    },
    # Add other tasks as needed
}
