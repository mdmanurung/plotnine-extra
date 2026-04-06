"""
Grid facets with nested (merged) strip labels.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from plotnine.facets.facet_grid import facet_grid

if TYPE_CHECKING:
    from typing import Optional, Sequence

    from plotnine.typing import FacetSpaceRatios


class facet_nested(facet_grid):
    """
    Grid facets with nested strips.

    Extends :class:`plotnine.facet_grid` so that hierarchical
    strip labels are merged when adjacent panels share the
    same parent category.

    Parameters
    ----------
    rows : str or list of str, optional
        Variables to facet by in rows.
    cols : str or list of str, optional
        Variables to facet by in columns.
    margins : bool or list of str
        Whether to display marginal facets.
    scales : str
        Whether scales are fixed or free.
    space : str or dict
        Panel spacing mode.
    shrink : bool
        Whether to shrink scales to fit output of statistics.
    labeller : str
        Labelling function for strip text.
    as_table : bool
        If True, facets are laid out like a table.
    drop : bool
        Whether to drop unused factor levels.
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
        nest_line: bool = False,
        solo_line: bool = False,
        resect: float = 0,
        bleed: bool = False,
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
        self.nest_line = nest_line
        self.solo_line = solo_line
        self.resect = resect
        self.bleed = bleed
        # TODO: Override strip rendering to merge adjacent
        # strips sharing the same parent category and draw
        # nesting indicator lines.
