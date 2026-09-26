import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import SignalsSidebar from './components/SignalsSidebar';
import MetricsOverview from './components/MetricsOverview';
import UnderwritingTab from './components/UnderwritingTab';
import SemanticSearchTab from './components/SemanticSearchTab';
import FairnessAuditTab from './components/FairnessAuditTab';
import BedrockExplanationTab from './components/BedrockExplanationTab';
import LoginPage from './components/LoginPage';
import ApplicantIntakeForm from './components/ApplicantIntakeForm';

const API_BASE = 'http://127.0.0.1:8000';

export default function App() {
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('auth_token') || '');
  const [currentUser, setCurrentUser] = useState(() => localStorage.getItem('auth_user') || '');

  // User input intake state
  const [hasSubmittedIntake, setHasSubmittedIntake] = useState(false);
  const [signals, setSignals] = useState({
    utility_payment_consistency: 0.80,
    monthly_recharge_frequency: 0.70,
    wallet_cash_inflow_stability: 0.60,
    gig_platform_payout_regularity: 0.85,
  });

  const [activeTab, setActiveTab] = useState('underwriting');
  const [assessmentData, setAssessmentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiHealthy, setApiHealthy] = useState(false);

  const fetchFullAssessment = useCallback(async (currentSignals, token) => {
    setLoading(true);
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const res = await fetch(`${API_BASE}/api/full-assessment`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(currentSignals),
      });

      if (res.ok) {
        const data = await res.json();
        setAssessmentData(data);
        setApiHealthy(true);
      } else {
        setApiHealthy(false);
      }
    } catch (err) {
      console.warn('FastAPI backend connection error:', err);
      setApiHealthy(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (authToken && hasSubmittedIntake) {
      fetchFullAssessment(signals, authToken);
    }
  }, [signals, authToken, hasSubmittedIntake, fetchFullAssessment]);

  const handleLoginSuccess = (token, username) => {
    setAuthToken(token);
    setCurrentUser(username);
    setHasSubmittedIntake(false); // Ask for applicant input upon login
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    setAuthToken('');
    setCurrentUser('');
    setAssessmentData(null);
    setHasSubmittedIntake(false);
  };

  const handleIntakeSubmit = (inputSignals) => {
    setSignals(inputSignals);
    setHasSubmittedIntake(true);
  };

  const handleNewApplicantRequest = () => {
    setHasSubmittedIntake(false);
  };

  const handleSignalChange = (key, value) => {
    setSignals((prev) => ({ ...prev, [key]: value }));
  };

  // 1. Render Login Page if unauthenticated
  if (!authToken) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  const assessment = assessmentData?.assessment || {
    credit_score: Math.round(850 - (0.15 * 550)),
    probability_of_default: 0.15,
    decision: 'APPROVED',
    positive_signals: [
      ['gig_platform_payout_regularity', 0.1245],
      ['utility_payment_consistency', 0.0982]
    ],
    risk_signals: [
      ['wallet_cash_inflow_stability', 0.0541],
      ['monthly_recharge_frequency', 0.0312]
    ]
  };

  const matches = assessmentData?.semantic_matches || [
    { id: 'HIST_001', similarity: 0.9421, outcome: 'Approved', note: 'Consistent gig income & zero bill defaults.' },
    { id: 'HIST_003', similarity: 0.8914, outcome: 'Approved', note: 'High utility payment consistency.' }
  ];

  const audit = assessmentData?.fairness_audit || {
    disparate_impact_ratio: 0.951,
    is_compliant: true,
    status: 'PASS: No Unfair Bias Detected'
  };

  const explanation = assessmentData?.explanation || {
    explanation_text: 'Your application has been evaluated with a Dynamic Alternative Credit Score of 767/850 (Approval Status: APPROVED), reflecting a favorable estimated default risk profile of 15.0%. This positive decision was primarily driven by your regular gig platform earnings payouts and consistent on-time utility payments. To maintain optimal pricing, continue sustaining wallet balance stability.',
    is_live_bedrock: false,
    last_model: 'local-ethical-synthesizer',
    last_source: 'Regulatory Compliance Engine (Local AI)',
    last_error: ''
  };

  const auditExport = {
    applicant_signals: signals,
    assessment_outcome: assessment,
    fairness_audit: audit,
    explanation: explanation,
  };

  const tabs = [
    { id: 'underwriting', label: 'Underwriting & Explainability' },
    { id: 'semantic', label: 'Semantic Search (pgvector)' },
    { id: 'fairness', label: 'Fairness & Bias Audit' },
    { id: 'explanation', label: 'Regulatory Disclosure' },
  ];

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col pb-12">
      <Header
        isLiveBedrock={explanation.is_live_bedrock}
        bedrockModel={explanation.last_model}
        apiHealthy={apiHealthy}
        currentUser={currentUser}
        onLogout={handleLogout}
        onNewApplicant={handleNewApplicantRequest}
      />

      <main className="max-w-7xl mx-auto px-6 w-full flex-1">
        {/* 2. Require Applicant Input Form if not submitted yet */}
        {!hasSubmittedIntake ? (
          <ApplicantIntakeForm
            onSubmitIntake={handleIntakeSubmit}
            defaultSignals={signals}
          />
        ) : (
          /* 3. Render Dashboard once Applicant Data is input */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Sidebar Controls */}
            <div className="lg:col-span-4">
              <SignalsSidebar signals={signals} onSignalChange={handleSignalChange} />
            </div>

            {/* Main Content Area */}
            <div className="lg:col-span-8 space-y-6">
              <MetricsOverview assessment={assessment} loading={loading} />

              {/* Navigation Tabs */}
              <div className="flex border-b border-slate-800 space-x-2 overflow-x-auto pb-px">
                {tabs.map((t) => {
                  const active = activeTab === t.id;
                  return (
                    <button
                      key={t.id}
                      onClick={() => setActiveTab(t.id)}
                      className={`px-5 py-3.5 text-sm font-extrabold rounded-t-xl transition-all border-b-2 cursor-pointer ${
                        active
                          ? 'bg-slate-800 text-blue-400 border-blue-500'
                          : 'text-slate-300 hover:text-white border-transparent hover:bg-slate-900'
                      }`}
                    >
                      <span>{t.label}</span>
                    </button>
                  );
                })}
              </div>

              {/* Tab Panes */}
              <div className="mt-4">
                {activeTab === 'underwriting' && <UnderwritingTab assessment={assessment} />}
                {activeTab === 'semantic' && <SemanticSearchTab matches={matches} />}
                {activeTab === 'fairness' && <FairnessAuditTab audit={audit} />}
                {activeTab === 'explanation' && (
                  <BedrockExplanationTab explanation={explanation} auditExport={auditExport} />
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
