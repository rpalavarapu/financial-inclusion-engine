import json
import sys
import os
from pathlib import Path

# Explicitly append root project path to Python's search path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import boto3
try:
    import streamlit as st
except ImportError:
    st = None

try:
    from config.settings import AWS_REGION, BEDROCK_MODEL_ID
except ModuleNotFoundError:
    AWS_REGION = "us-east-1"
    BEDROCK_MODEL_ID = "anthropic.claude-v2"

class BedrockExplainer:
    """Invokes AWS Bedrock to synthesize SHAP factors into regulatory-compliant letters."""
    def __init__(self):
        aws_key = None
        aws_secret = None
        
        # Check Streamlit Cloud Secrets first, then OS Environment Variables
        if st and hasattr(st, "secrets") and "AWS_ACCESS_KEY_ID" in st.secrets:
            aws_key = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret = st.secrets["AWS_SECRET_ACCESS_KEY"]
            region = st.secrets.get("AWS_DEFAULT_REGION", AWS_REGION)
        else:
            aws_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
            region = os.getenv("AWS_DEFAULT_REGION", AWS_REGION)

        try:
            if aws_key and aws_secret:
                self.client = boto3.client(
                    service_name="bedrock-runtime",
                    region_name=region,
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret
                )
            else:
                self.client = boto3.client(service_name="bedrock-runtime", region_name=region)
        except Exception:
            self.client = None

    def generate_explanation(self, assessment_result: dict) -> str:
        if not self.client:
            return f"Mock Bedrock Output: Score is {assessment_result['credit_score']}. Strong utility payment consistency was a key positive factor."

        prompt = f"""
        You are an ethical AI Credit Explanation Engine for an underserved underwriting platform.
        Synthesize the following score factors into a clear, 3-sentence explanation for the applicant.

        Applicant Score: {assessment_result['credit_score']}
        Positive Indicators: {assessment_result['positive_signals']}
        Risk Factors: {assessment_result['risk_signals']}

        Guidelines:
        1. Avoid complex financial jargon.
        2. Explain positive habits that boosted the score.
        3. Provide one actionable tip for improving credit eligibility.
        """

        body = json.dumps({
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 200,
            "temperature": 0.2
        })

        try:
            response = self.client.invoke_model(modelId=BEDROCK_MODEL_ID, body=body)
            result = json.loads(response.get("body").read())
            return result.get("completion", "").strip()
        except Exception as e:
            return f"Mock Bedrock Output: Score is {assessment_result['credit_score']}. Strong utility payment consistency was a key positive factor. (API Notice: {str(e)})"
