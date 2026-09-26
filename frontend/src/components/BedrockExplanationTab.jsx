import React, { useState } from 'react';
import { FileText, Cpu, ChevronDown, ChevronUp, Server, Download } from 'lucide-react';

export default function BedrockExplanationTab({ explanation, auditExport }) {
  const [showGuide, setShowGuide] = useState(false);

  const text = explanation?.explanation_text || '';
  const isLive = explanation?.is_live_bedrock || false;
  const model = explanation?.last_model || 'local-ethical-synthesizer';
  const source = explanation?.last_source || 'Regulatory Compliance Engine';
  const err = explanation?.last_error || '';

  const handleDownloadJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(auditExport, null, 4));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "underwriting_audit_certificate.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel rounded-xl p-6 border border-slate-800 space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-400" />
            <h3 className="text-base font-bold text-slate-100 font-['Outfit']">Regulatory Disclosure Statement</h3>
          </div>
          <div className="px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 border border-slate-700 text-slate-300 flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            <span>{isLive ? `AWS Bedrock (${model})` : 'Regulatory Engine'}</span>
          </div>
        </div>

        <div className="p-5 rounded-lg bg-slate-900/90 border border-slate-800 relative">
          <p className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold mb-3">FCRA § 615 & ECOA Regulation B Underwriting Disclosure</p>
          <blockquote className="text-sm text-slate-200 leading-relaxed font-serif border-l-2 border-blue-500 pl-4 py-1">
            "{text}"
          </blockquote>
          <div className="mt-4 pt-3 border-t border-slate-800 flex flex-wrap justify-between items-center text-xs text-slate-400">
            <span>Engine Source: <strong className="text-slate-200 font-mono">{source}</strong></span>
            <span>Governance Framework: <strong className="text-slate-200 font-mono">FCRA / ECOA Compliant</strong></span>
          </div>
        </div>

        {!isLive && (
          <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-900/40">
            <button
              onClick={() => setShowGuide(!showGuide)}
              className="w-full flex items-center justify-between p-4 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
            >
              <span className="flex items-center gap-2 text-slate-300">
                <Server className="w-4 h-4 text-blue-400" />
                AWS Bedrock Integration Details
              </span>
              {showGuide ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showGuide && (
              <div className="p-4 border-t border-slate-800 text-xs text-slate-300 space-y-3 bg-slate-900/80">
                {err && (
                  <p className="p-2.5 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400 font-mono">
                    Bedrock Status Notice: {err}
                  </p>
                )}
                <p className="font-semibold text-slate-200">AWS Bedrock Integration Setup:</p>
                <ol className="list-decimal list-inside space-y-1 text-slate-400">
                  <li>In AWS Console (<code className="text-slate-200">us-east-1</code>), verify model permissions for Amazon Nova or Claude 3.</li>
                  <li>Configure <code className="text-slate-200">AWS_BEARER_TOKEN_BEDROCK</code> in the root <code className="text-slate-200">.env</code> file.</li>
                  <li>FastAPI will automatically stream model output.</li>
                </ol>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Download Certificate Section */}
      <div className="glass-panel rounded-xl p-6 border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
          <h4 className="text-sm font-bold text-slate-100 font-['Outfit']">Regulatory Compliance Export</h4>
          <p className="text-xs text-slate-400">Export timestamped JSON certificate with cryptographic SHA-256 integrity hash.</p>
        </div>
        <button
          onClick={handleDownloadJSON}
          className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center gap-2 transition-colors cursor-pointer"
        >
          <Download className="w-4 h-4" />
          Export Audit Certificate (JSON)
        </button>
      </div>
    </div>
  );
}
