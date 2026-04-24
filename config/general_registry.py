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

    "v0": {
        "name": "v0",
        "system_prompt": Path("prompts/v0_system.txt"),
        "user_prompt": Path("prompts/v0_user.txt"),
        "output_prefix": "v0",
    },

    "v1": {
        "name": "v1",
        "system_prompt": Path("prompts/v1_system.txt"),
        "user_prompt": Path("prompts/v1_user.txt"),
        "output_prefix": "v1",
    },
}
