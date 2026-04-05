from ..doctools import document
from .geom_map import geom_map


@document
class geom_sf(geom_map):
    """
    Draw simple feature geometries

    {usage}

    A convenience wrapper around [](`~plotnine.geoms.geom_map`)
    for drawing GeoDataFrame geometries. Supports all shapely
    geometry types: Point, MultiPoint, LineString, MultiLineString,
    Polygon, MultiPolygon.

    Parameters
    ----------
    {common_parameters}

    Notes
    -----
    The data should be a GeoDataFrame with a `geometry` column.

    See Also
    --------
    plotnine.geom_map : The parent geom.
    """

    DEFAULT_PARAMS = {"stat": "identity"}
