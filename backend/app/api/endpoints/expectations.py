"""
Expectations endpoint — GET /api/expectations

Returns expectation breakdowns by role, salary band, tenure band,
plus retention risk groups and silent strength zones.
"""

from fastapi import APIRouter

from app.analytics.metrics import add_band_columns
from app.analytics.segmentation import (
    compute_retention_risk,
    compute_silent_strength,
    expectation_by_role,
    expectation_by_salary_band,
    expectation_by_tenure_band,
)
from app.etl.pipeline import get_dataframe
from app.models.metrics import ExpectationsResponse

router = APIRouter(tags=["expectations"])


@router.get("/expectations", response_model=ExpectationsResponse)
def get_expectations() -> ExpectationsResponse:
    """Return expectation analysis with retention risk and silent strength zones."""
    df = get_dataframe()
    df = add_band_columns(df)

    return ExpectationsResponse(
        by_role=expectation_by_role(df),
        by_salary_band=expectation_by_salary_band(df),
        by_tenure_band=expectation_by_tenure_band(df),
        retention_risk=compute_retention_risk(df),
        silent_strength=compute_silent_strength(df),
    )
