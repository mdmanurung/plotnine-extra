"""
Per-panel position scales for facetted plots.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Sequence


class FacettedPosScales:
    """
    Container for per-panel position scales.

    Holds lists of x and/or y scales that are applied
    individually to each facet panel column (x) or row (y).

    Parameters
    ----------
    x : list of scales, optional
        Position scales for the x-axis, one per panel column.
    y : list of scales, optional
        Position scales for the y-axis, one per panel row.
    """

    def __init__(
        self,
        x: Optional[Sequence] = None,
        y: Optional[Sequence] = None,
    ):
        self.x: list = list(x) if x is not None else []
        self.y: list = list(y) if y is not None else []

    # TODO: Integrate with facet layout so that each panel
    # trains and applies its own position scale from these
    # lists.


def facetted_pos_scales(
    x: Optional[Sequence] = None,
    y: Optional[Sequence] = None,
) -> FacettedPosScales:
    """
    Set individual position scales for facet panels.

    Parameters
    ----------
    x : list of scales, optional
        Position scales for the x-axis, one per panel
        column.
    y : list of scales, optional
        Position scales for the y-axis, one per panel
        row.

    Returns
    -------
    FacettedPosScales
        Object that can be added to a ggplot to apply
        per-panel position scales.
    """
    return FacettedPosScales(x=x, y=y)
