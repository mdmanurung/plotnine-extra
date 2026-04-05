from __future__ import annotations

from typing import TYPE_CHECKING

from ..doctools import document
from .stat import stat

if TYPE_CHECKING:
    import pandas as pd

    from plotnine.iapi import panel_scales


@document
class stat_sf(stat):
    """
    Identity stat for simple features

    {usage}

    This is essentially an identity stat that passes through
    GeoDataFrame geometry information.

    Parameters
    ----------
    {common_parameters}
    """

    REQUIRED_AES = set()
    DEFAULT_PARAMS = {
        "geom": "sf",
    }

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        return data
