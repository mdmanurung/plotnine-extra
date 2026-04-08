"""
Extra scale helpers ported from ggh4x.
"""

from .scale_manual import scale_x_manual, scale_y_manual
from .scale_multi import (
    scale_color_multi,
    scale_colour_multi,
    scale_fill_multi,
    scale_listed,
)

__all__ = (
    "scale_color_multi",
    "scale_colour_multi",
    "scale_fill_multi",
    "scale_listed",
    "scale_x_manual",
    "scale_y_manual",
)
