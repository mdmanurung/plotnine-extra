from __future__ import annotations

import numpy as np
import pandas as pd

from plotnine.doctools import document
from plotnine.stats.stat import stat


@document
class stat_align(stat):
    """
    Align observations across groups

    {usage}

    Aligns x values across groups by interpolating y values at a
    common set of x positions. Useful for ribbon/area plots that
    compare groups.

    Parameters
    ----------
    {common_parameters}
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "line",
    }

    def compute_panel(self, data, scales):
        # Get all unique x values across all groups
        all_x = np.sort(data["x"].unique())

        results = []
        for group, gdata in data.groupby("group"):
            gdata = gdata.sort_values("x")
            # Interpolate y values at all x positions
            y_interp = np.interp(
                all_x,
                gdata["x"].to_numpy(),
                gdata["y"].to_numpy(),
            )
            new_data = pd.DataFrame(
                {
                    "x": all_x,
                    "y": y_interp,
                    "group": group,
                }
            )
            # Carry over other columns from first row
            for col in gdata.columns:
                if col not in ("x", "y", "group"):
                    new_data[col] = gdata[col].iloc[0]
            results.append(new_data)

        if results:
            return pd.concat(results, ignore_index=True)
        return data
