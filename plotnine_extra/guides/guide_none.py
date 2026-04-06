from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from plotnine.guides.guide import guide

if TYPE_CHECKING:
    from typing import Optional

    from matplotlib.offsetbox import PackerBase

    from plotnine.iapi import guide_text
    from plotnine.layer import Layers
    from plotnine.scales.scale import scale

    from plotnine.guides.guides import GuidesElements


@dataclass
class guide_none(guide):
    """
    No guide

    This guide suppresses any legend / colorbar that would otherwise
    be drawn for the aesthetic.
    """

    # Non-Parameter Attributes
    available_aes: set[str] = field(
        init=False, default_factory=lambda: {"any"}
    )

    def train(
        self,
        scale: scale,
        aesthetic: Optional[str] = None,
    ):
        return None

    def draw(self) -> PackerBase:
        from matplotlib.offsetbox import AuxTransformBox
        from matplotlib.transforms import Bbox, BboxTransform

        # Return an empty drawing area
        bbox = Bbox.from_bounds(0, 0, 0, 0)
        return AuxTransformBox(BboxTransform(bbox, bbox))

    def create_geoms(
        self,
        plot_layers: Layers,
        elements: GuidesElements,
        text: guide_text,
    ):
        pass
