"""HTTP routes. Wire the core pipeline in here once it is ready."""

from fastapi import APIRouter, HTTPException

from app.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """regex -> NFA -> DFA -> minimized DFA (+ simulation of test strings)."""
    raise HTTPException(status_code=501, detail="Not implemented yet")