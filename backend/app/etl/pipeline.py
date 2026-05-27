"""
ETL pipeline orchestrator — reads, cleans, parses, validates, and caches.

The pipeline runs once on first access and caches the result in memory
since the underlying dataset is static.
"""

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING

import pandas as pd

from app.config import settings
from app.etl.reader import read_excel
from app.etl.cleaners import clean
from app.etl.parsers import parse_tenure_column
from app.etl.validators import validate

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def run_pipeline() -> pd.DataFrame:
    """
    Execute the full ETL pipeline and return the clean dataframe.

    Steps:
        1. Read raw Excel data.
        2. Clean column names, string values, expectativa, and cargo.
        3. Parse tenure strings to float years.
        4. Validate data integrity.

    The result is cached via ``lru_cache`` — subsequent calls return
    the same dataframe without re-reading the file.

    Returns
    -------
    pd.DataFrame
        Cleaned, parsed, and validated employee dataframe.
    """
    logger.info("Starting ETL pipeline …")

    # Step 1 — Read
    df = read_excel(settings.dataset_path)
    logger.info("Read %d rows, %d columns from %s", len(df), len(df.columns), settings.dataset_path)

    # Step 2 — Clean
    df = clean(df)
    logger.info("Cleaning complete")

    # Step 3 — Parse tenure
    df = parse_tenure_column(df)
    logger.info("Tenure parsing complete")

    # Step 4 — Validate
    df = validate(df)
    logger.info("ETL pipeline finished successfully")

    return df


def get_dataframe() -> pd.DataFrame:
    """
    Public accessor for the cached dataframe.

    Returns a *copy* to prevent accidental mutation of the cached data.
    """
    return run_pipeline().copy()
