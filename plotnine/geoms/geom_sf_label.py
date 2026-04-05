from ..doctools import document
from .geom_label import geom_label


@document
class geom_sf_label(geom_label):
    """
    Labels for simple feature geometries

    {usage}

    Places labels at the centroid of each geometry. The data should
    be a GeoDataFrame with a `geometry` column.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_sf : Draw simple feature geometries.
    plotnine.geom_sf_text : Text variant without background box.
    """

    DEFAULT_PARAMS = {"stat": "sf_coordinates"}
