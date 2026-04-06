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
class stat_welch_anova_test(stat):
    """
    Add Welch's ANOVA test p-values to a plot

    Performs Welch's one-way ANOVA, which does not assume
    equal variances across groups, and displays the result
    as a text annotation.

    {usage}

    Parameters
    ----------
    {common_parameters}
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
    "label"    # Formatted test result label
    "p"        # P-value
    "p_signif" # Significance symbol
    "f"        # F-statistic
    "df1"      # Numerator degrees of freedom
    "df2"      # Denominator degrees of freedom
    "method"   # Name of the test
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_AES = {"label": after_stat("label")}
    DEFAULT_PARAMS = {
        "geom": "text",
        "position": "identity",
        "na_rm": False,
        "label_x_npc": "center",
        "label_y_npc": "top",
        "p_digits": 3,
    }
    CREATES = {
        "label", "p", "p_signif", "f", "df1", "df2", "method",
    }

    def compute_panel(self, data, scales):
        # Group data by x categories
        groups = [
            grp["y"].to_numpy(dtype=float)
            for _, grp in data.groupby("x")
        ]

        if len(groups) < 2:
            return pd.DataFrame()

        result = run_stat_test(groups, method="welch.anova")
        p_digits = self.params["p_digits"]
        p_str = format_p_value(result.p_value, digits=p_digits)
        p_signif = p_to_signif(result.p_value)

        df1 = result.df if result.df is not None else np.nan
        df2 = result.df2 if result.df2 is not None else np.nan
        label = (
            f"Welch's ANOVA, F({df1:.0f}, {df2:.1f})"
            f" = {result.statistic:.2f}, {p_str}"
        )

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
                    "f": [result.statistic],
                    "df1": [df1],
                    "df2": [df2],
                    "method": [result.method],
                }
            ),
            data,
        )
