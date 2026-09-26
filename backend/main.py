import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Tuple, Dict, Any, Optional

from src.model import DynamicRiskEngine
from src.bedrock_explainability import BedrockExplainer
from src.vector_search import SemanticApplicantMatcher
from src.fairness_audit import BiasFairnessAuditor
from src.security import SecuritySanitizer
from src.guardrails import PromptGuardrails
from backend.auth import create_access_token, verify_token, TokenResponse
from backend.auth_db import user_db
from backend.logger import CloudWatchLoggingMiddleware

app = FastAPI(
    title="Financial Inclusion Underwriting Platform API",
    description="Real-Time Dynamic Risk Assessment, Bedrock LLM Explainability, Security Layer & JSON DB Auth API",
    version="2.1.0"
)

# Enable CloudWatch Logging Middleware & Security Headers
app.add_middleware(CloudWatchLoggingMiddleware)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML & Security engines
risk_engine = DynamicRiskEngine()
bedrock_explainer = BedrockExplainer()
semantic_matcher = SemanticApplicantMatcher()
fairness_auditor = BiasFairnessAuditor()

# Pydantic Schemas
class AuthRequest(BaseModel):
    username: str = Field(..., example="underwriter_demo")
    password: str = Field(..., example="secure123")

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, example="john_underwriter")
    email: str = Field(..., example="john@financialinclusion.com")
    password: str = Field(..., min_length=6, example="securePassword123")

class UserProfileResponse(BaseModel):
    username: str
    email: str
    role: str

class ApplicantSignals(BaseModel):
    utility_payment_consistency: float = Field(..., ge=0.0, le=1.0, example=0.88)
    monthly_recharge_frequency: float = Field(..., ge=0.0, le=1.0, example=0.75)
    wallet_cash_inflow_stability: float = Field(..., ge=0.0, le=1.0, example=0.62)
    gig_platform_payout_regularity: float = Field(..., ge=0.0, le=1.0, example=0.90)
    applicant_notes: Optional[str] = Field(None, description="Optional qualitative application notes evaluated by LLM Guardrails")

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
    guardrail_status: str

class SecurityStatusResponse(BaseModel):
    jwt_auth: str
    pii_redaction: str
    prompt_guardrails: str
    cloudwatch_logging: str
    audit_hash_algo: str
    json_user_db: str

class FullAssessmentResponse(BaseModel):
    applicant_signals: Dict[str, float]
    assessment: AssessmentResponse
    semantic_matches: List[SemanticMatchItem]
    fairness_audit: FairnessAuditResponse
    explanation: ExplanationResponse
    audit_certificate_hash: str
    authenticated_principal: str

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Financial Inclusion Underwriting API",
        "cloud_layer": "AWS App Runner / Docker Containerized",
        "security_layer": "JWT + Guardrails Active",
        "database": "data/users.json Active"
    }

