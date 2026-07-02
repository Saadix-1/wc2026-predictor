"""GET /api/bracket — full 2026 WC bracket with predictions for upcoming matches."""
from fastapi import APIRouter, HTTPException
from app.data.wc2026_results import COMPLETED_MATCHES, UPCOMING_MATCHES
from app.ml.predict import predict_match

router = APIRouter()


@router.get("/bracket")
def get_bracket():
    """
    Returns the full 2026 WC bracket:
    - Completed matches with actual scores
    - Upcoming matches with model predictions
    """
    try:
        upcoming_with_predictions = []
        for match in UPCOMING_MATCHES:
            prediction = predict_match(
                match["team_a"],
                match["team_b"],
                stage=match.get("round", "Round of 16"),
            )
            upcoming_with_predictions.append({**match, "prediction": prediction})

        return {
            "completed": COMPLETED_MATCHES,
            "upcoming":  upcoming_with_predictions,
            "total_completed": len(COMPLETED_MATCHES),
            "total_upcoming":  len(UPCOMING_MATCHES),
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
