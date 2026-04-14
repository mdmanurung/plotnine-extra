"""
``geom_pwc`` — geom counterpart of :class:`stat_pwc`.

In ggpubr, ``geom_pwc`` and ``stat_pwc`` are interchangeable;
both attach pairwise comparison brackets to a plot. The geom
form simply binds the default ``stat`` to ``pwc`` and accepts
the same parameters.
"""

from __future__ import annotations

from plotnine.doctools import document
from plotnine.geoms.geom import geom
from plotnine.geoms.geom_path import geom_path


@document
class geom_pwc(geom):
    """
    Pairwise comparison brackets (geom form of ``stat_pwc``).

    {usage}

    Parameters
    ----------
    {common_parameters}

    Notes
    -----
    All statistical-test parameters live on
    :class:`plotnine_extra.stats.stat_pwc`. This class only
    sets the default ``stat`` so that calling
    ``geom_pwc(...)`` is equivalent to writing
    ``stat_pwc(geom='bracket', ...)``.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_AES = {
        "color": "black",
        "alpha": 1,
    }
    DEFAULT_PARAMS = {
        "stat": "pwc",
        "position": "identity",
        "na_rm": False,
        "tip_length": 0.02,
        "bracket_nudge_y": 0,
        "label_size": 8,
        "vjust": 0,
    }
    draw_legend = staticmethod(geom_path.draw_legend)
