import React, { useState } from 'react';

export default function LoginPage({ onLoginSuccess }) {
  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const endpoint = mode === 'login' ? '/api/auth/login' : '/api/auth/register';
    const payload = mode === 'login' 
      ? { username, password }
      : { username, email, password };

    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok && data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('auth_user', username);
        onLoginSuccess(data.access_token, username);
      } else {
        setError(data.detail || 'Authentication failed. Check credentials.');
      }
    } catch (err) {
      setError('Unable to connect to FastAPI authentication server.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    setUsername('underwriter_demo');
    setPassword('secure123');
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col justify-center items-center p-6">
      <div className="max-w-md w-full glass-panel rounded-2xl p-8 border border-slate-700 shadow-2xl space-y-6">
        
        {/* Header Title */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-extrabold text-white tracking-tight font-['Outfit']">
            Financial Inclusion Engine
          </h1>
          <p className="text-sm font-semibold text-slate-300">
            Enterprise Underwriting Portal Authentication
          </p>
        </div>

        {/* Mode Toggle Tabs */}
        <div className="grid grid-cols-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800">
          <button
            type="button"
            onClick={() => { setMode('login'); setError(''); }}
            className={`py-2 text-sm font-extrabold rounded-lg transition-colors cursor-pointer ${
              mode === 'login' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            SIGN IN
          </button>
          <button
            type="button"
            onClick={() => { setMode('register'); setError(''); }}
            className={`py-2 text-sm font-extrabold rounded-lg transition-colors cursor-pointer ${
              mode === 'register' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            CREATE ACCOUNT
          </button>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="p-3.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-bold text-center">
            {error}
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-extrabold text-slate-200 uppercase tracking-wider">Username</label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. underwriter_demo"
              className="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm font-semibold focus:outline-none focus:border-blue-500"
            />
          </div>

          {mode === 'register' && (
            <div className="space-y-1.5">
              <label className="text-xs font-extrabold text-slate-200 uppercase tracking-wider">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="ab@mail.com"
                className="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm font-semibold focus:outline-none focus:border-blue-500"
              />
            </div>
          )}

          <div className="space-y-1.5">
            <label className="text-xs font-extrabold text-slate-200 uppercase tracking-wider">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              className="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm font-semibold focus:outline-none focus:border-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-extrabold transition-all cursor-pointer shadow-lg shadow-blue-600/30"
          >
            {loading ? 'AUTHENTICATING...' : mode === 'login' ? 'SIGN IN TO DASHBOARD' : 'CREATE USER ACCOUNT'}
          </button>
        </form>

        {/* Demo Credentials Quick Fill */}
        <div className="pt-2 text-center border-t border-slate-800">
          <button
            type="button"
            onClick={handleDemoLogin}
            className="text-xs font-bold text-blue-400 hover:text-blue-300 underline cursor-pointer"
          >
            Fill Default Demo Credentials (underwriter_demo)
          </button>
        </div>

        {/* Security Note */}
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-semibold text-slate-400 text-center">
          Credentials stored as salted SHA-256 hashes in <code className="text-slate-200">data/users.json</code>.
        </div>
      </div>
    </div>
  );
}
