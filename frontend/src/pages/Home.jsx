import { Link } from 'react-router-dom'

const features = [
  { title: 'XGBoost + Elo Model', desc: 'Trained on 45,000+ historical matches. Uses Elo ratings, recent form, head-to-head records, and tournament stage.' },
  { title: 'Monte Carlo Simulator', desc: 'Run 10,000 tournament simulations to calculate each team\'s real probability of winning the World Cup.' },
  { title: 'AI Match Analysis', desc: 'GPT-4o-mini generates journalist-quality pre-match previews with key stats and matchup breakdown.' },
  { title: 'Live Bracket', desc: 'Every upcoming match with win probabilities. Updates as tournament results come in.' },
]

const stats = [
  { value: '45,000+', label: 'Historical Matches' },
  { value: '1872',    label: 'Data Since' },
  { value: 'XGBoost', label: 'Core Model' },
  { value: 'GPT-4o',  label: 'AI Engine' },
]

export default function Home() {
  return (
    <div className="page">
      <div className="container">

        {/* Hero */}
        <div style={{ textAlign: 'center', padding: '4rem 1rem 3rem', maxWidth: 700, margin: '0 auto' }} className="fade-in">
          <h1 style={{ marginBottom: '1rem' }}>
            <span className="gradient-text display-font" style={{ fontSize: 'clamp(2.5rem,7vw,5rem)' }}>
              WC2026.AI
            </span>
          </h1>
          <p style={{ fontSize: '1.15rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', lineHeight: 1.7 }}>
            AI-powered 2026 FIFA World Cup predictions.
          </p>
          <p style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '2rem', lineHeight: 1.7 }}>
            Machine learning meets the beautiful game. Real probabilities, not gut feelings.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/predict" className="btn btn-primary" style={{ fontSize: '1rem', padding: '0.85rem 2rem' }}>
              Predict a Match
            </Link>
            <Link to="/bracket" className="btn btn-secondary" style={{ fontSize: '1rem', padding: '0.85rem 2rem' }}>
              View Bracket
            </Link>
          </div>
        </div>

        {/* Stats bar */}
        <div className="glass-card fade-in" style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '0', marginBottom: '3rem', overflow: 'hidden' }}>
          {stats.map(({ value, label }, i) => (
            <div key={label} style={{ padding: '1.5rem', textAlign: 'center', borderRight: i < stats.length - 1 ? '1px solid var(--border)' : 'none' }}>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--gold)', fontFamily: 'Bebas Neue, sans-serif', letterSpacing: '0.05em' }}>{value}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 2 }}>{label}</div>
            </div>
          ))}
        </div>

        {/* Features grid */}
        <div className="grid-2" style={{ marginBottom: '3rem' }}>
          {features.map(({ title, desc }) => (
            <div key={title} className="glass-card fade-in" style={{ padding: '1.75rem' }}>
              <h3 style={{ marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--gold)' }}>{title}</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>{desc}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="glass-card" style={{ padding: '2.5rem', textAlign: 'center', background: 'rgba(245,158,11,0.04)', borderColor: 'var(--border-gold)' }}>
          <h2 style={{ marginBottom: '0.75rem' }}>Simulate the World Cup</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Run 10,000 tournament simulations and see which team the model picks to win it all.
          </p>
          <Link to="/simulator" className="btn btn-primary" style={{ fontSize: '1rem', padding: '0.85rem 2.5rem' }}>
            Run the Simulator
          </Link>
        </div>

      </div>
    </div>
  )
}
