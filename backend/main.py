import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Tuple, Dict, Any, Optional

from src.model import DynamicRiskEngine
from src.bedrock_explainability import BedrockExplainer
from src.vector_search import SemanticApplicantMatcher
from src.fairness_audit import BiasFairnessAuditor

app = FastAPI(
    title="Financial Inclusion Underwriting API",
    description="Real-Time Dynamic Risk Assessment, Credit Risk Attribution & Regulatory Compliance API",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML engines
risk_engine = DynamicRiskEngine()
bedrock_explainer = BedrockExplainer()
semantic_matcher = SemanticApplicantMatcher()
fairness_auditor = BiasFairnessAuditor()

# Pydantic Schemas
class ApplicantSignals(BaseModel):
    utility_payment_consistency: float = Field(..., ge=0.0, le=1.0, example=0.88)
    monthly_recharge_frequency: float = Field(..., ge=0.0, le=1.0, example=0.75)
    wallet_cash_inflow_stability: float = Field(..., ge=0.0, le=1.0, example=0.62)
    gig_platform_payout_regularity: float = Field(..., ge=0.0, le=1.0, example=0.90)

class SignalFactor(BaseModel):
    feature: str
    impact_score: float

class AssessmentResponse(BaseModel):
    credit_score: int
    probability_of_default: float
    decision: str
    positive_signals: List[Tuple[str, float]]
    risk_signals: List[Tuple[str, float]]

class SemanticMatchItem(BaseModel):
    id: str
    similarity: float
    outcome: str
    note: str

class FairnessAuditResponse(BaseModel):
    disparate_impact_ratio: float
    is_compliant: bool
    status: str

class ExplanationResponse(BaseModel):
    explanation_text: str
    is_live_bedrock: bool
    last_model: str
    last_source: str
    last_error: str

class FullAssessmentResponse(BaseModel):
    applicant_signals: Dict[str, float]
    assessment: AssessmentResponse
    semantic_matches: List[SemanticMatchItem]
    fairness_audit: FairnessAuditResponse
    explanation: ExplanationResponse

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Financial Inclusion Underwriting API"}

@app.post("/api/evaluate", response_model=AssessmentResponse)
def evaluate_applicant(signals: ApplicantSignals):
    df = pd.DataFrame([signals.model_dump()])
    result = risk_engine.evaluate_applicant(df)
    score = result["credit_score"]
    decision = "APPROVED" if score >= 650 else "REJECTED"
    
    return AssessmentResponse(
        credit_score=result["credit_score"],
        probability_of_default=result["probability_of_default"],
        decision=decision,
        positive_signals=result["positive_signals"],
        risk_signals=result["risk_signals"]
    )

@app.post("/api/semantic-search", response_model=List[SemanticMatchItem])
def semantic_search(signals: ApplicantSignals):
    vector = np.array([
        signals.utility_payment_consistency,
        signals.monthly_recharge_frequency,
        signals.wallet_cash_inflow_stability,
        signals.gig_platform_payout_regularity
    ])
    similar_cases = semantic_matcher.find_similar_profiles(vector)
    return [SemanticMatchItem(**case) for case in similar_cases]

@app.get("/api/fairness-audit", response_model=FairnessAuditResponse)
def get_fairness_audit():
    audit_results = fairness_auditor.calculate_disparate_impact()
    return FairnessAuditResponse(**audit_results)

@app.post("/api/generate-explanation", response_model=ExplanationResponse)
def generate_explanation(signals: ApplicantSignals):
    df = pd.DataFrame([signals.model_dump()])
    assessment = risk_engine.evaluate_applicant(df)
    explanation_text = bedrock_explainer.generate_explanation(assessment)
    
    return ExplanationResponse(
        explanation_text=explanation_text,
        is_live_bedrock=bedrock_explainer.is_live,
        last_model=bedrock_explainer.last_model if bedrock_explainer.is_live else "local-ethical-synthesizer",
        last_source=bedrock_explainer.last_source,
        last_error=bedrock_explainer.last_error or ""
    )

@app.post("/api/full-assessment", response_model=FullAssessmentResponse)
def full_assessment(signals: ApplicantSignals):
    signals_dict = signals.model_dump()
    df = pd.DataFrame([signals_dict])
    
    # 1. Risk Evaluation
    assessment_raw = risk_engine.evaluate_applicant(df)
    score = assessment_raw["credit_score"]
    decision = "APPROVED" if score >= 650 else "REJECTED"
    assessment_resp = AssessmentResponse(
        credit_score=assessment_raw["credit_score"],
        probability_of_default=assessment_raw["probability_of_default"],
        decision=decision,
        positive_signals=assessment_raw["positive_signals"],
        risk_signals=assessment_raw["risk_signals"]
    )
    
    # 2. Semantic Search
    vector = np.array([
        signals.utility_payment_consistency,
        signals.monthly_recharge_frequency,
        signals.wallet_cash_inflow_stability,
        signals.gig_platform_payout_regularity
    ])
    similar_cases = semantic_matcher.find_similar_profiles(vector)
    semantic_matches = [SemanticMatchItem(**case) for case in similar_cases]
    
    # 3. Fairness Audit
    audit_results = fairness_auditor.calculate_disparate_impact()
    fairness_resp = FairnessAuditResponse(**audit_results)
    
    # 4. Bedrock Explanation
    explanation_text = bedrock_explainer.generate_explanation(assessment_raw)
    explanation_resp = ExplanationResponse(
        explanation_text=explanation_text,
        is_live_bedrock=bedrock_explainer.is_live,
        last_model=bedrock_explainer.last_model if bedrock_explainer.is_live else "local-ethical-synthesizer",
        last_source=bedrock_explainer.last_source,
        last_error=bedrock_explainer.last_error or ""
    )
    
    return FullAssessmentResponse(
        applicant_signals=signals_dict,
        assessment=assessment_resp,
        semantic_matches=semantic_matches,
        fairness_audit=fairness_resp,
        explanation=explanation_resp
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
