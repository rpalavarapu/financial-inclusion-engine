import React from 'react';
import { Database, Search, ArrowUpRight, CheckCircle, XCircle } from 'lucide-react';

export default function SemanticSearchTab({ matches }) {
  const cases = matches || [];

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-slate-100 font-['Outfit']">Semantic Profile Retrieval (pgvector)</h3>
          <p className="text-xs text-slate-400">
            Vector database retrieval matching qualitative cashflow behavior against historical repayment records.
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5" />
          <span>pgvector Cosine Search</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cases.map((c) => {
          const simPct = (c.similarity * 100).toFixed(1);
          const isApproved = c.outcome.toLowerCase() === 'approved';

          return (
            <div key={c.id} className="glass-card rounded-xl p-5 border border-slate-700/60 glass-card-hover space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                  {c.id}
                </span>
                <span className={`text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1 ${
                  isApproved ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                }`}>
                  {isApproved ? <CheckCircle className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                  {c.outcome}
                </span>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Cosine Similarity Score</span>
                  <span className="font-bold text-blue-400 font-mono">{simPct}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${simPct}%` }} />
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                <span className="font-semibold text-slate-400">Historical Note:</span> "{c.note}"
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
