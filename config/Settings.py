import os

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
BEDROCK_MODEL_ID = "anthropic.claude-v2"
DEFAULT_SCORE_MIN = 300
DEFAULT_SCORE_MAX = 850
