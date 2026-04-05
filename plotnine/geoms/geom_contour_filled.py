from ..doctools import document
from .geom_polygon import geom_polygon


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
    plotnine.stat_contour_filled : The default `stat` for this `geom`.
    plotnine.geom_contour : Unfilled contour variant.
    """

    DEFAULT_PARAMS = {"stat": "contour_filled"}
