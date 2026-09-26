import React, { useState } from 'react';

export default function ApplicantIntakeForm({ onSubmitIntake, defaultSignals }) {
  const [utility, setUtility] = useState(defaultSignals?.utility_payment_consistency ?? 0.80);
  const [recharge, setRecharge] = useState(defaultSignals?.monthly_recharge_frequency ?? 0.70);
  const [inflow, setInflow] = useState(defaultSignals?.wallet_cash_inflow_stability ?? 0.60);
  const [gig, setGig] = useState(defaultSignals?.gig_platform_payout_regularity ?? 0.85);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmitIntake({
      utility_payment_consistency: parseFloat(utility),
      monthly_recharge_frequency: parseFloat(recharge),
      wallet_cash_inflow_stability: parseFloat(inflow),
      gig_platform_payout_regularity: parseFloat(gig),
    });
  };

  const handleSampleFill = (preset) => {
    if (preset === 'high') {
      setUtility(0.92);
      setRecharge(0.88);
      setInflow(0.85);
      setGig(0.95);
    } else if (preset === 'medium') {
      setUtility(0.75);
      setRecharge(0.68);
      setInflow(0.62);
      setGig(0.70);
    } else {
      setUtility(0.35);
      setRecharge(0.40);
      setInflow(0.30);
      setGig(0.25);
    }
  };

  return (
    <div className="max-w-2xl mx-auto glass-panel rounded-2xl p-8 border border-slate-700 shadow-2xl space-y-6">
      <div className="text-center space-y-2 border-b border-slate-800 pb-4">
        <h2 className="text-2xl font-extrabold text-white tracking-tight font-['Outfit']">
          New Applicant Risk Evaluation Intake
        </h2>
        <p className="text-sm font-semibold text-slate-300">
          Enter the applicant's alternative behavioral cashflow parameters to evaluate credit risk.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Utility Payment Consistency */}
          <div className="space-y-2 bg-slate-900 p-4 rounded-xl border border-slate-800">
            <div className="flex justify-between items-center">
              <label className="text-xs font-extrabold text-slate-200 uppercase">Utility Payment Consistency</label>
              <span className="text-xs font-mono font-black text-blue-400">{utility}</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={utility}
              onChange={(e) => setUtility(e.target.value)}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-[11px] font-semibold text-slate-400">On-time electricity, water & gas bill payments ratio</p>
          </div>

          {/* Monthly Recharge Frequency */}
          <div className="space-y-2 bg-slate-900 p-4 rounded-xl border border-slate-800">
            <div className="flex justify-between items-center">
              <label className="text-xs font-extrabold text-slate-200 uppercase">Monthly Recharge Frequency</label>
              <span className="text-xs font-mono font-black text-blue-400">{recharge}</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={recharge}
              onChange={(e) => setRecharge(e.target.value)}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-[11px] font-semibold text-slate-400">Mobile data & prepaid talktime recharge regularity</p>
          </div>

          {/* Wallet Cash Inflow Stability */}
          <div className="space-y-2 bg-slate-900 p-4 rounded-xl border border-slate-800">
            <div className="flex justify-between items-center">
              <label className="text-xs font-extrabold text-slate-200 uppercase">Wallet Inflow Stability</label>
              <span className="text-xs font-mono font-black text-blue-400">{inflow}</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={inflow}
              onChange={(e) => setInflow(e.target.value)}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-[11px] font-semibold text-slate-400">Digital wallet & UPI transaction flow variance</p>
          </div>

          {/* Gig Platform Payout Regularity */}
          <div className="space-y-2 bg-slate-900 p-4 rounded-xl border border-slate-800">
            <div className="flex justify-between items-center">
              <label className="text-xs font-extrabold text-slate-200 uppercase">Gig Payout Regularity</label>
              <span className="text-xs font-mono font-black text-blue-400">{gig}</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={gig}
              onChange={(e) => setGig(e.target.value)}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-[11px] font-semibold text-slate-400">E-commerce, ride-share & delivery income cadence</p>
          </div>
        </div>

        {/* Preset sample buttons */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800">
          <span className="text-xs font-extrabold text-slate-400">QUICK PRESETS:</span>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => handleSampleFill('high')}
              className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs font-extrabold text-emerald-400 border border-slate-700 cursor-pointer"
            >
              Prime Liquidity Profile
            </button>
            <button
              type="button"
              onClick={() => handleSampleFill('medium')}
              className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs font-extrabold text-blue-400 border border-slate-700 cursor-pointer"
            >
              Moderate Profile
            </button>
            <button
              type="button"
              onClick={() => handleSampleFill('low')}
              className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs font-extrabold text-rose-400 border border-slate-700 cursor-pointer"
            >
              Thin-File Risk Profile
            </button>
          </div>
        </div>

        <button
          type="submit"
          className="w-full py-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-base font-black transition-all cursor-pointer shadow-lg shadow-blue-600/30 tracking-wide"
        >
          EVALUATE APPLICANT RISK & GENERATE DISCLOSURE
        </button>
      </form>
    </div>
  );
}
