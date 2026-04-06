from __future__ import annotations

import typing

from plotnine.coords.coord_cartesian import coord_cartesian

if typing.TYPE_CHECKING:
    from typing import Any

    from plotnine.iapi import panel_view


class coord_sf(coord_cartesian):
    """
    Coordinate system for simple features

    A coordinate system designed for spatial data that handles
    CRS (Coordinate Reference System) information from GeoDataFrames.

    Parameters
    ----------
    xlim : tuple
        Limits for the x (longitude) axis.
    ylim : tuple
        Limits for the y (latitude) axis.
    expand : bool
        If ``True``, expand the coordinate axes by some factor.
    datum : str or CRS
        The CRS to use as the datum for the plot. Default is WGS84
        (EPSG:4326).
    """

    is_linear = True

    def __init__(
        self,
        xlim: tuple[Any, Any] | None = None,
        ylim: tuple[Any, Any] | None = None,
        expand: bool = True,
        datum: Any = None,
    ):
        super().__init__(xlim=xlim, ylim=ylim, expand=expand)
        self.datum = datum

    def aspect(self, panel_params: panel_view) -> float | None:
        import numpy as np

        # Apply Mercator-like correction
        y_range = panel_params.y.range
        y_mid = np.mean(y_range)
        return 1 / np.cos(np.radians(y_mid))
