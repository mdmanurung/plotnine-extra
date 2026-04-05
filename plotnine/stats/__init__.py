"""
Statistics
"""

from .stat_align import stat_align
from .stat_bin import stat_bin
from .stat_bin_2d import stat_bin2d, stat_bin_2d
from .stat_bin_hex import stat_bin_hex, stat_binhex
from .stat_bindot import stat_bindot
from .stat_boxplot import stat_boxplot
from .stat_connect import stat_connect
from .stat_contour import stat_contour
from .stat_contour_filled import stat_contour_filled
from .stat_count import stat_count
from .stat_density import stat_density
from .stat_density_2d import stat_density_2d
from .stat_density_2d_filled import stat_density_2d_filled
from .stat_ecdf import stat_ecdf
from .stat_ellipse import stat_ellipse
from .stat_function import stat_function
from .stat_hull import stat_hull
from .stat_identity import stat_identity
from .stat_manual import stat_manual
from .stat_pointdensity import stat_pointdensity
from .stat_qq import stat_qq
from .stat_qq_line import stat_qq_line
from .stat_quantile import stat_quantile
from .stat_sf import stat_sf
from .stat_sf_coordinates import stat_sf_coordinates
from .stat_sina import stat_sina
from .stat_smooth import stat_smooth
from .stat_spoke import stat_spoke
from .stat_sum import stat_sum
from .stat_summary import stat_summary
from .stat_summary_2d import stat_summary_2d
from .stat_summary_bin import stat_summary_bin
from .stat_summary_hex import stat_summary_hex
from .stat_unique import stat_unique
from .stat_ydensity import stat_ydensity

__all__ = (
    "stat_contour",
    "stat_contour_filled",
    "stat_align",
    "stat_connect",
    "stat_count",
    "stat_bin",
    "stat_bin_2d",
    "stat_bin2d",
    "stat_bin_hex",
    "stat_binhex",
    "stat_bindot",
    "stat_boxplot",
    "stat_density",
    "stat_ecdf",
    "stat_ellipse",
    "stat_density_2d",
    "stat_density_2d_filled",
    "stat_function",
    "stat_hull",
    "stat_identity",
    "stat_manual",
    "stat_pointdensity",
    "stat_qq",
    "stat_qq_line",
    "stat_quantile",
    "stat_sf",
    "stat_sf_coordinates",
    "stat_sina",
    "stat_spoke",
    "stat_smooth",
    "stat_sum",
    "stat_summary",
    "stat_summary_2d",
    "stat_summary_bin",
    "stat_summary_hex",
    "stat_unique",
    "stat_ydensity",
)
