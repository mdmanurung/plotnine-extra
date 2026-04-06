from plotnine.doctools import document
from plotnine.geoms.geom_polygon import geom_polygon


@document
class geom_contour_filled(geom_polygon):
    """
    Filled contour bands from a 2D grid of z values

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine_extra.stats.stat_contour_filled : The default `stat`.
    plotnine_extra.geoms.geom_contour : Unfilled contour variant.
    """

    DEFAULT_PARAMS = {"stat": "contour_filled"}
