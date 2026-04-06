from plotnine.doctools import document

from ._base_stat_test import _base_stat_test


@document
class stat_kruskal_test(_base_stat_test):
    """
    Add Kruskal-Wallis test p-values to a plot

    Performs a Kruskal-Wallis rank sum test and displays
    the result as a text annotation. This is a non-parametric
    alternative to one-way ANOVA.

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
    "label"      # Formatted test result label
    "p"          # P-value
    "p_signif"   # Significance symbol
    "statistic"  # Test statistic (H)
    "df"         # Degrees of freedom
    "method"     # Name of the test
    ```

    """
    DEFAULT_PARAMS = {
        "geom": "text",
        "position": "identity",
        "na_rm": False,
        "label_x_npc": "center",
        "label_y_npc": "top",
        "p_digits": 3,
    }
    CREATES = {"label", "p", "p_signif", "statistic", "df", "method"}

    _test_method = "kruskal.test"
    _min_groups = 2
