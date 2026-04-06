from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from plotnine.doctools import document
from plotnine.mapping.evaluation import after_stat
from plotnine.stats.binning import fuzzybreaks
from plotnine.stats.stat import stat
from plotnine.stats.stat_bin_2d import dual_param

if TYPE_CHECKING:
    from plotnine.iapi import panel_scales


@document
class stat_summary_2d(stat):
    """
    Summarise z values at rectangular 2D bins

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=30
        Number of bins. Overridden by binwidth.
    binwidth : float, default=None
        The width of the bins.
    breaks : array_like | tuple[array_like, array_like], default=None
        Bin boundaries.
    drop : bool, default=True
        If `True`{{.py}}, removes all cells with zero counts.
    fun : callable, default=None
        Summary function that takes an array and returns a single
        value. Default is `numpy.mean`.

    See Also
    --------
    plotnine.geom_bin_2d : Related geom.
    plotnine.stat_summary_bin : 1D variant.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "xmin"    # x lower bound for the bin
    "xmax"    # x upper bound for the bin
    "ymin"    # y lower bound for the bin
    "ymax"    # y upper bound for the bin
    "value"   # summary value
    ```
    """
    REQUIRED_AES = {"x", "y", "z"}
    DEFAULT_PARAMS = {
        "geom": "rect",
        "bins": 30,
        "breaks": None,
        "binwidth": None,
        "drop": True,
        "fun": None,
    }
    DEFAULT_AES = {"fill": after_stat("value")}
    CREATES = {"xmin", "xmax", "ymin", "ymax", "value"}

    def setup_params(self, data):
        params = self.params
        params["bins"] = dual_param(params["bins"])
        params["breaks"] = dual_param(params["breaks"])
        params["binwidth"] = dual_param(params["binwidth"])

        if params["fun"] is None:
            params["fun"] = np.mean

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        bins = self.params["bins"]
        breaks = self.params["breaks"]
        binwidth = self.params["binwidth"]
        drop = self.params["drop"]
        fun = self.params["fun"]

        range_x = scales.x.dimension()
        range_y = scales.y.dimension()

        x = np.append(data["x"], range_x)
        y = np.append(data["y"], range_y)

        xbreaks = fuzzybreaks(
            scales.x,
            breaks=breaks.x,
            binwidth=binwidth.x,
            bins=bins.x,
        )
        ybreaks = fuzzybreaks(
            scales.y,
            breaks.y,
            binwidth=binwidth.y,
            bins=bins.y,
        )

        xbins = pd.cut(x, bins=xbreaks, labels=False, right=True)
        ybins = pd.cut(y, bins=ybreaks, labels=False, right=True)

        xbins = xbins[:-2]
        ybins = ybins[:-2]

        ybreaks[0] -= np.diff(np.diff(ybreaks))[0]
        xbreaks[0] -= np.diff(np.diff(xbreaks))[0]

        df = pd.DataFrame(
            {
                "xbins": xbins,
                "ybins": ybins,
                "z": data["z"].to_numpy(),
            }
        )

        rects = []
        keys = itertools.product(
            range(len(ybreaks) - 1), range(len(xbreaks) - 1)
        )
        for j, i in keys:
            mask = (df["xbins"] == i) & (df["ybins"] == j)
            zvals = df.loc[mask, "z"]

            if len(zvals) == 0:
                if drop:
                    continue
                value = np.nan
            else:
                value = fun(zvals.to_numpy())

            row = [
                xbreaks[i],
                xbreaks[i + 1],
                ybreaks[j],
                ybreaks[j + 1],
                value,
            ]
            rects.append(row)

        new_data = pd.DataFrame(
            rects,
            columns=["xmin", "xmax", "ymin", "ymax", "value"],
        )
        return new_data