@app.post("/api/auth/register", response_model=TokenResponse)
def register_user(req: RegisterRequest):
    """Creates a new user account, hashes credentials into data/users.json, and issues a JWT token."""
    try:
        user = user_db.register_user(req.username, req.email, req.password)
        token = create_access_token(subject=user["username"])
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=TokenResponse)
def login_for_access_token(auth_req: AuthRequest):
    """Verifies user credentials against hashed records in data/users.json and issues a JWT token."""
    user = user_db.verify_user(auth_req.username, auth_req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(subject=user["username"])
    return TokenResponse(access_token=token)

@app.get("/api/auth/me", response_model=UserProfileResponse)
def get_current_user(principal: dict = Depends(verify_token)):
    username = principal.get("sub", "guest_underwriter")
    user = user_db.get_user(username)
    email = user["email"] if user else "ab@mail.com"
    return UserProfileResponse(username=username, email=email, role=principal.get("role", "underwriter"))

@app.get("/api/security-status", response_model=SecurityStatusResponse)
def get_security_status(principal: dict = Depends(verify_token)):
    return SecurityStatusResponse(
        jwt_auth="ACTIVE (HMAC SHA-256)",
        pii_redaction="ENABLED (Regex Sanitization)",
        prompt_guardrails="ACTIVE (Injection Detection)",
        cloudwatch_logging="STREAMING (JSON Structured Audit)",
        audit_hash_algo="SHA-256 Cryptographic Proof",
        json_user_db="PERSISTED (data/users.json Salted Hashes)"
    )

@app.post("/api/evaluate", response_model=AssessmentResponse)
def evaluate_applicant(signals: ApplicantSignals, principal: dict = Depends(verify_token)):
    valid, errors = PromptGuardrails.validate_signal_ranges(signals.model_dump(exclude={"applicant_notes"}))
    if not valid:
        raise HTTPException(status_code=422, detail="; ".join(errors))

    df = pd.DataFrame([signals.model_dump(exclude={"applicant_notes"})])
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
def semantic_search(signals: ApplicantSignals, principal: dict = Depends(verify_token)):
    vector = np.array([
        signals.utility_payment_consistency,
        signals.monthly_recharge_frequency,
        signals.wallet_cash_inflow_stability,
        signals.gig_platform_payout_regularity
    ])
    similar_cases = semantic_matcher.find_similar_profiles(vector)
    return [SemanticMatchItem(**case) for case in similar_cases]

@app.get("/api/fairness-audit", response_model=FairnessAuditResponse)
def get_fairness_audit(principal: dict = Depends(verify_token)):
    audit_results = fairness_auditor.calculate_disparate_impact()
    return FairnessAuditResponse(**audit_results)

@app.post("/api/generate-explanation", response_model=ExplanationResponse)
def generate_explanation(signals: ApplicantSignals, principal: dict = Depends(verify_token)):
    guardrail_msg = "Safe"
    if signals.applicant_notes:
        safe, msg = PromptGuardrails.validate_prompt_safety(signals.applicant_notes)
        guardrail_msg = msg
        if not safe:
            raise HTTPException(status_code=400, detail=msg)

    df = pd.DataFrame([signals.model_dump(exclude={"applicant_notes"})])
    assessment = risk_engine.evaluate_applicant(df)
    explanation_text = bedrock_explainer.generate_explanation(assessment)
    masked_text = SecuritySanitizer.mask_pii_string(explanation_text)
    
    return ExplanationResponse(
        explanation_text=masked_text,
        is_live_bedrock=bedrock_explainer.is_live,
        last_model=bedrock_explainer.last_model if bedrock_explainer.is_live else "local-ethical-synthesizer",
        last_source=bedrock_explainer.last_source,
        last_error=bedrock_explainer.last_error or "",
        guardrail_status=guardrail_msg
    )

@app.post("/api/full-assessment", response_model=FullAssessmentResponse)
def full_assessment(signals: ApplicantSignals, principal: dict = Depends(verify_token)):
    signals_dict = signals.model_dump(exclude={"applicant_notes"})
    
    # 1. Guardrails Check
    valid, errors = PromptGuardrails.validate_signal_ranges(signals_dict)
    if not valid:
        raise HTTPException(status_code=422, detail="; ".join(errors))
        
    guardrail_msg = "Passed All Safety Guardrails"
    if signals.applicant_notes:
        safe, msg = PromptGuardrails.validate_prompt_safety(signals.applicant_notes)
        if not safe:
            raise HTTPException(status_code=400, detail=msg)
        guardrail_msg = msg

    df = pd.DataFrame([signals_dict])
    
    # 2. Risk Evaluation
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
    
    # 3. Semantic Search
    vector = np.array([
        signals.utility_payment_consistency,
        signals.monthly_recharge_frequency,
        signals.wallet_cash_inflow_stability,
        signals.gig_platform_payout_regularity
    ])
    similar_cases = semantic_matcher.find_similar_profiles(vector)
    semantic_matches = [SemanticMatchItem(**case) for case in similar_cases]
    
    # 4. Fairness Audit
    audit_results = fairness_auditor.calculate_disparate_impact()
    fairness_resp = FairnessAuditResponse(**audit_results)
    
    # 5. Bedrock Explanation + PII Sanitization
    explanation_text = bedrock_explainer.generate_explanation(assessment_raw)
    masked_text = SecuritySanitizer.mask_pii_string(explanation_text)
    
    explanation_resp = ExplanationResponse(
        explanation_text=masked_text,
        is_live_bedrock=bedrock_explainer.is_live,
        last_model=bedrock_explainer.last_model if bedrock_explainer.is_live else "local-ethical-synthesizer",
        last_source=bedrock_explainer.last_source,
        last_error=bedrock_explainer.last_error or "",
        guardrail_status=guardrail_msg
    )
    
    # 6. Audit Certificate Cryptographic SHA-256 Proof Hash
    cert_hash = SecuritySanitizer.generate_audit_hash({
        "signals": signals_dict,
        "score": score,
        "decision": decision,
        "dir": audit_results["disparate_impact_ratio"]
    })
    
    return FullAssessmentResponse(
        applicant_signals=signals_dict,
        assessment=assessment_resp,
        semantic_matches=semantic_matches,
        fairness_audit=fairness_resp,
        explanation=explanation_resp,
        audit_certificate_hash=cert_hash,
        authenticated_principal=principal.get("sub", "guest_underwriter")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
