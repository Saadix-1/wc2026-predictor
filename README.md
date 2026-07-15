# WC2026.AI — FIFA World Cup Prediction System 

> AI-powered match predictions for the 2026 FIFA World Cup. Machine learning meets the beautiful game. 

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=flat-square&logo=vercel)](https://frontend-pi77fr3uj-saad-m.vercel.app)
[![API](https://img.shields.io/badge/API-Railway-purple?style=flat-square&logo=railway)](https://wc2026-backend-production-c2b3.up.railway.app/docs)
[![GitHub](https://img.shields.io/badge/GitHub-Saadix--1-181717?style=flat-square&logo=github)](https://github.com/Saadix-1/wc2026-predictor)

--- 
 
## Live URLs 

| Service | URL |
|---------|-----|
| Frontend | https://frontend-pi77fr3uj-saad-m.vercel.app |
| Backend API | https://wc2026-backend-production-c2b3.up.railway.app |
| API Docs (Swagger) | https://wc2026-backend-production-c2b3.up.railway.app/docs |

---

## What it does

**WC2026.AI** predicts the outcome of every FIFA World Cup 2026 match using a machine learning model trained on 45,000+ international results dating back to 1872.

- **Match Predictor** — Select any two teams and a tournament stage. Get win/draw/loss probabilities backed by a calibrated XGBoost model.
- **Tournament Simulator** — Run up to 50,000 Monte Carlo simulations to compute each team's real probability of winning the World Cup.
- **Live Bracket** — Every upcoming match with predictions, updated after each real result.
- **AI Match Analysis** — GPT-4o-mini generates a journalist-quality pre-match preview for any matchup.

---

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API framework |
| **XGBoost** | Core prediction model |
| **Custom Elo Engine** | Team rating system (like chess, for football) |
| **scikit-learn** | Probability calibration (Platt scaling) |
| **Pandas** | Data processing pipeline |
| **OpenAI GPT-4o-mini** | AI match narrative generation |
| **Railway** | Backend deployment |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React + Vite** | UI framework |
| **React Router** | Client-side routing |
| **Recharts** | Championship probability bar charts |
| **Axios** | API communication |
| **Vercel** | Frontend deployment |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Vercel)                  │
│  React + Vite  ·  React Router  ·  Recharts         │
│                                                      │
│  Pages: Home / Predict / Bracket / Simulator        │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS (Axios)
┌──────────────────────▼──────────────────────────────┐
│                  Backend (Railway)                   │
│  FastAPI  ·  Uvicorn                                │
│                                                      │
│  /api/predict    POST  → XGBoost inference          │
│  /api/bracket    GET   → All WC2026 matches         │
│  /api/simulate   POST  → Monte Carlo simulation     │
│  /api/analysis   GET   → GPT-4o-mini narrative      │
│  /api/elo        GET   → Elo ratings leaderboard    │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   ML Pipeline                        │
│                                                      │
│  results.csv (49,487 matches, 1872–2026)            │
│       ↓                                             │
│  Elo Rating System (336 teams)                      │
│       ↓                                             │
│  Feature Engineering (22 features):                 │
│    · Elo difference      · Recent form (5 games)    │
│    · Head-to-head record · Tournament stage         │
│    · Home/neutral flag   · Goal difference          │
│       ↓                                             │
│  XGBoost Classifier + Platt Calibration             │
│  CV Accuracy: 58.3% ± 1.8%  (3-class baseline: 33%)|
└─────────────────────────────────────────────────────┘
```

---

## ML Model Details

The model predicts one of three outcomes: **Home Win / Draw / Away Win**.

| Metric | Value |
|--------|-------|
| Training samples | 25,425 matches |
| Features | 22 |
| Cross-validation | 5-fold time-series |
| CV Accuracy | **58.3% ± 1.8%** |
| Baseline (random) | 33.3% |
| Calibration | Platt scaling |

### Feature Engineering
- **Elo Rating** — Custom Elo system computed chronologically across all 49,487 matches
- **Elo Difference** — Rating gap between teams (strongest single predictor)
- **Recent Form** — Win rate over last 5 matches for each team
- **Head-to-Head** — Historical win rate between the two specific teams
- **Tournament Stage** — Knockout round pressure encoded as a feature
- **Neutral Ground** — Whether the match is on neutral territory

---

## API Reference

### `POST /api/predict`
Predict the outcome of a match.

```bash
curl -X POST https://wc2026-backend-production-c2b3.up.railway.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"team_a": "France", "team_b": "Brazil", "stage": "Semifinal"}'
```

```json
{
  "team_a": "France",
  "team_b": "Brazil",
  "home_win_prob": 0.5137,
  "draw_prob": 0.2873,
  "away_win_prob": 0.1990,
  "predicted_winner": "France",
  "confidence": "moderate",
  "elo_a": 2212.2,
  "elo_b": 2118.5,
  "elo_diff": 93.7,
  "stage": "Semifinal"
}
```

### `POST /api/simulate`
Run Monte Carlo tournament simulation.

```bash
curl -X POST https://wc2026-backend-production-c2b3.up.railway.app/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"iterations": 10000}'
```

### `GET /api/bracket`
Get all WC2026 matches with predictions.

### `GET /api/analysis/{team_a}/{team_b}`
Get GPT-4o-mini pre-match narrative.

### `GET /api/elo`
Get Elo ratings for all teams.

---

## Local Setup

### Requirements
- Python 3.12+
- Node.js 18+
- OpenAI API key

### 1. Clone the repo
```bash
git clone https://github.com/Saadix-1/wc2026-predictor.git
cd wc2026-predictor
```

### 2. Backend setup
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Add your OpenAI API key
```

### 3. Train the model
The pre-trained model is included in the repo. To retrain from scratch:
```bash
# Download dataset from Kaggle first
python download_data.py
# Then retrain
python -m app.ml.train
```

### 4. Start the API
```bash
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

### 5. Frontend setup
```bash
cd ../frontend
npm install --legacy-peer-deps
cp .env.example .env   # Set VITE_API_URL=http://localhost:8000
npm run dev
# → http://localhost:5173
```

---

## Project Structure

```
wc2026-predictor/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── narrator.py          # GPT-4o-mini integration
│   │   ├── ml/
│   │   │   ├── elo.py               # Custom Elo rating engine
│   │   │   ├── features.py          # Feature engineering pipeline
│   │   │   ├── train.py             # XGBoost training script
│   │   │   ├── predict.py           # Inference module
│   │   │   └── simulator.py         # Monte Carlo simulator
│   │   ├── routes/
│   │   │   ├── predictions.py       # POST /api/predict
│   │   │   ├── bracket.py           # GET  /api/bracket
│   │   │   ├── simulate.py          # POST /api/simulate
│   │   │   ├── analysis.py          # GET  /api/analysis
│   │   │   └── elo.py               # GET  /api/elo
│   │   └── main.py                  # FastAPI app entrypoint
│   ├── data/
│   │   └── results.csv              # 49,487 international matches
│   ├── models/
│   │   ├── xgb_model.pkl            # Trained XGBoost classifier
│   │   └── elo_system.pkl           # Serialized Elo ratings
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Predict.jsx
│       │   ├── Bracket.jsx
│       │   └── Simulator.jsx
│       └── components/
│           ├── MatchCard.jsx
│           ├── AnalysisModal.jsx
│           └── SimulatorPanel.jsx
├── docker-compose.yml
├── railway.json
└── README.md
```

---

## Built by

**Saad Mehamdi** — Software Engineering @ University of Ottawa  
[Portfolio](https://saadmehamdi.netlify.app) · [LinkedIn](https://linkedin.com/in/saad-mehamdi) · [GitHub](https://github.com/Saadix-1)
