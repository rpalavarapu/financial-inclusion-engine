import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np

from src.model import DynamicRiskEngine
from src.bedrock_explainability import BedrockExplainer
from src.vector_search import SemanticApplicantMatcher

# Page Setup
st.set_page_config(page_title="AI Financial Inclusion Engine", layout="wide", page_icon="💳")

st.title("💳 AI-Powered Financial Inclusion Engine")
st.caption("Real-Time Dynamic Risk Assessment & Explainable AI for Underserved Segments")

# Sidebar - Feature Controls
st.sidebar.header("📊 Applicant Behavioral Signals")
utility_score = st.sidebar.slider("Utility Payment Consistency", 0.0, 1.0, 0.88, 0.01)
recharge_freq = st.sidebar.slider("Monthly Recharge Frequency", 0.0, 1.0, 0.75, 0.01)
inflow_stability = st.sidebar.slider("Wallet Cash Inflow Stability", 0.0, 1.0, 0.62, 0.01)
gig_payout = st.sidebar.slider("Gig Platform Payout Regularity", 0.0, 1.0, 0.90, 0.01)

# Construct Input Dataframe
applicant_data = pd.DataFrame([{
    "utility_payment_consistency": utility_score,
    "monthly_recharge_frequency": recharge_freq,
    "wallet_cash_inflow_stability": inflow_stability,
    "gig_platform_payout_regularity": gig_payout
}])

# Execute ML Scoring Engine
engine = DynamicRiskEngine()
assessment = engine.evaluate_applicant(applicant_data)

# Layout: Top Key Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Dynamic Credit Score", f"{assessment['credit_score']} / 850")
col2.metric("Probability of Default (PD)", f"{assessment['probability_of_default'] * 100:.2f}%")

status = "APPROVED ✅" if assessment["credit_score"] >= 650 else "REJECTED ❌"
col3.metric("Underwriting Decision", status)

st.divider()

# Layout: Explainability & Vector Search Columns
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🔍 Explainable AI (SHAP Impact Attribution)")
    
    # Feature Impact Native Streamlit Bar Chart
    shap_factors = assessment["positive_signals"] + assessment["risk_signals"]
    shap_df = pd.DataFrame(shap_factors, columns=["Feature", "Impact Score"]).set_index("Feature")
    st.bar_chart(shap_df)
    
    st.write("**Top Drivers:**")
    for feat, score in assessment["positive_signals"]:
        st.write(f"🟢 **Positive Impact**: `{feat}` (+{score})")
    for feat, score in assessment["risk_signals"]:
        st.write(f"🔴 **Risk Impact**: `{feat}` (+{score})")

with right_col:
    st.subheader("🌐 Semantic Profile Retrieval (pgvector)")
    matcher = SemanticApplicantMatcher()
    input_vector = np.array([utility_score, recharge_freq, inflow_stability, gig_payout])
    similar_cases = matcher.find_similar_profiles(input_vector)
    
    for case in similar_cases:
        st.info(f"**Matched Historical Case:** `{case['id']}`\n\n"
                f"**Similarity Score:** {case['similarity']*100:.1f}%\n\n"
                f"**Outcome:** {case['outcome']}\n\n"
                f"**Profile Note:** {case['note']}")

st.divider()

# Regulatory Transparency Letter Section
st.subheader("📜 AWS Bedrock Regulatory Transparency Output")
explainer_bedrock = BedrockExplainer()
explanation_text = explainer_bedrock.generate_explanation(assessment)
st.success(explanation_text)
