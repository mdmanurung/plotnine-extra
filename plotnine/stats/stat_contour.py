from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from ..doctools import document
from ..mapping.evaluation import after_stat
from ._contour import contour_lines
from .stat import stat

if TYPE_CHECKING:
    from plotnine.iapi import panel_scales


@document
class stat_contour(stat):
    """
    Compute contour lines from a 2D grid of z values

    {usage}

    Parameters
    ----------
    {common_parameters}
    levels : int | array_like, default=5
        Contour levels. If an integer, it specifies the maximum number
        of levels. If array_like, it is the levels themselves.

    See Also
    --------
    plotnine.geom_contour : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "level"     # density level of a contour
    "piece"     # Numeric id of a contour in a given group
    ```
    """
    REQUIRED_AES = {"x", "y", "z"}
    DEFAULT_PARAMS = {
        "geom": "contour",
        "levels": 5,
    }
    DEFAULT_AES = {"color": after_stat("level")}
    CREATES = {"level", "piece"}

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        group = data["group"].iloc[0]
        levels = self.params["levels"]

        X, Y, Z = _grid_from_data(data)
        result = contour_lines(X, Y, Z, levels)

        if len(result) == 0:
            return pd.DataFrame()

        groups = str(group) + "-00" + result["piece"].astype(str)
        result["group"] = groups
        return result


def _grid_from_data(data: pd.DataFrame):
    """
    Reshape x, y, z columns into 2D grids.

    Assumes the data represent a regular grid (all unique x values
    paired with all unique y values).
    """
    x_unique = np.sort(data["x"].unique())
    y_unique = np.sort(data["y"].unique())
    nx = len(x_unique)
    ny = len(y_unique)

    if nx * ny != len(data):
        from scipy.interpolate import griddata

        X, Y = np.meshgrid(x_unique, y_unique)
        Z = griddata(
            (data["x"].to_numpy(), data["y"].to_numpy()),
            data["z"].to_numpy(),
            (X, Y),
            method="linear",
        )
        Z = np.nan_to_num(Z, nan=0.0)
    else:
        sorted_data = data.sort_values(["y", "x"])
        Z = sorted_data["z"].to_numpy().reshape(ny, nx)
        X, Y = np.meshgrid(x_unique, y_unique)

    return X, Y, Z
