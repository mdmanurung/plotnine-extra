"""
Viridis convenience scales.
"""

from __future__ import annotations

from dataclasses import InitVar, dataclass

from plotnine._utils.registry import alias
from plotnine.scales.scale_color import (
    scale_color_cmap,
    scale_color_cmap_d,
)


# Viridis convenience scales (continuous)
@dataclass
class scale_color_viridis_c(scale_color_cmap):
    """
    Viridis continuous color scale

    See Also
    --------
    plotnine.scale_color_cmap : The parent class.
    """

    cmap_name: InitVar[str] = "viridis"


@dataclass
class scale_fill_viridis_c(scale_color_viridis_c):
    """
    Viridis continuous fill scale
    """

    _aesthetics = ["fill"]


# Viridis convenience scales (discrete)
@dataclass
class scale_color_viridis_d(scale_color_cmap_d):
    """
    Viridis discrete color scale

    See Also
    --------
    plotnine.scale_color_cmap_d : The parent class.
    """

    cmap_name: InitVar[str] = "viridis"


@dataclass
class scale_fill_viridis_d(scale_color_viridis_d):
    """
    Viridis discrete fill scale
    """

    _aesthetics = ["fill"]


# British spelling aliases for viridis
@alias
class scale_colour_viridis_c(scale_color_viridis_c):
    pass


@alias
class scale_colour_viridis_d(scale_color_viridis_d):
    pass
