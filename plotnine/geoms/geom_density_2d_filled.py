from ..doctools import document
from .geom_polygon import geom_polygon


@document
class geom_density_2d_filled(geom_polygon):
    """
    Filled 2D density estimate contours

    {usage}

    This is a filled version of [](`~plotnine.geoms.geom_density_2d`).

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_density_2d_filled : The default `stat` for this `geom`.
    plotnine.geom_density_2d : Unfilled 2D density contours.
    """

    DEFAULT_PARAMS = {"stat": "density_2d_filled"}
