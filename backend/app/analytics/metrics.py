"""
Core metrics computation — aggregated statistics for salary, tenure,
and expectations.

Also provides helper functions for band classification used across
multiple analytics modules.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.config import settings
from app.models.enums import SalaryBand, TenureBand
from app.models.metrics import (
    ExpectationBreakdown,
    SalaryStats,
    TenureStats,
    HistogramBin,
)


# ═══════════════════════════════════════════════════════════════════════
#  Band classification helpers
# ═══════════════════════════════════════════════════════════════════════


def classify_salary_band(salary: float) -> SalaryBand:
    """Classify a salary value into its band."""
    if salary <= settings.salary_band_junior_max:
        return SalaryBand.JUNIOR
    elif salary <= settings.salary_band_pleno_max:
        return SalaryBand.PLENO
    elif salary <= settings.salary_band_senior_max:
        return SalaryBand.SENIOR
    else:
        return SalaryBand.ESPECIALISTA


def classify_tenure_band(tenure_years: float) -> TenureBand:
    """Classify a tenure value (in years) into its band."""
    if tenure_years <= settings.tenure_band_newcomer_max:
        return TenureBand.NEWCOMER
    elif tenure_years <= settings.tenure_band_growing_max:
        return TenureBand.GROWING
    elif tenure_years <= settings.tenure_band_established_max:
        return TenureBand.ESTABLISHED
    elif tenure_years <= settings.tenure_band_veteran_max:
        return TenureBand.VETERAN
    else:
        return TenureBand.LEGACY


def add_band_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``salary_band`` and ``tenure_band`` columns to the dataframe."""
    df = df.copy()
    df["salary_band"] = df["salario"].apply(classify_salary_band)
    df["tenure_band"] = df["tenure_years"].apply(classify_tenure_band)
    return df


# ═══════════════════════════════════════════════════════════════════════
#  Expectation metrics
# ═══════════════════════════════════════════════════════════════════════


def compute_expectation_breakdown(df: pd.DataFrame) -> ExpectationBreakdown:
    """Compute positive/negative expectation counts and percentages."""
    total = len(df)
    positive = int(df["expectativa"].sum())
    negative = total - positive
    return ExpectationBreakdown(
        positive=positive,
        negative=negative,
        positive_pct=round(positive / total * 100, 2) if total else 0.0,
        negative_pct=round(negative / total * 100, 2) if total else 0.0,
    )


def compute_confidence_index(df: pd.DataFrame) -> float:
    """Compute the overall confidence index (% positive expectations)."""
    total = len(df)
    if total == 0:
        return 0.0
    return round(float(df["expectativa"].sum()) / total * 100, 2)


# ═══════════════════════════════════════════════════════════════════════
#  Salary metrics
# ═══════════════════════════════════════════════════════════════════════


def compute_salary_stats(df: pd.DataFrame) -> SalaryStats:
    """Compute descriptive statistics for the salary column."""
    s = df["salario"]
    return SalaryStats(
        avg=round(float(s.mean()), 2),
        median=round(float(s.median()), 2),
        min=round(float(s.min()), 2),
        max=round(float(s.max()), 2),
        std=round(float(s.std()), 2),
    )


def compute_salary_histogram(df: pd.DataFrame, bins: int = 10) -> list[HistogramBin]:
    """Generate histogram bins for salary distribution."""
    counts, bin_edges = np.histogram(df["salario"].dropna(), bins=bins)
    return [
        HistogramBin(
            bin_start=round(float(bin_edges[i]), 2),
            bin_end=round(float(bin_edges[i + 1]), 2),
            count=int(counts[i]),
        )
        for i in range(len(counts))
    ]


# ═══════════════════════════════════════════════════════════════════════
#  Tenure metrics
# ═══════════════════════════════════════════════════════════════════════


def compute_tenure_stats(df: pd.DataFrame) -> TenureStats:
    """Compute descriptive statistics for tenure_years."""
    t = df["tenure_years"]
    return TenureStats(
        avg=round(float(t.mean()), 2),
        median=round(float(t.median()), 2),
        min=round(float(t.min()), 2),
        max=round(float(t.max()), 2),
    )


def compute_tenure_histogram(df: pd.DataFrame, bins: int = 10) -> list[HistogramBin]:
    """Generate histogram bins for tenure distribution."""
    counts, bin_edges = np.histogram(df["tenure_years"].dropna(), bins=bins)
    return [
        HistogramBin(
            bin_start=round(float(bin_edges[i]), 4),
            bin_end=round(float(bin_edges[i + 1]), 4),
            count=int(counts[i]),
        )
        for i in range(len(counts))
    ]
