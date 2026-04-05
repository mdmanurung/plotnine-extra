"""
Stepped colorbar guide - shows discrete color steps instead of
a smooth gradient.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .guide_colorbar import guide_colorbar


@dataclass
class guide_colorsteps(guide_colorbar):
    """
    Colorbar guide that shows discrete steps

    Like [](`~plotnine.guides.guide_colorbar`) but shows
    distinct color blocks instead of a continuous gradient.

    Parameters
    ----------
    nbin : int
        Number of color bins.
    show_limits : bool
        Whether to show limits at the ends of the guide.
    """

    nbin: int = 5
    """Number of color steps."""

    show_limits: bool = False
    """Whether to show the limits."""

    # Non-Parameter Attributes
    available_aes: set[str] = field(
        init=False, default_factory=lambda: {"colour", "color", "fill"}
    )

    def __post_init__(self):
        # Override the display type to rectangles
        self.display = "rectangles"
        super().__post_init__()


@dataclass
class guide_coloursteps(guide_colorsteps):
    """
    Alias for guide_colorsteps (British spelling)
    """
