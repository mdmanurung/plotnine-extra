"""
Plot composition, re-exported from plotnine.

plotnine ships plot composition natively: the composing operators
(``|``, ``/``, ``-``, ``+``) live on ``plotnine.ggplot`` and the composition
objects live in ``plotnine.composition``. plotnine-extra does **not** vendor
its own copy -- doing so caused a namespace collision where ``p1 | p2``
produced plotnine's ``Beside`` while ``plot_layout`` came from plotnine-extra,
and mixing the two crashed.

Everything re-exported here has shipped in plotnine 0.16, which is this
package's minimum. Syncing composition is therefore automatic: it rides along
with the installed plotnine.
"""

from __future__ import annotations

from plotnine.composition import (
    Beside,
    Compose,
    Stack,
    Wrap,
    guide_area,
    inset_element,
    plot_annotation,
    plot_layout,
    plot_spacer,
)

__all__ = (
    "Compose",
    "Stack",
    "Beside",
    "Wrap",
    "guide_area",
    "inset_element",
    "plot_annotation",
    "plot_layout",
    "plot_spacer",
)
