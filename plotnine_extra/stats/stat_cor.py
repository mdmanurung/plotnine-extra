import numpy as np
import pandas as pd
from plotnine.doctools import document
from plotnine.mapping.evaluation import after_stat
from plotnine.stats.stat import stat
from scipy import stats as sp_stats


@document
class stat_cor(stat):
    """
    Add correlation coefficients with p-values to a scatter plot

    Computes correlation coefficients (Pearson, Spearman, or
    Kendall) and formats them as text labels including p-values.

    {usage}

    Parameters
    ----------
    {common_parameters}
    method : str, default="pearson"
        Correlation method. One of ``"pearson"``,
        ``"spearman"``, or ``"kendall"``.
    alternative : str, default="two-sided"
        Alternative hypothesis. One of ``"two-sided"``,
        ``"greater"``, or ``"less"``.
    label_x_npc : float or str, default="left"
        Normalized x position for the label. Float in
        [0, 1] or one of ``"left"``, ``"center"``,
        ``"right"``.
    label_y_npc : float or str, default="top"
        Normalized y position for the label. Float in
        [0, 1] or one of ``"top"``, ``"center"``,
        ``"bottom"``.
    r_accuracy : float, default=0.01
        Decimal accuracy for the correlation coefficient.
    p_accuracy : float, default=0.001
        Decimal accuracy for the p-value.
    label_sep : str, default=", "
        Separator between the correlation and p-value
        labels.

    See Also
    --------
    plotnine.geom_text : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "label"    # Formatted correlation label
    "r"        # Correlation coefficient
    "rr"       # R-squared
    "p"        # P-value
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_AES = {"label": after_stat("label")}
    DEFAULT_PARAMS = {
        "geom": "text",
        "position": "identity",
        "na_rm": False,
        "method": "pearson",
        "alternative": "two-sided",
        "label_x_npc": "left",
        "label_y_npc": "top",
        "r_accuracy": 0.01,
        "p_accuracy": 0.001,
        "label_sep": ", ",
    }
    CREATES = {"label", "r", "rr", "p"}

    def compute_group(self, data, scales):
        x = data["x"].to_numpy(dtype=float)
        y = data["y"].to_numpy(dtype=float)
        method = self.params["method"]
        alternative = self.params["alternative"]

        if len(x) < 3:
            return pd.DataFrame()

        # Compute correlation
        if method == "pearson":
            result = sp_stats.pearsonr(
                x, y, alternative=alternative
            )
            coef_name = "R"
        elif method == "spearman":
            result = sp_stats.spearmanr(
                x, y, alternative=alternative
            )
            coef_name = "ρ"
        elif method == "kendall":
            result = sp_stats.kendalltau(
                x, y, alternative=alternative
            )
            coef_name = "τ"
        else:
            raise ValueError(
                f"method must be 'pearson', 'spearman', "
                f"or 'kendall', got '{method}'"
            )

        r = result.statistic
        p = result.pvalue
        rr = r**2

        # Format label
        r_accuracy = self.params["r_accuracy"]
        p_accuracy = self.params["p_accuracy"]
        label_sep = self.params["label_sep"]

        r_digits = _accuracy_to_digits(r_accuracy)
        r_str = f"{coef_name} = {r:.{r_digits}f}"
        p_str = _format_p(p, p_accuracy)
        label = f"{r_str}{label_sep}{p_str}"

        # Position the label
        x_pos = _npc_to_data(
            self.params["label_x_npc"], x.min(), x.max()
        )
        y_pos = _npc_to_data(
            self.params["label_y_npc"], y.min(), y.max()
        )

        return pd.DataFrame(
            {
                "x": [x_pos],
                "y": [y_pos],
                "label": [label],
                "r": [r],
                "rr": [rr],
                "p": [p],
            }
        )


def _accuracy_to_digits(accuracy):
    """Convert accuracy (e.g. 0.01) to number of digits (e.g. 2)."""
    if accuracy >= 1:
        return 0
    return max(0, int(np.ceil(-np.log10(accuracy))))


def _format_p(p, accuracy):
    """Format a p-value with the given accuracy."""
    if p < accuracy:
        digits = _accuracy_to_digits(accuracy)
        return f"p < {accuracy:.{digits}f}"
    digits = _accuracy_to_digits(accuracy)
    return f"p = {p:.{digits}f}"


def _npc_to_data(npc, data_min, data_max):
    """Convert normalized plot coordinates to data coordinates."""
    npc_map = {
        "left": 0.05,
        "center": 0.5,
        "middle": 0.5,
        "right": 0.95,
        "top": 0.95,
        "bottom": 0.05,
    }
    if isinstance(npc, str):
        npc = npc_map.get(npc, 0.5)

    data_range = data_max - data_min
    return data_min + npc * data_range
