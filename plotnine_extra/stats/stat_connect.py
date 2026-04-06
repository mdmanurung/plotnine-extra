from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine.doctools import document
from plotnine.stats.stat import stat

if TYPE_CHECKING:
    import pandas as pd

    from plotnine.iapi import panel_scales


@document
class stat_connect(stat):
    """
    Connect observations in order of x value

    {usage}

    Sorts data by x value and connects observations with lines.
    Similar to stat_identity but ensures proper ordering.

    Parameters
    ----------
    {common_parameters}
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "line",
    }

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        return data.sort_values("x").reset_index(drop=True)
