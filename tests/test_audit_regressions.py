"""
Regression tests for audit-surfaced bugs.

Every test here is a `.draw()` exercise of a symbol that was
previously crashing or silently producing wrong output. These
tests guard against regressions on the fixes landed after the
multi-pass repo audit.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest
from plotnine import (
    aes,
    geom_boxplot,
    geom_point,
    ggplot,
)
from plotnine.data import mpg

import plotnine_extra as pe


@pytest.fixture(autouse=True)
def _silence():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


# ---------------------------------------------------------------
# Slice B — geoms and stats BLOCKERS
# ---------------------------------------------------------------


def test_geom_text_aimed_draws():
    """BLOCKER: geom_text_aimed crashed with KeyError 'path_effects'."""
    df = pd.DataFrame(
        {
            "x": [0.0, 1.0, 2.0, 3.0],
            "y": [0.0, 1.0, 0.5, 1.5],
            "label": ["a", "b", "c", "d"],
            "xend": [1.0, 2.0, 3.0, 4.0],
            "yend": [1.0, 0.5, 1.5, 2.0],
        }
    )
    p = ggplot(df, aes("x", "y", label="label", xend="xend", yend="yend"))
    p = p + pe.geom_text_aimed()
    p.draw(show=False)


def test_stat_rle_draws():
    """BLOCKER: stat_rle dropped PANEL + group columns."""
    df = pd.DataFrame(
        {
            "x": np.arange(20),
            "label": ["a"] * 5 + ["b"] * 5 + ["a"] * 5 + ["b"] * 5,
        }
    )
    p = ggplot(df, aes("x", label="label")) + pe.stat_rle(geom="rect")
    p.draw(show=False)


def test_geom_pwc_draws():
    """BLOCKER: geom_pwc had no draw_group and raised NotImplementedError."""
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot() + pe.geom_pwc()
    p.draw(show=False)


def test_geom_signif_ggsignif_kwargs():
    """BLOCKER: geom_signif rejected y_position / annotations."""
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + pe.geom_signif(xmin=1, xmax=3, y_position=7, annotations="***")
    )
    p.draw(show=False)


# ---------------------------------------------------------------
# Slice A — guides / scales / coords BLOCKERS
# ---------------------------------------------------------------


@pytest.mark.parametrize(
    "factory",
    [
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
    ],
)
def test_guide_axis_spec_addable(factory):
    """BLOCKER: every guide_axis_* crashed on ``plot + guide``."""
    fn = getattr(pe, factory)
    p = ggplot(mpg, aes("displ", "hwy")) + geom_point() + fn()
    # No crash; the spec is a no-op and emits a UserWarning on
    # first use but must not break the pipeline.
    p.draw(show=False)


def test_scale_colour_multi_does_not_split_string():
    """BLOCKER: aesthetics='colour' iterated character-by-character."""
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3], "cls": ["a", "b", "c"]})
    scales = pe.scale_colour_multi(
        {"colour": ["#E64B35", "#4DBBD5", "#00A087"]},
        discrete=True,
    )
    p = ggplot(df, aes("x", "y", colour="cls")) + geom_point() + scales
    p.draw(show=False)


def test_scale_fill_multi_draws():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3], "cls": ["a", "b", "c"]})
    scales = pe.scale_fill_multi(
        {"fill": ["#E64B35", "#4DBBD5", "#00A087"]},
        discrete=True,
    )
    p = (
        ggplot(df, aes("x", "y", fill="cls"))
        + geom_point(shape="s", size=8)
        + scales
    )
    p.draw(show=False)


def test_coord_axes_inside_actually_moves_spines():
    """BLOCKER: coord_axes_inside was a silent no-op."""
    p = (
        ggplot(mpg, aes("displ", "hwy"))
        + geom_point()
        + pe.coord_axes_inside(xintercept=4, yintercept=25)
    )
    fig = p.draw(show=False)
    ax = fig.axes[0]
    assert ax.spines["left"].get_position() == ("data", 4)
    assert ax.spines["bottom"].get_position() == ("data", 25)
    assert not ax.spines["right"].get_visible()
    assert not ax.spines["top"].get_visible()


def test_apply_axes_inside_exported():
    """MAJOR: apply_axes_inside was missing from the top-level API."""
    assert hasattr(pe, "apply_axes_inside")
    assert "apply_axes_inside" in pe._extra_all


# ---------------------------------------------------------------
# Slice C — palettes / summary / styling BLOCKERS
# ---------------------------------------------------------------


def test_add_summary_pointrange_draws():
    """BLOCKER: add_summary passed dicts to stat_summary.fun_data."""
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot()
    pe.add_summary(p, "mean_se", "pointrange").draw(show=False)


def test_add_summary_errorbar_draws():
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot()
    pe.add_summary(p, "mean_ci", "errorbar").draw(show=False)


def test_add_summary_linerange_draws():
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot()
    pe.add_summary(p, "mean_sd", "linerange").draw(show=False)


def test_add_summary_crossbar_draws():
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot()
    pe.add_summary(p, "median_iqr", "crossbar").draw(show=False)


def test_add_summary_upper_errorbar_truncates():
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot()
    pe.add_summary(p, "median_iqr", "upper_errorbar").draw(show=False)


def test_add_summary_lower_pointrange_truncates():
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot()
    pe.add_summary(p, "median_range", "lower_pointrange").draw(show=False)


def test_theme_pubclean_draws():
    """BLOCKER: grey80 is not a valid matplotlib color."""
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + pe.theme_pubclean()
    )
    p.draw(show=False)


def test_theme_cleveland_draws():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + pe.theme_cleveland()
    )
    p.draw(show=False)


def test_grids_default_color_draws():
    """BLOCKER: grids(color='grey92') crashed matplotlib."""
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot() + pe.grids()
    p.draw(show=False)


def test_show_point_shapes_draws():
    """BLOCKER: numeric R shape codes crashed matplotlib."""
    pe.show_point_shapes().draw(show=False)


# ---------------------------------------------------------------
# Slice C — correctness MAJORS
# ---------------------------------------------------------------


def test_mean_range_ggpubr_formula():
    """MAJOR: mean_range used min/max, ggpubr uses mean ± (max-min)."""
    out = pe.mean_range(np.arange(1, 11, dtype=float))
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] == pytest.approx(-3.5)
    assert out["ymax"] == pytest.approx(14.5)


def test_median_range_ggpubr_formula():
    """MAJOR: median_range used min/max, ggpubr uses median ± (max-min)."""
    out = pe.median_range(np.arange(1, 11, dtype=float))
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] == pytest.approx(-3.5)
    assert out["ymax"] == pytest.approx(14.5)


def test_median_hilow_uses_percentile():
    """MAJOR: median_hilow_ used Hmisc-style order stats;
    ggpubr uses simple percentiles."""
    x = np.arange(1, 11, dtype=float)
    out = pe.median_hilow_(x, conf_int=0.95)
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] == pytest.approx(np.quantile(x, 0.025))
    assert out["ymax"] == pytest.approx(np.quantile(x, 0.975))
