"""
Shared contour computation utilities.

Used by stat_contour, stat_contour_filled, stat_density_2d,
and stat_density_2d_filled.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


def contour_lines(X, Y, Z, levels: int | FloatArrayLike):
    """
    Calculate contour lines from a 2D grid of values.

    Parameters
    ----------
    X : array_like
        X coordinates of the grid.
    Y : array_like
        Y coordinates of the grid.
    Z : array_like
        Values at each grid point.
    levels : int or array_like
        Number of contour levels, or explicit level values.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns x, y, level, piece.
    """
    from contourpy import contour_generator

    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Z = np.asarray(Z, dtype=np.float64)
    zmin, zmax = Z.min(), Z.max()
    cgen = contour_generator(
        X, Y, Z, name="mpl2014", corner_mask=False, chunk_size=0
    )

    if isinstance(levels, int):
        from mizani.breaks import breaks_extended

        levels = breaks_extended(n=levels)((zmin, zmax))

    segments = []
    piece_ids = []
    level_values = []
    start_pid = 1
    for level in levels:
        vertices, *_ = cgen.create_contour(level)
        for pid, piece in enumerate(vertices, start=start_pid):
            n = len(piece)  # pyright: ignore
            segments.append(piece)
            piece_ids.append(np.repeat(pid, n))
            level_values.append(np.repeat(level, n))
            start_pid = pid + 1

    if segments:
        x, y = np.vstack(segments).T
        piece = np.hstack(piece_ids)
        level = np.hstack(level_values)
    else:
        x, y = [], []
        piece = []
        level = []

    data = pd.DataFrame(
        {
            "x": x,
            "y": y,
            "level": level,
            "piece": piece,
        }
    )
    return data


def contour_filled(X, Y, Z, levels: int | FloatArrayLike):
    """
    Calculate filled contour polygons from a 2D grid of values.

    Parameters
    ----------
    X : array_like
        X coordinates of the grid.
    Y : array_like
        Y coordinates of the grid.
    Z : array_like
        Values at each grid point.
    levels : int or array_like
        Number of contour levels, or explicit level values.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns x, y, level, piece.
    """
    from contourpy import contour_generator

    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Z = np.asarray(Z, dtype=np.float64)
    zmin, zmax = Z.min(), Z.max()
    cgen = contour_generator(
        X, Y, Z, name="mpl2014", corner_mask=False, chunk_size=0
    )

    if isinstance(levels, int):
        from mizani.breaks import breaks_extended

        levels = breaks_extended(n=levels)((zmin, zmax))

    segments = []
    piece_ids = []
    level_values = []
    start_pid = 1

    for i in range(len(levels) - 1):
        level_low = levels[i]
        level_high = levels[i + 1]
        vertices, *_ = cgen.create_filled_contour(level_low, level_high)
        for pid, piece in enumerate(vertices, start=start_pid):
            n = len(piece)  # pyright: ignore
            segments.append(piece)
            piece_ids.append(np.repeat(pid, n))
            level_values.append(np.repeat(level_low, n))
            start_pid = pid + 1

    if segments:
        x, y = np.vstack(segments).T
        piece = np.hstack(piece_ids)
        level = np.hstack(level_values)
    else:
        x, y = [], []
        piece = []
        level = []

    data = pd.DataFrame(
        {
            "x": x,
            "y": y,
            "level": level,
            "piece": piece,
        }
    )
    return data
