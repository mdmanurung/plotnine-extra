from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from ..doctools import document
from ..mapping.evaluation import after_stat
from .stat import stat

if TYPE_CHECKING:
    from plotnine.iapi import panel_scales


@document
class stat_summary_hex(stat):
    """
    Summarise z values in hexagonal bins

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=30
        Approximate number of bins across the x range.
    fun : callable, default=None
        Summary function that takes an array and returns a single value.
        Default is `numpy.mean`.

    See Also
    --------
    plotnine.geom_hex : The default `geom` for this `stat`.
    plotnine.stat_bin_hex : Hex binning without z summary.
    plotnine.stat_summary_2d : Rectangular 2D summary.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "value"   # summary value for each hex bin
    ```
    """
    REQUIRED_AES = {"x", "y", "z"}
    DEFAULT_PARAMS = {
        "geom": "hex",
        "bins": 30,
        "fun": None,
    }
    DEFAULT_AES = {"fill": after_stat("value")}
    CREATES = {"value"}

    def setup_params(self, data):
        if self.params["fun"] is None:
            self.params["fun"] = np.mean

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        bins = self.params["bins"]
        fun = self.params["fun"]

        range_x = scales.x.dimension()
        range_y = scales.y.dimension()

        x = data["x"].to_numpy()
        y = data["y"].to_numpy()
        z = data["z"].to_numpy()

        # Compute hex centers using the same logic as stat_bin_hex
        x_span = range_x[1] - range_x[0]
        if x_span == 0:
            return pd.DataFrame(columns=["x", "y", "value"])

        sx = x_span / bins
        sy = sx * np.sqrt(3)

        # Assign to hex centers
        jx = (x - range_x[0]) / sx
        iy = (y - range_y[0]) / sy

        ix1 = np.round(jx).astype(int)
        iy1 = np.round(iy).astype(int)
        ix2 = np.floor(jx + 0.5).astype(int)
        iy2 = np.floor(iy + 0.5).astype(int)

        cx1 = range_x[0] + ix1 * sx
        cy1 = range_y[0] + iy1 * sy
        cx2 = range_x[0] + (ix2 + 0.5) * sx
        cy2 = range_y[0] + (iy2 + 0.5) * sy

        d1 = (x - cx1) ** 2 + (y - cy1) ** 2
        d2 = (x - cx2) ** 2 + (y - cy2) ** 2

        use_grid2 = d2 < d1
        hx = np.where(use_grid2, cx2, cx1)
        hy = np.where(use_grid2, cy2, cy1)

        df = pd.DataFrame({"hx": hx, "hy": hy, "z": z})
        grouped = df.groupby(["hx", "hy"], sort=False)
        result = grouped["z"].agg(fun).reset_index()
        result.columns = ["x", "y", "value"]

        return result
