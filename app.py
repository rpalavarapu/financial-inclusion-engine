import sys
from pathlib import Path

# Explicitly add the project root directory to Python's module lookup path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from src.model import DynamicRiskEngine
from src.bedrock_explainability import BedrockExplainer

def main():
    print("=== Synchrony Hackathon: Dynamic Risk Assessment Engine ===")
    
    # Sample applicant profile using alternative behavioral signals
    applicant_data = pd.DataFrame([{
        "utility_payment_consistency": 0.88,
        "monthly_recharge_frequency": 0.75,
        "wallet_cash_inflow_stability": 0.62,
        "gig_platform_payout_regularity": 0.90
    }])

    # Step 1: Run Risk Scoring & SHAP Explainability
    engine = DynamicRiskEngine()
    assessment = engine.evaluate_applicant(applicant_data)
    
    print("\n--- Assessment Outcome ---")
    print(f"Dynamic Credit Score: {assessment['credit_score']}")
    print(f"Probability of Default: {assessment['probability_of_default']}")
    print(f"Positive Factors: {assessment['positive_signals']}")
    print(f"Risk Factors: {assessment['risk_signals']}")

    # Step 2: Generate Transparent Regulatory Letter via Bedrock
    explainer = BedrockExplainer()
    explanation = explainer.generate_explanation(assessment)
    
    print("\n--- Regulatory Transparency Output ---")
    print(explanation)

if __name__ == "__main__":
    main()
