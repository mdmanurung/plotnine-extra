import pandas as pd
from plotnine.doctools import document
from plotnine.stats.stat import stat


@document
class stat_mean(stat):
    """
    Compute group mean points

    Calculates the mean x and y coordinates for each group,
    producing a single centroid point per group.

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_point : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}
    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "point",
        "position": "identity",
        "na_rm": False,
    }

    def compute_group(self, data, scales):
        return pd.DataFrame(
            {
                "x": [data["x"].mean()],
                "y": [data["y"].mean()],
            }
        )
