from __future__ import annotations

import numpy as np
import pandas as pd
from plotnine.doctools import document
from plotnine.stats.stat import stat
from scipy.stats import chi2


@document
class stat_conf_ellipse(stat):
    """
    Compute confidence ellipses around group barycenters

    Draws a confidence ellipse based on the covariance
    structure of the bivariate data within each group.

    {usage}

    Parameters
    ----------
    {common_parameters}
    level : float, default=0.95
        Confidence level for the ellipse.
    npoint : int, default=100
        Number of points used to draw the ellipse.
    bary : bool, default=True
        If ``True``, compute the ellipse around the
        barycenter (mean). If ``False``, compute the
        ellipse around the data cloud.

    See Also
    --------
    plotnine.geom_path : The default `geom` for this `stat`.
    plotnine.geom_polygon : Alternative `geom` for filled
        ellipses.
    """

    _aesthetics_doc = """
    {aesthetics_table}
    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "path",
        "position": "identity",
        "na_rm": False,
        "level": 0.95,
        "npoint": 100,
        "bary": True,
    }

    def compute_group(self, data, scales) -> pd.DataFrame:
        x = data["x"].to_numpy(dtype=float)
        y = data["y"].to_numpy(dtype=float)

        if len(x) < 3:
            return pd.DataFrame({"x": [], "y": []})

        level = self.params["level"]
        npoint = self.params["npoint"]
        bary = self.params["bary"]

        center_x = np.mean(x)
        center_y = np.mean(y)

        # Covariance matrix
        cov_mat = np.cov(x, y)

        if bary:
            cov_mat = cov_mat / len(x)

        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_mat)

        # Scaling factor from chi-squared distribution
        scale = np.sqrt(chi2.ppf(level, 2))

        # Generate ellipse points
        theta = np.linspace(0, 2 * np.pi, npoint)
        unit_circle = np.column_stack([np.cos(theta), np.sin(theta)])

        # Transform unit circle to ellipse
        transform = eigenvectors @ np.diag(np.sqrt(eigenvalues))
        ellipse = unit_circle @ transform.T * scale

        ellipse_x = ellipse[:, 0] + center_x
        ellipse_y = ellipse[:, 1] + center_y

        return pd.DataFrame(
            {
                "x": ellipse_x,
                "y": ellipse_y,
            }
        )
