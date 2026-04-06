from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from plotnine.doctools import document
from plotnine.stats.stat import stat

if TYPE_CHECKING:
    import pandas as pd

    from plotnine.iapi import panel_scales


@document
class stat_spoke(stat):
    """
    Convert angle and radius to xend and yend

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_spoke : The default `geom` for this `stat`.
    """

    REQUIRED_AES = {"x", "y", "angle", "radius"}
    DEFAULT_PARAMS = {
        "geom": "spoke",
    }
    CREATES = {"xend", "yend"}

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        data = data.copy()
        data["xend"] = (
            data["x"] + np.cos(data["angle"]) * data["radius"]
        )
        data["yend"] = (
            data["y"] + np.sin(data["angle"]) * data["radius"]
        )
        return data
