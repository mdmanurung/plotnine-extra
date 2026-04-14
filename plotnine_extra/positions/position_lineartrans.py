"""
Linear (2x2) coordinate transform position adjustment.

A direct port of ``ggh4x::position_lineartrans``: every (x, y)
data point is left-multiplied by a 2x2 matrix and optionally
translated. Useful for shearing, rotating or scaling layers
without touching the underlying data.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from plotnine.positions.position import position

if TYPE_CHECKING:
    import pandas as pd


class position_lineartrans(position):
    """
    Apply an affine 2x2 linear transformation to ``x`` and ``y``.

    Parameters
    ----------
    scale : tuple of float, default ``(1, 1)``
        Scale factors ``(sx, sy)``.
    shear : tuple of float, default ``(0, 0)``
        Shear factors ``(shx, shy)``.
    angle : float, default 0
        Rotation in degrees, applied after scale + shear.
    M : array-like, optional
        A 2x2 matrix that overrides ``scale`` / ``shear`` /
        ``angle`` if supplied.
    """

    REQUIRED_AES = {"x", "y"}

    def __init__(
        self,
        scale: tuple[float, float] = (1.0, 1.0),
        shear: tuple[float, float] = (0.0, 0.0),
        angle: float = 0.0,
        M: np.ndarray | None = None,
    ):
        super().__init__()
        self.scale = scale
        self.shear = shear
        self.angle = angle
        self.M = (
            np.asarray(M, dtype=float)
            if M is not None
            else self._build_matrix()
        )

    def _build_matrix(self) -> np.ndarray:
        sx, sy = self.scale
        shx, shy = self.shear
        # scale + shear
        S = np.array([[sx, shx], [shy, sy]], dtype=float)
        if self.angle:
            theta = np.deg2rad(self.angle)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array([[c, -s], [s, c]], dtype=float)
            return R @ S
        return S

    def setup_params(self, data):
        return {"M": self.M}

    @classmethod
    def compute_layer(
        cls,
        data: "pd.DataFrame",
        params,
        layout,
    ) -> "pd.DataFrame":
        M = params["M"]
        xy = np.column_stack([data["x"].to_numpy(), data["y"].to_numpy()])
        new = xy @ M.T
        data = data.copy()
        data["x"] = new[:, 0]
        data["y"] = new[:, 1]
        return data
