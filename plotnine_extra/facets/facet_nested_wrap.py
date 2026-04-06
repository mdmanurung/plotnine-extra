"""
Wrapped facets with nested (merged) strip labels.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from plotnine.facets.facet_wrap import facet_wrap

if TYPE_CHECKING:
    from typing import Optional, Sequence


class facet_nested_wrap(facet_wrap):
    """
    Wrapped facets with nested strips.

    Extends :class:`plotnine.facet_wrap` so that hierarchical
    strip labels are merged when adjacent panels share the
    same parent category.

    Parameters
    ----------
    facets : str or list of str, optional
        Variables to facet by.
    nrow : int, optional
        Number of rows.
    ncol : int, optional
        Number of columns.
    scales : str
        Whether scales are fixed or free.
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
    nest_line : bool
        If True, draw a nesting indicator line between
        parent and child strip levels.
    solo_line : bool
        If True, draw a line even when a parent category
        has only one child.
    resect : float
        Amount (in [0, 1]) to shorten the nesting line
        at each end.
    bleed : bool
        If True, allow nesting indicators to extend into
        neighbouring strips.
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
        nest_line: bool = False,
        solo_line: bool = False,
        resect: float = 0,
        bleed: bool = False,
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
        self.nest_line = nest_line
        self.solo_line = solo_line
        self.resect = resect
        self.bleed = bleed
        # TODO: Override strip rendering to merge adjacent
        # strips sharing the same parent category and draw
        # nesting indicator lines.
