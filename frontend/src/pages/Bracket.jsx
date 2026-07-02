import { useState, useEffect } from 'react'
import { getBracket } from '../api/client'
import MatchCard from '../components/MatchCard'

export default function BracketPage() {
  const [bracket, setBracket] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [tab, setTab] = useState('upcoming')

  useEffect(() => {
    getBracket()
      .then(setBracket)
      .catch(() => setError('Could not load bracket. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  const tabs = [
    { key: 'upcoming',  label: '🔮 Upcoming', count: bracket?.total_upcoming },
    { key: 'completed', label: '✅ Completed', count: bracket?.total_completed },
  ]

  return (
    <div className="page">
      <div className="container">
        <div className="page-header">
          <h1 className="gradient-text">2026 WC Bracket</h1>
          <p>Live predictions for every remaining match, updated after each result.</p>
        </div>

        {/* Accuracy tracker */}
        {bracket && (
          <div className="glass-card fade-in" style={{ padding: '1rem 1.5rem', marginBottom: '2rem', display: 'flex', flexWrap: 'wrap', gap: '1.5rem', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Matches Predicted</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--gold)' }}>{bracket.total_upcoming}</div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Completed</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--green)' }}>{bracket.total_completed}</div>
            </div>
            <div style={{ marginLeft: 'auto' }}>
              <span className="badge badge-gold">🏆 WC 2026 USA</span>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
          {tabs.map(t => (
            <button key={t.key} className={`btn ${tab === t.key ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTab(t.key)}>
              {t.label} {t.count !== undefined && <span style={{ opacity: 0.7, fontSize: '0.8rem' }}>({t.count})</span>}
            </button>
          ))}
        </div>

        {loading && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(480px, 1fr))', gap: '1.5rem' }}>
            {[1,2,3,4].map(i => <div key={i} className="skeleton" style={{ height: 220, borderRadius: 'var(--radius-lg)' }} />)}
          </div>
        )}

        {error && (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--red)' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚠️</div>
            <p>{error}</p>
          </div>
        )}

        {bracket && !loading && (
          <div className="grid-2">
            {tab === 'upcoming' && bracket.upcoming.map(m => <MatchCard key={m.id} match={m} completed={false} />)}
            {tab === 'completed' && bracket.completed.map(m => <MatchCard key={m.id} match={m} completed={true} />)}
          </div>
        )}
      </div>
    </div>
  )
}
