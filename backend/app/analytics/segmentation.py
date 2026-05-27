"""
Segmentation analytics — breakdowns by role, band, and expectation.

All functions take a dataframe (already enriched with band columns)
and return lists of Pydantic sub-models ready for serialization.
"""

from __future__ import annotations

import pandas as pd

from app.models.enums import SalaryBand, TenureBand
from app.models.metrics import (
    BandBreakdown,
    CareerHorizonPoint,
    CompensationFrictionPoint,
    RetentionRiskGroup,
    RoleExpectation,
    RoleHeadcount,
    RoleSalary,
    RoleSummary,
    RoleTenure,
    SalaryByExpectation,
    SentimentHeatmapCell,
    SilentStrengthZone,
    TenureByExpectation,
)


# ═══════════════════════════════════════════════════════════════════════
#  Role-based segmentation
# ═══════════════════════════════════════════════════════════════════════


def top_roles_by_headcount(df: pd.DataFrame, top_n: int = 10) -> list[RoleHeadcount]:
    """Return roles sorted by headcount (descending)."""
    counts = df["cargo"].value_counts().head(top_n)
    return [
        RoleHeadcount(role=role, count=int(count))
        for role, count in counts.items()
    ]


def expectation_by_role(df: pd.DataFrame) -> list[RoleExpectation]:
    """Compute expectation breakdown per role."""
    results: list[RoleExpectation] = []
    for role, group in df.groupby("cargo"):
        total = len(group)
        positive = int(group["expectativa"].sum())
        negative = total - positive
        results.append(RoleExpectation(
            role=str(role),
            total=total,
            positive=positive,
            negative=negative,
            confidence_pct=round(positive / total * 100, 2) if total else 0.0,
        ))
    return sorted(results, key=lambda r: r.total, reverse=True)


def expectation_by_salary_band(df: pd.DataFrame) -> list[BandBreakdown]:
    """Compute expectation breakdown per salary band."""
    band_order = [b.value for b in SalaryBand]
    results: list[BandBreakdown] = []
    for band in band_order:
        group = df[df["salary_band"] == band]
        total = len(group)
        if total == 0:
            continue
        positive = int(group["expectativa"].sum())
        results.append(BandBreakdown(
            band=band,
            total=total,
            positive=positive,
            negative=total - positive,
            confidence_pct=round(positive / total * 100, 2),
        ))
    return results


def expectation_by_tenure_band(df: pd.DataFrame) -> list[BandBreakdown]:
    """Compute expectation breakdown per tenure band."""
    band_order = [b.value for b in TenureBand]
    results: list[BandBreakdown] = []
    for band in band_order:
        group = df[df["tenure_band"] == band]
        total = len(group)
        if total == 0:
            continue
        positive = int(group["expectativa"].sum())
        results.append(BandBreakdown(
            band=band,
            total=total,
            positive=positive,
            negative=total - positive,
            confidence_pct=round(positive / total * 100, 2),
        ))
    return results


# ═══════════════════════════════════════════════════════════════════════
#  Retention risk & silent strength
# ═══════════════════════════════════════════════════════════════════════


def compute_retention_risk(df: pd.DataFrame) -> list[RetentionRiskGroup]:
    """
    Identify retention risk groups — roles where employees have
    negative expectations, aggregated by role.
    """
    negative = df[df["expectativa"] == False]  # noqa: E712
    results: list[RetentionRiskGroup] = []
    for role, group in negative.groupby("cargo"):
        results.append(RetentionRiskGroup(
            role=str(role),
            count=len(group),
            avg_salary=round(float(group["salario"].mean()), 2),
            avg_tenure=round(float(group["tenure_years"].mean()), 2),
        ))
    return sorted(results, key=lambda r: r.count, reverse=True)


def compute_silent_strength(df: pd.DataFrame) -> list[SilentStrengthZone]:
    """
    Identify silent strength zones — roles with high confidence
    (≥ 70%) but below-median salary.  These are undervalued teams.
    """
    median_salary = df["salario"].median()
    results: list[SilentStrengthZone] = []
    for role, group in df.groupby("cargo"):
        total = len(group)
        if total < 2:
            continue  # need at least 2 people for a meaningful signal
        positive = int(group["expectativa"].sum())
        confidence = positive / total * 100
        avg_sal = float(group["salario"].mean())
        if confidence >= 70.0 and avg_sal < median_salary:
            results.append(SilentStrengthZone(
                role=str(role),
                count=total,
                confidence_pct=round(confidence, 2),
                avg_salary=round(avg_sal, 2),
            ))
    return sorted(results, key=lambda r: r.confidence_pct, reverse=True)


# ═══════════════════════════════════════════════════════════════════════
#  Salary segmentation
# ═══════════════════════════════════════════════════════════════════════


def salary_by_role(df: pd.DataFrame) -> list[RoleSalary]:
    """Salary stats per role."""
    results: list[RoleSalary] = []
    for role, group in df.groupby("cargo"):
        s = group["salario"]
        results.append(RoleSalary(
            role=str(role),
            count=len(group),
            avg_salary=round(float(s.mean()), 2),
            median_salary=round(float(s.median()), 2),
            min_salary=round(float(s.min()), 2),
            max_salary=round(float(s.max()), 2),
        ))
    return sorted(results, key=lambda r: r.avg_salary, reverse=True)


