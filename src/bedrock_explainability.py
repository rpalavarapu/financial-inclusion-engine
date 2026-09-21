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
        BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "zai.glm-4.7-flash")


MANTLE_ENDPOINT = "https://bedrock-mantle.us-east-1.api.aws/v1/chat/completions"

# Ordered list of available Mantle models to try, cheapest/fastest first
MANTLE_CANDIDATE_MODELS = [
    "zai.glm-4.7-flash",        # $0.07 / $0.40 per 1M tokens - fastest & cheapest
    "google.gemma-4-e2b",       # $0.04 / $0.08 per 1M tokens
    "nvidia.nemotron-nano-3-30b",
    "minimax.minimax-m2.5",
    "anthropic.claude-opus-4-7",
    "openai.gpt-5.6-luna",
]


class BedrockExplainer:
    """
    Invokes AWS Bedrock Mantle (OpenAI-compatible endpoint) to synthesize SHAP factors
    into regulatory-compliant disclosure letters.
    Falls back to an ethical FCRA/ECOA-compliant synthesis engine when Bedrock is unreachable.
    """
    def __init__(self):
        self.is_live: bool = False
        self.last_model: str = ""
        self.last_source: str = ""
        self.last_error: str = ""
        self.region = AWS_REGION
        self._bearer_token: str = ""

        # 1. Safely retrieve credentials from Streamlit Secrets or Environment Variables
        bearer_token = None
        aws_secret = None

        if st:
            try:
                secrets = getattr(st, "secrets", None)
                if secrets is not None:
                    bearer_token = secrets.get("AWS_BEARER_TOKEN_BEDROCK") or secrets.get("BEDROCK_API_KEY")
                    aws_secret = secrets.get("AWS_SECRET_ACCESS_KEY")
            except Exception:
                pass

        bearer_token = bearer_token or os.getenv("AWS_BEARER_TOKEN_BEDROCK") or os.getenv("BEDROCK_API_KEY")
        aws_secret = aws_secret or os.getenv("AWS_SECRET_ACCESS_KEY")

        # 2. Detect Bedrock API Keys (ABSK prefix) passed as the secret access key
        if aws_secret and aws_secret.startswith("ABSK"):
            bearer_token = bearer_token or aws_secret

        self._bearer_token = bearer_token or ""

    def _synthesize_local_explanation(self, assessment_result: dict) -> str:
        """
        Synthesizes a compliant, transparent 3-sentence regulatory disclosure letter
        from objective behavioral signals and SHAP factor attribution (FCRA/ECOA principles).
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
            return (
                f"Your application has been evaluated with a Dynamic Alternative Credit Score of {score}/850 "
                f"(Approval Status: APPROVED), reflecting a favorable estimated default risk profile of {pd_pct}%. "
                f"This positive decision was primarily driven by your {pos_desc}, which establishes strong recurring "
                f"liquidity management outside legacy banking barriers. "
                f"To maintain or further enhance your credit standing, continue sustaining {risk_desc}, "
                f"which will qualify your profile for prime underwriting rates under algorithmic fairness standards."
            )
        else:
            return (
                f"Your application has been evaluated with a Dynamic Alternative Credit Score of {score}/850 "
                f"(Status: ADDITIONAL REVIEW REQUIRED), with an estimated default risk of {pd_pct}% under our unbanked inclusion model. "
                f"While your profile demonstrated positive habits in {pos_desc}, "
                f"the primary factors limiting your tier were {risk_desc}. "
                f"To achieve automatic approval, we recommend maintaining steady wallet balances and routine weekly recharges "
                f"for 60 consecutive days to bolster cashflow predictability under FCRA transparency guidelines."
            )

    def generate_explanation(self, assessment_result: dict) -> str:
        """
        Calls Bedrock Mantle via OpenAI-compatible chat/completions API with model fallback.
        Falls back to the ethical synthesis engine if all models fail.
        """
        import requests as req

        prompt = (
            f"You are an ethical AI Credit Explanation Engine for an underserved underwriting platform. "
            f"Synthesize the following score factors into a clear, 3-sentence regulatory transparency explanation for the applicant.\n\n"
            f"Applicant Score: {assessment_result.get('credit_score', 650)} / 850\n"
            f"Probability of Default: {assessment_result.get('probability_of_default', 0.10) * 100:.2f}%\n"
            f"Decision: {'APPROVED' if assessment_result.get('credit_score', 650) >= 650 else 'ADDITIONAL REVIEW / REJECTED'}\n"
            f"Positive Drivers: {[f for f, _ in assessment_result.get('positive_signals', [])]}\n"
            f"Risk Drivers: {[f for f, _ in assessment_result.get('risk_signals', [])]}\n\n"
            f"Guidelines: Avoid jargon. Explain what boosted the score. Give one actionable tip. Exactly 3 sentences."
        )

        if not self._bearer_token:
            self.last_error = "No AWS Bedrock API key found. Set AWS_BEARER_TOKEN_BEDROCK in Streamlit Secrets or .env"
            self.last_source = "Regulatory Compliance Engine (Local AI)"
            return self._synthesize_local_explanation(assessment_result)

        headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "Content-Type": "application/json"
        }

        # Build candidate models: user preference first, then fallbacks
        preferred = os.getenv("BEDROCK_MODEL_ID", "zai.glm-4.7-flash")
        candidates = [preferred] + [m for m in MANTLE_CANDIDATE_MODELS if m != preferred]

        for model_id in candidates:
            try:
                payload = {
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 350,
                    "temperature": 0.3
                }
                response = req.post(MANTLE_ENDPOINT, headers=headers, json=payload, timeout=25)

                if response.status_code == 200:
                    result = response.json()
                    output_text = result["choices"][0]["message"]["content"].strip()
                    if output_text:
                        self.is_live = True
                        self.last_model = model_id
                        self.last_source = f"AWS Bedrock Mantle Live ({model_id})"
                        self.last_error = ""
                        return output_text
                else:
                    err_body = response.json().get("error", {})
                    err_msg = err_body.get("message", response.text[:200])
                    if response.status_code == 403:
                        self.last_error = f"Permission denied for '{model_id}': {err_msg}"
                    elif response.status_code == 404:
                        self.last_error = f"Model '{model_id}' not found on Mantle."
                    else:
                        self.last_error = f"HTTP {response.status_code} for '{model_id}': {err_msg}"
                    continue

            except Exception as e:
                self.last_error = f"Connection error for '{model_id}': {str(e)[:120]}"
                continue

        # All models failed — use ethical synthesis engine
        self.is_live = False
        self.last_source = "Regulatory Compliance Engine (Local AI)"
        return self._synthesize_local_explanation(assessment_result)
