import React, { useState } from 'react';
import SecurityBadgeModal from './SecurityBadgeModal';

export default function Header({ isLiveBedrock, bedrockModel, apiHealthy, currentUser, onLogout, onNewApplicant }) {
  const [showSecurityModal, setShowSecurityModal] = useState(false);

  return (
    <>
      <header className="glass-panel border-b border-slate-800 sticky top-0 z-40 px-6 py-4 mb-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl md:text-2xl font-extrabold text-white tracking-tight font-['Outfit']">
              Financial Inclusion Underwriting Platform
            </h1>
            <p className="text-xs font-semibold text-slate-300 mt-1">
              Alternative Credit Scoring, SHAP Risk Attribution & Regulatory Disclosure Engine
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Evaluate New Applicant Button */}
            <button
              onClick={onNewApplicant}
              className="px-3 py-1.5 rounded-lg text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white transition-colors cursor-pointer"
            >
              + New Applicant Input
            </button>

            {/* User Profile & Logout */}
            <div className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 border border-slate-700 text-slate-200 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span>User: {currentUser || 'underwriter_demo'}</span>
              <button
                onClick={onLogout}
                className="ml-2 text-[11px] font-bold text-rose-400 hover:text-rose-300 underline cursor-pointer"
              >
                LOGOUT
              </button>
            </div>

            {/* Security Architecture Badge Button */}
            <button
              onClick={() => setShowSecurityModal(true)}
              className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-100 transition-colors cursor-pointer"
            >
              Security & Governance
            </button>

            {/* API Health Badge */}
            <div className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 border border-slate-700 text-slate-200 flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${apiHealthy ? 'bg-emerald-400' : 'bg-amber-400'}`} />
              <span>API: {apiHealthy ? 'Online' : 'Connecting...'}</span>
            </div>

            {/* Bedrock Status Badge */}
            <div className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 border border-slate-700 text-slate-200">
              <span>LLM Engine: {isLiveBedrock ? `AWS Bedrock (${bedrockModel})` : 'Regulatory Synthesizer'}</span>
            </div>
          </div>
        </div>
      </header>

      <SecurityBadgeModal
        isOpen={showSecurityModal}
        onClose={() => setShowSecurityModal(false)}
        apiHealthy={apiHealthy}
      />
    </>
  );
}
