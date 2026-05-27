"""
Roles endpoint — GET /api/roles

Returns a comprehensive role summary table and a sentiment heatmap
(role × tenure band).
"""

from fastapi import APIRouter

from app.analytics.metrics import add_band_columns
from app.analytics.segmentation import role_summary_table, sentiment_heatmap
from app.etl.pipeline import get_dataframe
from app.models.metrics import RolesResponse

router = APIRouter(tags=["roles"])


@router.get("/roles", response_model=RolesResponse)
def get_roles() -> RolesResponse:
    """Return per-role summary and sentiment heatmap."""
    df = get_dataframe()
    df = add_band_columns(df)

    return RolesResponse(
        summary=role_summary_table(df),
        sentiment_heatmap=sentiment_heatmap(df),
    )
