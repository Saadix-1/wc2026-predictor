"""
features.py
-----------
Feature engineering pipeline for the XGBoost match prediction model.

Each match is described by features computed from:
- Elo ratings at match time
- Recent form (last 10 matches)
- Head-to-head historical record
- Tournament context
"""

import pandas as pd
import numpy as np
from app.ml.elo import EloRatingSystem


def compute_recent_form(
    df: pd.DataFrame,
    team: str,
    before_date: pd.Timestamp,
    n: int = 10,
) -> dict:
    """
    Computes a team's form over the last `n` matches before a given date.
    Returns wins, draws, losses, goals scored, goals conceded.
    """
    mask = (
        ((df["home_team"] == team) | (df["away_team"] == team))
        & (df["date"] < before_date)
    )
    recent = df[mask].sort_values("date").tail(n)

    wins = draws = losses = 0
    goals_for = goals_against = 0

    for _, row in recent.iterrows():
        if row["home_team"] == team:
            gf, ga = row["home_score"], row["away_score"]
        else:
            gf, ga = row["away_score"], row["home_score"]

        goals_for += gf
        goals_against += ga

        if gf > ga:
            wins += 1
        elif gf == ga:
            draws += 1
        else:
            losses += 1

    n_played = len(recent)
    return {
        "win_rate":        wins   / n_played if n_played else 0.5,
        "draw_rate":       draws  / n_played if n_played else 0.25,
        "loss_rate":       losses / n_played if n_played else 0.25,
        "goals_for_avg":   goals_for     / n_played if n_played else 1.0,
        "goals_against_avg": goals_against / n_played if n_played else 1.0,
        "goal_diff_avg":   (goals_for - goals_against) / n_played if n_played else 0.0,
        "matches_played":  n_played,
    }


def compute_h2h(
    df: pd.DataFrame,
    team_a: str,
    team_b: str,
    before_date: pd.Timestamp,
    n: int = 20,
) -> dict:
    """
    Computes head-to-head record between two teams before a given date.
    """
    mask = (
        (
            ((df["home_team"] == team_a) & (df["away_team"] == team_b))
            | ((df["home_team"] == team_b) & (df["away_team"] == team_a))
        )
        & (df["date"] < before_date)
    )
    h2h = df[mask].sort_values("date").tail(n)

    a_wins = b_wins = draws = 0
    for _, row in h2h.iterrows():
        if row["home_team"] == team_a:
            gf, ga = row["home_score"], row["away_score"]
        else:
            gf, ga = row["away_score"], row["home_score"]

        if gf > ga:
            a_wins += 1
        elif gf < ga:
            b_wins += 1
        else:
            draws += 1

    n_played = len(h2h)
    return {
        "h2h_a_win_rate":  a_wins / n_played if n_played else 0.33,
        "h2h_b_win_rate":  b_wins / n_played if n_played else 0.33,
        "h2h_draw_rate":   draws  / n_played if n_played else 0.33,
        "h2h_matches":     n_played,
    }


def build_feature_row(
    df: pd.DataFrame,
    elo_system: EloRatingSystem,
    home_team: str,
    away_team: str,
    match_date: pd.Timestamp,
    neutral: bool = True,
    tournament: str = "FIFA World Cup",
) -> dict:
    """
    Builds the full feature vector for a single match.
    Used for both training (historical) and inference (live prediction).
    """
    # ── Elo features ───────────────────────────────────────────────────
    elo_home = elo_system.get_rating(home_team)
    elo_away = elo_system.get_rating(away_team)
    elo_diff = elo_home - elo_away

    # ── Recent form ────────────────────────────────────────────────────
    form_home = compute_recent_form(df, home_team, match_date)
    form_away = compute_recent_form(df, away_team, match_date)

    # ── Head-to-head ───────────────────────────────────────────────────
    h2h = compute_h2h(df, home_team, away_team, match_date)

    # ── Tournament stage weight ─────────────────────────────────────────
    stage_weights = {
        "FIFA World Cup":                  1.0,
        "FIFA World Cup qualification":    0.8,
        "friendly":                        0.3,
    }
    tournament_weight = next(
        (v for k, v in stage_weights.items() if k.lower() in tournament.lower()),
        0.6,
    )

    return {
        # Elo
        "elo_home":                elo_home,
        "elo_away":                elo_away,
        "elo_diff":                elo_diff,
        "elo_diff_squared":        elo_diff ** 2,

        # Recent form — home
        "home_win_rate":           form_home["win_rate"],
        "home_draw_rate":          form_home["draw_rate"],
        "home_goals_for_avg":      form_home["goals_for_avg"],
        "home_goals_against_avg":  form_home["goals_against_avg"],
        "home_goal_diff_avg":      form_home["goal_diff_avg"],

        # Recent form — away
        "away_win_rate":           form_away["win_rate"],
        "away_draw_rate":          form_away["draw_rate"],
        "away_goals_for_avg":      form_away["goals_for_avg"],
        "away_goals_against_avg":  form_away["goals_against_avg"],
        "away_goal_diff_avg":      form_away["goal_diff_avg"],

        # Form differentials
        "win_rate_diff":           form_home["win_rate"] - form_away["win_rate"],
        "goal_diff_diff":          form_home["goal_diff_avg"] - form_away["goal_diff_avg"],

        # Head-to-head
        "h2h_home_win_rate":       h2h["h2h_a_win_rate"],
        "h2h_away_win_rate":       h2h["h2h_b_win_rate"],
        "h2h_draw_rate":           h2h["h2h_draw_rate"],
        "h2h_matches":             h2h["h2h_matches"],

        # Context
        "is_neutral":              int(neutral),
        "tournament_weight":       tournament_weight,
    }


def build_training_dataset(
    df: pd.DataFrame,
    elo_system: EloRatingSystem,
    tournament_filter: list[str] | None = None,
    min_date: str = "2000-01-01",
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Builds the training dataset by iterating chronologically over matches.
    
    Target variable (y):
        0 = home win
        1 = draw
        2 = away win

    Args:
        df:                 Historical results DataFrame
        elo_system:         Pre-fitted EloRatingSystem
        tournament_filter:  If set, only include these tournaments
        min_date:           Only use matches after this date (avoids early noise)
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] >= min_date].sort_values("date").reset_index(drop=True)

    if tournament_filter:
        mask = df["tournament"].apply(
            lambda t: any(f.lower() in t.lower() for f in tournament_filter)
        )
        df = df[mask].reset_index(drop=True)

    rows = []
    labels = []

    for _, row in df.iterrows():
        try:
            features = build_feature_row(
                df=df,
                elo_system=elo_system,
                home_team=row["home_team"],
                away_team=row["away_team"],
                match_date=row["date"],
                neutral=bool(row.get("neutral", False)),
                tournament=row["tournament"],
            )

            # Label
            if row["home_score"] > row["away_score"]:
                label = 0  # home win
            elif row["home_score"] == row["away_score"]:
                label = 1  # draw
            else:
                label = 2  # away win

            rows.append(features)
            labels.append(label)
        except Exception:
            continue  # Skip malformed rows

    X = pd.DataFrame(rows)
    y = pd.Series(labels, name="outcome")
    return X, y
