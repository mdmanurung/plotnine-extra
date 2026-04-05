"""
Binned color and fill scales.
"""

from __future__ import annotations

from dataclasses import KW_ONLY, InitVar, dataclass
from typing import Literal, Sequence

from .._utils.registry import alias
from .scale_binned import scale_binned


@dataclass
class _scale_color_binned(scale_binned[Literal["legend", "colorbar"] | None]):
    """
    Base class for all binned color scales
    """

    _aesthetics = ["color"]
    _: KW_ONLY
    guide: Literal["legend", "colorbar"] | None = "legend"
    na_value: str = "#7F7F7F"


@dataclass
class scale_color_binned(_scale_color_binned):
    """
    Binned continuous color scale

    Maps continuous data to discrete color bins using the
    default colormap (viridis).

    See Also
    --------
    plotnine.scale_color_cmap : Continuous color scale.
    """

    cmap_name: InitVar[str] = "viridis"
    """
    Matplotlib colormap name.
    """

    def __post_init__(self, cmap_name):
        from mizani.palettes import cmap_pal

        super().__post_init__()
        self.palette = cmap_pal(cmap_name)


@dataclass
class scale_fill_binned(scale_color_binned):
    """
    Binned continuous fill scale
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_steps(_scale_color_binned):
    """
    Binned gradient color scale

    See Also
    --------
    plotnine.scale_color_gradient : Continuous gradient scale.
    """

    low: InitVar[str] = "#132B43"
    """Low color."""

    high: InitVar[str] = "#56B1F7"
    """High color."""

    def __post_init__(self, low, high):
        from mizani.palettes import gradient_n_pal

        super().__post_init__()
        self.palette = gradient_n_pal([low, high])


@dataclass
class scale_fill_steps(scale_color_steps):
    """
    Binned gradient fill scale
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_steps2(_scale_color_binned):
    """
    Binned diverging color scale

    See Also
    --------
    plotnine.scale_color_gradient2 : Continuous diverging gradient.
    """

    low: InitVar[str] = "#832424"
    """Low color."""

    mid: InitVar[str] = "#FFFFFF"
    """Mid-point color."""

    high: InitVar[str] = "#3A3A98"
    """High color."""

    def __post_init__(self, low, mid, high):
        from mizani.palettes import gradient_n_pal

        super().__post_init__()
        self.palette = gradient_n_pal([low, mid, high])


@dataclass
class scale_fill_steps2(scale_color_steps2):
    """
    Binned diverging fill scale
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_stepsn(_scale_color_binned):
    """
    Binned n-color gradient scale

    See Also
    --------
    plotnine.scale_color_gradientn : Continuous n-color gradient.
    """

    colors: InitVar[Sequence[str]] = ("#132B43", "#56B1F7")
    """List of colors."""

    def __post_init__(self, colors):
        from mizani.palettes import gradient_n_pal

        super().__post_init__()
        self.palette = gradient_n_pal(list(colors))


@dataclass
class scale_fill_stepsn(scale_color_stepsn):
    """
    Binned n-color gradient fill scale
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_fermenter(_scale_color_binned):
    """
    Binned sequential/diverging color scale from ColorBrewer

    See Also
    --------
    plotnine.scale_color_brewer : Discrete brewer scale.
    plotnine.scale_color_distiller : Continuous brewer scale.
    """

    type: InitVar[str] = "seq"
    """Type of brewer palette: 'seq', 'div', or 'qual'."""

    palette: InitVar[int | str] = 1
    """Brewer palette name or index."""

    direction: InitVar[int] = 1
    """Order of colors: 1 or -1."""

    def __post_init__(self, type, palette, direction):
        from mizani.palettes import brewer_pal, gradient_n_pal

        super().__post_init__()
        colors = brewer_pal(type, palette, direction=direction)(7)
        self.palette = gradient_n_pal(colors)


@dataclass
class scale_fill_fermenter(scale_color_fermenter):
    """
    Binned sequential/diverging fill scale from ColorBrewer
    """

    _aesthetics = ["fill"]


# British spelling aliases
@alias
class scale_colour_binned(scale_color_binned):
    pass


@alias
class scale_colour_steps(scale_color_steps):
    pass


@alias
class scale_colour_steps2(scale_color_steps2):
    pass


@alias
class scale_colour_stepsn(scale_color_stepsn):
    pass


@alias
class scale_colour_fermenter(scale_color_fermenter):
    pass
