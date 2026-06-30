"""
wc2026_results.py
-----------------
Live 2026 FIFA World Cup bracket data.
Update the 'score' and 'winner' fields after each real match.
"""

# ── Teams still in the tournament as of June 30, 2026 ──────────────────────
WC2026_TEAMS = [
    "Argentina", "Australia", "Belgium", "Brazil", "Canada", "Colombia",
    "Croatia", "Ecuador", "Egypt", "England", "France", "Germany",
    "Hungary", "Iran", "Ivory Coast", "Japan", "Mexico", "Morocco",
    "Netherlands", "New Zealand", "Nigeria", "Norway", "Panama",
    "Paraguay", "Peru", "Portugal", "Saudi Arabia", "Senegal",
    "Serbia", "South Korea", "Spain", "Sweden", "Switzerland",
    "Ukraine", "Uruguay", "USA",
]

# ── Completed group-stage results (add as they finish) ────────────────────
# Format: { id, round, team_a, team_b, score_a, score_b, winner (or "draw"), date }
COMPLETED_MATCHES = [
    # Round of 32 results (examples — update with real scores)
    {
        "id": "r32_01", "round": "Round of 32",
        "team_a": "Brazil", "team_b": "Japan",
        "score_a": 2, "score_b": 1, "winner": "Brazil", "date": "2026-06-29"
    },
    {
        "id": "r32_02", "round": "Round of 32",
        "team_a": "Morocco", "team_b": "Netherlands",
        "score_a": 1, "score_b": 1, "winner": "Morocco",  # Morocco won on penalties
        "penalty_winner": "Morocco", "date": "2026-06-29"
    },
    {
        "id": "r32_03", "round": "Round of 32",
        "team_a": "Germany", "team_b": "Paraguay",
        "score_a": 1, "score_b": 1, "winner": "Paraguay",  # Paraguay won on penalties
        "penalty_winner": "Paraguay", "date": "2026-06-29"
    },
    {
        "id": "r32_04", "round": "Round of 32",
        "team_a": "Canada", "team_b": "Serbia",
        "score_a": 2, "score_b": 0, "winner": "Canada", "date": "2026-06-29"
    },
]

# ── Upcoming matches (will be predicted by the model) ────────────────────
UPCOMING_MATCHES = [
    {
        "id": "r32_05", "round": "Round of 32",
        "team_a": "Ivory Coast", "team_b": "Norway", "date": "2026-06-30",
        "venue": "Dallas"
    },
    {
        "id": "r32_06", "round": "Round of 32",
        "team_a": "France", "team_b": "Sweden", "date": "2026-06-30",
        "venue": "New York/New Jersey"
    },
    {
        "id": "r32_07", "round": "Round of 32",
        "team_a": "Mexico", "team_b": "Ecuador", "date": "2026-06-30",
        "venue": "Mexico City"
    },
    {
        "id": "r16_01", "round": "Round of 16",
        "team_a": "Canada", "team_b": "Morocco", "date": "2026-07-04",
        "venue": "Houston"
    },
    # Add more as the bracket unfolds...
]

# ── Round labels for display ───────────────────────────────────────────────
ROUND_ORDER = [
    "Round of 32",
    "Round of 16",
    "Quarterfinal",
    "Semifinal",
    "Final",
]

TOURNAMENT_STAGE_WEIGHT = {
    "Round of 32":  1.0,
    "Round of 16":  1.2,
    "Quarterfinal": 1.4,
    "Semifinal":    1.6,
    "Final":        2.0,
}
