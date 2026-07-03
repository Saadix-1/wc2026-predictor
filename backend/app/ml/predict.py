"""
predict.py
----------
Inference functions for match outcome prediction.
Loads saved model + Elo system and exposes a clean prediction API.
"""

import joblib
import pandas as pd
from pathlib import Path
from functools import lru_cache

from app.ml.elo import EloRatingSystem
from app.ml.features import build_feature_row

BASE_DIR   = Path(__file__).resolve().parents[2]  # backend/app/ml/predict.py → backend/
MODELS_DIR = BASE_DIR / "models"


@lru_cache(maxsize=1)
def load_model():
    """Loads the trained XGBoost model (cached after first call)."""
    model_path = MODELS_DIR / "xgb_model.pkl"
    if not model_path.exists():
        raise FileNotFoundError(
            "Model not found. Run: python -m app.ml.train"
        )
    return joblib.load(model_path)


@lru_cache(maxsize=1)
def load_elo_system() -> EloRatingSystem:
    """Loads the fitted Elo rating system (cached)."""
    elo_path = MODELS_DIR / "elo_system.pkl"
    if not elo_path.exists():
        raise FileNotFoundError(
            "Elo system not found. Run: python -m app.ml.train"
        )
    return joblib.load(elo_path)


@lru_cache(maxsize=1)
def load_feature_names() -> list[str]:
    return joblib.load(MODELS_DIR / "feature_names.pkl")


@lru_cache(maxsize=1)
def load_historical_data() -> pd.DataFrame:
    """Loads historical results for feature computation."""
    path = BASE_DIR / "data" / "results.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df["home_score"] = df["home_score"].fillna(0).astype(int)
    df["away_score"] = df["away_score"].fillna(0).astype(int)
    df["neutral"]    = df["neutral"].fillna(False).astype(bool)
    return df


def predict_match(
    team_a: str,
    team_b: str,
    stage: str = "Round of 16",
    neutral: bool = True,
) -> dict:
    """
    Predicts the outcome of a match between team_a and team_b.

    Returns:
        {
            "team_a": str,
            "team_b": str,
            "home_win_prob": float,   # team_a wins
            "draw_prob": float,
            "away_win_prob": float,   # team_b wins
            "predicted_winner": str,
            "confidence": str,        # "high" | "moderate" | "low"
            "elo_a": float,
            "elo_b": float,
            "elo_diff": float,
        }
    """
    model    = load_model()
    elo      = load_elo_system()
    df_hist  = load_historical_data()
    features = load_feature_names()

    match_date = pd.Timestamp("2026-07-01")  # Approximate current date

    feat_row = build_feature_row(
        df=df_hist,
        elo_system=elo,
        home_team=team_a,
        away_team=team_b,
        match_date=match_date,
        neutral=neutral,
        tournament="FIFA World Cup",
    )

    X = pd.DataFrame([feat_row])[features]
    proba = model.predict_proba(X)[0]  # [home_win, draw, away_win]

    home_win = float(proba[0])
    draw     = float(proba[1])
    away_win = float(proba[2])

    max_prob = max(home_win, away_win)
    if max_prob > 0.60:
        confidence = "high"
    elif max_prob > 0.45:
        confidence = "moderate"
    else:
        confidence = "low"

    if home_win > away_win:
        predicted_winner = team_a
    elif away_win > home_win:
        predicted_winner = team_b
    else:
        predicted_winner = "Draw likely"

    elo_a = elo.get_rating(team_a)
    elo_b = elo.get_rating(team_b)

    return {
        "team_a":           team_a,
        "team_b":           team_b,
        "home_win_prob":    round(home_win, 4),
        "draw_prob":        round(draw, 4),
        "away_win_prob":    round(away_win, 4),
        "predicted_winner": predicted_winner,
        "confidence":       confidence,
        "elo_a":            round(elo_a, 1),
        "elo_b":            round(elo_b, 1),
        "elo_diff":         round(elo_a - elo_b, 1),
        "stage":            stage,
    }


def get_all_elo_ratings() -> list[dict]:
    """Returns all teams sorted by Elo rating."""
    elo = load_elo_system()
    return (
        elo.get_all_ratings()
        .rename(columns={"elo_rating": "elo"})
        .to_dict(orient="records")
    )
