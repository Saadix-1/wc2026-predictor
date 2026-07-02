import { useState } from 'react'
import { simulate } from '../api/client'
import { getFlag, pct } from '../utils/helpers'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const GOLD = '#f59e0b'
const COLORS = ['#f59e0b','#fbbf24','#34d399','#60a5fa','#a78bfa','#f87171','#94a3b8']

export default function SimulatorPanel() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [iterations, setIterations] = useState(10000)

  const handleSimulate = async () => {
    setLoading(true)
    try {
      const data = await simulate(iterations)
      setResults(data)
    } catch {
      alert('Simulation failed. Make sure the backend is running and model is trained.')
    } finally {
      setLoading(false)
    }
  }

  const chartData = results
    ? Object.entries(results.championship_probabilities)
        .filter(([, p]) => p > 0)
        .slice(0, 16)
        .map(([team, prob]) => ({ team: team.length > 10 ? team.slice(0,9)+'…' : team, fullName: team, prob: +(prob * 100).toFixed(1) }))
    : []

  return (
    <div>
      {/* Controls */}
      <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem', display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center' }}>
        <div style={{ flex: 1, minWidth: 200 }}>
          <label style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 6 }}>
            Simulations
          </label>
          <select value={iterations} onChange={e => setIterations(+e.target.value)}
            style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', padding: '0.5rem 0.8rem', fontSize: '0.9rem', width: '100%' }}>
            <option value={1000}>1,000 (fast)</option>
            <option value={10000}>10,000 (recommended)</option>
            <option value={50000}>50,000 (precise)</option>
          </select>
        </div>
        <button className="btn btn-primary" onClick={handleSimulate} disabled={loading} style={{ marginTop: 22 }}>
          {loading ? <><div className="spinner" style={{width:16,height:16}} /> Simulating…</> : '🎲 Run Simulation'}
        </button>
      </div>

      {/* Results */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
          <div className="spinner" style={{ width: 40, height: 40, margin: '0 auto 1rem', borderWidth: 3 }} />
          <p>Running {iterations.toLocaleString()} tournament simulations…</p>
        </div>
      )}

      {results && !loading && (
        <div className="fade-in">
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
            Based on <strong style={{ color: 'var(--text-primary)' }}>{results.iterations.toLocaleString()}</strong> simulated tournaments across{' '}
            <strong style={{ color: 'var(--text-primary)' }}>{results.teams_simulated}</strong> remaining teams.
          </p>

          {/* Bar chart */}
          <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
            <h3 style={{ marginBottom: '1.2rem', fontSize: '1rem' }}>🏆 Championship Probability</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={chartData} margin={{ left: -10 }}>
                <XAxis dataKey="team" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tickFormatter={v => `${v}%`} tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ background: '#0d1526', border: '1px solid rgba(245,158,11,0.3)', borderRadius: 8 }}
                  formatter={(v, _, { payload }) => [`${v}%`, payload.fullName]}
                  labelStyle={{ display: 'none' }}
                />
                <Bar dataKey="prob" radius={[4, 4, 0, 0]}>
                  {chartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Team cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '0.75rem' }}>
            {Object.entries(results.championship_probabilities)
              .filter(([, p]) => p > 0)
              .map(([team, prob], i) => (
                <div key={team} className="glass-card" style={{ padding: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span style={{ fontSize: '1.5rem', fontFamily: 'Bebas Neue', color: 'var(--text-muted)', width: 24, flexShrink: 0 }}>{i + 1}</span>
                  <span style={{ fontSize: '1.6rem' }}>{getFlag(team)}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{team}</div>
                    <div style={{ fontSize: '0.8rem', color: i === 0 ? 'var(--gold)' : 'var(--text-secondary)' }}>{pct(prob)} chance</div>
                  </div>
                  {i === 0 && <span style={{ fontSize: '1.2rem' }}>🏆</span>}
                </div>
              ))}
          </div>
        </div>
      )}

      {!results && !loading && (
        <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🎲</div>
          <p style={{ fontSize: '1.1rem' }}>Click "Run Simulation" to calculate each team's championship probability using Monte Carlo simulation.</p>
        </div>
      )}
    </div>
  )
}
