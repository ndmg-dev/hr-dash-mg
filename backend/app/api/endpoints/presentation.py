"""
Presentation endpoint — GET /api/presentation

Returns narrative story cards, key findings, and recommendations
for the executive presentation view. ALL content is derived from data.
"""

from fastapi import APIRouter

from app.analytics.insights import (
    generate_key_findings,
    generate_recommendations,
    generate_story_cards,
)
from app.etl.pipeline import get_dataframe
from app.models.metrics import PresentationResponse

router = APIRouter(tags=["presentation"])


@router.get("/presentation", response_model=PresentationResponse)
def get_presentation() -> PresentationResponse:
    """Return narrative presentation data with story cards and recommendations."""
    df = get_dataframe()

    return PresentationResponse(
        story_cards=generate_story_cards(df),
        key_findings=generate_key_findings(df),
        recommendations=generate_recommendations(df),
    )
