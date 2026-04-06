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
    - geom_bracket: Significance brackets with labels
    - annotation_stripes: Alternating background stripes

Stats:
    - stat_pointdensity: Density estimation at each point
    - stat_mean: Group mean points (centroids)
    - stat_chull: Convex hull of point groups
    - stat_stars: Star segments from centroid to data points
    - stat_central_tendency: Mean/median/mode lines
    - stat_conf_ellipse: Confidence ellipses
    - stat_cor: Correlation coefficients with p-values
    - stat_regline_equation: Regression equations with R²
    - stat_overlay_normal_density: Normal density overlays
    - stat_compare_means: Group comparison p-values
    - stat_anova_test: ANOVA test annotations
    - stat_kruskal_test: Kruskal-Wallis test annotations
    - stat_welch_anova_test: Welch ANOVA annotations
    - stat_friedman_test: Friedman test annotations
    - stat_pvalue_manual: Manual p-value placement
    - stat_pwc: Pairwise comparison p-values with brackets

Composition:
    - Compose, Beside, Stack, Wrap: Plot composition operators
    - plot_layout: Customise composition layout
    - plot_annotation: Annotate compositions
    - plot_spacer: Blank space in compositions

Animation:
    - PlotnineAnimation: Create animations from ggplot objects

Datasets (via ``plotnine_extra.data``):
    - ToothGrowth: Tooth growth in guinea pigs (ggpubr example data)
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
from .geoms import (
    annotation_stripes,
    geom_bracket,
    geom_pointdensity,
    geom_spoke,
)
from .stats import (
    stat_anova_test,
    stat_central_tendency,
    stat_chull,
    stat_compare_means,
    stat_conf_ellipse,
    stat_cor,
    stat_friedman_test,
    stat_kruskal_test,
    stat_mean,
    stat_overlay_normal_density,
    stat_pointdensity,
    stat_pvalue_manual,
    stat_pwc,
    stat_regline_equation,
    stat_stars,
    stat_welch_anova_test,
)

__version__ = "0.1.0"

# Extend plotnine's __all__ with our extras
_extra_all = (
    # Geoms
    "annotation_stripes",
    "geom_bracket",
    "geom_pointdensity",
    "geom_spoke",
    # Stats
    "stat_anova_test",
    "stat_central_tendency",
    "stat_chull",
    "stat_compare_means",
    "stat_conf_ellipse",
    "stat_cor",
    "stat_friedman_test",
    "stat_kruskal_test",
    "stat_mean",
    "stat_overlay_normal_density",
    "stat_pointdensity",
    "stat_pvalue_manual",
    "stat_pwc",
    "stat_regline_equation",
    "stat_stars",
    "stat_welch_anova_test",
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
