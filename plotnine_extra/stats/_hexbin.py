"""
Shared hexagonal binning utilities.

Used by stat_bin_hex, stat_summary_hex, and geom_hex.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def hexbin(
    x,
    y,
    weight=None,
    bins=30,
    range_x=None,
    range_y=None,
):
    """
    Perform hexagonal binning of 2D data.

    Parameters
    ----------
    x, y : array_like
        Data coordinates.
    weight : array_like, optional
        Weights for each point.
    bins : int
        Approximate number of bins across the x range.
    range_x, range_y : tuple of float
        Data range for x and y axes.

    Returns
    -------
    pandas.DataFrame
        With columns: x, y (hex centers), count, density,
        and hex vertex columns for polygon rendering.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    if weight is None:
        weight = np.ones_like(x)
    else:
        weight = np.asarray(weight, dtype=np.float64)

    if range_x is None:
        range_x = (x.min(), x.max())
    if range_y is None:
        range_y = (y.min(), y.max())

    # Compute hex grid spacing
    x_span = range_x[1] - range_x[0]
    y_span = range_y[1] - range_y[0]

    if x_span == 0 or y_span == 0:
        return pd.DataFrame(columns=["x", "y", "count", "density"])

    # Hex dimensions
    sx = x_span / bins
    sy = sx * np.sqrt(3)  # Regular hexagon height

    # Assign each point to a hex cell
    # Use offset coordinates for hex grid
    jx = (x - range_x[0]) / sx
    iy = (y - range_y[0]) / sy

    # Two offset grids
    ix1 = np.round(jx).astype(int)
    iy1 = np.round(iy).astype(int)

    ix2 = np.floor(jx + 0.5).astype(int)
    iy2 = np.floor(iy + 0.5).astype(int)

    # Offset for odd/even rows
    cx1 = range_x[0] + ix1 * sx
    cy1 = range_y[0] + iy1 * sy
    cx2 = range_x[0] + (ix2 + 0.5) * sx
    cy2 = range_y[0] + (iy2 + 0.5) * sy

    d1 = (x - cx1) ** 2 + (y - cy1) ** 2
    d2 = (x - cx2) ** 2 + (y - cy2) ** 2

    # Choose the closest hex center
    use_grid2 = d2 < d1
    hx = np.where(use_grid2, cx2, cx1)
    hy = np.where(use_grid2, cy2, cy1)

    # Aggregate by hex center
    df = pd.DataFrame({"hx": hx, "hy": hy, "weight": weight})
    grouped = df.groupby(["hx", "hy"], sort=False)
    result = grouped["weight"].agg(["sum", "count"]).reset_index()
    result.columns = ["x", "y", "count", "npoints"]
    result["count"] = result["count"].astype(float)

    total = result["count"].sum()
    result["density"] = result["count"] / total if total > 0 else 0

    return result


def hex_vertices(cx, cy, sx, sy=None):
    """
    Generate vertices for a regular hexagon centered at (cx, cy).

    Parameters
    ----------
    cx, cy : float
        Center coordinates.
    sx : float
        Half-width of the hexagon (distance from center to vertex
        along the x-axis).
    sy : float, optional
        Half-height. If None, computed for regular hexagon.

    Returns
    -------
    numpy.ndarray
        Array of shape (7, 2) with vertex coordinates (closed polygon).
    """
    if sy is None:
        sy = sx * np.sqrt(3) / 2

    angles = np.linspace(0, 2 * np.pi, 7)
    vx = cx + sx * np.cos(angles)
    vy = cy + sy * np.sin(angles)
    return np.column_stack([vx, vy])
