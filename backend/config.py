import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    CLAUDE_MODEL_ID = os.getenv(
        "CLAUDE_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"
    )
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))


config = Config()
