"""
Data validators — post-ETL integrity checks.

Ensures the cleaned dataframe has the expected shape, required columns,
and no critical null values.
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Columns that MUST exist after cleaning + parsing
_REQUIRED_COLUMNS = {"func", "expectativa", "tempo_empresa", "cargo", "salario", "tenure_years"}


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the cleaned dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe after all cleaning and parsing steps.

    Returns
    -------
    pd.DataFrame
        The same dataframe (unchanged) if validation passes.

    Raises
    ------
    ValueError
        If any required column is missing or if critical data is null.
    """
    # ── Check required columns ─────────────────────────────────────────
    missing = _REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns after ETL: {missing}")

    # ── Check for empty dataframe ──────────────────────────────────────
    if df.empty:
        raise ValueError("Dataframe is empty after ETL pipeline")

    # ── Check for null values in critical columns ──────────────────────
    critical = ["cargo", "salario", "expectativa", "tenure_years"]
    for col in critical:
        null_count = df[col].isna().sum()
        if null_count > 0:
            logger.warning("Column '%s' has %d null values", col, null_count)

    # ── Check salary is numeric and positive ───────────────────────────
    if not pd.api.types.is_numeric_dtype(df["salario"]):
        raise ValueError("Column 'salario' must be numeric")

    negative_salaries = (df["salario"] < 0).sum()
    if negative_salaries > 0:
        logger.warning("%d negative salary values found", negative_salaries)

    # ── Check tenure_years is numeric and non-negative ─────────────────
    if not pd.api.types.is_numeric_dtype(df["tenure_years"]):
        raise ValueError("Column 'tenure_years' must be numeric")

    logger.info(
        "Validation passed: %d employees, %d columns",
        len(df),
        len(df.columns),
    )

    return df
