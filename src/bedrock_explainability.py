import json
import sys
import os
from pathlib import Path

# Explicitly append root project path to Python's search path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import boto3
try:
    import streamlit as st
except ImportError:
    st = None

try:
    from config import AWS_REGION, BEDROCK_MODEL_ID
except Exception:
    try:
        from config.settings import AWS_REGION, BEDROCK_MODEL_ID
    except Exception:
        AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0")

# Ensure model ID is not the retired Claude v2
if BEDROCK_MODEL_ID == "anthropic.claude-v2":
    BEDROCK_MODEL_ID = "amazon.nova-micro-v1:0"


class BedrockExplainer:
    """
    Invokes AWS Bedrock to synthesize SHAP factors into regulatory-compliant disclosure letters.
    Supports Amazon Bedrock API Key bearer token authentication (ABSK prefix),
    traditional AWS IAM SigV4 credentials, Bedrock Converse API, and an ethical fallback engine.
    """
    def __init__(self):
        self.is_live: bool = False
        self.last_model: str = ""
        self.last_source: str = ""
        self.last_error: str = ""
        self.client = None
        self.region = AWS_REGION
        self.preferred_model_id = BEDROCK_MODEL_ID

        # 1. Safely retrieve secrets from Streamlit Secrets or Environment Variables
        aws_key = None
        aws_secret = None
        bearer_token = None

        if st:
            try:
                secrets = getattr(st, "secrets", None)
                if secrets is not None:
                    aws_key = secrets.get("AWS_ACCESS_KEY_ID")
                    aws_secret = secrets.get("AWS_SECRET_ACCESS_KEY")
                    bearer_token = secrets.get("AWS_BEARER_TOKEN_BEDROCK") or secrets.get("BEDROCK_API_KEY")
                    self.region = secrets.get("AWS_DEFAULT_REGION", self.region)
                    self.preferred_model_id = secrets.get("BEDROCK_MODEL_ID", self.preferred_model_id)
            except Exception:
                # Outside Streamlit or missing secrets.toml
                pass

        aws_key = aws_key or os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = aws_secret or os.getenv("AWS_SECRET_ACCESS_KEY")
        bearer_token = bearer_token or os.getenv("AWS_BEARER_TOKEN_BEDROCK") or os.getenv("BEDROCK_API_KEY")
        self.region = os.getenv("AWS_DEFAULT_REGION", self.region)
        self.preferred_model_id = os.getenv("BEDROCK_MODEL_ID", self.preferred_model_id)

        # 2. Smart credential detection: Handle Bedrock API Keys (ABSK bearer token)
        # Bedrock API keys start with ABSK. When passed as secret or key, they are bearer tokens, NOT SigV4 keys.
        if aws_secret and aws_secret.startswith("ABSK"):
            bearer_token = aws_secret
            aws_key = None
            aws_secret = None
        elif aws_key and aws_key.startswith("ABSK"):
            bearer_token = aws_key
            aws_key = None
            aws_secret = None

        if bearer_token:
            os.environ["AWS_BEARER_TOKEN_BEDROCK"] = bearer_token
            # Remove dummy IAM keys from environment so boto3 doesn't attempt invalid SigV4
            if os.environ.get("AWS_ACCESS_KEY_ID", "").startswith("BedrockAPIKey"):
                os.environ.pop("AWS_ACCESS_KEY_ID", None)
                os.environ.pop("AWS_SECRET_ACCESS_KEY", None)

        # 3. Initialize Boto3 Bedrock Runtime Client
        try:
            if aws_key and aws_secret and (aws_key.startswith("AKIA") or aws_key.startswith("ASIA")):
                self.client = boto3.client(
                    service_name="bedrock-runtime",
                    region_name=self.region,
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret
                )
            else:
                self.client = boto3.client(
                    service_name="bedrock-runtime",
                    region_name=self.region
                )
        except Exception as e:
            self.client = None
            self.last_error = f"Client initialization error: {str(e)}"

    def _synthesize_local_explanation(self, assessment_result: dict) -> str:
        """
        Synthesizes a compliant, transparent 3-sentence regulatory adverse action or approval letter
        derived from objective behavioral signals and SHAP factor attribution under FCRA/ECOA principles.
        """
        score = assessment_result.get("credit_score", 650)
        pd_proba = assessment_result.get("probability_of_default", 0.15)
        pd_pct = round(pd_proba * 100, 1)
        is_approved = score >= 650

        feature_display = {
            "utility_payment_consistency": "consistent on-time utility payments",
            "monthly_recharge_frequency": "regular mobile recharge cadence",
            "wallet_cash_inflow_stability": "stable digital wallet cash inflows",
            "gig_platform_payout_regularity": "regular gig platform earnings payouts"
        }

        pos_signals = assessment_result.get("positive_signals", [])
        risk_signals = assessment_result.get("risk_signals", [])

        pos_phrases = [feature_display.get(f, f.replace('_', ' ')) for f, _ in pos_signals]
        risk_phrases = [feature_display.get(f, f.replace('_', ' ')) for f, _ in risk_signals]

        pos_desc = " and ".join(pos_phrases[:2]) if pos_phrases else "responsible alternative liquidity activity"
        risk_desc = " and ".join(risk_phrases[:2]) if risk_phrases else "periodic cashflow volatility"

        if is_approved:
            s1 = (
                f"Your application has been evaluated with a Dynamic Alternative Credit Score of {score}/850 (Approval Status: APPROVED), "
                f"reflecting a favorable estimated default risk profile of {pd_pct}%."
            )
            s2 = (
                f"This positive decision was primarily driven by your {pos_desc}, "
                f"which establishes strong recurring liquidity management outside legacy banking barriers."
            )
            s3 = (
                f"To maintain or further enhance your credit standing, continue sustaining {risk_desc}, "
                f"which will qualify your profile for prime underwriting rates under algorithmic fairness standards."
            )
        else:
            s1 = (
                f"Your application has been evaluated with a Dynamic Alternative Credit Score of {score}/850 (Status: ADDITIONAL REVIEW REQUIRED), "
                f"with an estimated default risk of {pd_pct}% under our unbanked inclusion model."
            )
            s2 = (
                f"While your profile demonstrated positive habits in {pos_desc}, "
                f"the primary factors limiting your tier were {risk_desc}."
            )
            s3 = (
                f"To achieve automatic approval, we recommend maintaining steady wallet balances and routine weekly recharges for 60 consecutive days "
                f"to bolster cashflow predictability under FCRA transparency guidelines."
            )

        return f"{s1} {s2} {s3}"

    def generate_explanation(self, assessment_result: dict) -> str:
        """
        Attempts live AWS Bedrock inference using the Converse API with automatic model fallback.
        Gracefully falls back to the deterministic ethical compliance engine if Bedrock model access is pending.
        """
        prompt = (
            f"You are an ethical AI Credit Explanation Engine for an underserved underwriting platform.\n"
            f"Synthesize the following score factors into a clear, 3-sentence regulatory transparency explanation for the applicant.\n\n"
            f"Applicant Score: {assessment_result.get('credit_score', 650)} / 850\n"
            f"Probability of Default: {assessment_result.get('probability_of_default', 0.10) * 100:.2f}%\n"
            f"Underwriting Decision: {'APPROVED' if assessment_result.get('credit_score', 650) >= 650 else 'ADDITIONAL REVIEW / REJECTED'}\n"
            f"Positive Drivers: {assessment_result.get('positive_signals', [])}\n"
            f"Risk Drivers: {assessment_result.get('risk_signals', [])}\n\n"
            f"Guidelines:\n"
            f"1. Avoid complex financial jargon.\n"
            f"2. Clearly explain positive habits that boosted the score.\n"
            f"3. Provide one actionable tip for improving credit eligibility.\n"
            f"4. Exactly 3 sentences."
        )

        candidate_models = [
            self.preferred_model_id,
            "amazon.nova-micro-v1:0",
            "us.amazon.nova-micro-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "us.anthropic.claude-3-haiku-20240307-v1:0",
            "amazon.titan-text-express-v1"
        ]
        # Remove duplicates and EOL models
        seen = set()
        clean_candidates = []
        for m in candidate_models:
            if m and m != "anthropic.claude-v2" and m not in seen:
                seen.add(m)
                clean_candidates.append(m)

        if self.client:
            for model_id in clean_candidates:
                try:
                    response = self.client.converse(
                        modelId=model_id,
                        messages=[{"role": "user", "content": [{"text": prompt}]}],
                        inferenceConfig={"maxTokens": 300, "temperature": 0.2}
                    )
                    content_list = response.get("output", {}).get("message", {}).get("content", [])
                    if content_list and "text" in content_list[0]:
                        output_text = content_list[0]["text"].strip()
                        if output_text:
                            self.is_live = True
                            self.last_model = model_id
                            self.last_source = f"AWS Bedrock Live ({model_id})"
                            self.last_error = ""
                            return output_text
                except Exception as e:
                    self.last_error = f"{type(e).__name__} ({model_id}): {str(e)}"
                    continue

        # If live Bedrock could not be reached or model access is pending, generate the compliant explanation
        self.is_live = False
        self.last_source = "Regulatory Compliance Engine (Local AI)"
        return self._synthesize_local_explanation(assessment_result)
