"""POST /api/simulate — run Monte Carlo tournament simulation."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.ml.simulator import run_simulation
from app.data.wc2026_results import UPCOMING_MATCHES, COMPLETED_MATCHES

router = APIRouter()


class SimulateRequest(BaseModel):
    iterations: int = Field(default=10_000, ge=100, le=50_000)
    remaining_teams: list[str] | None = None  # Auto-detected if not provided
    current_round_idx: int = 0


@router.post("/simulate")
def simulate(req: SimulateRequest):
    """
    Runs N Monte Carlo simulations of the remaining tournament.
    Returns each team's probability of winning the championship.
    """
    try:
        # Auto-detect remaining teams from upcoming matches if not provided
        if req.remaining_teams is None:
            remaining = set()
            for match in UPCOMING_MATCHES:
                remaining.add(match["team_a"])
                remaining.add(match["team_b"])
            remaining_teams = list(remaining)
        else:
            remaining_teams = req.remaining_teams

        if len(remaining_teams) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 remaining teams")

        probs = run_simulation(
            remaining_teams=remaining_teams,
            current_round_idx=req.current_round_idx,
            iterations=req.iterations,
        )

        # Sort by probability descending
        sorted_probs = dict(sorted(probs.items(), key=lambda x: -x[1]))

        return {
            "iterations":      req.iterations,
            "teams_simulated": len(remaining_teams),
            "championship_probabilities": sorted_probs,
        }
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
