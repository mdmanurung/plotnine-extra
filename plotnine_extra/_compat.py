"""The one place plotnine-extra reaches into private plotnine names.

Every underscore-prefixed plotnine name this package depends on is imported
here and nowhere else. A plotnine bump that renames or removes one then breaks
this file, and ``tests/test_canary.py`` names the missing item.

Two kinds of coupling live here:

* ``PRIVATE_NAMES``: names we import. A removal raises ``ImportError``.
* ``FACET_HOOKS``: methods plotnine calls on a facet and we override. A removal
  does not raise. The override just stops being called, which is how
  ``facet_manual`` once went dead without any error.

Prefer plotnine's public API. Add a name below only when no public route
exists, and say why in the comment beside it.
"""

from __future__ import annotations

from plotnine._mpl.axes import p9Axes
from plotnine._mpl.gridspec import p9GridSpec
from plotnine._utils import (
    groupby_apply,
    join_keys,
    match,
    resolution,
    to_rgba,
)
from plotnine.facets.facet import facet

__all__ = [
    "FACET_HOOKS",
    "PRIVATE_NAMES",
    "groupby_apply",
    "join_keys",
    "match",
    "missing_facet_hooks",
    "p9Axes",
    "p9GridSpec",
    "resolution",
    "to_rgba",
]

# "plotnine.module.name": why we need it.
PRIVATE_NAMES: dict[str, str] = {
    "plotnine._mpl.axes.p9Axes": "facet_manual creates axes itself",
    "plotnine._mpl.gridspec.p9GridSpec": "facet_manual and at_panel grids",
    "plotnine._utils.groupby_apply": "beeswarm and quasirandom positions",
    "plotnine._utils.join_keys": "facet_manual panel keys",
    "plotnine._utils.match": "facet_manual panel keys",
    "plotnine._utils.resolution": "beeswarm point size",
    "plotnine._utils.to_rgba": "richtext and textbox colours",
}

# Facet methods that plotnine calls and our facets override.
FACET_HOOKS: tuple[str, ...] = ("compute_layout", "_make_gridspec")


def missing_facet_hooks() -> list[str]:
    """Return the overridden hooks that plotnine's ``facet`` no longer has."""
    return [name for name in FACET_HOOKS if not hasattr(facet, name)]
