import SimulatorPanel from '../components/SimulatorPanel'

export default function SimulatorPage() {
  return (
    <div className="page">
      <div className="container">
        <div className="page-header">
          <h1 className="gradient-text">Tournament Simulator</h1>
          <p>Run thousands of Monte Carlo simulations to calculate each team's real probability of lifting the trophy.</p>
        </div>
        <SimulatorPanel />
      </div>
    </div>
  )
}
