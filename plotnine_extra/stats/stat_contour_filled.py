from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from plotnine.doctools import document
from plotnine.mapping.evaluation import after_stat
from plotnine.stats.stat import stat

from ._contour import contour_filled
from .stat_contour import _grid_from_data

if TYPE_CHECKING:
    from plotnine.iapi import panel_scales


@document
class stat_contour_filled(stat):
    """
    Compute filled contour bands from a 2D grid of z values

    {usage}

    Parameters
    ----------
    {common_parameters}
    levels : int | array_like, default=5
        Contour levels. If an integer, it specifies the maximum number
        of levels. If array_like, it is the levels themselves.

    See Also
    --------
    plotnine_extra.geoms.geom_contour_filled : The default `geom`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "level"     # density level of a contour band (lower bound)
    "piece"     # Numeric id of a contour in a given group
    ```
    """
    REQUIRED_AES = {"x", "y", "z"}
    DEFAULT_PARAMS = {
        "geom": "contour_filled",
        "levels": 5,
    }
    DEFAULT_AES = {"fill": after_stat("level")}
    CREATES = {"level", "piece"}

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        group = data["group"].iloc[0]
        levels = self.params["levels"]

        X, Y, Z = _grid_from_data(data)
        result = contour_filled(X, Y, Z, levels)

        if len(result) == 0:
            return pd.DataFrame()

        groups = str(group) + "-00" + result["piece"].astype(str)
        result["group"] = groups
        return result
