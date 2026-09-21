import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import json

from src.model import DynamicRiskEngine
from src.bedrock_explainability import BedrockExplainer
from src.vector_search import SemanticApplicantMatcher
from src.fairness_audit import BiasFairnessAuditor

# Page Setup
st.set_page_config(page_title="Financial Inclusion Underwriting Platform", layout="wide")

st.title("Financial Inclusion Underwriting Engine")
st.caption("Real-Time Dynamic Risk Assessment, Credit Risk Attribution & Regulatory Compliance")

# Sidebar - Feature Controls
st.sidebar.header("Applicant Behavioral Signals")
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

status = "APPROVED" if assessment["credit_score"] >= 650 else "REJECTED"
col3.metric("Underwriting Decision", status)

st.divider()

# Create Main Tabs for Advanced Evaluation
tab1, tab2, tab3 = st.tabs(["Underwriting & Explainability", "Semantic Search (pgvector)", "Fairness & Bias Audit"])

with tab1:
    st.subheader("Feature Impact Attribution (SHAP)")
    
    shap_factors = assessment["positive_signals"] + assessment["risk_signals"]
    shap_df = pd.DataFrame(shap_factors, columns=["Feature", "Impact Score"]).set_index("Feature")
    st.bar_chart(shap_df)
    
    st.write("**Top Key Factors:**")
    col_pos, col_neg = st.columns(2)
    with col_pos:
        for feat, score in assessment["positive_signals"]:
            st.success(f"**Positive Driver**: `{feat}` (+{score})")
    with col_neg:
        for feat, score in assessment["risk_signals"]:
            st.error(f"**Risk Driver**: `{feat}` (+{score})")

with tab2:
    st.subheader("Semantic Profile Retrieval (pgvector)")
    matcher = SemanticApplicantMatcher()
    input_vector = np.array([utility_score, recharge_freq, inflow_stability, gig_payout])
    similar_cases = matcher.find_similar_profiles(input_vector)
    
    for case in similar_cases:
        st.info(f"**Matched Historical Case:** `{case['id']}` | **Similarity:** {case['similarity']*100:.1f}%\n\n"
                f"**Outcome:** {case['outcome']} | **Note:** {case['note']}")

with tab3:
    st.subheader("Demographic Parity & Algorithmic Fairness")
    auditor = BiasFairnessAuditor()
    audit_results = auditor.calculate_disparate_impact()
    
    st.metric("Disparate Impact Ratio (DIR)", f"{audit_results['disparate_impact_ratio']} (Threshold >= 0.80)")
    if audit_results["is_compliant"]:
        st.success(f"{audit_results['status']} — Model adheres to regulatory fairness standards across demographic cohorts.")
    else:
        st.warning(f"{audit_results['status']} — Model requires demographic re-weighting.")

st.divider()

# Regulatory Transparency Letter Section
st.subheader("Regulatory Disclosure Statement")
explainer_bedrock = BedrockExplainer()
explanation_text = explainer_bedrock.generate_explanation(assessment)

# Status Badge
if explainer_bedrock.is_live:
    st.success(f"**Live AWS Bedrock Connected** — Model: `{explainer_bedrock.last_model}`")
else:
    st.info("**Synthesized via Regulatory Compliance Engine** (FCRA & ECOA Compliant)")

st.markdown(f"""
> **Official Underwriting Disclosure Statement:**
> 
> {explanation_text}
""")

# Expandable Cloud Diagnostics & Setup Guide
if not explainer_bedrock.is_live:
    with st.expander("AWS Bedrock Cloud Setup & Status Guide", expanded=False):
        if explainer_bedrock.last_error:
            st.markdown(f"**Current Bedrock Notice:** `{explainer_bedrock.last_error}`")
        st.markdown("""
        **To activate real-time Live AWS Bedrock generation:**
        1. **Model Access in AWS Console:** Open the **Amazon Bedrock Console** (region `us-east-1`). In the left navigation, click **Model access** -> **Modify model access**, check **Amazon Nova Micro** (or **Anthropic Claude 3 Haiku**), and submit. Access for Amazon models is granted immediately.
        2. **Streamlit Cloud Secrets:** In your Streamlit Cloud app settings under **Secrets**, ensure you have:
        ```toml
        AWS_BEARER_TOKEN_BEDROCK = "your_bedrock_api_key"
        AWS_DEFAULT_REGION = "us-east-1"
        BEDROCK_MODEL_ID = "amazon.nova-micro-v1:0"
        ```
        *(Or your standard AWS IAM `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`)*.
        """)

# Downloadable Audit Trail JSON
st.divider()
st.subheader("Regulatory Compliance Export")
audit_export = {
    "applicant_signals": applicant_data.to_dict(orient="records")[0],
    "assessment_outcome": assessment,
    "fairness_audit": audit_results,
    "explanation": {
        "text": explanation_text,
        "source": explainer_bedrock.last_source,
        "is_live_bedrock": explainer_bedrock.is_live,
        "model": explainer_bedrock.last_model if explainer_bedrock.is_live else "local-ethical-synthesizer"
    }
}
st.download_button(
    label="Download Compliance Certificate (JSON)",
    data=json.dumps(audit_export, indent=4),
    file_name="underwriting_audit_certificate.json",
    mime="application/json"
)

