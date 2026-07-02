#!/usr/bin/env python3
"""
download_data.py
----------------
Downloads the Kaggle FIFA dataset automatically using the Kaggle API.

Requirements:
    pip install kaggle
    Set up ~/.kaggle/kaggle.json with your API credentials
    (get it at https://www.kaggle.com/settings → API → Create New Token)

Usage:
    python download_data.py
"""

import subprocess
import sys
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATASET  = "martj42/international-football-results-from-1872-to-2017"


def main():
    # Check kaggle CLI
    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Kaggle CLI not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "kaggle"], check=True)

    # Check credentials
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("\n❌ Kaggle credentials not found!")
        print("1. Go to: https://www.kaggle.com/settings")
        print("2. Click 'API' → 'Create New Token'")
        print(f"3. Move the downloaded kaggle.json to: {kaggle_json}")
        print("\nOr manually download from:")
        print(f"   https://www.kaggle.com/datasets/{DATASET}")
        print(f"   and place results.csv in: {DATA_DIR}/")
        sys.exit(1)

    print(f"📥 Downloading dataset: {DATASET}")
    DATA_DIR.mkdir(exist_ok=True)

    subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATASET,
         "--unzip", "-p", str(DATA_DIR)],
        check=True
    )

    # Verify
    results_csv = DATA_DIR / "results.csv"
    if results_csv.exists():
        import pandas as pd
        df = pd.read_csv(results_csv)
        print(f"\n✅ Dataset ready: {len(df):,} matches ({df['date'].min()[:4]}–{df['date'].max()[:4]})")
        print(f"   Saved to: {DATA_DIR}/")
        print("\n🚀 Next step: python -m app.ml.train")
    else:
        print("⚠️  Download completed but results.csv not found. Check manually.")


if __name__ == "__main__":
    main()
