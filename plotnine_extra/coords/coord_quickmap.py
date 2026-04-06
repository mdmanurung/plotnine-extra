from __future__ import annotations

import typing

import numpy as np

from plotnine.coords.coord_cartesian import coord_cartesian

if typing.TYPE_CHECKING:
    from typing import Any

    from plotnine.iapi import panel_view


class coord_quickmap(coord_cartesian):
    """
    Quick map coordinate system with fixed aspect ratio

    Attempts a quick approximation of a map projection by setting
    the aspect ratio so that 1 unit of latitude and 1 unit of
    longitude have the same distance at the center of the plot.

    Parameters
    ----------
    xlim : tuple
        Limits for the x (longitude) axis.
    ylim : tuple
        Limits for the y (latitude) axis.
    expand : bool
        If ``True``, expand the coordinate axes by some factor.
    """

    is_linear = True

    def __init__(
        self,
        xlim: tuple[Any, Any] | None = None,
        ylim: tuple[Any, Any] | None = None,
        expand: bool = True,
    ):
        super().__init__(xlim=xlim, ylim=ylim, expand=expand)

    def aspect(self, panel_params: panel_view) -> float | None:
        y_range = panel_params.y.range
        y_mid = np.mean(y_range)
        # Approximate Mercator correction for latitude
        return 1 / np.cos(np.radians(y_mid))
