import { NavLink } from 'react-router-dom'

export default function Header() {
  return (
    <nav className="nav">
      <div className="container nav-inner">
        <NavLink to="/" className="nav-logo">⚽ WC2026.AI</NavLink>
        <ul className="nav-links">
          <li><NavLink to="/" end className={({isActive}) => isActive ? 'active' : ''}>
            <span>🏠</span><span>Home</span>
          </NavLink></li>
          <li><NavLink to="/predict" className={({isActive}) => isActive ? 'active' : ''}>
            <span>🔮</span><span>Predict</span>
          </NavLink></li>
          <li><NavLink to="/bracket" className={({isActive}) => isActive ? 'active' : ''}>
            <span>🏟️</span><span>Bracket</span>
          </NavLink></li>
          <li><NavLink to="/simulator" className={({isActive}) => isActive ? 'active' : ''}>
            <span>🎲</span><span>Simulator</span>
          </NavLink></li>
        </ul>
      </div>
    </nav>
  )
}
