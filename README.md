# WC2026 Predictor 🏆  

> **AI-powered 2026 FIFA World Cup match prediction platform** — predicts match outcomes using XGBoost + Elo ratings, simulates the full tournament bracket with Monte Carlo simulations, and generates AI-written match narratives via GPT-4o-mini.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.1-FF6600)](https://xgboost.readthedocs.io/)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-OpenAI-412991?logo=openai)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚧 Status: In Active Development

> The 2026 FIFA World Cup is live! This project is being built in real time as the tournament progresses. Predictions update after every real match result.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **ML Predictions** | XGBoost ensemble model trained on 45,000+ historical matches (1872–2026) |
| 📊 **Elo Rating System** | Custom football Elo engine with tournament-specific K-factors and goal-difference weighting |
| 🔄 **Monte Carlo Simulator** | Runs 10,000 tournament simulations to calculate each team's championship probability |
| 📝 **AI Match Narratives** | GPT-4o-mini generates pre-match analysis with key stats and matchup breakdowns |
| 🏟️ **Live Bracket** | Interactive knockout bracket that updates in real time as results come in |
| 📈 **Model Accuracy Tracker** | Displays how many predictions the model got right so far in the tournament |

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API
- [XGBoost](https://xgboost.readthedocs.io/) — Match outcome classifier
- [Scikit-learn](https://scikit-learn.org/) — Calibration + cross-validation
- [Pandas / NumPy](https://pandas.pydata.org/) — Feature engineering
- [OpenAI Python SDK](https://github.com/openai/openai-python) — GPT-4o-mini narratives

**Frontend** *(coming soon)*
- [React 18](https://react.dev/) + [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [@g-loot/react-tournament-brackets](https://github.com/g-loot/react-tournament-brackets)

**Deployment** *(coming soon)*
- Backend → [Railway](https://railway.app/)
- Frontend → [Vercel](https://vercel.com/)

---

## 🏗️ Architecture

```
wc2026-predictor/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── routes/              # API route handlers
│   │   ├── ml/                  # ML pipeline
│   │   │   ├── elo.py           # Custom Elo rating engine
│   │   │   ├── features.py      # Feature engineering
│   │   │   ├── train.py         # XGBoost training
│   │   │   ├── predict.py       # Inference
│   │   │   └── simulator.py     # Monte Carlo bracket sim
│   │   ├── data/                # 2026 WC live results
│   │   └── ai/                  # OpenAI narrative generator
│   └── data/                    # Historical FIFA dataset (not in git)
│
└── frontend/                    # React app (coming soon)
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Saadix-1/wc2026-predictor.git
cd wc2026-predictor
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download the dataset
Download **`results.csv`** from:
👉 [Kaggle — International football results 1872–2026](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017)

Place it in `backend/data/results.csv`

### 4. Set up environment variables
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 5. Train the model
```bash
cd backend
python -m app.ml.train
```
> This takes ~2 minutes. Model is saved to `backend/models/`.

### 6. Run the API
```bash
uvicorn app.main:app --reload
```
API docs available at: `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/predict` | Predict match outcome |
| `GET`  | `/api/bracket` | Full 2026 WC bracket with predictions |
| `POST` | `/api/simulate` | Monte Carlo tournament simulation |
| `GET`  | `/api/analysis/{team_a}/{team_b}` | AI-generated match narrative |
| `GET`  | `/api/elo` | All team Elo ratings |

### Example
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"team_a": "France", "team_b": "Brazil", "stage": "Semifinal"}'
```

```json
{
  "team_a": "France",
  "team_b": "Brazil",
  "home_win_prob": 0.4821,
  "draw_prob": 0.2134,
  "away_win_prob": 0.3045,
  "predicted_winner": "France",
  "confidence": "moderate",
  "elo_a": 2041.3,
  "elo_b": 2089.7,
  "elo_diff": -48.4
}
```

---

## 🧠 Model Details

- **Algorithm**: XGBoost (calibrated with Platt scaling for reliable probabilities)
- **Training data**: 45,000+ international matches (2000–2026)
- **Validation**: Time-series cross-validation (never leaks future data)
- **Features**: Elo ratings, recent form (last 10 matches), head-to-head record, tournament stage, neutral venue
- **Output**: 3-class probabilities (Home Win / Draw / Away Win)

---

## 👤 Author

**Saad Mehamdi** — Software Engineering Student @ University of Ottawa

[![LinkedIn](https://img.shields.io/badge/LinkedIn-saad--mehamdi-0077B5?logo=linkedin)](https://linkedin.com/in/saad-mehamdi)
[![GitHub](https://img.shields.io/badge/GitHub-Saadix--1-181717?logo=github)](https://github.com/Saadix-1)
[![Portfolio](https://img.shields.io/badge/Portfolio-saadmehamdi.netlify.app-FF6B6B)](https://saadmehamdi.netlify.app/)

---

## 📄 License

MIT — feel free to fork and build on this!
