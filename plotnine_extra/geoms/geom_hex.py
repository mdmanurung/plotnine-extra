from __future__ import annotations

import typing

import numpy as np
from plotnine._utils import SIZE_FACTOR, to_rgba
from plotnine.doctools import document
from plotnine.geoms.geom import geom

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_hex(geom):
    """
    Hexagonal binned heatmap

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine_extra.stats.stat_bin_hex : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": None,
        "fill": "#333333",
        "linetype": "solid",
        "size": 0.1,
    }
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {"stat": "bin_hex"}

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.collections import PolyCollection

        data = coord.transform(data, panel_params)
        data["linewidth"] = data["size"] * SIZE_FACTOR

        # Determine hex size from the data
        # Use the median distance between adjacent hex centers
        ux = np.sort(data["x"].unique())
        sx = (
            np.median(np.diff(ux)) / 2
            if len(ux) > 1
            else 0.5
        )

        uy = np.sort(data["y"].unique())
        sy = (
            np.median(np.diff(uy)) / 2
            if len(uy) > 1
            else sx * np.sqrt(3) / 2
        )

        # Build hex vertices for each center
        angles = np.linspace(0, 2 * np.pi, 7)
        hex_x = sx * np.cos(angles)
        hex_y = sy * np.sin(angles)

        verts = []
        facecolor = []
        edgecolor = []
        linewidth = []

        for _, row in data.iterrows():
            vx = row["x"] + hex_x
            vy = row["y"] + hex_y
            verts.append(list(zip(vx, vy)))

            fill = to_rgba(row["fill"], row["alpha"])
            facecolor.append("none" if fill is None else fill)
            edgecolor.append(row["color"] or "none")
            linewidth.append(row["linewidth"])

        col = PolyCollection(
            verts,
            facecolors=facecolor,
            edgecolors=edgecolor,
            linewidths=linewidth,
            zorder=params["zorder"],
            rasterized=params["raster"],
        )

        ax.add_collection(col)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        from matplotlib.patches import RegularPolygon

        linewidth = data["size"] * SIZE_FACTOR
        linewidth = np.min([linewidth, da.width / 4, da.height / 4])

        if data["color"] is None:
            linewidth = 0

        facecolor = to_rgba(data["fill"], data["alpha"])
        if facecolor is None:
            facecolor = "none"

        radius = min(da.width, da.height) / 2
        hex_patch = RegularPolygon(
            (da.width / 2, da.height / 2),
            numVertices=6,
            radius=radius,
            linewidth=linewidth,
            facecolor=facecolor,
            edgecolor=data["color"],
        )
        da.add_artist(hex_patch)
        return da