def salary_by_expectation(df: pd.DataFrame) -> list[SalaryByExpectation]:
    """Salary stats split by positive/negative expectation."""
    results: list[SalaryByExpectation] = []
    for label, flag in [("Positiva", True), ("Negativa", False)]:
        group = df[df["expectativa"] == flag]
        if len(group) == 0:
            continue
        results.append(SalaryByExpectation(
            expectation=label,
            count=len(group),
            avg_salary=round(float(group["salario"].mean()), 2),
            median_salary=round(float(group["salario"].median()), 2),
        ))
    return results


def salary_band_breakdown(df: pd.DataFrame) -> list[BandBreakdown]:
    """Headcount per salary band with confidence."""
    return expectation_by_salary_band(df)


def compensation_friction_map(df: pd.DataFrame) -> list[CompensationFrictionPoint]:
    """
    Identify compensation friction points — roles where low pay
    and/or low confidence create retention risk.

    Signals:
    - "low_pay_low_confidence": avg salary below overall median AND confidence < 50%
    - "low_pay_high_confidence": avg salary below overall median AND confidence ≥ 70% (undervalued)
    - "high_pay_low_confidence": avg salary above overall median AND confidence < 50% (disengaged despite pay)
    """
    median_salary = df["salario"].median()
    results: list[CompensationFrictionPoint] = []

    for role, group in df.groupby("cargo"):
        total = len(group)
        if total == 0:
            continue
        positive = int(group["expectativa"].sum())
        confidence = positive / total * 100
        avg_sal = float(group["salario"].mean())

        signal = None
        if avg_sal < median_salary and confidence < 50:
            signal = "low_pay_low_confidence"
        elif avg_sal < median_salary and confidence >= 70:
            signal = "low_pay_high_confidence"
        elif avg_sal >= median_salary and confidence < 50:
            signal = "high_pay_low_confidence"

        if signal:
            results.append(CompensationFrictionPoint(
                role=str(role),
                avg_salary=round(avg_sal, 2),
                confidence_pct=round(confidence, 2),
                count=total,
                signal=signal,
            ))

    return sorted(results, key=lambda r: r.confidence_pct)


# ═══════════════════════════════════════════════════════════════════════
#  Tenure segmentation
# ═══════════════════════════════════════════════════════════════════════


def tenure_by_role(df: pd.DataFrame) -> list[RoleTenure]:
    """Tenure stats per role."""
    results: list[RoleTenure] = []
    for role, group in df.groupby("cargo"):
        t = group["tenure_years"]
        results.append(RoleTenure(
            role=str(role),
            count=len(group),
            avg_tenure=round(float(t.mean()), 2),
            median_tenure=round(float(t.median()), 2),
        ))
    return sorted(results, key=lambda r: r.avg_tenure, reverse=True)


def tenure_by_expectation(df: pd.DataFrame) -> list[TenureByExpectation]:
    """Tenure stats split by positive/negative expectation."""
    results: list[TenureByExpectation] = []
    for label, flag in [("Positiva", True), ("Negativa", False)]:
        group = df[df["expectativa"] == flag]
        if len(group) == 0:
            continue
        results.append(TenureByExpectation(
            expectation=label,
            count=len(group),
            avg_tenure=round(float(group["tenure_years"].mean()), 2),
            median_tenure=round(float(group["tenure_years"].median()), 2),
        ))
    return results


def career_horizon_matrix(df: pd.DataFrame) -> list[CareerHorizonPoint]:
    """
    Build the career horizon scatter data — each employee's
    tenure + salary + expectation for visualization.
    """
    return [
        CareerHorizonPoint(
            tenure_years=round(float(row["tenure_years"]), 4),
            salario=round(float(row["salario"]), 2),
            expectativa=bool(row["expectativa"]),
            cargo=str(row["cargo"]),
        )
        for _, row in df.iterrows()
    ]


# ═══════════════════════════════════════════════════════════════════════
#  Roles comprehensive summary
# ═══════════════════════════════════════════════════════════════════════


def role_summary_table(df: pd.DataFrame) -> list[RoleSummary]:
    """Comprehensive per-role summary: count, salary, tenure, confidence."""
    results: list[RoleSummary] = []
    for role, group in df.groupby("cargo"):
        total = len(group)
        positive = int(group["expectativa"].sum())
        results.append(RoleSummary(
            role=str(role),
            count=total,
            avg_salary=round(float(group["salario"].mean()), 2),
            median_salary=round(float(group["salario"].median()), 2),
            avg_tenure=round(float(group["tenure_years"].mean()), 2),
            median_tenure=round(float(group["tenure_years"].median()), 2),
            confidence_pct=round(positive / total * 100, 2) if total else 0.0,
            positive=positive,
            negative=total - positive,
        ))
    return sorted(results, key=lambda r: r.count, reverse=True)


def sentiment_heatmap(df: pd.DataFrame) -> list[SentimentHeatmapCell]:
    """
    Build a sentiment heatmap: role × tenure band with confidence %.

    Only includes cells where at least 1 employee exists.
    """
    band_order = [b.value for b in TenureBand]
    results: list[SentimentHeatmapCell] = []

    for (role, band), group in df.groupby(["cargo", "tenure_band"]):
        total = len(group)
        positive = int(group["expectativa"].sum())
        results.append(SentimentHeatmapCell(
            role=str(role),
            tenure_band=str(band),
            count=total,
            confidence_pct=round(positive / total * 100, 2) if total else 0.0,
        ))

    # Sort by role name, then by tenure band order
    return sorted(
        results,
        key=lambda c: (c.role, band_order.index(c.tenure_band) if c.tenure_band in band_order else 99),
    )
