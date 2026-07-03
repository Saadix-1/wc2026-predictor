"""
simulator.py
------------
Monte Carlo bracket simulator for the 2026 FIFA World Cup.

Runs N tournament simulations from the current bracket state,
sampling match outcomes using an on-demand (lazy) prediction cache
to maximize performance.
"""

import random
from collections import defaultdict
from app.ml.predict import predict_match
from app.data.wc2026_results import ROUND_ORDER


def get_match_prob_key(team_a: str, team_b: str, stage: str) -> str:
    # Key is alphabetical to handle order variations (e.g. France-Brazil vs Brazil-France)
    sorted_teams = sorted([team_a, team_b])
    return f"{sorted_teams[0]}_{sorted_teams[1]}_{stage}"


def simulate_single_match(team_a: str, team_b: str, stage: str, cache: dict) -> str:
    """Simulates one match using an on-demand (lazy) prediction cache."""
    key = get_match_prob_key(team_a, team_b, stage)
    
    # Lazy evaluation: compute prediction only when the match actually occurs for the first time
    if key not in cache:
        try:
            res = predict_match(team_a, team_b, stage=stage)
            cache[key] = {
                "team_a": team_a,
                "team_b": team_b,
                "home_win_prob": res["home_win_prob"],
                "draw_prob": res["draw_prob"],
                "away_win_prob": res["away_win_prob"],
                "elo_a": res["elo_a"],
                "elo_b": res["elo_b"]
            }
        except Exception:
            # Fallback if prediction fails
            cache[key] = {
                "team_a": team_a,
                "team_b": team_b,
                "home_win_prob": 0.4,
                "draw_prob": 0.2,
                "away_win_prob": 0.4,
                "elo_a": 1500,
                "elo_b": 1500
            }

    match_data = cache[key]
    is_home = (team_a == match_data["team_a"])
    p_win = match_data["home_win_prob"] if is_home else match_data["away_win_prob"]
    p_draw = match_data["draw_prob"]
    
    r = random.random()
    if r < p_win:
        return team_a
    elif r < p_win + p_draw:
        # Penalty shootout edge
        elo_a = match_data["elo_a"] if is_home else match_data["elo_b"]
        elo_b = match_data["elo_b"] if is_home else match_data["elo_a"]
        elo_edge = (elo_a - elo_b) / 400.0
        p_a_wins_penalties = 0.5 + 0.1 * (1.0 if elo_edge > 1 else -1.0 if elo_edge < -1 else elo_edge)
        return team_a if random.random() < p_a_wins_penalties else team_b
    else:
        return team_b


def simulate_tournament(remaining_teams: list[str], cache: dict, current_round_idx: int = 0) -> str:
    """Simulates the entire remaining tournament using the on-demand cache."""
    teams = list(remaining_teams)
    round_idx = current_round_idx

    while len(teams) > 1:
        stage = ROUND_ORDER[min(round_idx, len(ROUND_ORDER) - 1)]
        next_round = []
        random.shuffle(teams)

        for i in range(0, len(teams) - 1, 2):
            winner = simulate_single_match(teams[i], teams[i + 1], stage, cache)
            next_round.append(winner)

        if len(teams) % 2 == 1:
            next_round.append(teams[-1])

        teams = next_round
        round_idx += 1

    return teams[0]


def run_simulation(
    remaining_teams: list[str],
    current_round_idx: int = 0,
    iterations: int = 10_000,
) -> dict[str, float]:
    # Shared cache across all iterations
    cache = {}
    
    # Run simulations
    win_counts: dict[str, int] = defaultdict(int)
    for _ in range(iterations):
        champion = simulate_tournament(remaining_teams, cache, current_round_idx)
        win_counts[champion] += 1

    # Format results
    probs = {
        team: round(count / iterations, 4)
        for team, count in sorted(win_counts.items(), key=lambda x: -x[1])
    }

    for team in remaining_teams:
        if team not in probs:
            probs[team] = 0.0

    return probs
