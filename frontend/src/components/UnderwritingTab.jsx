import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, TrendingDown, Info } from 'lucide-react';

export default function UnderwritingTab({ assessment }) {
  const positiveSignals = assessment?.positive_signals || [];
  const riskSignals = assessment?.risk_signals || [];

  // Format data for Recharts
  const chartData = [
    ...positiveSignals.map(([feature, score]) => ({
      name: feature.replace(/_/g, ' '),
      impact: score,
      type: 'positive',
    })),
    ...riskSignals.map(([feature, score]) => ({
      name: feature.replace(/_/g, ' '),
      impact: -score,
      type: 'risk',
    })),
  ];

  return (
    <div className="space-y-6">
      <div className="glass-panel rounded-2xl p-6 border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-100 font-['Outfit']">Feature Impact Attribution (SHAP)</h3>
            <p className="text-xs text-slate-400">Quantitative attribution of alternative behavioral signals on applicant creditworthiness.</p>
          </div>
        </div>

        <div className="h-64 w-full mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ top: 10, right: 30, left: 80, bottom: 10 }}>
              <XAxis type="number" stroke="#64748b" tickFormatter={(v) => Math.abs(v).toFixed(2)} />
              <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fontSize: 12 }} width={160} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                formatter={(value) => [Math.abs(value).toFixed(4), 'SHAP Value']}
              />
              <Bar dataKey="impact" radius={[4, 4, 4, 4]}>
                {chartData.map((entry, idx) => (
                  <Cell key={`cell-${idx}`} fill={entry.type === 'positive' ? '#10b981' : '#f43f5e'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Positive Drivers */}
        <div className="glass-panel rounded-2xl p-6 border border-emerald-500/20 bg-emerald-500/5">
          <div className="flex items-center gap-2 mb-4 text-emerald-400">
            <TrendingUp className="w-5 h-5" />
            <h4 className="font-bold text-slate-100 font-['Outfit']">Positive Credit Drivers</h4>
          </div>
          <div className="space-y-3">
            {positiveSignals.map(([feature, score], idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-emerald-500/20">
                <span className="text-sm font-medium text-slate-200 capitalize">{feature.replace(/_/g, ' ')}</span>
                <span className="text-xs font-bold font-mono px-2 py-1 rounded bg-emerald-500/10 text-emerald-400">
                  +{score.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Drivers */}
        <div className="glass-panel rounded-2xl p-6 border border-rose-500/20 bg-rose-500/5">
          <div className="flex items-center gap-2 mb-4 text-rose-400">
            <TrendingDown className="w-5 h-5" />
            <h4 className="font-bold text-slate-100 font-['Outfit']">Primary Risk Factors</h4>
          </div>
          <div className="space-y-3">
            {riskSignals.map(([feature, score], idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-rose-500/20">
                <span className="text-sm font-medium text-slate-200 capitalize">{feature.replace(/_/g, ' ')}</span>
                <span className="text-xs font-bold font-mono px-2 py-1 rounded bg-rose-500/10 text-rose-400">
                  +{score.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
