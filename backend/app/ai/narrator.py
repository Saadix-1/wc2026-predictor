"""
narrator.py
-----------
GPT-4o-mini powered match narrative generator.

Given two teams and their stats, generates a concise, insightful
pre-match analysis that reads like a sports journalist wrote it.
"""

import os
from openai import AsyncOpenAI
from app.ml.predict import predict_match, load_elo_system, load_historical_data
from app.ml.features import compute_recent_form, compute_h2h
import pandas as pd

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _build_stats_context(team_a: str, team_b: str) -> dict:
    """Gathers all stats needed to construct the GPT prompt."""
    prediction = predict_match(team_a, team_b)
    elo = load_elo_system()
    df = load_historical_data()
    now = pd.Timestamp("today")

    form_a = compute_recent_form(df, team_a, now, n=10)
    form_b = compute_recent_form(df, team_b, now, n=10)
    h2h    = compute_h2h(df, team_a, team_b, now, n=20)

    return {
        "team_a": team_a,
        "team_b": team_b,
        "prediction": prediction,
        "elo_a": round(elo.get_rating(team_a), 0),
        "elo_b": round(elo.get_rating(team_b), 0),
        "form_a": form_a,
        "form_b": form_b,
        "h2h": h2h,
    }


def _build_prompt(ctx: dict) -> str:
    a = ctx["team_a"]
    b = ctx["team_b"]
    p = ctx["prediction"]
    fa = ctx["form_a"]
    fb = ctx["form_b"]
    h  = ctx["h2h"]

    favorite = a if p["home_win_prob"] > p["away_win_prob"] else b
    fav_prob  = max(p["home_win_prob"], p["away_win_prob"])
    underdog  = b if favorite == a else a

    return f"""You are an expert football analyst covering the 2026 FIFA World Cup.

Write a sharp, compelling pre-match analysis for: {a} vs {b}

Match Statistics:
- {a} win probability: {p['home_win_prob']*100:.1f}%
- Draw probability: {p['draw_prob']*100:.1f}%
- {b} win probability: {p['away_win_prob']*100:.1f}%
- Predicted winner: {p['predicted_winner']} ({p['confidence']} confidence)

Elo Ratings:
- {a}: {ctx['elo_a']} | {b}: {ctx['elo_b']}

Recent Form (last 10 matches):
- {a}: {fa['win_rate']*100:.0f}% win rate, {fa['goals_for_avg']:.1f} goals/game scored, {fa['goals_against_avg']:.1f} conceded
- {b}: {fb['win_rate']*100:.0f}% win rate, {fb['goals_for_avg']:.1f} goals/game scored, {fb['goals_against_avg']:.1f} conceded

Head-to-Head (last 20 meetings):
- {a} wins: {h['h2h_a_win_rate']*100:.0f}% | Draws: {h['h2h_draw_rate']*100:.0f}% | {b} wins: {h['h2h_b_win_rate']*100:.0f}%

Instructions:
- Write 3–4 sentences maximum
- Start with the favorite and their win probability
- Mention one concrete stat from recent form
- Mention the head-to-head edge if significant
- End with a sentence about what gives the underdog a chance
- Tone: confident, analytical, like The Athletic or ESPN FC
- Do NOT use bullet points — flowing prose only
- Do NOT make up player names — reference teams and stats only
"""


async def generate_narrative(team_a: str, team_b: str) -> dict:
    """
    Generates a GPT-4o-mini match narrative for the given matchup.

    Returns:
        {
            "team_a": str,
            "team_b": str,
            "narrative": str,
            "stats": { win probs, elo, form, h2h }
        }
    """
    ctx = _build_stats_context(team_a, team_b)

    # Fallback if no API key configured
    if not os.getenv("OPENAI_API_KEY"):
        p = ctx["prediction"]
        fav = team_a if p["home_win_prob"] > p["away_win_prob"] else team_b
        fav_pct = max(p["home_win_prob"], p["away_win_prob"]) * 100
        narrative = (
            f"{fav} enters this match as the {fav_pct:.0f}% favourite according to our model, "
            f"backed by an Elo rating of {ctx['elo_a'] if fav == team_a else ctx['elo_b']:.0f}. "
            f"Head-to-head history slightly favours {fav}, but this is a World Cup knockout — "
            f"anything can happen."
        )
        return {"team_a": team_a, "team_b": team_b, "narrative": narrative, "stats": ctx}

    prompt = _build_prompt(ctx)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )

    narrative = response.choices[0].message.content.strip()

    return {
        "team_a":    team_a,
        "team_b":    team_b,
        "narrative": narrative,
        "stats": {
            "home_win_prob":    ctx["prediction"]["home_win_prob"],
            "draw_prob":        ctx["prediction"]["draw_prob"],
            "away_win_prob":    ctx["prediction"]["away_win_prob"],
            "predicted_winner": ctx["prediction"]["predicted_winner"],
            "confidence":       ctx["prediction"]["confidence"],
            "elo_a":            ctx["elo_a"],
            "elo_b":            ctx["elo_b"],
            "form_a_win_rate":  round(ctx["form_a"]["win_rate"], 3),
            "form_b_win_rate":  round(ctx["form_b"]["win_rate"], 3),
            "h2h_a_win_rate":   round(ctx["h2h"]["h2h_a_win_rate"], 3),
            "h2h_b_win_rate":   round(ctx["h2h"]["h2h_b_win_rate"], 3),
        },
    }
