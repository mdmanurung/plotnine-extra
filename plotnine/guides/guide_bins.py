"""
Binned legend guide - shows binned value ranges.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .guide_legend import guide_legend


@dataclass
class guide_bins(guide_legend):
    """
    A binned version of the legend guide

    Used for binned scales, it displays keys as rectangles
    between bin boundaries rather than individual symbols.

    Parameters
    ----------
    show_limits : bool
        Whether to show the limits of the bins at the
        boundaries.
    """

    show_limits: bool = False
    """Whether to show the min/max limits."""

    # Non-Parameter Attributes
    available_aes: set[str] = field(
        init=False, default_factory=lambda: {"any"}
    )
