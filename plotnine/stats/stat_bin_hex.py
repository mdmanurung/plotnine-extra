from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..doctools import document
from ..mapping.evaluation import after_stat
from ._hexbin import hexbin
from .stat import stat

if TYPE_CHECKING:
    import pandas as pd

    from plotnine.iapi import panel_scales


@document
class stat_bin_hex(stat):
    """
    Hexagonal bin counts

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=30
        Approximate number of bins across the x range.

    See Also
    --------
    plotnine.geom_hex : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "count"   # number of points in hex bin
    "density" # density of points in bin, scaled to integrate to 1
    ```
    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "hex",
        "bins": 30,
    }
    DEFAULT_AES = {"fill": after_stat("count"), "weight": None}
    CREATES = {"count", "density"}

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        bins = self.params["bins"]
        weight = data.get("weight")

        if weight is None:
            weight = np.ones(len(data["x"]))

        range_x = scales.x.dimension()
        range_y = scales.y.dimension()

        result = hexbin(
            data["x"].to_numpy(),
            data["y"].to_numpy(),
            weight=weight.to_numpy()
            if hasattr(weight, "to_numpy")
            else weight,
            bins=bins,
            range_x=range_x,
            range_y=range_y,
        )

        if "npoints" in result.columns:
            result = result.drop(columns=["npoints"])

        return result


stat_binhex = stat_bin_hex
