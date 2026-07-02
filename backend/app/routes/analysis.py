"""GET /api/analysis/{team_a}/{team_b} — AI match narrative + stats."""
from fastapi import APIRouter, HTTPException
from app.ai.narrator import generate_narrative

router = APIRouter()


@router.get("/analysis/{team_a}/{team_b}")
async def get_analysis(team_a: str, team_b: str):
    """
    Generates a GPT-4o-mini match preview narrative for the given matchup.
    Falls back to a rule-based template if no API key is configured.
    """
    try:
        return await generate_narrative(team_a, team_b)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
