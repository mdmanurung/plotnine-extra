from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine.doctools import document

from ._base_stat_test import _base_stat_test

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


@document
class stat_friedman_test(_base_stat_test):
    """
    Add Friedman test p-values to a plot

    Performs the Friedman test, a non-parametric test for
    repeated measures (alternative to repeated-measures
    ANOVA), and displays the result as a text annotation.

    {usage}

    Parameters
    ----------
    {common_parameters}
    wid : str, default=None
        Column name identifying subjects/individuals.
        Required for reshaping the data into the wide
        format needed by the Friedman test.
    label_x_npc : float or str, default="center"
        Normalized x position for the label.
    label_y_npc : float or str, default="top"
        Normalized y position for the label.
    p_digits : int, default=3
        Number of digits for p-value formatting.

    See Also
    --------
    plotnine.geom_text : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "label"      # Formatted test result label
    "p"          # P-value
    "p_signif"   # Significance symbol
    "statistic"  # Test statistic (chi-squared)
    "df"         # Degrees of freedom
    "method"     # Name of the test
    ```

    """
    DEFAULT_PARAMS = {
        "geom": "text",
        "position": "identity",
        "na_rm": False,
        "wid": None,
        "label_x_npc": "center",
        "label_y_npc": "top",
        "p_digits": 3,
    }
    CREATES = {
        "label", "p", "p_signif", "statistic", "df", "method",
    }

    _test_method = "friedman.test"
    _min_groups = 3

    def _extract_groups(
        self,
        data: pd.DataFrame,
    ) -> list[np.ndarray]:
        """
        Extract groups, using *wid* for subject alignment
        when available.
        """
        wid = self.params.get("wid")

        if wid and wid in data.columns:
            groups = []
            for _, grp in data.groupby("x"):
                sorted_vals = (
                    grp.sort_values(wid)["y"]
                    .to_numpy(dtype=float)
                )
                groups.append(sorted_vals)
        else:
            groups = [
                grp["y"].to_numpy(dtype=float)
                for _, grp in data.groupby("x")
            ]

        # Ensure equal group sizes for Friedman test
        if groups:
            min_len = min(len(g) for g in groups)
            groups = [g[:min_len] for g in groups]

        return groups
