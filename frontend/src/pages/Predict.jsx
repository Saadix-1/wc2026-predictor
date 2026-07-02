import { useState } from 'react'
import { predictMatch, getAnalysis } from '../api/client'
import { getFlag, pct, confidenceBadge } from '../utils/helpers'
import AnalysisModal from '../components/AnalysisModal'

const WC_TEAMS = [
  'Argentina','Australia','Belgium','Brazil','Canada','Colombia','Croatia',
  'Ecuador','Egypt','England','France','Germany','Hungary','Iran','Ivory Coast',
  'Japan','Mexico','Morocco','Netherlands','New Zealand','Nigeria','Norway',
  'Panama','Paraguay','Peru','Portugal','Saudi Arabia','Senegal','Serbia',
  'South Korea','Spain','Sweden','Switzerland','Ukraine','Uruguay','USA',
]

const STAGES = ['Round of 32','Round of 16','Quarterfinal','Semifinal','Final']

export default function PredictPage() {
  const [teamA, setTeamA] = useState('France')
  const [teamB, setTeamB] = useState('Brazil')
  const [stage, setStage] = useState('Round of 16')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)
  const [showModal, setShowModal] = useState(false)

  const handlePredict = async () => {
    if (teamA === teamB) { alert('Please select two different teams.'); return }
    setLoading(true); setResult(null); setAnalysis(null)
    try {
      const data = await predictMatch(teamA, teamB, stage)
      setResult(data)
    } catch {
      alert('Prediction failed. Make sure the backend is running and model is trained.')
    } finally { setLoading(false) }
  }

  const handleAnalysis = async () => {
    setLoadingAnalysis(true)
    try {
      const data = await getAnalysis(teamA, teamB)
      setAnalysis(data); setShowModal(true)
    } catch { alert('Analysis unavailable.') }
    finally { setLoadingAnalysis(false) }
  }

  const selStyle = { background: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '0.7rem 1rem', fontSize: '0.95rem', width: '100%', cursor: 'pointer' }

  return (
    <div className="page">
      <div className="container" style={{ maxWidth: 680 }}>
        <div className="page-header">
          <h1 className="gradient-text">Match Predictor</h1>
          <p>Select any two teams and get an AI-powered outcome prediction.</p>
        </div>

        {/* Input card */}
        <div className="glass-card fade-in" style={{ padding: '2rem', marginBottom: '1.5rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '1rem', alignItems: 'end', marginBottom: '1.25rem' }}>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Team A</label>
              <div style={{ position: 'relative' }}>
                <span style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', fontSize: '1.2rem' }}>{getFlag(teamA)}</span>
                <select value={teamA} onChange={e => setTeamA(e.target.value)} style={{ ...selStyle, paddingLeft: '2.2rem' }}>
                  {WC_TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
            </div>
            <div style={{ textAlign: 'center', paddingBottom: 4, color: 'var(--text-muted)', fontWeight: 700 }}>VS</div>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Team B</label>
              <div style={{ position: 'relative' }}>
                <span style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', fontSize: '1.2rem' }}>{getFlag(teamB)}</span>
                <select value={teamB} onChange={e => setTeamB(e.target.value)} style={{ ...selStyle, paddingLeft: '2.2rem' }}>
                  {WC_TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
            </div>
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Tournament Stage</label>
            <select value={stage} onChange={e => setStage(e.target.value)} style={selStyle}>
              {STAGES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          <button className="btn btn-primary" onClick={handlePredict} disabled={loading} style={{ width: '100%', padding: '0.85rem', fontSize: '1rem' }}>
            {loading ? <><div className="spinner" style={{width:18,height:18}} /> Predicting…</> : '🔮 Predict Match'}
          </button>
        </div>

        {/* Result card */}
        {result && (
          <div className="glass-card fade-in" style={{ padding: '2rem' }}>
            {/* Winner banner */}
            <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 8 }}>Predicted Winner</div>
              <div style={{ fontSize: '3rem', marginBottom: 4 }}>{getFlag(result.predicted_winner)}</div>
              <div style={{ fontSize: '1.6rem', fontWeight: 800 }}>{result.predicted_winner}</div>
              <span className={`badge ${confidenceBadge(result.confidence)}`} style={{ marginTop: 8 }}>{result.confidence} confidence</span>
            </div>

            {/* Probability bars */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.75rem' }}>
              {[
                { label: `${getFlag(result.team_a)} ${result.team_a}`, val: result.home_win_prob, cls: 'win' },
                { label: '🤝 Draw',                                      val: result.draw_prob,     cls: 'draw' },
                { label: `${getFlag(result.team_b)} ${result.team_b}`,  val: result.away_win_prob, cls: 'loss' },
              ].map(({ label, val, cls }) => (
                <div key={label}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4, fontSize: '0.85rem' }}>
                    <span>{label}</span>
                    <span style={{ fontWeight: 700 }}>{pct(val)}</span>
                  </div>
                  <div className="prob-bar-track">
                    <div className={`prob-bar-fill ${cls}`} style={{ width: `${val * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>

            {/* Elo ratings */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1.5rem' }}>
              {[
                { label: `${result.team_a} Elo`, value: result.elo_a },
                { label: `${result.team_b} Elo`, value: result.elo_b },
              ].map(({ label, value }) => (
                <div key={label} style={{ background: 'rgba(245,158,11,0.06)', border: '1px solid var(--border-gold)', borderRadius: 'var(--radius-md)', padding: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: 2 }}>{label}</div>
                  <div style={{ fontWeight: 700, fontSize: '1.2rem', color: 'var(--gold)' }}>{value}</div>
                </div>
              ))}
            </div>

            <button className="btn btn-secondary" onClick={handleAnalysis} disabled={loadingAnalysis} style={{ width: '100%' }}>
              {loadingAnalysis ? <><div className="spinner" style={{width:16,height:16}} /> Generating…</> : '✨ Get AI Match Analysis'}
            </button>
          </div>
        )}
      </div>

      {showModal && analysis && <AnalysisModal analysis={analysis} onClose={() => setShowModal(false)} />}
    </div>
  )
}
