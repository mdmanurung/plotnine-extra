from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
from plotnine.doctools import document
from plotnine.geoms.geom import geom
from plotnine.geoms.geom_path import geom_path

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_bracket(geom):
    """
    Draw significance brackets with labels

    Draws a U-shaped bracket (two vertical tips connected
    by a horizontal bar) with a centered text label,
    typically used for significance annotations.

    {usage}

    Parameters
    ----------
    {common_parameters}
    tip_length : float, default=0.02
        Length of the bracket tips as a fraction of the
        y data range.
    bracket_nudge_y : float, default=0
        Vertical offset for the bracket.
    label_size : float, default=8
        Font size for the label text.
    vjust : float, default=0
        Vertical justification of the label relative
        to the bracket.
    """

    _aesthetics_doc = """
    {aesthetics_table}
    """
    REQUIRED_AES = {"xmin", "xmax", "y", "label"}
    DEFAULT_AES = {
        "color": "black",
        "alpha": 1,
    }
    DEFAULT_PARAMS = {
        "stat": "identity",
        "position": "identity",
        "na_rm": False,
        "tip_length": 0.02,
        "bracket_nudge_y": 0,
        "label_size": 8,
        "vjust": 0,
    }
    draw_legend = staticmethod(geom_path.draw_legend)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        tip_length = params.get("tip_length", 0.02)
        bracket_nudge_y = params.get("bracket_nudge_y", 0)
        label_size = params.get("label_size", 8)
        vjust = params.get("vjust", 0)

        for _, row in data.iterrows():
            xmin = row["xmin"]
            xmax = row["xmax"]
            y = row["y"] + bracket_nudge_y
            label = row.get("label", "")
            color = row.get("color", "black")
            alpha = row.get("alpha", 1.0)

            # Compute tip length in data coordinates
            y_range = panel_params.y.range
            tip = tip_length * (y_range[1] - y_range[0])

            # Draw the bracket: two tips + horizontal bar
            bracket_x = [
                xmin, xmin, xmax, xmax,
            ]
            bracket_y = [
                y - tip, y, y, y - tip,
            ]

            ax.plot(
                bracket_x,
                bracket_y,
                color=color,
                alpha=alpha,
                linewidth=0.75,
                solid_capstyle="butt",
            )

            # Draw the label centered above the bracket
            x_mid = (xmin + xmax) / 2
            y_text = y + tip * 0.3 + vjust
            if label:
                ax.text(
                    x_mid,
                    y_text,
                    str(label),
                    ha="center",
                    va="bottom",
                    fontsize=label_size,
                    color=color,
                    alpha=alpha,
                )

        return np.nan
