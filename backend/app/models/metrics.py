"""
API response models — Pydantic v2 models for every endpoint.

Each model is designed to be serialized directly to JSON.
Salary values are always raw floats (never BRL-formatted strings).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════
#  Shared / reusable sub-models
# ═══════════════════════════════════════════════════════════════════════


class ExpectationBreakdown(BaseModel):
    """Count of positive vs. negative expectations."""
    positive: int
    negative: int
    positive_pct: float
    negative_pct: float


class SalaryStats(BaseModel):
    """Descriptive salary statistics."""
    avg: float
    median: float
    min: float
    max: float
    std: float


class TenureStats(BaseModel):
    """Descriptive tenure statistics."""
    avg: float
    median: float
    min: float
    max: float


class RoleHeadcount(BaseModel):
    """Role name and its headcount."""
    role: str
    count: int


class BandBreakdown(BaseModel):
    """Expectation breakdown within a band."""
    band: str
    total: int
    positive: int
    negative: int
    confidence_pct: float


class RoleExpectation(BaseModel):
    """Expectation breakdown per role."""
    role: str
    total: int
    positive: int
    negative: int
    confidence_pct: float


class RoleSalary(BaseModel):
    """Salary stats per role."""
    role: str
    count: int
    avg_salary: float
    median_salary: float
    min_salary: float
    max_salary: float


class RoleTenure(BaseModel):
    """Tenure stats per role."""
    role: str
    count: int
    avg_tenure: float
    median_tenure: float


class RetentionRiskGroup(BaseModel):
    """A group of employees with negative outlook, grouped by role."""
    role: str
    count: int
    avg_salary: float
    avg_tenure: float


class SilentStrengthZone(BaseModel):
    """High confidence + low salary roles (undervalued teams)."""
    role: str
    count: int
    confidence_pct: float
    avg_salary: float


class HistogramBin(BaseModel):
    """A single bin in a histogram."""
    bin_start: float
    bin_end: float
    count: int


class SalaryByExpectation(BaseModel):
    """Salary stats split by expectation."""
    expectation: str
    count: int
    avg_salary: float
    median_salary: float


class CompensationFrictionPoint(BaseModel):
    """Roles where salary dispersion or low pay + low confidence overlap."""
    role: str
    avg_salary: float
    confidence_pct: float
    count: int
    signal: str


class CareerHorizonPoint(BaseModel):
    """A single point in the career horizon scatter plot."""
    tenure_years: float
    salario: float
    expectativa: bool
    cargo: str


class TenureByExpectation(BaseModel):
    """Tenure stats split by expectation."""
    expectation: str
    count: int
    avg_tenure: float
    median_tenure: float


class RoleSummary(BaseModel):
    """Comprehensive per-role summary for the roles dashboard."""
    role: str
    count: int
    avg_salary: float
    median_salary: float
    avg_tenure: float
    median_tenure: float
    confidence_pct: float
    positive: int
    negative: int


class SentimentHeatmapCell(BaseModel):
    """A single cell in the sentiment heatmap (role × tenure band)."""
    role: str
    tenure_band: str
    count: int
    confidence_pct: float


class StoryCard(BaseModel):
    """A narrative insight card for the presentation view."""
    title: str
    body: str
    category: str
    metric: str | None = None
    value: str | None = None


# ═══════════════════════════════════════════════════════════════════════
#  Top-level API response models (one per endpoint)
# ═══════════════════════════════════════════════════════════════════════


class OverviewResponse(BaseModel):
    """GET /api/overview"""
    total_employees: int
    confidence_index: float = Field(..., description="% of employees with positive outlook")
    salary: SalaryStats
    tenure: TenureStats
    expectations: ExpectationBreakdown
    top_roles: list[RoleHeadcount]


class ExpectationsResponse(BaseModel):
    """GET /api/expectations"""
    by_role: list[RoleExpectation]
    by_salary_band: list[BandBreakdown]
    by_tenure_band: list[BandBreakdown]
    retention_risk: list[RetentionRiskGroup]
    silent_strength: list[SilentStrengthZone]


class SalaryResponse(BaseModel):
    """GET /api/salary"""
    stats: SalaryStats
    distribution: list[HistogramBin]
    by_role: list[RoleSalary]
    by_expectation: list[SalaryByExpectation]
    by_band: list[BandBreakdown]
    compensation_friction: list[CompensationFrictionPoint]


class TenureResponse(BaseModel):
    """GET /api/tenure"""
    stats: TenureStats
    distribution: list[HistogramBin]
    by_role: list[RoleTenure]
    by_expectation: list[TenureByExpectation]
    by_band: list[BandBreakdown]
    career_horizon: list[CareerHorizonPoint]


class RolesResponse(BaseModel):
    """GET /api/roles"""
    summary: list[RoleSummary]
    sentiment_heatmap: list[SentimentHeatmapCell]


class PresentationResponse(BaseModel):
    """GET /api/presentation"""
    story_cards: list[StoryCard]
    key_findings: list[str]
    recommendations: list[str]


class ConfidentialEmployeeResponse(BaseModel):
    """GET /api/confidential/employees"""
    func: str
    cargo: str
    salario: float
    tenure_years: float
    expectativa: bool
    risk_signal: str | None = None

