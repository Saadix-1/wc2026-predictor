"""
wc2026_results.py
-----------------
Live 2026 FIFA World Cup bracket data.
Update the 'score' and 'winner' fields after each real match.
"""

# ── Teams in the tournament ──────────────────────────────────────────────
WC2026_TEAMS = [
    "Algeria", "Argentina", "Australia", "Austria", "Belgium", "Bosnia and Herzegovina",
    "Brazil", "Canada", "Cape Verde", "Colombia", "Croatia", "DR Congo", "Ecuador",
    "Egypt", "England", "France", "Germany", "Ghana", "Ivory Coast", "Japan",
    "Mexico", "Morocco", "Netherlands", "Norway", "Paraguay", "Portugal", "Senegal",
    "South Africa", "Spain", "Sweden", "Switzerland", "USA"
]

# ── Completed matches (Round of 32 & completed Round of 16) ─────────────
COMPLETED_MATCHES = [
    # --- Round of 32 ---
    {
        "id": "r32_01", "round": "Round of 32",
        "team_a": "Germany", "team_b": "Paraguay",
        "score_a": 1, "score_b": 1, "winner": "Paraguay",
        "penalty_winner": "Paraguay", "date": "2026-06-29"
    },
    {
        "id": "r32_02", "round": "Round of 32",
        "team_a": "France", "team_b": "Sweden",
        "score_a": 3, "score_b": 0, "winner": "France", "date": "2026-06-29"
    },
    {
        "id": "r32_03", "round": "Round of 32",
        "team_a": "South Africa", "team_b": "Canada",
        "score_a": 0, "score_b": 1, "winner": "Canada", "date": "2026-06-29"
    },
    {
        "id": "r32_04", "round": "Round of 32",
        "team_a": "Netherlands", "team_b": "Morocco",
        "score_a": 1, "score_b": 1, "winner": "Morocco",
        "penalty_winner": "Morocco", "date": "2026-06-29"
    },
    {
        "id": "r32_05", "round": "Round of 32",
        "team_a": "Portugal", "team_b": "Croatia",
        "score_a": 2, "score_b": 1, "winner": "Portugal", "date": "2026-06-29"
    },
    {
        "id": "r32_06", "round": "Round of 32",
        "team_a": "Spain", "team_b": "Austria",
        "score_a": 3, "score_b": 0, "winner": "Spain", "date": "2026-06-29"
    },
    {
        "id": "r32_07", "round": "Round of 32",
        "team_a": "USA", "team_b": "Bosnia and Herzegovina",
        "score_a": 2, "score_b": 0, "winner": "USA", "date": "2026-06-29"
    },
    {
        "id": "r32_08", "round": "Round of 32",
        "team_a": "Belgium", "team_b": "Senegal",
        "score_a": 3, "score_b": 2, "winner": "Belgium", "date": "2026-06-29"
    },
    {
        "id": "r32_09", "round": "Round of 32",
        "team_a": "Brazil", "team_b": "Japan",
        "score_a": 2, "score_b": 1, "winner": "Brazil", "date": "2026-06-29"
    },
    {
        "id": "r32_10", "round": "Round of 32",
        "team_a": "Ivory Coast", "team_b": "Norway",
        "score_a": 1, "score_b": 2, "winner": "Norway", "date": "2026-06-29"
    },
    {
        "id": "r32_11", "round": "Round of 32",
        "team_a": "Mexico", "team_b": "Ecuador",
        "score_a": 2, "score_b": 0, "winner": "Mexico", "date": "2026-06-29"
    },
    {
        "id": "r32_12", "round": "Round of 32",
        "team_a": "England", "team_b": "DR Congo",
        "score_a": 2, "score_b": 1, "winner": "England", "date": "2026-06-29"
    },
    {
        "id": "r32_13", "round": "Round of 32",
        "team_a": "Argentina", "team_b": "Cape Verde",
        "score_a": 3, "score_b": 2, "winner": "Argentina", "date": "2026-06-29"
    },
    {
        "id": "r32_14", "round": "Round of 32",
        "team_a": "Australia", "team_b": "Egypt",
        "score_a": 1, "score_b": 1, "winner": "Egypt",
        "penalty_winner": "Egypt", "date": "2026-06-29"
    },
    {
        "id": "r32_15", "round": "Round of 32",
        "team_a": "Switzerland", "team_b": "Algeria",
        "score_a": 2, "score_b": 0, "winner": "Switzerland", "date": "2026-06-29"
    },
    {
        "id": "r32_16", "round": "Round of 32",
        "team_a": "Colombia", "team_b": "Ghana",
        "score_a": 1, "score_b": 0, "winner": "Colombia", "date": "2026-06-29"
    },
    # --- Round of 16 Completed ---
    {
        "id": "r16_01", "round": "Round of 16",
        "team_a": "Paraguay", "team_b": "France",
        "score_a": 0, "score_b": 1, "winner": "France", "date": "2026-07-04"
    },
    {
        "id": "r16_02", "round": "Round of 16",
        "team_a": "Canada", "team_b": "Morocco",
        "score_a": 0, "score_b": 3, "winner": "Morocco", "date": "2026-07-04"
    },
    {
        "id": "r16_03", "round": "Round of 16",
        "team_a": "Brazil", "team_b": "Norway",
        "score_a": 1, "score_b": 2, "winner": "Norway", "date": "2026-07-04"
    },
    {
        "id": "r16_04", "round": "Round of 16",
        "team_a": "Mexico", "team_b": "England",
        "score_a": 2, "score_b": 3, "winner": "England", "date": "2026-07-04"
    }
]

# ── Upcoming matches (will be predicted by the model) ────────────────────
UPCOMING_MATCHES = [
    # Round of 16
    {
        "id": "r16_05", "round": "Round of 16",
        "team_a": "Portugal", "team_b": "Spain", "date": "2026-07-06",
        "venue": "Munich"
    },
    {
        "id": "r16_06", "round": "Round of 16",
        "team_a": "USA", "team_b": "Belgium", "date": "2026-07-06",
        "venue": "Stuttgart"
    },
    {
        "id": "r16_07", "round": "Round of 16",
        "team_a": "Argentina", "team_b": "Egypt", "date": "2026-07-07",
        "venue": "Frankfurt"
    },
    {
        "id": "r16_08", "round": "Round of 16",
        "team_a": "Switzerland", "team_b": "Colombia", "date": "2026-07-07",
        "venue": "Cologne"
    },
    # Quarterfinals Lined Up
    {
        "id": "qf_01", "round": "Quarterfinal",
        "team_a": "France", "team_b": "Morocco", "date": "2026-07-09",
        "venue": "Berlin"
    },
    {
        "id": "qf_03", "round": "Quarterfinal",
        "team_a": "Norway", "team_b": "England", "date": "2026-07-11",
        "venue": "Dusseldorf"
    }
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
