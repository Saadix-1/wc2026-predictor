import { useState } from 'react'
import { getFlag, pct } from '../utils/helpers'
import { getAnalysis } from '../api/client'
import AnalysisModal from './AnalysisModal'

export default function MatchCard({ match, completed = false }) {
  const [analysis, setAnalysis] = useState(null)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)
  const [showModal, setShowModal] = useState(false)

  const pred = match.prediction
  const homeWin = pred?.home_win_prob ?? 0
  const draw    = pred?.draw_prob ?? 0
  const awayWin = pred?.away_win_prob ?? 0

  const handleAnalysis = async () => {
    if (analysis) { setShowModal(true); return }
    setLoadingAnalysis(true)
    try {
      const data = await getAnalysis(match.team_a, match.team_b)
      setAnalysis(data)
      setShowModal(true)
    } catch {
      alert('Analysis unavailable. Make sure the backend is running.')
    } finally {
      setLoadingAnalysis(false)
    }
  }

  return (
    <>
      <div className="glass-card match-card fade-in" style={{ padding: '1.5rem' }}>
        {/* Round + date */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
          <span className="badge badge-gray">{match.round}</span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{match.date}</span>
        </div>

        {/* Teams row */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', gap: '1rem', marginBottom: '1.4rem' }}>
          {/* Team A */}
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '0.3rem' }}>{getFlag(match.team_a)}</div>
            <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{match.team_a}</div>
            {completed && (
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--gold)', marginTop: '0.25rem' }}>
                {match.score_a}
              </div>
            )}
            {!completed && pred && (
              <div style={{ fontSize: '0.85rem', color: 'var(--green)', marginTop: '0.25rem', fontWeight: 600 }}>
                {pct(homeWin)}
              </div>
            )}
          </div>

          {/* Score / VS divider */}
          <div style={{ textAlign: 'center' }}>
            {completed ? (
              <div style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '8px', padding: '0.4rem 0.8rem' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem', display: 'block', marginBottom: 2, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Final</span>
                <span style={{ fontWeight: 800, fontSize: '1.1rem' }}>{match.score_a} – {match.score_b}</span>
                {match.penalty_winner && <span style={{ fontSize: '0.7rem', color: 'var(--gold)', display: 'block', textTransform: 'uppercase' }}>PEN</span>}
              </div>
            ) : (
              <span style={{ color: 'var(--text-muted)', fontWeight: 700, fontSize: '0.85rem' }}>vs</span>
            )}
          </div>

          {/* Team B */}
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '0.3rem' }}>{getFlag(match.team_b)}</div>
            <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{match.team_b}</div>
            {completed && (
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--gold)', marginTop: '0.25rem' }}>
                {match.score_b}
              </div>
            )}
            {!completed && pred && (
              <div style={{ fontSize: '0.85rem', color: 'var(--red)', marginTop: '0.25rem', fontWeight: 600 }}>
                {pct(awayWin)}
              </div>
            )}
          </div>
        </div>

        {/* Probability bars (upcoming only) */}
        {!completed && pred && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.2rem' }}>
            {[
              { label: match.team_a, val: homeWin, cls: 'win' },
              { label: 'Draw',       val: draw,    cls: 'draw' },
              { label: match.team_b, val: awayWin, cls: 'loss' },
            ].map(({ label, val, cls }) => (
              <div key={label} style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', width: 72, flexShrink: 0 }}>{label}</span>
                <div className="prob-bar-track" style={{ flex: 1 }}>
                  <div className={`prob-bar-fill ${cls}`} style={{ width: `${val * 100}%` }} />
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 600, width: 38, textAlign: 'right' }}>{pct(val)}</span>
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {completed ? (
            <span className="badge badge-gray">{match.winner} wins</span>
          ) : pred ? (
            <span className={`badge ${pred.confidence === 'high' ? 'badge-green' : pred.confidence === 'moderate' ? 'badge-gold' : 'badge-gray'}`}>
              {pred.confidence} confidence
            </span>
          ) : <span />}

          {!completed && (
            <button className="btn btn-secondary" style={{ padding: '0.4rem 0.9rem', fontSize: '0.8rem' }}
              onClick={handleAnalysis} disabled={loadingAnalysis}>
              {loadingAnalysis ? <><div className="spinner" style={{width:14,height:14}} /> Analyzing…</> : 'AI Analysis'}
            </button>
          )}
        </div>
      </div>

      {showModal && analysis && (
        <AnalysisModal analysis={analysis} onClose={() => setShowModal(false)} />
      )}
    </>
  )
}
