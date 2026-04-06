"""
plotnine_extra — Extra geoms, stats, scales, and more for plotnine.

A Grammar of Graphics extension package that provides additional
components not yet available in the upstream plotnine.

Usage
-----
Import everything from plotnine plus all extras::

    from plotnine_extra import *

Or import selectively::

    from plotnine import *  # standard plotnine
    from plotnine_extra.geoms import geom_hex  # just one extra
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("plotnine-extra")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"
finally:
    del version
    del PackageNotFoundError

# Re-export everything from plotnine
from plotnine import *  # noqa: F401, F403

# Apply patches to plotnine internals that are required for
# our extra components to work (e.g., polar projection support)
from plotnine_extra._patches import apply_patches as _apply_patches

_apply_patches()
del _apply_patches

# Import and register all extra components
# (auto-registers via plotnine's Register metaclass)
# Combine __all__ from plotnine with our extras
import plotnine as _plotnine  # noqa: E402

from plotnine_extra.coords import (  # noqa: F401, E402
    coord_polar,
    coord_quickmap,
    coord_radial,
    coord_sf,
)
from plotnine_extra.geoms import (  # noqa: F401, E402
    geom_contour,
    geom_contour_filled,
    geom_curve,
    geom_density_2d_filled,
    geom_function,
    geom_hex,
    geom_sf,
    geom_sf_label,
    geom_sf_text,
)
from plotnine_extra.guides import (  # noqa: F401, E402
    guide_bins,
    guide_colorsteps,
    guide_coloursteps,
    guide_custom,
    guide_none,
)
from plotnine_extra.scales import (  # noqa: F401, E402
    dup_axis,
    scale_binned,
    scale_color_binned,
    scale_color_fermenter,
    scale_color_steps,
    scale_color_steps2,
    scale_color_stepsn,
    scale_color_viridis_c,
    scale_color_viridis_d,
    scale_colour_binned,
    scale_colour_fermenter,
    scale_colour_steps,
    scale_colour_steps2,
    scale_colour_stepsn,
    scale_colour_viridis_c,
    scale_colour_viridis_d,
    scale_fill_binned,
    scale_fill_fermenter,
    scale_fill_steps,
    scale_fill_steps2,
    scale_fill_stepsn,
    scale_fill_viridis_c,
    scale_fill_viridis_d,
    scale_linewidth,
    scale_linewidth_continuous,
    scale_linewidth_discrete,
    scale_linewidth_ordinal,
    sec_axis,
)
from plotnine_extra.stats import (  # noqa: F401, E402
    stat_align,
    stat_bin_hex,
    stat_binhex,
    stat_connect,
    stat_contour,
    stat_contour_filled,
    stat_density_2d_filled,
    stat_manual,
    stat_sf,
    stat_sf_coordinates,
    stat_spoke,
    stat_summary_2d,
    stat_summary_hex,
)

_extra_all = (
    # coords
    "coord_polar",
    "coord_quickmap",
    "coord_radial",
    "coord_sf",
    # geoms
    "geom_contour",
    "geom_contour_filled",
    "geom_curve",
    "geom_density_2d_filled",
    "geom_function",
    "geom_hex",
    "geom_sf",
    "geom_sf_label",
    "geom_sf_text",
    # guides
    "guide_bins",
    "guide_colorsteps",
    "guide_coloursteps",
    "guide_custom",
    "guide_none",
    # scales
    "dup_axis",
    "scale_binned",
    "scale_color_binned",
    "scale_colour_binned",
    "scale_color_steps",
    "scale_colour_steps",
    "scale_color_steps2",
    "scale_colour_steps2",
    "scale_color_stepsn",
    "scale_colour_stepsn",
    "scale_color_fermenter",
    "scale_colour_fermenter",
    "scale_color_viridis_c",
    "scale_color_viridis_d",
    "scale_colour_viridis_c",
    "scale_colour_viridis_d",
    "scale_fill_binned",
    "scale_fill_fermenter",
    "scale_fill_steps",
    "scale_fill_steps2",
    "scale_fill_stepsn",
    "scale_fill_viridis_c",
    "scale_fill_viridis_d",
    "scale_linewidth",
    "scale_linewidth_continuous",
    "scale_linewidth_discrete",
    "scale_linewidth_ordinal",
    "sec_axis",
    # stats
    "stat_align",
    "stat_bin_hex",
    "stat_binhex",
    "stat_connect",
    "stat_contour",
    "stat_contour_filled",
    "stat_density_2d_filled",
    "stat_manual",
    "stat_sf",
    "stat_sf_coordinates",
    "stat_spoke",
    "stat_summary_2d",
    "stat_summary_hex",
)

__all__ = tuple(set(getattr(_plotnine, "__all__", ())) | set(_extra_all))
del _plotnine
