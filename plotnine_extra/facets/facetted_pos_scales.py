"""
Per-panel position scales for facetted plots.

This module provides :func:`facetted_pos_scales`, which allows
applying distinct position scales (x and/or y) to individual
facet panels.  When added to a :class:`~plotnine.ggplot` object
via the ``+`` operator, the per-panel scales replace the cloned
defaults that plotnine creates during ``init_scales``.

.. note::

   The facet used in the plot must produce a layout where each
   panel has a unique ``SCALE_X`` / ``SCALE_Y`` value (i.e.
   ``scales="free"`` or ``scales="free_x"``/``"free_y"``, or
   the panel must be produced by :class:`facet_grid2` with
   ``independent="x"``/``"y"``/``"all"``).  When scales are
   shared (``SCALE_X == 1`` for all panels) there is only a
   single scale object and per-panel overrides have no effect.
"""

from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Sequence

    from plotnine import ggplot


class FacettedPosScales:
    """
    Container for per-panel position scales.

    Holds lists of x and/or y scales that are applied
    individually to each facet panel column (x) or row (y).

    When added to a ggplot (via ``+``), it stores itself on the
    plot object so that :class:`facet_grid2` or
    :class:`facet_wrap2` can pick it up during scale
    initialisation.

    Parameters
    ----------
    x : list of scales, optional
        Position scales for the x-axis, one per panel or per
        unique ``SCALE_X`` group.  ``None`` entries are
        skipped (the default scale is kept for that panel).
    y : list of scales, optional
        Position scales for the y-axis, one per panel or per
        unique ``SCALE_Y`` group.  ``None`` entries are
        skipped.
    """

    def __init__(
        self,
        x: Optional[Sequence] = None,
        y: Optional[Sequence] = None,
    ):
        self.x: list = list(x) if x is not None else []
        self.y: list = list(y) if y is not None else []

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Allow ``ggplot() + facetted_pos_scales(...)``.

        Attaches this object to the plot so that compatible
        facets can consume it during scale initialisation.
        """
        other._facetted_pos_scales = self  # type: ignore[attr-defined]
        return other

    def apply(self, scales_ns: object) -> None:
        """
        Replace scale objects in *scales_ns* with those stored here.

        Parameters
        ----------
        scales_ns : SimpleNamespace
            The namespace returned by ``facet.init_scales()``.
            It has ``.x`` and ``.y`` attributes, each a
            :class:`~plotnine.scales.scales.Scales` list.
        """
        if self.x and hasattr(scales_ns, "x"):
            panel_scales_x = scales_ns.x  # type: ignore[union-attr]
            for i, sc in enumerate(self.x):
                if sc is not None and i < len(panel_scales_x):
                    cloned = sc.clone() if hasattr(sc, "clone") else copy(sc)
                    panel_scales_x[i] = cloned

        if self.y and hasattr(scales_ns, "y"):
            panel_scales_y = scales_ns.y  # type: ignore[union-attr]
            for i, sc in enumerate(self.y):
                if sc is not None and i < len(panel_scales_y):
                    cloned = sc.clone() if hasattr(sc, "clone") else copy(sc)
                    panel_scales_y[i] = cloned


def facetted_pos_scales(
    x: Optional[Sequence] = None,
    y: Optional[Sequence] = None,
) -> FacettedPosScales:
    """
    Set individual position scales for facet panels.

    Returns an object that, when added to a
    :class:`~plotnine.ggplot`, attaches per-panel position
    scales.  Compatible facets (e.g. :class:`facet_grid2`,
    :class:`facet_wrap2`) will pick up these scales and apply
    them during plotting.

    Parameters
    ----------
    x : list of scales, optional
        Position scales for the x-axis, one per panel
        column (or per unique ``SCALE_X`` group).
    y : list of scales, optional
        Position scales for the y-axis, one per panel
        row (or per unique ``SCALE_Y`` group).

    Returns
    -------
    FacettedPosScales
        Object that can be added to a ggplot to apply
        per-panel position scales.

    Examples
    --------
    .. code-block:: python

        from plotnine import *
        from plotnine_extra.facets import (
            facet_wrap2,
            facetted_pos_scales,
        )

        (
            ggplot(df, aes("x", "y"))
            + geom_point()
            + facet_wrap2("group", scales="free_x")
            + facetted_pos_scales(
                x=[
                    scale_x_continuous(limits=(0, 10)),
                    scale_x_continuous(limits=(0, 50)),
                ]
            )
        )
    """
    return FacettedPosScales(x=x, y=y)
