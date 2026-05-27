"""
Salary endpoint — GET /api/salary

Returns salary stats, distribution histogram, breakdowns by role,
expectation, and band, plus compensation friction map.
"""

from fastapi import APIRouter

from app.analytics.metrics import (
    add_band_columns,
    compute_salary_histogram,
    compute_salary_stats,
)
from app.analytics.segmentation import (
    compensation_friction_map,
    salary_band_breakdown,
    salary_by_expectation,
    salary_by_role,
)
from app.etl.pipeline import get_dataframe
from app.models.metrics import SalaryResponse

router = APIRouter(tags=["salary"])


@router.get("/salary", response_model=SalaryResponse)
def get_salary() -> SalaryResponse:
    """Return comprehensive salary analysis."""
    df = get_dataframe()
    df = add_band_columns(df)

    return SalaryResponse(
        stats=compute_salary_stats(df),
        distribution=compute_salary_histogram(df),
        by_role=salary_by_role(df),
        by_expectation=salary_by_expectation(df),
        by_band=salary_band_breakdown(df),
        compensation_friction=compensation_friction_map(df),
    )
