"""
elo.py
------
Custom Elo rating engine tuned for international football.

Key design decisions vs. off-the-shelf libraries:
- Football-specific K-factor: varies by tournament prestige
- Draw handling: both teams get partial credit
- Margin of victory multiplier: 3-0 win ≠ 1-0 win
- Home advantage: explicit +100 Elo offset when not at neutral venue
"""

import pandas as pd
import numpy as np
from typing import Optional


# ── Constants ─────────────────────────────────────────────────────────────
BASE_ELO = 1500
HOME_ADVANTAGE = 100  # Elo points added to home team's effective rating

# K-factor by tournament type (how much each match shifts ratings)
K_FACTORS = {
    "FIFA World Cup": 60,
    "FIFA World Cup qualification": 40,
    "Confederations Cup": 50,
    "UEFA Euro": 50,
    "Copa America": 50,
    "AFC Asian Cup": 50,
    "Africa Cup of Nations": 50,
    "Gold Cup": 40,
    "friendly": 20,
    "default": 30,
}


class EloRatingSystem:
    """
    Tracks and updates Elo ratings for all international football teams.
    Processes historical match data chronologically to compute current ratings.
    """

    def __init__(self, base_elo: float = BASE_ELO):
        self.base_elo = base_elo
        self.ratings: dict[str, float] = {}

    def get_rating(self, team: str) -> float:
        """Returns current Elo rating, initialising to base if unseen."""
        return self.ratings.get(team, self.base_elo)

    def _get_k_factor(self, tournament: str) -> float:
        """Maps tournament name to appropriate K-factor."""
        tournament_lower = tournament.lower()
        for key, k in K_FACTORS.items():
            if key.lower() in tournament_lower:
                return k
        return K_FACTORS["default"]

    def _expected_score(self, rating_a: float, rating_b: float) -> float:
        """Standard Elo expected score for team A against team B."""
        return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))

    def _actual_score(
        self,
        home_goals: int,
        away_goals: int,
        outcome: str  # "home" | "away" | "draw"
    ) -> tuple[float, float]:
        """
        Returns (score_home, score_away) where:
        - Win  = 1.0
        - Draw = 0.5
        - Loss = 0.0
        """
        if outcome == "home":
            return 1.0, 0.0
        elif outcome == "away":
            return 0.0, 1.0
        else:
            return 0.5, 0.5

    def _goal_difference_multiplier(self, goal_diff: int) -> float:
        """
        Weights larger victories more heavily.
        Formula based on World Football Elo Ratings methodology.
        """
        gd = abs(goal_diff)
        if gd <= 1:
            return 1.0
        elif gd == 2:
            return 1.5
        else:
            return (11 + gd) / 8.0

    def update(
        self,
        home_team: str,
        away_team: str,
        home_score: int,
        away_score: int,
        tournament: str,
        neutral: bool = False,
    ) -> tuple[float, float]:
        """
        Processes a single match result and updates ratings.
        Returns (new_home_rating, new_away_rating).
        """
        # Effective ratings (home gets advantage unless neutral venue)
        r_home = self.get_rating(home_team)
        r_away = self.get_rating(away_team)
        r_home_eff = r_home + (0 if neutral else HOME_ADVANTAGE)

        # Expected outcomes
        e_home = self._expected_score(r_home_eff, r_away)
        e_away = 1.0 - e_home

        # Actual outcomes
        if home_score > away_score:
            s_home, s_away = 1.0, 0.0
        elif home_score < away_score:
            s_home, s_away = 0.0, 1.0
        else:
            s_home, s_away = 0.5, 0.5

        # K-factor and goal difference multiplier
        k = self._get_k_factor(tournament)
        gd_mult = self._goal_difference_multiplier(home_score - away_score)

        # New ratings
        new_r_home = r_home + k * gd_mult * (s_home - e_home)
        new_r_away = r_away + k * gd_mult * (s_away - e_away)

        self.ratings[home_team] = new_r_home
        self.ratings[away_team] = new_r_away

        return new_r_home, new_r_away

    def fit_historical(self, df: pd.DataFrame) -> "EloRatingSystem":
        """
        Processes an entire historical results DataFrame chronologically.
        
        Expected columns:
            date, home_team, away_team, home_score, away_score, tournament, neutral
        """
        df = df.sort_values("date").reset_index(drop=True)

        for _, row in df.iterrows():
            self.update(
                home_team=row["home_team"],
                away_team=row["away_team"],
                home_score=int(row["home_score"]),
                away_score=int(row["away_score"]),
                tournament=row["tournament"],
                neutral=bool(row.get("neutral", False)),
            )

        return self

    def get_all_ratings(self) -> pd.DataFrame:
        """Returns a sorted DataFrame of all team ratings."""
        return (
            pd.DataFrame(
                list(self.ratings.items()), columns=["team", "elo_rating"]
            )
            .sort_values("elo_rating", ascending=False)
            .reset_index(drop=True)
        )

    def predict_proba(
        self,
        team_a: str,
        team_b: str,
        neutral: bool = True,
    ) -> dict[str, float]:
        """
        Pure-Elo win probability estimate.
        Returns {"home_win": p, "draw": p, "away_win": p}.
        Note: Elo doesn't natively model draws — we use a simplified split.
        """
        r_a = self.get_rating(team_a)
        r_b = self.get_rating(team_b)
        r_a_eff = r_a + (0 if neutral else HOME_ADVANTAGE)

        p_win = self._expected_score(r_a_eff, r_b)

        # Empirically, ~25% of international matches end in draws
        # We redistribute probability symmetrically around 0.5
        draw_prob = 0.25 * (1 - abs(p_win - 0.5) * 2)
        home_win = p_win - draw_prob / 2
        away_win = 1 - home_win - draw_prob

        return {
            "home_win": round(max(home_win, 0.0), 4),
            "draw":     round(max(draw_prob, 0.0), 4),
            "away_win": round(max(away_win, 0.0), 4),
        }
