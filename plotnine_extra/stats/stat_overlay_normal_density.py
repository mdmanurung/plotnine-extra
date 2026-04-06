import numpy as np
import pandas as pd
from plotnine.doctools import document
from plotnine.stats.stat import stat
from scipy.stats import norm


@document
class stat_overlay_normal_density(stat):
    """
    Overlay a normal density curve on a histogram or density plot

    Computes a theoretical normal distribution with the same
    mean and standard deviation as the data, useful for
    checking normality assumptions.

    {usage}

    Parameters
    ----------
    {common_parameters}
    n : int, default=512
        Number of points at which to evaluate the density.

    See Also
    --------
    plotnine.geom_line : The default `geom` for this `stat`.
    plotnine.stat_density : For kernel density estimation.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "density"  # Normal density at each point
    ```

    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "line",
        "position": "identity",
        "na_rm": False,
        "n": 512,
    }
    CREATES = {"density"}

    def compute_group(self, data, scales):
        x = data["x"].to_numpy(dtype=float)
        n = self.params["n"]

        mean = np.mean(x)
        std = np.std(x, ddof=1)

        if std == 0:
            return pd.DataFrame({"x": [], "density": []})

        x_grid = np.linspace(mean - 4 * std, mean + 4 * std, n)
        density = norm.pdf(x_grid, mean, std)

        return pd.DataFrame(
            {
                "x": x_grid,
                "density": density,
            }
        )
