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

# ── Completed matches (add as they finish) ──────────────────────────────────
COMPLETED_MATCHES = [
    {
        "id": "r32_01", "round": "Round of 32",
        "team_a": "Brazil", "team_b": "Japan",
        "score_a": 2, "score_b": 1, "winner": "Brazil", "date": "2026-06-29"
    },
    {
        "id": "r32_02", "round": "Round of 32",
        "team_a": "Morocco", "team_b": "Netherlands",
        "score_a": 1, "score_b": 1, "winner": "Morocco",
        "penalty_winner": "Morocco", "date": "2026-06-29"
    },
    {
        "id": "r32_03", "round": "Round of 32",
        "team_a": "Germany", "team_b": "Paraguay",
        "score_a": 1, "score_b": 1, "winner": "Paraguay",
        "penalty_winner": "Paraguay", "date": "2026-06-29"
    },
    {
        "id": "r32_04", "round": "Round of 32",
        "team_a": "Canada", "team_b": "Serbia",
        "score_a": 2, "score_b": 0, "winner": "Canada", "date": "2026-06-29"
    },
    {
        "id": "r32_05", "round": "Round of 32",
        "team_a": "Argentina", "team_b": "Australia",
        "score_a": 3, "score_b": 0, "winner": "Argentina", "date": "2026-06-29"
    },
    {
        "id": "r32_06", "round": "Round of 32",
        "team_a": "Spain", "team_b": "Egypt",
        "score_a": 2, "score_b": 0, "winner": "Spain", "date": "2026-06-29"
    },
    {
        "id": "r32_07", "round": "Round of 32",
        "team_a": "England", "team_b": "Saudi Arabia",
        "score_a": 4, "score_b": 1, "winner": "England", "date": "2026-06-29"
    },
    {
        "id": "r32_08", "round": "Round of 32",
        "team_a": "Belgium", "team_b": "South Korea",
        "score_a": 1, "score_b": 0, "winner": "Belgium", "date": "2026-06-29"
    },
]

# ── Upcoming matches (will be predicted by the model) ────────────────────
UPCOMING_MATCHES = [
    # Remaining Round of 32 matches
    {
        "id": "r32_09", "round": "Round of 32",
        "team_a": "France", "team_b": "Sweden", "date": "2026-06-30",
        "venue": "New York/New Jersey"
    },
    {
        "id": "r32_10", "round": "Round of 32",
        "team_a": "Ivory Coast", "team_b": "Norway", "date": "2026-06-30",
        "venue": "Dallas"
    },
    {
        "id": "r32_11", "round": "Round of 32",
        "team_a": "Mexico", "team_b": "Ecuador", "date": "2026-06-30",
        "venue": "Mexico City"
    },
    {
        "id": "r32_12", "round": "Round of 32",
        "team_a": "Portugal", "team_b": "Iran", "date": "2026-06-30",
        "venue": "Miami"
    },
    {
        "id": "r32_13", "round": "Round of 32",
        "team_a": "Uruguay", "team_b": "Ukraine", "date": "2026-06-30",
        "venue": "Atlanta"
    },
    {
        "id": "r32_14", "round": "Round of 32",
        "team_a": "Colombia", "team_b": "USA", "date": "2026-06-30",
        "venue": "Los Angeles"
    },
    {
        "id": "r32_15", "round": "Round of 32",
        "team_a": "Senegal", "team_b": "Switzerland", "date": "2026-06-30",
        "venue": "Seattle"
    },
    {
        "id": "r32_16", "round": "Round of 32",
        "team_a": "Croatia", "team_b": "Hungary", "date": "2026-06-30",
        "venue": "Boston"
    },

    # Lined up Round of 16 matches (based on completed matches)
    {
        "id": "r16_01", "round": "Round of 16",
        "team_a": "Paraguay", "team_b": "Brazil", "date": "2026-07-04",
        "venue": "San Francisco"
    },
    {
        "id": "r16_02", "round": "Round of 16",
        "team_a": "Morocco", "team_b": "Canada", "date": "2026-07-04",
        "venue": "Houston"
    },
    {
        "id": "r16_03", "round": "Round of 16",
        "team_a": "Argentina", "team_b": "Spain", "date": "2026-07-05",
        "venue": "Philadelphia"
    },
    {
        "id": "r16_04", "round": "Round of 16",
        "team_a": "England", "team_b": "Belgium", "date": "2026-07-05",
        "venue": "Vancouver"
    },
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
