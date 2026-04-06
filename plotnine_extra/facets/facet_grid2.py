"""
Extended grid facets with independent scales and inner axes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from plotnine.facets.facet_grid import facet_grid

if TYPE_CHECKING:
    from typing import Optional, Sequence

    from plotnine.typing import FacetSpaceRatios


class facet_grid2(facet_grid):
    """
    Extended grid facets with independent scales.

    Extends :class:`plotnine.facet_grid` with support for truly
    independent position scales, configurable inner axes, and
    selective label removal.

    Parameters
    ----------
    rows : str or list of str, optional
        Variables to facet by in rows.
    cols : str or list of str, optional
        Variables to facet by in columns.
    margins : bool or list of str
        Whether to display marginal facets.
    scales : str
        Whether scales are fixed ("fixed"), free ("free",
        "free_x", "free_y").
    space : str or dict
        Panel spacing: "fixed", "free", "free_x", "free_y"
        or a dict of ratios.
    shrink : bool
        Whether to shrink scales to fit output of statistics.
    labeller : str
        Labelling function for strip text.
    as_table : bool
        If True, facets are laid out like a table with the
        highest values at the bottom-right.
    drop : bool
        Whether to drop unused factor levels.
    independent : str
        Which axes have truly independent scales per panel.
        One of "none", "x", "y", or "all".
    axes : str
        Which inner axes to draw. One of "all", "x", "y",
        or "margins".
    remove_labels : str
        Which inner axis labels to remove. One of "none",
        "x", "y", or "all".
    """

    def __init__(
        self,
        rows: Optional[str | Sequence[str]] = None,
        cols: Optional[str | Sequence[str]] = None,
        *,
        margins: bool | Sequence[str] = False,
        scales: Literal[
            "fixed", "free", "free_x", "free_y"
        ] = "fixed",
        space: (
            Literal["fixed", "free", "free_x", "free_y"]
            | FacetSpaceRatios
        ) = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
        independent: Literal[
            "none", "x", "y", "all"
        ] = "none",
        axes: Literal[
            "all", "x", "y", "margins"
        ] = "margins",
        remove_labels: Literal[
            "none", "x", "y", "all"
        ] = "none",
    ):
        super().__init__(
            rows=rows,
            cols=cols,
            margins=margins,
            scales=scales,
            space=space,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
        )
        self.independent = independent
        self.axes = axes
        self.remove_labels = remove_labels
        # TODO: Override train_position_scales and strip/axis
        # rendering to implement truly independent scales and
        # inner axis control.
