import React from 'react';
import { Sliders, Zap, Smartphone, Wallet, Briefcase } from 'lucide-react';

export default function SignalsSidebar({ signals, onSignalChange }) {
  const signalConfigs = [
    {
      key: 'utility_payment_consistency',
      label: 'Utility Payment Consistency',
      icon: Zap,
      color: 'text-amber-400',
      description: 'On-time electricity, water & gas bill payments ratio',
    },
    {
      key: 'monthly_recharge_frequency',
      label: 'Monthly Recharge Frequency',
      icon: Smartphone,
      color: 'text-blue-400',
      description: 'Mobile data & prepaid talktime recharge regularity',
    },
    {
      key: 'wallet_cash_inflow_stability',
      label: 'Wallet Cash Inflow Stability',
      icon: Wallet,
      color: 'text-emerald-400',
      description: 'Digital wallet & UPI transaction flow variance',
    },
    {
      key: 'gig_platform_payout_regularity',
      label: 'Gig Platform Payout Regularity',
      icon: Briefcase,
      color: 'text-purple-400',
      description: 'E-commerce, ride-share & delivery income cadence',
    },
  ];

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800">
      <div className="flex items-center gap-2 mb-6 pb-4 border-b border-slate-800">
        <Sliders className="w-5 h-5 text-blue-400" />
        <h2 className="text-lg font-bold text-slate-100 font-['Outfit']">Applicant Behavioral Signals</h2>
      </div>

      <div className="space-y-6">
        {signalConfigs.map((cfg) => {
          const Icon = cfg.icon;
          const val = signals[cfg.key];
          const pct = Math.round(val * 100);

          return (
            <div key={cfg.key} className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-200">
                  <Icon className={`w-4 h-4 ${cfg.color}`} />
                  {cfg.label}
                </label>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">
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
                className="w-full"
              />

              <p className="text-[11px] text-slate-400">{cfg.description}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-8 p-4 rounded-xl bg-blue-500/5 border border-blue-500/10 text-xs text-slate-300">
        <p className="font-semibold text-blue-400 mb-1">Alternative Data Underwriting</p>
        <p>Adjusting these signals dynamically re-evaluates the LightGBM default risk model, SHAP attributions, and regulatory letters in real-time.</p>
      </div>
    </div>
  );
}
