// Utility: team name → flag emoji
const FLAGS = {
  'Argentina': '🇦🇷', 'Australia': '🇦🇺', 'Belgium': '🇧🇪', 'Brazil': '🇧🇷',
  'Canada': '🇨🇦', 'Colombia': '🇨🇴', 'Croatia': '🇭🇷', 'Ecuador': '🇪🇨',
  'Egypt': '🇪🇬', 'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'France': '🇫🇷', 'Germany': '🇩🇪',
  'Hungary': '🇭🇺', 'Iran': '🇮🇷', 'Ivory Coast': '🇨🇮', 'Japan': '🇯🇵',
  'Mexico': '🇲🇽', 'Morocco': '🇲🇦', 'Netherlands': '🇳🇱', 'New Zealand': '🇳🇿',
  'Nigeria': '🇳🇬', 'Norway': '🇳🇴', 'Panama': '🇵🇦', 'Paraguay': '🇵🇾',
  'Peru': '🇵🇪', 'Portugal': '🇵🇹', 'Saudi Arabia': '🇸🇦', 'Senegal': '🇸🇳',
  'Serbia': '🇷🇸', 'South Korea': '🇰🇷', 'Spain': '🇪🇸', 'Sweden': '🇸🇪',
  'Switzerland': '🇨🇭', 'Ukraine': '🇺🇦', 'Uruguay': '🇺🇾', 'USA': '🇺🇸',
  'United States': '🇺🇸',
}
export const getFlag = (team) => FLAGS[team] || '🏳️'

// Confidence → badge class
export const confidenceBadge = (c) => ({ high: 'badge-green', moderate: 'badge-gold', low: 'badge-gray' }[c] || 'badge-gray')

// Format probability as percentage string
export const pct = (p) => `${(p * 100).toFixed(1)}%`
