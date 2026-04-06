"""
Extended wrapped facets with inner axes and trimming.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from plotnine.facets.facet_wrap import facet_wrap

if TYPE_CHECKING:
    from typing import Optional, Sequence


class facet_wrap2(facet_wrap):
    """
    Extended wrapped facets.

    Extends :class:`plotnine.facet_wrap` with configurable inner
    axes, selective label removal, and blank-panel trimming.

    Parameters
    ----------
    facets : str or list of str, optional
        Variables to facet by.
    nrow : int, optional
        Number of rows.
    ncol : int, optional
        Number of columns.
    scales : str
        Whether scales are fixed ("fixed"), free ("free",
        "free_x", "free_y").
    shrink : bool
        Whether to shrink scales to fit output of statistics.
    labeller : str
        Labelling function for strip text.
    as_table : bool
        If True, facets are laid out like a table.
    drop : bool
        Whether to drop unused factor levels.
    dir : str
        Direction: "h" for horizontal, "v" for vertical.
    axes : str
        Which inner axes to draw. One of "all", "x", "y",
        or "margins".
    remove_labels : str
        Which inner axis labels to remove. One of "none",
        "x", "y", or "all".
    trim_blank : bool
        If True, trim blank panels from the layout.
    """

    def __init__(
        self,
        facets: Optional[str | Sequence[str]] = None,
        *,
        nrow: Optional[int] = None,
        ncol: Optional[int] = None,
        scales: Literal[
            "fixed", "free", "free_x", "free_y"
        ] = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
        dir: Literal["h", "v"] = "h",
        axes: Literal[
            "all", "x", "y", "margins"
        ] = "margins",
        remove_labels: Literal[
            "none", "x", "y", "all"
        ] = "none",
        trim_blank: bool = True,
    ):
        super().__init__(
            facets=facets,
            nrow=nrow,
            ncol=ncol,
            scales=scales,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
            dir=dir,
        )
        self.axes = axes
        self.remove_labels = remove_labels
        self.trim_blank = trim_blank
        # TODO: Override axis/label rendering to implement
        # inner axis control and blank-panel trimming.
