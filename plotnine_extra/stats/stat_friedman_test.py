import numpy as np
import pandas as pd
from plotnine.doctools import document
from plotnine.mapping.evaluation import after_stat
from plotnine.stats.stat import stat

from ._common import preserve_panel_columns
from ._label_utils import compute_label_position
from ._p_format import format_p_value, p_to_signif
from ._stat_test import run_stat_test


@document
class stat_friedman_test(stat):
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
    REQUIRED_AES = {"x", "y"}
    DEFAULT_AES = {"label": after_stat("label")}
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

    def compute_panel(self, data, scales):
        wid = self.params.get("wid")

        if wid and wid in data.columns:
            # Reshape: pivot so each subject has one row,
            # columns are treatment levels
            groups = []
            for _, grp in data.groupby("x"):
                # Sort by subject ID for alignment
                sorted_vals = (
                    grp.sort_values(wid)["y"]
                    .to_numpy(dtype=float)
                )
                groups.append(sorted_vals)
        else:
            # Fall back to grouping by x
            groups = [
                grp["y"].to_numpy(dtype=float)
                for _, grp in data.groupby("x")
            ]

        if len(groups) < 3:
            return pd.DataFrame()

        # Ensure equal group sizes for Friedman test
        min_len = min(len(g) for g in groups)
        groups = [g[:min_len] for g in groups]

        result = run_stat_test(groups, method="friedman.test")
        p_digits = self.params["p_digits"]
        p_str = format_p_value(result.p_value, digits=p_digits)
        p_signif = p_to_signif(result.p_value)
        label = f"Friedman test, {p_str}"

        x_pos = compute_label_position(
            data["x"].min(),
            data["x"].max(),
            self.params["label_x_npc"],
        )
        y_pos = compute_label_position(
            data["y"].min(),
            data["y"].max(),
            self.params["label_y_npc"],
        )

        return preserve_panel_columns(
            pd.DataFrame(
                {
                    "x": [x_pos],
                    "y": [y_pos],
                    "label": [label],
                    "p": [result.p_value],
                    "p_signif": [p_signif],
                    "statistic": [result.statistic],
                    "df": [
                        result.df
                        if result.df is not None
                        else np.nan
                    ],
                    "method": [result.method],
                }
            ),
            data,
        )
