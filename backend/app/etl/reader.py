"""
Excel reader — loads the raw dataset from disk.

Drops any unnamed / index-leak columns that pandas sometimes creates
when reading Excel files.
"""

from pathlib import Path

import pandas as pd


def read_excel(path: Path) -> pd.DataFrame:
    """
    Read the HR dataset from an Excel file.

    Parameters
    ----------
    path : Path
        Absolute or relative path to the ``.xlsx`` file.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with unnamed columns removed.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at *path*.
    ValueError
        If the file is empty or contains no usable columns.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_excel(path, engine="openpyxl")

    # Drop columns whose header starts with "Unnamed"
    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    if df.empty or len(df.columns) == 0:
        raise ValueError("Dataset is empty or has no usable columns")

    return df
