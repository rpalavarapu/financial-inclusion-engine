import React from 'react';

export default function SignalsSidebar({ signals, onSignalChange }) {
  const signalConfigs = [
    {
      key: 'utility_payment_consistency',
      label: 'Utility Payment Consistency',
      description: 'On-time electricity, water & gas bill payments ratio',
    },
    {
      key: 'monthly_recharge_frequency',
      label: 'Monthly Recharge Frequency',
      description: 'Mobile data & prepaid talktime recharge regularity',
    },
    {
      key: 'wallet_cash_inflow_stability',
      label: 'Wallet Cash Inflow Stability',
      description: 'Digital wallet & UPI transaction flow variance',
    },
    {
      key: 'gig_platform_payout_regularity',
      label: 'Gig Platform Payout Regularity',
      description: 'E-commerce, ride-share & delivery income cadence',
    },
  ];

  return (
    <div className="glass-panel rounded-xl p-6 border border-slate-800">
      <div className="mb-6 pb-4 border-b border-slate-800">
        <h2 className="text-xl font-extrabold text-white font-['Outfit'] tracking-tight">Alternative Behavioral Inputs</h2>
      </div>

      <div className="space-y-6">
        {signalConfigs.map((cfg) => {
          const val = signals[cfg.key];
          const pct = Math.round(val * 100);

          return (
            <div key={cfg.key} className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-bold text-slate-100">
                  {cfg.label}
                </label>
                <span className="text-sm font-extrabold px-2.5 py-1 rounded bg-slate-800 text-white border border-slate-700 font-mono">
                  {val.toFixed(2)} ({pct}%)
                </span>
              </div>

              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={val}
                onChange={(e) => onSignalChange(cfg.key, parseFloat(e.target.value))}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />

              <p className="text-xs font-semibold text-slate-300">{cfg.description}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-8 p-4 rounded-lg bg-slate-900 border border-slate-800 text-sm text-slate-200 space-y-1">
        <p className="font-extrabold text-white">Model Sensitivity Note</p>
        <p className="font-semibold text-slate-300">Modifying these inputs updates the credit risk model, SHAP attributions, and regulatory statements in real time.</p>
      </div>
    </div>
  );
}
