"""POST /api/predict — predict a single match outcome."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml.predict import predict_match

router = APIRouter()


class PredictRequest(BaseModel):
    team_a: str
    team_b: str
    stage: str = "Round of 16"
    neutral: bool = True


@router.post("/predict")
def predict(req: PredictRequest):
    try:
        return predict_match(req.team_a, req.team_b, stage=req.stage, neutral=req.neutral)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
