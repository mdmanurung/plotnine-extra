"""
Custom guide that accepts user-provided content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from plotnine.guides.guide import guide

if TYPE_CHECKING:
    from typing import Optional

    from matplotlib.artist import Artist
    from matplotlib.offsetbox import PackerBase

    from plotnine.iapi import guide_text
    from plotnine.layer import Layers
    from plotnine.scales.scale import scale

    from plotnine.guides.guides import GuidesElements


@dataclass
class guide_custom(guide):
    """
    Custom guide with user-provided content

    Allows users to create a legend entry with custom matplotlib
    artists.

    Parameters
    ----------
    grob : matplotlib.artist.Artist
        A matplotlib artist to use as the legend key.
    """

    grob: Optional[Artist] = None
    """Matplotlib artist for the legend key."""

    # Non-Parameter Attributes
    available_aes: set[str] = field(
        init=False, default_factory=lambda: {"any"}
    )

    def train(
        self,
        scale: scale,
        aesthetic: Optional[str] = None,
    ):
        return self

    def draw(self) -> PackerBase:
        from matplotlib.offsetbox import (
            AuxTransformBox,
            DrawingArea,
        )
        from matplotlib.transforms import Bbox, BboxTransform

        if self.grob is not None:
            da = DrawingArea(20, 20)
            da.add_artist(self.grob)
            return da

        bbox = Bbox.from_bounds(0, 0, 0, 0)
        return AuxTransformBox(BboxTransform(bbox, bbox))

    def create_geoms(
        self,
        plot_layers: Layers,
        elements: GuidesElements,
        text: guide_text,
    ):
        pass
