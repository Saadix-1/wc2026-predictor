"""GET /api/elo — all team Elo ratings."""
from fastapi import APIRouter, HTTPException
from app.ml.predict import get_all_elo_ratings

router = APIRouter()


@router.get("/elo")
def elo_ratings():
    """Returns all international teams sorted by Elo rating (descending)."""
    try:
        return {"ratings": get_all_elo_ratings()}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
