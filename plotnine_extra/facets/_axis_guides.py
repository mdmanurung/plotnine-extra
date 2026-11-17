"""
Facet-side hook for plotnine-extra axis guides.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..guides import install_axis_guide_hook

if TYPE_CHECKING:
    from plotnine.ggplot import ggplot


class AxisGuideFacet:
    """
    Mixin that gives a facet plotnine-extra axis-guide rendering.

    plotnine 0.16 moved per-panel axes setup out of the facet and into
    ``coord.setup_ax``. The axis-guide specs (``guide_axis_manual`` and
    friends) still need a per-panel hook, so this installs one on the plot's
    coordinate system the first time the facet is set up for a draw.

    Mix in *before* the plotnine facet class::

        class facet_wrap2(AxisGuideFacet, facet_wrap):
            ...
    """

    def setup(self, plot: ggplot):
        # Runs once per draw, after every `+` has been applied, so
        # plot.coordinates is final and its `_owner` is already bound.
        result = super().setup(plot)  # type: ignore[misc]
        install_axis_guide_hook(plot)
        return result
