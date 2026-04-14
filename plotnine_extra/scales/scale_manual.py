"""
Manual position scales.

``scale_x_manual`` and ``scale_y_manual`` are thin wrappers
around plotnine's discrete position scales that let users pass
a complete set of breaks, labels and palette values in one
call. Port of ``ggh4x::scale_x_manual`` / ``scale_y_manual``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine.scales.scale_xy import (
    scale_x_discrete,
    scale_y_discrete,
)

if TYPE_CHECKING:
    from typing import Sequence


__all__ = ("scale_x_manual", "scale_y_manual")


def scale_x_manual(
    values: "Sequence",
    breaks: "Sequence | None" = None,
    labels: "Sequence | None" = None,
    name: str | None = None,
    **kwargs,
):
    """
    Discrete x-axis scale with explicit ``values`` ordering.

    Parameters
    ----------
    values : sequence
        Ordered list of category values that should appear on
        the axis. Acts as both ``limits`` and the axis order.
    breaks : sequence, optional
        Subset of ``values`` to label.
    labels : sequence, optional
        Display labels matching ``breaks``.
    name : str, optional
        Axis title.
    """
    if breaks is None:
        breaks = list(values)
    if labels is None:
        labels = list(values)
    return scale_x_discrete(
        limits=list(values),
        breaks=list(breaks),
        labels=list(labels),
        name=name,
        **kwargs,
    )


def scale_y_manual(
    values: "Sequence",
    breaks: "Sequence | None" = None,
    labels: "Sequence | None" = None,
    name: str | None = None,
    **kwargs,
):
    """
    Discrete y-axis scale with explicit ``values`` ordering.
    See :func:`scale_x_manual` for parameter descriptions.
    """
    if breaks is None:
        breaks = list(values)
    if labels is None:
        labels = list(values)
    return scale_y_discrete(
        limits=list(values),
        breaks=list(breaks),
        labels=list(labels),
        name=name,
        **kwargs,
    )
