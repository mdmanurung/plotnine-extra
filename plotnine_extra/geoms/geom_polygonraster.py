"""
``geom_polygonraster``: raster cells reparameterised as polygons.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from plotnine.doctools import document
from plotnine.geoms.geom_polygon import geom_polygon


@document
class geom_polygonraster(geom_polygon):
    """
    Draw raster-like cells as individual polygons.

    {usage}

    Parameters
    ----------
    {common_parameters}
    hjust, vjust : float
        Horizontal and vertical justification of each raster cell around
        its ``x`` and ``y`` coordinate.
    """

    DEFAULT_PARAMS = {
        "stat": "identity",
        "position": "identity",
        "na_rm": False,
        "hjust": 0.5,
        "vjust": 0.5,
    }

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.copy()
        hjust = self.params["hjust"]
        vjust = self.params["vjust"]

        x_width = _regular_step_width(data["x"])
        y_width = _regular_step_width(data["y"])

        data["xmin"] = data["x"] - x_width * (1 - hjust)
        data["xmax"] = data["x"] + x_width * hjust
        data["ymin"] = data["y"] - y_width * (1 - vjust)
        data["ymax"] = data["y"] + y_width * vjust
        data["_raster_group"] = np.arange(len(data))

        if not len(data):
            return data.iloc[0:0].copy()

        # One polygon per input cell: its four corners, in order.
        corners = np.stack(
            [
                data["xmin"].to_numpy(),
                data["xmax"].to_numpy(),
                data["xmax"].to_numpy(),
                data["xmin"].to_numpy(),
            ],
            axis=1,
        ).ravel()
        corner_y = np.stack(
            [
                data["ymin"].to_numpy(),
                data["ymin"].to_numpy(),
                data["ymax"].to_numpy(),
                data["ymax"].to_numpy(),
            ],
            axis=1,
        ).ravel()
        n_cells = len(data)
        # Every corner repeats its cell's other columns, so broadcast those
        # once instead of materialising a dict per cell.
        rows = np.repeat(np.arange(n_cells), 4)
        out = data.iloc[rows].reset_index(drop=True)
        out["x"] = corners
        out["y"] = corner_y
        out["_raster_group"] = np.repeat(np.arange(n_cells), 4)
        out["group"] = np.repeat(np.arange(n_cells), 4)
        return out


def _regular_step_width(values: pd.Series) -> float:
    unique = np.sort(pd.Series(values).dropna().unique())
    diffs = np.diff(unique)
    if len(diffs) == 0:
        return 1.0
    return float(diffs.min())
