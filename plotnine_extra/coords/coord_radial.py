from __future__ import annotations

import typing

from .coord_polar import coord_polar

if typing.TYPE_CHECKING:
    from typing import Any, Literal


class coord_radial(coord_polar):
    """
    Radial coordinate system

    A more modern version of
    :class:`~plotnine_extra.coords.coord_polar.coord_polar`,
    with the same functionality but a cleaner API.

    Parameters
    ----------
    theta : str
        Which variable to map to angle. Either ``"x"`` (default)
        or ``"y"``.
    start : float
        Offset from 12 o'clock in radians where theta starts.
    direction : int
        ``1`` for clockwise, ``-1`` for counterclockwise.
    r_axis_inside : bool
        If ``True``, place the r-axis labels inside the plot.
    expand : bool
        If ``True``, expand the coordinate axes by some factor.
    """

    def __init__(
        self,
        theta: Literal["x", "y"] = "x",
        start: float = 0,
        direction: int = 1,
        r_axis_inside: bool = False,
        xlim: tuple[Any, Any] | None = None,
        ylim: tuple[Any, Any] | None = None,
        expand: bool = True,
    ):
        super().__init__(
            theta=theta,
            start=start,
            direction=direction,
            xlim=xlim,
            ylim=ylim,
            expand=expand,
        )
        self.r_axis_inside = r_axis_inside
