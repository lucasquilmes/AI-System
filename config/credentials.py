import os
from dotenv import load_dotenv

def load_credentials() -> dict:
    """
    Load API credentials from environment variables or .env file.
    Call once at startup.
    """
    load_dotenv()

    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_base_url": os.getenv("OPENAI_BASE_URL"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
    }
