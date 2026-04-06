from plotnine.doctools import document
from plotnine.geoms.geom_path import geom_path


@document
class geom_contour(geom_path):
    """
    Contour lines from a 2D grid of z values

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine_extra.stats.stat_contour : The default `stat` for this `geom`.
    plotnine_extra.geoms.geom_contour_filled : Filled contour variant.
    """

    DEFAULT_PARAMS = {"stat": "contour"}
