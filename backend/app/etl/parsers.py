"""
Tenure string parser — converts Portuguese duration strings to float years.

Handles every known variation in the dataset:
- ``"9 anos"``          → 9.0
- ``"1 ano"``           → 1.0
- ``"1 anos"``          → 1.0   (typo in source data)
- ``"6 meses"``         → 0.5
- ``"2 meses"``         → 0.1667
- ``"1 ano 8 meses"``   → 1.6667
- ``"1 ano  8 meses"``  → 1.6667  (double space)
- ``"6 anos 3 meses"``  → 6.25
- ``"12 anos e 7 meses."`` → 12.5833  (with "e" and period)
"""

from __future__ import annotations

import re

import pandas as pd


# Regex pattern that extracts optional years and optional months from the
# Portuguese tenure string.  Handles "ano"/"anos", "mes"/"meses",
# optional "e" connector, extra whitespace, and trailing punctuation.
_TENURE_PATTERN = re.compile(
    r"(?:(\d+)\s*anos?)?[\s,e]*(?:(\d+)\s*m[eê]s(?:es)?)?",
    re.IGNORECASE,
)


def parse_tenure(value: str) -> float:
    """
    Parse a single Portuguese tenure string into fractional years.

    Parameters
    ----------
    value : str
        Raw string like ``"1 ano 8 meses"`` or ``"6 meses"``.

    Returns
    -------
    float
        Duration expressed in years (e.g. 1.6667 for 1 year 8 months).
        Returns 0.0 if the string cannot be parsed.
    """
    if not isinstance(value, str):
        return 0.0

    # Remove trailing periods and extra whitespace
    cleaned = value.strip().rstrip(".")

    match = _TENURE_PATTERN.search(cleaned)
    if not match:
        return 0.0

    years_str, months_str = match.groups()
    years = int(years_str) if years_str else 0
    months = int(months_str) if months_str else 0

    return round(years + months / 12, 4)


def parse_tenure_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a ``tenure_years`` column by parsing ``tempo_empresa``.

    The original ``tempo_empresa`` column is preserved for reference.
    """
    df["tenure_years"] = df["tempo_empresa"].apply(parse_tenure)
    return df
