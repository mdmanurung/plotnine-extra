"""
Extra scales for plotnine.
"""

from .scale_binned import scale_binned
from .scale_color_binned import (
    scale_color_binned,
    scale_color_fermenter,
    scale_color_steps,
    scale_color_steps2,
    scale_color_stepsn,
    scale_colour_binned,
    scale_colour_fermenter,
    scale_colour_steps,
    scale_colour_steps2,
    scale_colour_stepsn,
    scale_fill_binned,
    scale_fill_fermenter,
    scale_fill_steps,
    scale_fill_steps2,
    scale_fill_stepsn,
)
from .scale_color_viridis import (
    scale_color_viridis_c,
    scale_color_viridis_d,
    scale_colour_viridis_c,
    scale_colour_viridis_d,
    scale_fill_viridis_c,
    scale_fill_viridis_d,
)
from .scale_linewidth import (
    scale_linewidth,
    scale_linewidth_continuous,
    scale_linewidth_discrete,
    scale_linewidth_ordinal,
)
from .sec_axis import dup_axis, sec_axis

__all__ = (
    # binned base
    "scale_binned",
    # binned color
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
    # binned fill
    "scale_fill_binned",
    "scale_fill_steps",
    "scale_fill_steps2",
    "scale_fill_stepsn",
    "scale_fill_fermenter",
    # viridis
    "scale_color_viridis_c",
    "scale_color_viridis_d",
    "scale_colour_viridis_c",
    "scale_colour_viridis_d",
    "scale_fill_viridis_c",
    "scale_fill_viridis_d",
    # linewidth
    "scale_linewidth",
    "scale_linewidth_continuous",
    "scale_linewidth_discrete",
    "scale_linewidth_ordinal",
    # secondary axis
    "sec_axis",
    "dup_axis",
)
