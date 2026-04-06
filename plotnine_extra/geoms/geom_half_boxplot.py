"""
Half-boxplot geom for raincloud plots.

Draws a boxplot shifted to one side, useful for combining
with half-violins and jittered points.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plotnine.doctools import document
from plotnine.geoms.geom_boxplot import geom_boxplot

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_half_boxplot(geom_boxplot):
    """
    Half-width boxplot shifted to one side

    Draws a narrower boxplot offset to the left or right,
    designed for combining with half-violins and jittered
    points in raincloud plots.

    {usage}

    Parameters
    ----------
    {common_parameters}
    side : str
        Which side to shift to: ``"r"`` (right) or
        ``"l"`` (left). Default ``"r"``.
    nudge : float
        Additional horizontal offset in data units.
        Default ``0``.
    half_width : float
        Width of the half-boxplot as a fraction of the
        full boxplot width. Default ``0.5``.
    """

    _aesthetics_doc = """
    {aesthetics_table}
    """
    DEFAULT_PARAMS = {
        **geom_boxplot.DEFAULT_PARAMS,
        "side": "r",
        "nudge": 0,
        "half_width": 0.5,
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
        half_width = params.get("half_width", 0.5)

        # Modify the data to shift and narrow the box
        data = data.copy()

        if "xmin" in data.columns and "xmax" in data.columns:
            # Calculate the full width
            width = data["xmax"] - data["xmin"]
            center = (data["xmax"] + data["xmin"]) / 2
            new_width = width * half_width

            if side == "r":
                data["xmin"] = center + nudge
                data["xmax"] = center + new_width / 2 + nudge
            else:
                data["xmin"] = center - new_width / 2 + nudge
                data["xmax"] = center + nudge

        # Delegate to parent draw_group
        return geom_boxplot.draw_group(data, panel_params, coord, ax, params)
