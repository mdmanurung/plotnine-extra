"""
Guide helpers ported from ggh4x.

.. note::

    Most of the ``guide_axis_*`` family from ggh4x is **not**
    implemented as a drop-in subclass in plotnine_extra. The
    plotnine 0.15/0.16 :class:`plotnine.guides.guide_axis`
    class is currently a near-empty placeholder; tick / label
    rendering is done directly in
    :meth:`plotnine.facets.facet.facet.set_breaks_and_labels`
    via matplotlib calls (``ax.set_xticks(...)``,
    ``ax.set_yticks(...)``).

    Because there is no plotnine extension point for axis
    guides, the ``guide_axis_*`` family from ggh4x has to be
    re-implemented either by:

    1. Subclassing :class:`plotnine_extra.facets.facet_grid2`
       (or :class:`facet_wrap2`) and overriding
       ``set_breaks_and_labels`` to mutate the matplotlib
       axes after the standard call, or
    2. Walking the figure axes after ``ggplot.draw()`` and
       re-styling the ticks directly with matplotlib.

    Both routes are sensitive to plotnine internals.

The helpers in this module provide the *function form* of the
ggh4x API so users' R-style code keeps working — they return a
small dataclass that downstream `facet_grid2` /
`facet_wrap2` subclasses know how to consume. The actual
rendering hooks land in a future release.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, Sequence


# Track which guide kinds have already warned so ``plot +
# guide_axis_nested()`` does not repeat itself.
_WARNED_KINDS: set[str] = set()


__all__ = (
    "GuideAxisSpec",
    "guide_axis_nested",
    "guide_axis_manual",
    "guide_axis_minor",
    "guide_axis_logticks",
    "guide_axis_truncated",
    "guide_axis_scalebar",
    "guide_axis_colour",
    "guide_axis_color",
    "guide_dendro",
    "guide_stringlegend",
)


@dataclass
class GuideAxisSpec:
    """
    A descriptor for an axis guide.

    Returned by every ``guide_axis_*`` factory in this module.
    Plotnine extras that know how to render axis guides
    (currently a future release) accept these specs.

    Attributes
    ----------
    kind : str
        Identifies which guide variant this is.
    options : dict
        Free-form keyword arguments captured from the call
        site.

    Notes
    -----
    Adding a spec to a ``ggplot`` with ``+`` is currently a
    **no-op** — the rendering hooks for axis guides are not
    yet implemented on top of plotnine 0.15/0.16. The first
    use of each guide kind in a session emits a
    :class:`UserWarning` so scripts keep running but users
    know the guide had no visual effect.
    """

    kind: str
    options: dict = field(default_factory=dict)

    def __radd__(self, other):
        # ``ggplot + guide_axis_*()``: emit a one-time warning
        # per kind and return the plot unchanged so downstream
        # operations keep working.
        if self.kind not in _WARNED_KINDS:
            _WARNED_KINDS.add(self.kind)
            warnings.warn(
                f"guide_axis_{self.kind} is not yet implemented "
                "on top of plotnine and is currently a no-op. "
                "The plot is returned unchanged.",
                UserWarning,
                stacklevel=2,
            )
        return other

    def __add__(self, other):
        # ``guide_axis_*() + ggplot`` — mirror of ``__radd__``.
        return self.__radd__(other)


def guide_axis_nested(
    delim: str = "_",
    extend: float = 0.1,
    inv: bool = False,
    **kwargs,
) -> GuideAxisSpec:
    """
    Multi-level axis labels matching :func:`facet_nested`.
    """
    return GuideAxisSpec(
        "nested",
        {"delim": delim, "extend": extend, "inv": inv, **kwargs},
    )


def guide_axis_manual(
    breaks: "Sequence | None" = None,
    labels: "Sequence | None" = None,
    label_colour: "str | Sequence[str] | None" = None,
    label_size: "float | Sequence[float] | None" = None,
    title: str | None = None,
    **kwargs,
) -> GuideAxisSpec:
    """
    User-supplied breaks and labels.
    """
    return GuideAxisSpec(
        "manual",
        {
            "breaks": breaks,
            "labels": labels,
            "label_colour": label_colour,
            "label_size": label_size,
            "title": title,
            **kwargs,
        },
    )


def guide_axis_minor(**kwargs) -> GuideAxisSpec:
    """Annotate minor ticks (no labels)."""
    return GuideAxisSpec("minor", kwargs)


def guide_axis_logticks(
    sides: str = "bl",
    short: float = 0.5,
    mid: float = 1.0,
    long: float = 1.5,
    **kwargs,
) -> GuideAxisSpec:
    """Log-tick guide."""
    return GuideAxisSpec(
        "logticks",
        {
            "sides": sides,
            "short": short,
            "mid": mid,
            "long": long,
            **kwargs,
        },
    )


def guide_axis_truncated(
    trunc_lower: "Any | Callable | None" = None,
    trunc_upper: "Any | Callable | None" = None,
    **kwargs,
) -> GuideAxisSpec:
    """Axis line truncated to data extent."""
    return GuideAxisSpec(
        "truncated",
        {
            "trunc_lower": trunc_lower,
            "trunc_upper": trunc_upper,
            **kwargs,
        },
    )


def guide_axis_scalebar(
    size: float = 1.0,
    label: str | None = None,
    **kwargs,
) -> GuideAxisSpec:
    """Inline scalebar guide."""
    return GuideAxisSpec(
        "scalebar",
        {"size": size, "label": label, **kwargs},
    )


def guide_axis_colour(
    colours: "Sequence[str] | None" = None,
    **kwargs,
) -> GuideAxisSpec:
    """Per-tick coloured labels."""
    return GuideAxisSpec("colour", {"colours": colours, **kwargs})


# American spelling alias
guide_axis_color = guide_axis_colour


def guide_dendro(
    dendro: "Any | None" = None,
    position: str = "top",
    **kwargs,
) -> GuideAxisSpec:
    """
    Dendrogram axis guide.

    The ``dendro`` argument should be a precomputed
    :class:`scipy.cluster.hierarchy` linkage matrix or a
    ``dendrogram`` dict. The actual drawing requires a
    facet subclass that knows about :class:`GuideAxisSpec`
    (not yet shipped).
    """
    return GuideAxisSpec(
        "dendro",
        {"dendro": dendro, "position": position, **kwargs},
    )


def guide_stringlegend(
    ncol: int | None = None,
    nrow: int | None = None,
    **kwargs,
) -> GuideAxisSpec:
    """Compact text-only legend (placeholder)."""
    return GuideAxisSpec(
        "stringlegend",
        {"ncol": ncol, "nrow": nrow, **kwargs},
    )
