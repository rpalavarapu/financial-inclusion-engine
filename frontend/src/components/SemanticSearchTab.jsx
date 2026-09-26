import React from 'react';

export default function SemanticSearchTab({ matches }) {
  const cases = matches || [];

  return (
    <div className="glass-panel rounded-xl p-6 border border-slate-800 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-2">
        <div>
          <h3 className="text-xl font-extrabold text-white font-['Outfit']">Semantic Profile Retrieval (pgvector)</h3>
          <p className="text-sm font-semibold text-slate-300">
            Vector database retrieval matching qualitative cashflow behavior against historical repayment records.
          </p>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-bold self-start md:self-auto">
          pgvector Cosine Search
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {cases.map((c) => {
          const simPct = (c.similarity * 100).toFixed(1);
          const isApproved = c.outcome.toLowerCase() === 'approved';

          return (
            <div key={c.id} className="glass-card rounded-xl p-5 border border-slate-700 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-mono font-bold px-3 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">
                  {c.id}
                </span>
                <span className={`text-xs font-black px-3 py-1 rounded-lg ${
                  isApproved ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                }`}>
                  {c.outcome.toUpperCase()}
                </span>
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold mb-1.5">
                  <span className="text-slate-300">Cosine Similarity Score</span>
                  <span className="text-blue-400 font-mono text-sm">{simPct}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${simPct}%` }} />
                </div>
              </div>

              <div className="text-xs text-slate-200 font-semibold leading-relaxed bg-slate-900 p-3.5 rounded-lg border border-slate-800">
                <span className="font-extrabold text-slate-400">Historical Record:</span> "{c.note}"
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
