"""
Overview endpoint — GET /api/overview

Returns high-level dashboard metrics: total employees, confidence index,
salary/tenure stats, expectation breakdown, top roles.
"""

from fastapi import APIRouter

from app.analytics.metrics import (
    add_band_columns,
    compute_confidence_index,
    compute_expectation_breakdown,
    compute_salary_stats,
    compute_tenure_stats,
)
from app.analytics.segmentation import top_roles_by_headcount
from app.etl.pipeline import get_dataframe
from app.models.metrics import OverviewResponse

router = APIRouter(tags=["overview"])


@router.get("/overview", response_model=OverviewResponse)
def get_overview() -> OverviewResponse:
    """Return high-level overview metrics for the dashboard."""
    df = get_dataframe()
    df = add_band_columns(df)

    return OverviewResponse(
        total_employees=len(df),
        confidence_index=compute_confidence_index(df),
        salary=compute_salary_stats(df),
        tenure=compute_tenure_stats(df),
        expectations=compute_expectation_breakdown(df),
        top_roles=top_roles_by_headcount(df),
    )
