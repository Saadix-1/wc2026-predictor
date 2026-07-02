"""
simulator.py
------------
Monte Carlo bracket simulator for the 2026 FIFA World Cup.

Runs N tournament simulations from the current bracket state,
sampling match outcomes from the model's predicted probabilities.
Returns each team's championship probability.
"""

import random
import numpy as np
from collections import defaultdict
from app.ml.predict import predict_match
from app.data.wc2026_results import UPCOMING_MATCHES, COMPLETED_MATCHES, ROUND_ORDER


def simulate_single_match(team_a: str, team_b: str, stage: str) -> str:
    """
    Simulates one match. Returns the winner's name.
    In knockout rounds, draws are broken by a coin-flip penalty shootout
    weighted by Elo difference.
    """
    result = predict_match(team_a, team_b, stage=stage)
    r = random.random()

    if r < result["home_win_prob"]:
        return team_a
    elif r < result["home_win_prob"] + result["draw_prob"]:
        # Knockout: penalty shootout — slight edge to higher Elo
        elo_edge = (result["elo_a"] - result["elo_b"]) / 400.0
        p_a_wins_penalties = 0.5 + 0.1 * np.tanh(elo_edge)
        return team_a if random.random() < p_a_wins_penalties else team_b
    else:
        return team_b


def simulate_tournament(remaining_teams: list[str], current_round_idx: int = 0) -> str:
    """
    Simulates the entire remaining tournament from a given bracket state.
    Returns the name of the champion.
    """
    teams = list(remaining_teams)
    round_idx = current_round_idx

    while len(teams) > 1:
        stage = ROUND_ORDER[min(round_idx, len(ROUND_ORDER) - 1)]
        next_round = []
        random.shuffle(teams)  # Randomise bracket order for simulation variety

        for i in range(0, len(teams) - 1, 2):
            winner = simulate_single_match(teams[i], teams[i + 1], stage)
            next_round.append(winner)

        if len(teams) % 2 == 1:  # Bye — odd team advances (shouldn't happen in WC)
            next_round.append(teams[-1])

        teams = next_round
        round_idx += 1

    return teams[0]


def run_simulation(
    remaining_teams: list[str],
    current_round_idx: int = 0,
    iterations: int = 10_000,
) -> dict[str, float]:
    """
    Runs N Monte Carlo simulations and returns each team's
    probability of winning the tournament.

    Args:
        remaining_teams:   Teams still alive in the tournament
        current_round_idx: Index into ROUND_ORDER for the current round
        iterations:        Number of simulations to run

    Returns:
        Dict mapping team name → championship probability (0–1)
    """
    win_counts: dict[str, int] = defaultdict(int)

    for _ in range(iterations):
        champion = simulate_tournament(remaining_teams, current_round_idx)
        win_counts[champion] += 1

    # Convert to probabilities, sorted descending
    probs = {
        team: round(count / iterations, 4)
        for team, count in sorted(win_counts.items(), key=lambda x: -x[1])
    }

    # Fill in 0 for teams that never won
    for team in remaining_teams:
        if team not in probs:
            probs[team] = 0.0

    return probs
