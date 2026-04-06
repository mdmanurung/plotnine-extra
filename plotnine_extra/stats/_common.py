"""
Common helpers for stat layers.

Provides utilities for preserving panel/group columns
from the input data in compute_panel results.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def preserve_panel_columns(
    result: pd.DataFrame,
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ensure PANEL and group columns from input data
    are present in the result DataFrame.

    Parameters
    ----------
    result : DataFrame
        The computed result from compute_panel.
    data : DataFrame
        The input data to compute_panel.

    Returns
    -------
    DataFrame
        Result with PANEL and group columns preserved.
    """
    if result.empty:
        return result

    for col in ("PANEL", "group"):
        if col in data.columns and col not in result.columns:
            result[col] = data[col].iloc[0]

    return result
