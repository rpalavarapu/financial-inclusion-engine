import React from 'react';
import { Award, AlertTriangle, CheckCircle2, XCircle } from 'lucide-react';

export default function MetricsOverview({ assessment, loading }) {
  const score = assessment?.credit_score || 0;
  const pd = assessment?.probability_of_default ? (assessment.probability_of_default * 100).toFixed(2) : '0.00';
  const decision = assessment?.decision || 'REJECTED';
  const isApproved = decision === 'APPROVED';

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
      {/* Metric 1: Credit Score */}
      <div className="glass-panel glass-card-hover rounded-2xl p-6 relative overflow-hidden">
        <div className="flex items-center justify-between mb-4">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Dynamic Credit Score</span>
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 border border-blue-500/20">
            <Award className="w-5 h-5" />
          </div>
        </div>

        <div className="flex items-baseline gap-2">
          <span className="text-4xl font-extrabold text-white font-['Outfit']">{loading ? '...' : score}</span>
          <span className="text-slate-400 text-sm font-semibold">/ 850</span>
        </div>

        <div className="w-full bg-slate-800 rounded-full h-2 mt-4 overflow-hidden">
          <div
            className="bg-gradient-to-r from-blue-500 to-emerald-400 h-2 rounded-full transition-all duration-500"
            style={{ width: `${Math.min(100, Math.max(0, ((score - 300) / 550) * 100))}%` }}
          />
        </div>
      </div>

      {/* Metric 2: Probability of Default */}
      <div className="glass-panel glass-card-hover rounded-2xl p-6 relative overflow-hidden">
        <div className="flex items-center justify-between mb-4">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Probability of Default (PD)</span>
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-5 h-5" />
          </div>
        </div>

        <div className="flex items-baseline gap-2">
          <span className="text-4xl font-extrabold text-white font-['Outfit']">{loading ? '...' : `${pd}%`}</span>
          <span className="text-slate-400 text-xs font-medium">Estimated Default Risk</span>
        </div>

        <p className="text-xs text-slate-400 mt-4">
          Calculated via LightGBM ensemble scoring on alternative behavioral cashflow signals.
        </p>
      </div>

      {/* Metric 3: Underwriting Decision */}
      <div className={`glass-panel glass-card-hover rounded-2xl p-6 relative overflow-hidden border ${
        isApproved ? 'border-emerald-500/30' : 'border-rose-500/30'
      }`}>
        <div className="flex items-center justify-between mb-4">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Underwriting Decision</span>
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center border ${
            isApproved
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
              : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
          }`}>
            {isApproved ? <CheckCircle2 className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className={`text-3xl font-extrabold tracking-wide font-['Outfit'] ${
            isApproved ? 'text-emerald-400' : 'text-rose-400'
          }`}>
            {loading ? '...' : decision}
          </span>
        </div>

        <p className="text-xs text-slate-400 mt-4">
          {isApproved ? 'Qualifies for automated algorithmic approval.' : 'Requires manual review or liquidity buildup.'}
        </p>
      </div>
    </div>
  );
}
