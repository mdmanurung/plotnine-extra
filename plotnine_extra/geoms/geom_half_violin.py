"""
Half-violin geom for raincloud plots.

Draws only one side of a violin plot, useful for
combining with jittered points and boxplots to create
raincloud plots.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
from plotnine.doctools import document
from plotnine.geoms.geom_violin import geom_violin

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_half_violin(geom_violin):
    """
    Half-violin plot showing one side of the density

    Draws only the left or right half of a violin,
    enabling raincloud plots when combined with
    :class:`~plotnine.geom_boxplot` and jittered points.

    {usage}

    Parameters
    ----------
    {common_parameters}
    side : str
        Which side to draw: ``"r"`` (right/top) or
        ``"l"`` (left/bottom). Default ``"r"``.
    nudge : float
        Amount to shift the half-violin away from center
        in data units. Default ``0``.
    """

    _aesthetics_doc = """
    {aesthetics_table}
    """
    DEFAULT_PARAMS = {
        **geom_violin.DEFAULT_PARAMS,
        "side": "r",
        "nudge": 0,
    }

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        side = params.get("side", "r")
        nudge = params.get("nudge", 0)

        # The violin data has x, y, and violinwidth
        # columns. We modify x to clip to one side.
        if "violinwidth" not in data.columns:
            # Fall back to parent drawing
            return geom_violin.draw_group(
                data, panel_params, coord, ax, params
            )

        data = data.copy()
        half_w = data["violinwidth"] / 2

        if side == "r":
            # Keep only the right half: x stays at
            # center to center+width
            xmin = data["x"]
            xmax = data["x"] + half_w
        else:
            # Keep only the left half
            xmin = data["x"] - half_w
            xmax = data["x"]

        # Apply nudge
        xmin = xmin + nudge
        xmax = xmax + nudge

        # Build polygon for the half violin
        data = coord.transform(data, panel_params)

        # Re-derive in transformed coordinates
        x_center = data["x"].to_numpy(dtype=float)
        y_vals = data["y"].to_numpy(dtype=float)
        vw = data["violinwidth"].to_numpy(dtype=float)

        # Compute x range of transformed coords
        if len(x_center) < 2:
            return

        # Build the half-violin polygon
        half = vw / 2
        if side == "r":
            x_poly = np.concatenate([x_center, x_center[::-1] + half[::-1]])
            y_poly = np.concatenate([y_vals, y_vals[::-1]])
        else:
            x_poly = np.concatenate(
                [
                    x_center - half,
                    x_center[::-1],
                ]
            )
            y_poly = np.concatenate([y_vals, y_vals[::-1]])

        # Apply nudge in transformed space
        # (approximate: scale nudge by data range)
        if nudge != 0:
            x_range = panel_params.x.range[1] - panel_params.x.range[0]
            nudge_t = nudge / x_range if x_range > 0 else 0
            x_poly = x_poly + nudge_t

        color = data["color"].iloc[0]
        fill = data["fill"].iloc[0]
        alpha = data["alpha"].iloc[0]
        size = data["size"].iloc[0]

        from matplotlib.patches import Polygon

        poly = Polygon(
            np.column_stack([x_poly, y_poly]),
            closed=True,
            facecolor=fill,
            edgecolor=color,
            alpha=alpha,
            linewidth=size,
            zorder=params.get("zorder", 1),
        )
        ax.add_patch(poly)
