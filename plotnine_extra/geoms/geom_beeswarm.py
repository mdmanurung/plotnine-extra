"""
``geom_beeswarm`` – categorical scatter using the beeswarm algorithm,
ported from R's ``ggbeeswarm::geom_beeswarm``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine.doctools import document
from plotnine.geoms.geom_point import geom_point

from ..positions.position_beeswarm import position_beeswarm

if TYPE_CHECKING:
    from typing import Any, Optional


@document
class geom_beeswarm(geom_point):
    """
    Points jittered to avoid overplotting using the beeswarm algorithm

    Points are arranged so that they do not overlap, producing
    a layout that resembles a beeswarm.  The shape gives a good
    indication of the data distribution while showing every
    individual observation.

    {usage}

    Parameters
    ----------
    {common_parameters}
    method : str
        Algorithm for arranging points: ``"swarm"`` (default),
        ``"compactswarm"``, ``"center"`` / ``"centre"``,
        ``"hex"``, or ``"square"``.
    cex : float
        Scaling factor for point spacing (1–3 recommended).
    side : int
        ``0`` both sides (default), ``1`` right/up only,
        ``-1`` left/down only.
    priority : str
        Placement order: ``"ascending"`` (default),
        ``"descending"``, ``"density"``, ``"random"``,
        ``"none"``.
    dodge_width : float | None
        Amount by which to dodge overlapping groups.
    corral : str
        Handle runaway points: ``"none"`` (default),
        ``"gutter"``, ``"wrap"``, ``"random"``, ``"omit"``.
    corral_width : float
        Width of the corral region.

    See Also
    --------
    plotnine_extra.positions.position_beeswarm
    plotnine_extra.geoms.geom_quasirandom.geom_quasirandom
    """

    DEFAULT_PARAMS = {
        "stat": "identity",
        "position": "identity",
        "na_rm": False,
    }

    # Position parameter names and their defaults
    _position_params = {
        "method": "swarm",
        "cex": 1.0,
        "side": 0,
        "priority": "ascending",
        "dodge_width": None,
        "corral": "none",
        "corral_width": 0.9,
    }

    def __init__(
        self,
        mapping: Optional[Any] = None,
        data: Optional[Any] = None,
        **kwargs: Any,
    ):
        # Extract position parameters from kwargs
        pos_kwargs = {}
        for key, default in self._position_params.items():
            pos_kwargs[key] = kwargs.pop(key, default)

        kwargs["position"] = position_beeswarm(**pos_kwargs)
        super().__init__(mapping=mapping, data=data, **kwargs)
