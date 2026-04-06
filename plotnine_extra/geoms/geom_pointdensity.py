from __future__ import annotations

from plotnine.doctools import document
from plotnine.geoms.geom_point import geom_point


@document
class geom_pointdensity(geom_point):
    """
    Scatterplot with density estimation at each point

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine_extra.stats.stat_pointdensity.stat_pointdensity
    """

    DEFAULT_PARAMS = {
        "stat": "pointdensity",
        "position": "identity",
        "na_rm": False,
    }
