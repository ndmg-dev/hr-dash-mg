"""
Data cleaners — normalizes column names, string values, and categorical data.

Responsibilities:
- Rename Portuguese column headers to clean snake_case English names.
- Normalize ``expectativa`` ("sim"/"não") → boolean.
- Normalize ``cargo`` gender variations (e.g. "Administrativa" → "Administrativo").
- Trim all string values.
"""

from __future__ import annotations

import re

import pandas as pd


# ── Column renaming map ────────────────────────────────────────────────
# Keys must match the raw Excel headers exactly (including trailing spaces).
_COLUMN_MAP: dict[str, str] = {
    "Func.": "func",
    "Expectativa para daqui a 5 anos": "expectativa",
    "Tempo de empresa": "tempo_empresa",
    "Cargo": "cargo",
    "Salário ": "salario",   # note: trailing space in the original header
    "Salário": "salario",    # fallback without trailing space
}

# ── Cargo normalization rules ──────────────────────────────────────────
# Maps feminine/variant suffixes to their canonical masculine form.
_CARGO_REPLACEMENTS: list[tuple[str, str]] = [
    (r"\bAdministrativa\b", "Administrativo"),
]


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename raw Portuguese columns to clean snake_case names."""
    # Strip whitespace from column names first
    df.columns = [c.strip() for c in df.columns]

    # Now build rename map matching stripped names
    rename_map: dict[str, str] = {}
    for original, target in _COLUMN_MAP.items():
        stripped = original.strip()
        if stripped in df.columns:
            rename_map[stripped] = target

    df = df.rename(columns=rename_map)
    return df


def trim_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all string columns."""
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
    return df


def normalize_expectativa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the ``expectativa`` column from string to boolean.

    - ``"sim"`` → ``True``  (positive outlook)
    - ``"não"`` / anything else → ``False``
    """
    df["expectativa"] = (
        df["expectativa"]
        .str.lower()
        .str.strip()
        .map(lambda v: v == "sim")
    )
    return df


def normalize_cargo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize role names to canonical forms.

    Currently handles:
    - Gender variation: "Analista Administrativa I" → "Analista Administrativo I"
    """
    for pattern, replacement in _CARGO_REPLACEMENTS:
        df["cargo"] = df["cargo"].apply(
            lambda v: re.sub(pattern, replacement, v) if isinstance(v, str) else v
        )
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run all cleaning steps in order.

    Pipeline: rename → trim → normalize expectativa → normalize cargo.
    """
    df = rename_columns(df)
    df = trim_strings(df)
    df = normalize_expectativa(df)
    df = normalize_cargo(df)
    return df
