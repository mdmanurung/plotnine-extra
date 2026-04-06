from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine.doctools import document
from plotnine.stats.stat import stat

if TYPE_CHECKING:
    import pandas as pd

    from plotnine.iapi import panel_scales


@document
class stat_manual(stat):
    """
    Manual stat specification

    {usage}

    A pass-through stat for when the user provides pre-computed
    aesthetic values directly. Equivalent to stat_identity but
    makes the intent explicit.

    Parameters
    ----------
    {common_parameters}
    """

    REQUIRED_AES = set()
    DEFAULT_PARAMS = {
        "geom": "point",
    }

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        return data
