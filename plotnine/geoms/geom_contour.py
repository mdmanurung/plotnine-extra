from ..doctools import document
from .geom_path import geom_path


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
    plotnine.stat_contour : The default `stat` for this `geom`.
    plotnine.geom_contour_filled : Filled contour variant.
    """

    DEFAULT_PARAMS = {"stat": "contour"}
