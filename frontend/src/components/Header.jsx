import React, { useState } from 'react';
import { ShieldCheck, Activity, Cpu, Sparkles, Lock } from 'lucide-react';
import SecurityBadgeModal from './SecurityBadgeModal';

export default function Header({ isLiveBedrock, bedrockModel, apiHealthy }) {
  const [showSecurityModal, setShowSecurityModal] = useState(false);

  return (
    <>
      <header className="glass-panel border-b border-slate-800 sticky top-0 z-40 px-6 py-4 mb-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <ShieldCheck className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-white via-slate-200 to-blue-300 bg-clip-text text-transparent font-['Outfit']">
                Financial Inclusion Underwriting Platform
              </h1>
              <p className="text-xs md:text-sm text-slate-400">
                Real-Time Dynamic Risk Assessment, Bedrock LLM Attribution & Security Layer
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Security Architecture Badge Button */}
            <button
              onClick={() => setShowSecurityModal(true)}
              className="px-3 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20 transition-all hover:scale-105 cursor-pointer"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Security & Cloud Layer</span>
            </button>

            {/* API Health Badge */}
            <div className={`px-3 py-1.5 rounded-full text-xs font-medium flex items-center gap-2 border ${
              apiHealthy 
                ? 'bg-blue-500/10 border-blue-500/30 text-blue-400' 
                : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
            }`}>
              <span className={`w-2 h-2 rounded-full ${apiHealthy ? 'bg-blue-400 animate-pulse' : 'bg-amber-400'}`} />
              <Activity className="w-3.5 h-3.5" />
              <span>FastAPI: {apiHealthy ? 'Connected' : 'Connecting...'}</span>
            </div>

            {/* Bedrock Status Badge */}
            <div className={`px-3 py-1.5 rounded-full text-xs font-medium flex items-center gap-2 border ${
              isLiveBedrock
                ? 'bg-purple-500/10 border-purple-500/30 text-purple-400'
                : 'bg-slate-800 border-slate-700 text-slate-300'
            }`}>
              <Cpu className="w-3.5 h-3.5 text-purple-400" />
              <span>{isLiveBedrock ? `AWS Bedrock Live (${bedrockModel})` : 'Local Regulatory Synthesizer'}</span>
              {isLiveBedrock && <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-spin" />}
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
