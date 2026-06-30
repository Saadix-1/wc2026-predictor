"""
train.py
--------
XGBoost training pipeline for World Cup match outcome prediction.

Usage:
    python -m app.ml.train

This will:
1. Load the Kaggle historical FIFA dataset
2. Fit the Elo rating system chronologically
3. Build the feature matrix
4. Train + calibrate an XGBoost classifier
5. Save the model and Elo ratings to /models/
"""

import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, log_loss, classification_report
from xgboost import XGBClassifier

from app.ml.elo import EloRatingSystem
from app.ml.features import build_training_dataset

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)


def load_data(data_dir: Path) -> pd.DataFrame:
    """Loads and preprocesses the Kaggle international football results CSV."""
    results_path = data_dir / "results.csv"
    if not results_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {results_path}.\n"
            "Download from: https://www.kaggle.com/datasets/martj42/"
            "international-football-results-from-1872-to-2017\n"
            "Place results.csv in the backend/data/ directory."
        )

    df = pd.read_csv(results_path, parse_dates=["date"])
    df = df.dropna(subset=["home_score", "away_score"])
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)
    df["neutral"] = df["neutral"].fillna(False).astype(bool)
    print(f"✅ Loaded {len(df):,} historical matches ({df['date'].min().year}–{df['date'].max().year})")
    return df


def train(data_dir: Path = DATA_DIR, models_dir: Path = MODELS_DIR):
    print("\n🔄 Loading historical data...")
    df = load_data(data_dir)

    print("🔄 Fitting Elo rating system...")
    elo = EloRatingSystem()
    elo.fit_historical(df)

    # Save Elo ratings
    elo_df = elo.get_all_ratings()
    elo_df.to_csv(models_dir / "elo_ratings.csv", index=False)
    joblib.dump(elo, models_dir / "elo_system.pkl")
    print(f"✅ Elo ratings computed for {len(elo.ratings)} teams")

    print("🔄 Building feature matrix...")
    # Include World Cup + qualifiers + major tournaments for training
    X, y = build_training_dataset(
        df=df,
        elo_system=elo,
        tournament_filter=None,  # All tournaments
        min_date="2000-01-01",
    )
    print(f"✅ Feature matrix: {X.shape[0]:,} samples, {X.shape[1]} features")
    print(f"   Class distribution: {y.value_counts().to_dict()}")

    # ── Time-series cross-validation ───────────────────────────────────────
    print("\n🔄 Running time-series cross-validation...")
    tscv = TimeSeriesSplit(n_splits=5)

    xgb_base = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1,
    )

    cv_accuracies = []
    cv_log_losses = []

    for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

        xgb_base.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
        preds = xgb_base.predict(X_val)
        proba = xgb_base.predict_proba(X_val)

        acc = accuracy_score(y_val, preds)
        ll  = log_loss(y_val, proba)
        cv_accuracies.append(acc)
        cv_log_losses.append(ll)
        print(f"   Fold {fold+1}: Accuracy={acc:.3f}, LogLoss={ll:.3f}")

    print(f"\n✅ CV Results: Accuracy={np.mean(cv_accuracies):.3f}±{np.std(cv_accuracies):.3f}")

    # ── Final model: train on all data + calibrate ─────────────────────────
    print("\n🔄 Training final model on all data...")
    final_model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1,
    )

    # Calibrate for reliable probabilities
    calibrated_model = CalibratedClassifierCV(final_model, method="sigmoid", cv=3)
    calibrated_model.fit(X, y)

    # Save model + feature names
    joblib.dump(calibrated_model, models_dir / "xgb_model.pkl")
    joblib.dump(list(X.columns), models_dir / "feature_names.pkl")
    print(f"✅ Model saved to {models_dir / 'xgb_model.pkl'}")

    # ── Feature importance ─────────────────────────────────────────────────
    try:
        importances = final_model.feature_importances_
        feat_imp = (
            pd.DataFrame({"feature": X.columns, "importance": importances})
            .sort_values("importance", ascending=False)
        )
        print("\n📊 Top 10 Features:")
        print(feat_imp.head(10).to_string(index=False))
        feat_imp.to_csv(models_dir / "feature_importance.csv", index=False)
    except Exception:
        pass

    print("\n🎉 Training complete!")
    return calibrated_model, elo


if __name__ == "__main__":
    train()
