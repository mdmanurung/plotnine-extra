from plotnine.doctools import document
from plotnine.geoms.geom_polygon import geom_polygon


@document
class geom_density_2d_filled(geom_polygon):
    """
    Filled 2D density estimate contours

    {usage}

    This is a filled version of
    :class:`~plotnine.geoms.geom_density_2d.geom_density_2d`.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine_extra.stats.stat_density_2d_filled : The default `stat`.
    plotnine.geom_density_2d : Unfilled 2D density contours.
    """

    DEFAULT_PARAMS = {"stat": "density_2d_filled"}
