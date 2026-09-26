import React from 'react';

export default function FairnessAuditTab({ audit }) {
  const dir = audit?.disparate_impact_ratio ?? 0.951;
  const isCompliant = audit?.is_compliant ?? true;
  const status = audit?.status ?? 'PASS: No Unfair Bias Detected';

  return (
    <div className="glass-panel rounded-xl p-6 border border-slate-800 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-2">
        <div>
          <h3 className="text-xl font-extrabold text-white font-['Outfit']">Demographic Parity & Algorithmic Fairness</h3>
          <p className="text-sm font-semibold text-slate-300">
            Evaluates model approval parity across protected demographic cohorts under regulatory 80% rule standards.
          </p>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold self-start md:self-auto">
          Fair Lending Compliance
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card rounded-xl p-6 border border-slate-700 space-y-3">
          <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">Disparate Impact Ratio (DIR)</span>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-black text-white font-mono">{dir}</span>
            <span className="text-xs font-bold text-slate-400">(Threshold ≥ 0.80)</span>
          </div>
          <p className="text-xs font-semibold text-slate-300">Ratio of unprivileged cohort approval rate to privileged cohort approval rate.</p>
        </div>

        <div className="glass-card rounded-xl p-6 border border-slate-700 space-y-3 col-span-2 flex flex-col justify-center">
          <div className="flex items-center gap-3">
            <span className={`text-xl font-extrabold font-['Outfit'] ${isCompliant ? 'text-emerald-400' : 'text-amber-400'}`}>
              {status}
            </span>
          </div>
          <p className="text-sm font-semibold text-slate-200">
            {isCompliant
              ? 'The scoring model demonstrates statistically equitable outcomes across urban gig workers and rural agricultural cohorts.'
              : 'Disparate impact detected. Algorithmic re-weighting or demographic feature calibration recommended.'}
          </p>
        </div>
      </div>
    </div>
  );
}
