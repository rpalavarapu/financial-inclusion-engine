import React from 'react';

export default function MetricsOverview({ assessment, loading }) {
  const score = assessment?.credit_score || 0;
  const pd = assessment?.probability_of_default ? (assessment.probability_of_default * 100).toFixed(2) : '0.00';
  const decision = assessment?.decision || 'REJECTED';
  const isApproved = decision === 'APPROVED';

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {/* Metric 1: Credit Score */}
      <div className="glass-panel rounded-xl p-6 relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-bold uppercase tracking-wider text-slate-300">Dynamic Credit Score</span>
        </div>

        <div className="flex items-baseline gap-2">
          <span className="text-5xl font-black text-white font-['Outfit']">{loading ? '...' : score}</span>
          <span className="text-slate-300 text-base font-bold">/ 850</span>
        </div>

        <div className="w-full bg-slate-800 rounded-full h-2.5 mt-4 overflow-hidden">
          <div
            className="bg-gradient-to-r from-blue-500 to-emerald-400 h-2.5 rounded-full transition-all duration-500"
            style={{ width: `${Math.min(100, Math.max(0, ((score - 300) / 550) * 100))}%` }}
          />
        </div>
      </div>

      {/* Metric 2: Probability of Default */}
      <div className="glass-panel rounded-xl p-6 relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-bold uppercase tracking-wider text-slate-300">Probability of Default (PD)</span>
        </div>

        <div className="flex items-baseline gap-2">
          <span className="text-5xl font-black text-white font-['Outfit']">{loading ? '...' : `${pd}%`}</span>
        </div>

        <p className="text-xs font-semibold text-slate-300 mt-4">
          Calculated via LightGBM ensemble scoring on alternative behavioral cashflow signals.
        </p>
      </div>

      {/* Metric 3: Underwriting Decision */}
      <div className={`glass-panel rounded-xl p-6 relative overflow-hidden border ${
        isApproved ? 'border-emerald-500/40 bg-emerald-500/5' : 'border-rose-500/40 bg-rose-500/5'
      }`}>
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-bold uppercase tracking-wider text-slate-300">Underwriting Decision</span>
        </div>

        <div className="flex items-center gap-3">
          <span className={`text-4xl font-black tracking-wide font-['Outfit'] ${
            isApproved ? 'text-emerald-400' : 'text-rose-400'
          }`}>
            {loading ? '...' : decision}
          </span>
        </div>

        <p className="text-xs font-semibold text-slate-300 mt-4">
          {isApproved ? 'Qualifies for automated algorithmic approval.' : 'Requires manual review or liquidity buildup.'}
        </p>
      </div>
    </div>
  );
}
