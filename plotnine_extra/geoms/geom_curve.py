from __future__ import annotations

import typing

from plotnine._utils import SIZE_FACTOR, to_rgba
from plotnine.doctools import document
from plotnine.geoms.geom import geom
from plotnine.geoms.geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_curve(geom):
    """
    Curved line segments

    {usage}

    Parameters
    ----------
    {common_parameters}
    curvature : float, default=0.5
        Amount of curvature. Negative values produce left-hand curves,
        positive values produce right-hand curves, and zero produces a
        straight line.
    angle : float, default=90
        Amount of skewness in degrees.
    ncp : int, default=5
        Number of control points used to draw the curve. More control
        points creates a smoother curve.
    arrow : ~plotnine.geoms.geom_path.arrow, default=None
        Arrow specification. Default is no arrow.

    See Also
    --------
    plotnine.geom_segment : Straight line segments.
    plotnine.arrow : for adding arrowhead(s) to curves.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y", "xend", "yend"}
    NON_MISSING_AES = {"linetype", "size", "shape"}
    DEFAULT_PARAMS = {
        "curvature": 0.5,
        "angle": 90,
        "ncp": 5,
        "arrow": None,
    }

    draw_legend = staticmethod(geom_path.draw_legend)
    legend_key_size = staticmethod(geom_path.legend_key_size)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.patches import FancyArrowPatch

        data = coord.transform(data, panel_params)
        curvature = params.get("curvature", 0.5)

        for _, row in data.iterrows():
            color = to_rgba(row["color"], row["alpha"])
            linewidth = row["size"] * SIZE_FACTOR

            connectionstyle = f"arc3,rad={curvature}"

            arrow_patch = FancyArrowPatch(
                (row["x"], row["y"]),
                (row["xend"], row["yend"]),
                connectionstyle=connectionstyle,
                linewidth=linewidth,
                linestyle=row["linetype"],
                color=color,
                zorder=params["zorder"],
                rasterized=params["raster"],
            )

            if params.get("arrow"):
                arrow_patch.set_arrowstyle(
                    "->", head_length=8, head_width=5
                )

            ax.add_patch(arrow_patch)
