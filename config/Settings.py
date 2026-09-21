import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
env_path = ROOT_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2")
DEFAULT_SCORE_MIN = int(os.getenv("DEFAULT_SCORE_MIN", 300))
DEFAULT_SCORE_MAX = int(os.getenv("DEFAULT_SCORE_MAX", 850))
