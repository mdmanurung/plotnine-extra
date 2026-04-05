from __future__ import annotations

import typing

import numpy as np

from .coord_cartesian import coord_cartesian

if typing.TYPE_CHECKING:
    from typing import Any, Literal

    import pandas as pd

    from plotnine.iapi import labels_view
    from plotnine.typing import FloatArray, FloatSeries

    from ..iapi import panel_view


class coord_polar(coord_cartesian):
    """
    Polar coordinate system

    Maps x to angle (theta) and y to radius (r), or vice versa.

    Parameters
    ----------
    theta : str
        Which variable to map to angle. Either ``"x"`` (default)
        or ``"y"``.
    start : float
        Offset from 12 o'clock in radians where theta starts.
    direction : int
        ``1`` for clockwise, ``-1`` for counterclockwise.
    xlim : tuple
        Limits for the x axis.
    ylim : tuple
        Limits for the y axis.
    expand : bool
        If ``True``, expand the coordinate axes by some factor.
    """

    is_linear = False
    projection = "polar"

    def __init__(
        self,
        theta: Literal["x", "y"] = "x",
        start: float = 0,
        direction: int = 1,
        xlim: tuple[Any, Any] | None = None,
        ylim: tuple[Any, Any] | None = None,
        expand: bool = True,
    ):
        super().__init__(xlim=xlim, ylim=ylim, expand=expand)
        self.theta = theta
        self.start = start
        self.direction = direction

    def aspect(self, panel_params: panel_view) -> float | None:
        return 1.0

    def transform(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        munch: bool = False,
    ) -> pd.DataFrame:
        data = data.copy()

        # Determine which is theta and which is r
        if self.theta == "x":
            theta_range = panel_params.x.range
            r_range = panel_params.y.range
        else:
            theta_range = panel_params.y.range
            r_range = panel_params.x.range

        # Scale theta to [0, 2*pi]
        if "x" in data.columns and "y" in data.columns:
            if self.theta == "x":
                theta_data = data["x"]
                r_data = data["y"]
            else:
                theta_data = data["y"]
                r_data = data["x"]

            # Rescale theta to [0, 2*pi]
            theta_span = theta_range[1] - theta_range[0]
            if theta_span != 0:
                theta_scaled = (
                    ((theta_data - theta_range[0]) / theta_span) * 2 * np.pi
                )
            else:
                theta_scaled = np.zeros_like(theta_data)

            # Apply start offset and direction
            theta_scaled = self.start + self.direction * theta_scaled

            # Rescale r to [0, 1] range for the polar plot
            r_span = r_range[1] - r_range[0]
            if r_span != 0:
                r_scaled = (r_data - r_range[0]) / r_span
            else:
                r_scaled = np.ones_like(r_data) * 0.5

            # In matplotlib's polar axes, x = theta, y = r
            data["x"] = theta_scaled
            data["y"] = r_scaled

        # Handle segment endpoints
        for suffix in ("end", "min", "max"):
            xcol = f"x{suffix}"
            ycol = f"y{suffix}"
            if xcol in data.columns and ycol in data.columns:
                if self.theta == "x":
                    theta_data = data[xcol]
                    r_data = data[ycol]
                else:
                    theta_data = data[ycol]
                    r_data = data[xcol]

                theta_span = theta_range[1] - theta_range[0]
                if theta_span != 0:
                    theta_scaled = (
                        ((theta_data - theta_range[0]) / theta_span)
                        * 2
                        * np.pi
                    )
                else:
                    theta_scaled = np.zeros_like(theta_data)

                theta_scaled = self.start + self.direction * theta_scaled

                r_span = r_range[1] - r_range[0]
                if r_span != 0:
                    r_scaled = (r_data - r_range[0]) / r_span
                else:
                    r_scaled = np.ones_like(r_data) * 0.5

                data[xcol] = theta_scaled
                data[ycol] = r_scaled

        return data

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> FloatArray:
        # In polar coordinates, use arc length
        arc = np.sqrt(
            np.diff(np.asarray(x, dtype=np.float64)) ** 2
            + np.diff(np.asarray(y, dtype=np.float64)) ** 2,
            dtype=np.float64,
        )
        max_dist = 2 * np.pi  # max possible arc
        return arc / max_dist

    def labels(self, cur_labels: labels_view) -> labels_view:
        if self.theta == "y":
            cur_labels.x, cur_labels.y = cur_labels.y, cur_labels.x
        return cur_labels
