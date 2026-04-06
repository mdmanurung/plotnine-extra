from __future__ import annotations

import pandas as pd
from plotnine.doctools import document
from plotnine.stats.stat import stat


@document
class stat_stars(stat):
    """
    Draw star segments from centroid to each point

    Computes line segments from the group centroid (mean x, y)
    to each individual data point, creating a star-shaped pattern.

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_segment : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "xend"  # x-coordinate of segment endpoint
    "yend"  # y-coordinate of segment endpoint
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "segment",
        "position": "identity",
        "na_rm": False,
    }
    CREATES = {"xend", "yend"}

    def compute_group(self, data, scales) -> pd.DataFrame:
        mean_x = data["x"].mean()
        mean_y = data["y"].mean()

        return pd.DataFrame(
            {
                "x": mean_x,
                "y": mean_y,
                "xend": data["x"].to_numpy(),
                "yend": data["y"].to_numpy(),
            }
        )
