from ..doctools import document
from .geom_path import geom_path


@document
class geom_function(geom_path):
    """
    Draw a function as a continuous curve

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_function : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "function"}
