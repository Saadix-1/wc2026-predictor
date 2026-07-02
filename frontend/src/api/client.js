import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: BASE_URL, timeout: 30000 })

export const predictMatch = (teamA, teamB, stage = 'Round of 16') =>
  api.post('/api/predict', { team_a: teamA, team_b: teamB, stage }).then(r => r.data)

export const getBracket = () =>
  api.get('/api/bracket').then(r => r.data)

export const simulate = (iterations = 10000, remainingTeams = null) =>
  api.post('/api/simulate', { iterations, remaining_teams: remainingTeams }).then(r => r.data)

export const getAnalysis = (teamA, teamB) =>
  api.get(`/api/analysis/${encodeURIComponent(teamA)}/${encodeURIComponent(teamB)}`).then(r => r.data)

export const getEloRatings = () =>
  api.get('/api/elo').then(r => r.data)

export default api
