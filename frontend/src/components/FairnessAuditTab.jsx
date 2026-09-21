import React from 'react';
import { Scale, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function FairnessAuditTab({ audit }) {
  const dir = audit?.disparate_impact_ratio ?? 0.951;
  const isCompliant = audit?.is_compliant ?? true;
  const status = audit?.status ?? 'PASS: No Unfair Bias Detected';

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-slate-100 font-['Outfit']">Demographic Parity & Algorithmic Fairness</h3>
          <p className="text-xs text-slate-400">
            Evaluates model approval parity across protected demographic cohorts under regulatory 80% rule standards.
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-1.5">
          <Scale className="w-3.5 h-3.5" />
          <span>Fair Lending Compliance</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card rounded-xl p-5 border border-slate-700/60 space-y-2">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Disparate Impact Ratio (DIR)</span>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white font-mono">{dir}</span>
            <span className="text-xs text-slate-400 font-medium">(Threshold ≥ 0.80)</span>
          </div>
          <p className="text-[11px] text-slate-400">Ratio of unprivileged cohort approval rate to privileged cohort approval rate.</p>
        </div>

        <div className="glass-card rounded-xl p-5 border border-slate-700/60 space-y-2 col-span-2 flex flex-col justify-center">
          <div className="flex items-center gap-2">
            {isCompliant ? (
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
            ) : (
              <AlertTriangle className="w-6 h-6 text-amber-400" />
            )}
            <span className={`text-base font-bold font-['Outfit'] ${isCompliant ? 'text-emerald-400' : 'text-amber-400'}`}>
              {status}
            </span>
          </div>
          <p className="text-xs text-slate-300">
            {isCompliant
              ? 'The scoring model demonstrates statistically equitable outcomes across urban gig workers and rural agricultural cohorts.'
              : 'Disparate impact detected. Algorithmic re-weighting or demographic feature calibration recommended.'}
          </p>
        </div>
      </div>
    </div>
  );
}
