from __future__ import annotations

from typing import TYPE_CHECKING

from ..doctools import document
from .stat import stat

if TYPE_CHECKING:
    import pandas as pd

    from plotnine.iapi import panel_scales


@document
class stat_sf_coordinates(stat):
    """
    Extract centroid coordinates from simple feature geometries

    {usage}

    Computes the centroid of each geometry and returns x, y
    coordinates suitable for use with text or label geoms.

    Parameters
    ----------
    {common_parameters}
    """

    REQUIRED_AES = set()
    DEFAULT_PARAMS = {
        "geom": "text",
    }
    CREATES = {"x", "y"}

    def compute_group(
        self, data: pd.DataFrame, scales: panel_scales
    ) -> pd.DataFrame:
        if "geometry" not in data.columns:
            return data

        centroids = data["geometry"].apply(
            lambda geom: geom.centroid if hasattr(geom, "centroid") else geom
        )
        data = data.copy()
        data["x"] = centroids.apply(
            lambda p: p.x if hasattr(p, "x") else float("nan")
        )
        data["y"] = centroids.apply(
            lambda p: p.y if hasattr(p, "y") else float("nan")
        )
        return data
