from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from plotnine.doctools import document
from plotnine.stats.density import get_var_type, kde
from plotnine.stats.stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


@document
class stat_density_2d_filled(stat):
    """
    Compute filled 2D kernel density estimation contours

    {usage}

    Parameters
    ----------
    {common_parameters}
    contour : bool, default=True
        Whether to create filled contours of the 2d density estimate.
    n : int, default=64
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    levels : int | array_like, default=5
        Contour levels. If an integer, it specifies the maximum number
        of levels, if array_like it is the levels themselves.
    package : str, default="statsmodels"
        Package whose kernel density estimation to use.
    kde_params : dict
        Keyword arguments to pass on to the kde class.

    See Also
    --------
    plotnine_extra.geoms.geom_density_2d_filled : The default `geom`.
    plotnine.stat_density_2d : Unfilled variant.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "level"     # density level of a contour band
    "piece"     # Numeric id of a contour in a given group
    ```
    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "density_2d_filled",
        "contour": True,
        "package": "statsmodels",
        "kde_params": None,
        "n": 64,
        "levels": 5,
    }
    CREATES = {"y"}

    def setup_params(self, data):
        params = self.params
        if params["kde_params"] is None:
            params["kde_params"] = {}

        kde_params = params["kde_params"]
        if params["package"] == "statsmodels":
            params["package"] = "statsmodels-m"
            if "var_type" not in kde_params:
                x_type = get_var_type(data["x"])
                y_type = get_var_type(data["y"])
                kde_params["var_type"] = f"{x_type}{y_type}"

    def compute_group(self, data, scales):
        params = self.params
        package = params["package"]
        kde_params = params["kde_params"]

        group = data["group"].iloc[0]
        range_x = scales.x.dimension()
        range_y = scales.y.dimension()
        _x = np.linspace(range_x[0], range_x[1], params["n"])
        _y = np.linspace(range_y[0], range_y[1], params["n"])

        X, Y = np.meshgrid(_x, _y)
        x = cast("FloatArrayLike", data["x"].to_numpy())
        y = cast("FloatArrayLike", data["y"].to_numpy())
        var_data = np.array([x, y]).T
        grid = np.array([X.flatten(), Y.flatten()]).T
        density = kde(var_data, grid, package, **kde_params)

        if params["contour"]:
            Z = density.reshape(len(_x), len(_y))
            data = _contour_filled(X, Y, Z, params["levels"])
            groups = (
                str(group) + "-00" + data["piece"].astype(str)
            )
            data["group"] = groups
        else:
            data = pd.DataFrame(
                {
                    "x": X.flatten(),
                    "y": Y.flatten(),
                    "density": density.flatten(),
                    "group": group,
                    "level": 1,
                    "piece": 1,
                }
            )

        return data


def _contour_filled(X, Y, Z, levels: int | FloatArrayLike):
    """
    Calculate filled contour polygons
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
        vertices, *_ = cgen.create_filled_contour(
            level_low, level_high
        )
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
