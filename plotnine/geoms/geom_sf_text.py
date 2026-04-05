from ..doctools import document
from .geom_text import geom_text


@document
class geom_sf_text(geom_text):
    """
    Text for simple feature geometries

    {usage}

    Places text at the centroid of each geometry. The data should
    be a GeoDataFrame with a `geometry` column.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_sf : Draw simple feature geometries.
    plotnine.geom_sf_label : Label variant with background box.
    """

    DEFAULT_PARAMS = {"stat": "sf_coordinates"}
