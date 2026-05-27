"""
Tenure endpoint — GET /api/tenure

Returns tenure stats, distribution histogram, breakdowns by role,
expectation, and band, plus career horizon scatter data.
"""

from fastapi import APIRouter

from app.analytics.metrics import (
    add_band_columns,
    compute_tenure_histogram,
    compute_tenure_stats,
)
from app.analytics.segmentation import (
    career_horizon_matrix,
    expectation_by_tenure_band,
    tenure_by_expectation,
    tenure_by_role,
)
from app.etl.pipeline import get_dataframe
from app.models.metrics import TenureResponse

router = APIRouter(tags=["tenure"])


@router.get("/tenure", response_model=TenureResponse)
def get_tenure() -> TenureResponse:
    """Return comprehensive tenure analysis with career horizon data."""
    df = get_dataframe()
    df = add_band_columns(df)

    return TenureResponse(
        stats=compute_tenure_stats(df),
        distribution=compute_tenure_histogram(df),
        by_role=tenure_by_role(df),
        by_expectation=tenure_by_expectation(df),
        by_band=expectation_by_tenure_band(df),
        career_horizon=career_horizon_matrix(df),
    )
