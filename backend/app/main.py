"""
main.py
-------
FastAPI application entrypoint for WC2026 Predictor.

Run locally:
    uvicorn app.main:app --reload --port 8000

API docs: http://localhost:8000/docs
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import predictions, bracket, simulate, analysis, elo

load_dotenv()

app = FastAPI(
    title="WC2026 Predictor API",
    description=(
        "AI-powered 2026 FIFA World Cup match prediction platform. "
        "Predicts match outcomes using XGBoost + Elo ratings, simulates brackets "
        "with Monte Carlo, and generates GPT-4o-mini match narratives."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────────
app.include_router(predictions.router, prefix="/api", tags=["Predictions"])
app.include_router(bracket.router,     prefix="/api", tags=["Bracket"])
app.include_router(simulate.router,    prefix="/api", tags=["Simulator"])
app.include_router(analysis.router,    prefix="/api", tags=["AI Analysis"])
app.include_router(elo.router,         prefix="/api", tags=["Elo Ratings"])


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "message": "WC2026 Predictor API 🏆",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
