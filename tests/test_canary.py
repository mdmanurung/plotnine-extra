"""Canaries for the plotnine coupling that ggann and annplyr also rely on.

Run these alone with ``pytest -m canary``. The CI ``prerelease`` job
(non-blocking) runs them, with the rest of the suite, against the newest
plotnine pre-release, and the ``Nightly canary`` workflow runs them and
ggann's canaries every night against it. Each one asserts an *effect*, not
just that a name imports, because the plotnine 0.16.0a15 breaks were silent: ``at_panel``
filtered nothing and panel ratios were ignored, and nothing raised.

When one fails after a plotnine bump, fix ``plotnine_extra/_compat.py`` or the
code it points to, and add a row to the table in ``UPSTREAM_SYNC.md``.
"""

from __future__ import annotations

import importlib
from io import BytesIO

import matplotlib
import numpy as np
import pandas as pd
import pytest
from plotnine import aes, geom_point, ggplot
from plotnine.composition import plot_layout

import plotnine_extra as pe
from plotnine_extra import _compat

matplotlib.use("Agg")

pytestmark = pytest.mark.canary


def _points(n: int = 4) -> ggplot:
    df = pd.DataFrame({"x": range(n), "y": range(n)})
    return ggplot(df, aes("x", "y")) + geom_point()


def _render(figure) -> None:
    """plotnine 0.16 lays panels out when the figure renders, not in draw()."""
    figure.savefig(BytesIO(), format="png")


@pytest.mark.parametrize("dotted", sorted(_compat.PRIVATE_NAMES))
def test_private_name_still_exists(dotted):
    module, _, name = dotted.rpartition(".")
    assert hasattr(importlib.import_module(module), name), (
        f"plotnine no longer has {dotted} "
        f"({_compat.PRIVATE_NAMES[dotted]}). Update plotnine_extra/_compat.py."
    )


def test_overridden_facet_hooks_still_exist():
    # A removed base hook leaves our override as dead code and raises nothing.
    assert _compat.missing_facet_hooks() == []


def test_facet_manual_override_is_still_called():
    df = pd.DataFrame(
        {"x": [1, 2, 3, 4], "y": [1, 2, 3, 4], "g": list("AABB")}
    )
    p = (
        ggplot(df, aes("x", "y"))
        + geom_point()
        + pe.facet_manual("g", design="AA\nBB")
    )
    p.draw(show=False)
    # nrow/ncol are set by facet_manual.compute_layout, so they prove it ran.
    assert (p.built.facet.nrow, p.built.facet.ncol) == (2, 2)


def test_at_panel_filters_to_the_selected_panel():
    df = pd.DataFrame(
        {"x": [1, 2, 3, 4], "y": [1, 2, 3, 4], "g": ["a", "a", "b", "b"]}
    )
    layer = pe.at_panel(geom_point(), "g == 'b'")
    p = ggplot(df, aes("x", "y")) + layer + pe.facet_wrap2("g")
    out = p.layer_data(0)
    assert out["PANEL"].astype(int).unique().tolist() == [2]


def test_guide_stringlegend_runs_its_own_setup():
    guide = pe.guide_stringlegend()
    assert guide.kind == "stringlegend"
    assert guide._elements_cls.__name__ == "GuideElementsStringLegend"


def test_get_breaks_reads_a_built_plot():
    breaks = pe.get_breaks(_points(3), "x")
    assert len(breaks) >= 2


def test_beeswarm_separates_tied_values():
    df = pd.DataFrame({"g": ["a"] * 20, "y": [0.0] * 10 + [1.0] * 10})
    out = (ggplot(df, aes("g", "y")) + pe.geom_beeswarm()).layer_data(0)
    assert out.loc[out["y"] == 0.0, "x"].nunique() == 10


def test_composition_is_plotnines_own():
    from plotnine import composition

    for name in ("Beside", "Stack", "Wrap", "plot_layout", "plot_annotation"):
        assert getattr(pe, name) is getattr(composition, name), name


def test_plot_layout_ratios_reach_the_rendered_panels():
    # ggann's compose(widths=, heights=) relies on this.
    fig = (_points() / _points()) + plot_layout(heights=[1, 1.5])
    figure = fig.draw(show=False)
    _render(figure)
    top, bottom = (p.axs[0].get_position().height for p in fig.iter_plots())
    assert bottom / top == pytest.approx(1.5, rel=0.02)
    assert np.isfinite(top)


def test_plot_layout_after_native_or_applies_widths():
    # main's 178fc52cb fixed a crash here by ignoring the layout. With
    # composition delegated to plotnine the widths must actually apply.
    fig = (_points() | _points()) + pe.plot_layout(widths=[1.6, 1])
    figure = fig.draw(show=False)
    _render(figure)
    left, right = (p.axs[0].get_position().width for p in fig.iter_plots())
    assert left / right == pytest.approx(1.6, rel=0.02)
