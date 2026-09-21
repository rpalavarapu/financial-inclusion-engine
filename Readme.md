# Financial Inclusion Underwriting Engine

An AI-powered, real-time credit underwriting platform designed to expand financial inclusion for thin-file and unbanked applicants using alternative behavioral signals. Powered by **FastAPI**, **LightGBM**, **SHAP**, **AWS Bedrock LLMs**, and a modern **React JS (Vite)** dashboard.

---

## System Architecture

```
                        ┌───────────────────────────────────────────┐
                        │             React JS Frontend             │
                        │    (Vite + TailwindCSS + Recharts/Lucide) │
                        └─────────────────────┬─────────────────────┘
                                              │ HTTP / JSON API
                                              ▼
                        ┌───────────────────────────────────────────┐
                        │              FastAPI Backend              │
                        │             (backend/main.py)             │
                        └──────┬──────────────┬──────────────┬──────┘
                               │              │              │
                               ▼              ▼              ▼
                     ┌───────────┐    ┌─────────────┐   ┌─────────────┐
                     │ LightGBM  │    │  AWS Bedrock│   │  Simulated  │
                     │  + SHAP   │    │ Mantle LLM  │   │  pgvector   │
                     │  Engine   │    │ Explainer   │   │  Matcher    │
                     └───────────┘    └─────────────┘   └─────────────┘
```

---

## Key Features

1. **Alternative Data Credit Scoring**: Evaluates non-traditional signals (Utility Payment Consistency, Mobile Recharge Frequency, Wallet Cash Inflow Stability, Gig Platform Payout Regularity) using LightGBM.
2. **SHAP Feature Impact Attribution**: Visualizes positive drivers and primary risk factors with interactive horizontal bar charts.
3. **Semantic Profile Retrieval (pgvector)**: Matches current applicant behavior against historical repayment records via cosine vector similarity.
4. **Demographic Parity & Algorithmic Fairness**: Audits Disparate Impact Ratios (DIR) under regulatory 80% rule compliance standards.
5. **AWS Bedrock Regulatory Disclosure**: Synthesizes transparent 3-sentence regulatory letters via AWS Bedrock Mantle LLMs (FCRA § 615 / ECOA Regulation B).
6. **Audit Export**: Interactive download button for timestamped JSON compliance audit certificates.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup (FastAPI)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI REST server
uvicorn backend.main:app --reload --port 8000
```

The REST API will be live at `http://127.0.0.1:8000` with interactive Swagger docs available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup (React JS)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

The React dashboard will be live at `http://localhost:5173`.

---

## API Endpoints

- `GET  /api/health`: Service health check
- `POST /api/evaluate`: Runs LightGBM risk scoring & SHAP factor attribution
- `POST /api/semantic-search`: Executes pgvector cosine similarity matching on historical profiles
- `GET  /api/fairness-audit`: Returns demographic disparate impact ratio & compliance status
- `POST /api/generate-explanation`: Generates FCRA/ECOA regulatory disclosure letter via AWS Bedrock
- `POST /api/full-assessment`: Aggregates all model outputs into a single payload for dashboard rendering

---

## Environment Variables

Create a `.env` file in the project root to configure live AWS Bedrock integration:

```env
AWS_BEARER_TOKEN_BEDROCK=your_aws_bedrock_api_key
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL_ID=zai.glm-4.7-flash
```
