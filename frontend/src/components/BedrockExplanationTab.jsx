import React, { useState } from 'react';
import { FileText, Cpu, ChevronDown, ChevronUp, Key, Cloud, Download } from 'lucide-react';

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
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-bold text-slate-100 font-['Outfit']">Regulatory Disclosure Statement</h3>
          </div>
          <div className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 border ${
            isLive ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-slate-800 text-slate-300 border-slate-700'
          }`}>
            <Cpu className="w-3.5 h-3.5" />
            <span>{isLive ? `Bedrock Mantle Live (${model})` : 'Local AI Regulatory Engine'}</span>
          </div>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 relative">
          <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2">Official FCRA & ECOA Compliance Disclosure</p>
          <blockquote className="text-sm md:text-base text-slate-200 leading-relaxed font-serif italic border-l-4 border-blue-500 pl-4 py-1">
            "{text}"
          </blockquote>
          <div className="mt-4 pt-3 border-t border-slate-800 flex flex-wrap justify-between items-center text-xs text-slate-400">
            <span>Synthesis Source: <strong className="text-slate-200 font-mono">{source}</strong></span>
            <span>Compliance Standard: <strong className="text-emerald-400">FCRA § 615 / ECOA Regulation B</strong></span>
          </div>
        </div>

        {!isLive && (
          <div className="border border-slate-800 rounded-xl overflow-hidden bg-slate-900/40">
            <button
              onClick={() => setShowGuide(!showGuide)}
              className="w-full flex items-center justify-between p-4 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
            >
              <span className="flex items-center gap-2 text-blue-400">
                <Cloud className="w-4 h-4" />
                AWS Bedrock Cloud Setup & Status Guide
              </span>
              {showGuide ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showGuide && (
              <div className="p-4 border-t border-slate-800 text-xs text-slate-300 space-y-3 bg-slate-900/80">
                {err && (
                  <p className="p-2.5 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400 font-mono">
                    Bedrock Notice: {err}
                  </p>
                )}
                <p className="font-semibold text-slate-200">To activate real-time AWS Bedrock Mantle LLM generation:</p>
                <ol className="list-decimal list-inside space-y-1 text-slate-400">
                  <li>In Amazon Bedrock Console (<code className="text-blue-300">us-east-1</code>), grant access to Amazon Nova Micro or Claude 3 Haiku.</li>
                  <li>Set environment variable <code className="text-blue-300">AWS_BEARER_TOKEN_BEDROCK="your_api_key"</code> in your <code className="text-blue-300">.env</code> file.</li>
                  <li>The FastAPI backend will automatically stream live Bedrock Mantle completions.</li>
                </ol>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Download Certificate Section */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
          <h4 className="font-bold text-slate-100 font-['Outfit']">Regulatory Compliance Export</h4>
          <p className="text-xs text-slate-400">Export timestamped underwriting audit trail certificate for legal compliance archives.</p>
        </div>
        <button
          onClick={handleDownloadJSON}
          className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-blue-600/30 transition-all hover:scale-105"
        >
          <Download className="w-4 h-4" />
          Download Compliance Certificate (JSON)
        </button>
      </div>
    </div>
  );
}
