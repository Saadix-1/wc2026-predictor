import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Home from './pages/Home'
import Predict from './pages/Predict'
import Bracket from './pages/Bracket'
import Simulator from './pages/Simulator'

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/"          element={<Home />} />
        <Route path="/predict"   element={<Predict />} />
        <Route path="/bracket"   element={<Bracket />} />
        <Route path="/simulator" element={<Simulator />} />
      </Routes>
    </BrowserRouter>
  )
}
