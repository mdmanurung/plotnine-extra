"""
plotnine_extra: Extension package for plotnine
==============================================

This package extends plotnine with additional geoms, stats,
plot composition, and animation support.

Usage
-----
    from plotnine_extra import *

This imports all of plotnine's public API plus the extra
components provided by this package.

Extra Components
----------------
Geoms:
    - geom_pointdensity: Scatterplot with density estimation
    - geom_spoke: Line segments parameterised by angle/radius
    - annotation_stripes: Alternating background stripes

Stats:
    - stat_pointdensity: Density estimation at each point

Composition:
    - Compose, Beside, Stack, Wrap: Plot composition operators
    - plot_layout: Customise composition layout
    - plot_annotation: Annotate compositions
    - plot_spacer: Blank space in compositions

Animation:
    - PlotnineAnimation: Create animations from ggplot objects
"""

from plotnine import *  # noqa: F401, F403
from plotnine import __version__ as _plotnine_version

from .animation import PlotnineAnimation
from .composition import (
    Beside,
    Compose,
    Stack,
    Wrap,
    plot_annotation,
    plot_layout,
    plot_spacer,
)
from .geoms import annotation_stripes, geom_pointdensity, geom_spoke
from .stats import stat_pointdensity

__version__ = "0.1.0"

# Extend plotnine's __all__ with our extras
_extra_all = (
    # Geoms
    "annotation_stripes",
    "geom_pointdensity",
    "geom_spoke",
    # Stats
    "stat_pointdensity",
    # Composition
    "Compose",
    "Beside",
    "Stack",
    "Wrap",
    "plot_annotation",
    "plot_layout",
    "plot_spacer",
    # Animation
    "PlotnineAnimation",
)

__all__ = (  # noqa: F405
    *_extra_all,
)
