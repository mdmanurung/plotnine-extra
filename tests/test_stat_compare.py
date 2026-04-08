"""
Tests for ``stat_compare`` (port of ggcompare's ``stat_compare``).

These are mostly smoke tests verifying that each documented
mode of the stat builds without error and that the computed
p-values match what scipy returns directly.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest
from plotnine import (
    aes,
    facet_grid,
    geom_boxplot,
    ggplot,
)
from plotnine.data import mpg
from scipy import stats as sps

from plotnine_extra import stat_compare
from plotnine_extra.stats.stat_compare import (
    _adjust_pvalues,
    _format_labels,
    _pair_test,
    _resolve_scale,
    _run_test,
)


@pytest.fixture(autouse=True)
def _silence_runtime_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


# ---------------------------------------------------------------
# Pure-helper unit tests
# ---------------------------------------------------------------


def test_pair_test_wilcoxon():
    rng = np.random.default_rng(0)
    a = rng.normal(0, 1, 30)
    b = rng.normal(1, 1, 30)
    out = _pair_test(a, b, parametric=False, method=None, method_args={})
    expected = sps.mannwhitneyu(a, b, alternative="two-sided")
    assert out["p"] == pytest.approx(float(expected.pvalue))
    assert "Wilcoxon" in out["method"]


def test_pair_test_t_test():
    rng = np.random.default_rng(1)
    a = rng.normal(0, 1, 30)
    b = rng.normal(0.5, 1, 30)
    out = _pair_test(a, b, parametric=True, method=None, method_args={})
    expected = sps.ttest_ind(a, b, equal_var=False)
    assert out["p"] == pytest.approx(float(expected.pvalue))
    assert "t-test" in out["method"]


def test_pair_test_empty_input():
    out = _pair_test(
        np.array([]),
        np.array([1.0]),
        parametric=False,
        method=None,
        method_args={},
    )
    assert np.isnan(out["p"])


def test_run_test_multiple_kruskal():
    rng = np.random.default_rng(2)
    df = pd.DataFrame(
        {
            "y": np.concatenate(
                [
                    rng.normal(0, 1, 20),
                    rng.normal(1, 1, 20),
                    rng.normal(2, 1, 20),
                ]
            ),
            "group": ["a"] * 20 + ["b"] * 20 + ["c"] * 20,
        }
    )
    out = _run_test(
        df,
        multiple=True,
        parametric=False,
        method=None,
        method_args={},
    )
    assert out["p"] < 0.05
    assert "Kruskal" in out["method"]


def test_run_test_multiple_anova():
    rng = np.random.default_rng(3)
    df = pd.DataFrame(
        {
            "y": np.concatenate(
                [
                    rng.normal(0, 1, 20),
                    rng.normal(1, 1, 20),
                    rng.normal(2, 1, 20),
                ]
            ),
            "group": ["a"] * 20 + ["b"] * 20 + ["c"] * 20,
        }
    )
    out = _run_test(
        df,
        multiple=True,
        parametric=True,
        method=None,
        method_args={},
    )
    assert "ANOVA" in out["method"]


def test_format_labels_default():
    labs = _format_labels(
        np.array([1e-300, 0.001, 0.5, np.nan]),
        breaks=None,
        labels=None,
    )
    assert labs[0].startswith("p < ")
    assert labs[1] == "0.001"
    assert labs[2] == "0.5"
    assert labs[3] == ""


def test_format_labels_with_breaks():
    labs = _format_labels(
        np.array([0.0001, 0.005, 0.04, 0.5]),
        breaks=[0, 0.001, 0.01, 0.05, 1],
        labels=None,
    )
    assert labs == ["***", "**", "*", "ns"]


def test_format_labels_custom_labels():
    labs = _format_labels(
        np.array([0.0001, 0.5]),
        breaks=[0, 0.001, 1],
        labels=["sig", "ns"],
    )
    assert labs == ["sig", "ns"]


def test_format_labels_label_length_mismatch():
    with pytest.raises(ValueError):
        _format_labels(
            np.array([0.5]),
            breaks=[0, 0.5, 1],
            labels=["only-one"],
        )


def test_adjust_pvalues_holm():
    p = np.array([0.01, 0.02, 0.03, 0.04])
    out = _adjust_pvalues(p, "holm")
    # Adjusted p-values are non-decreasing in the same order
    assert (out >= p).all()
    assert out[0] <= out[-1]


def test_resolve_scale_numeric_passthrough():
    assert _resolve_scale(None, 3) == 3.0


def test_resolve_scale_no_scale_returns_value():
    assert _resolve_scale(None, "minivan") == "minivan"


# ---------------------------------------------------------------
# Smoke tests against actual ggplot pipelines
# ---------------------------------------------------------------


def _draw(plot):
    fig = plot.draw(show=False)
    assert fig is not None
    return fig


def test_global_mode():
    p = ggplot(mpg, aes("class", "displ")) + geom_boxplot() + stat_compare()
    _draw(p)


def test_bracket_false():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(bracket=False)
    )
    _draw(p)


def test_overall_mode():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(overall=True)
    )
    _draw(p)


def test_ref_group_string():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(ref_group="minivan")
    )
    _draw(p)


def test_ref_group_with_breaks():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(
            ref_group="minivan",
            breaks=[0, 0.001, 0.01, 0.05, 1],
        )
    )
    _draw(p)


def test_ref_group_with_cutoff():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(ref_group="minivan", cutoff=0.01)
    )
    _draw(p)


def test_explicit_comparisons():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(
            comparisons=[
                ("compact", "midsize"),
                ("pickup", "suv"),
            ],
            tip_length=0.05,
            step_increase=0,
        )
    )
    _draw(p)


def test_within_x_subgroups():
    p = (
        ggplot(mpg, aes("drv", "displ", fill="class"))
        + geom_boxplot()
        + stat_compare()
    )
    _draw(p)


def test_parametric_flag():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(parametric=True)
    )
    _draw(p)


def test_faceting_with_explicit_comparisons():
    drvs = sorted(mpg["drv"].unique())
    pairs = [
        (drvs[i], drvs[j])
        for i in range(len(drvs))
        for j in range(i + 1, len(drvs))
    ]
    p = (
        ggplot(mpg, aes("drv", "displ"))
        + geom_boxplot()
        + stat_compare(comparisons=pairs)
        + facet_grid(cols="class", scales="free")
    )
    _draw(p)


def test_layer_level_correction():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(ref_group=1, correction="fdr")
        + facet_grid(cols="cyl", scales="free")
    )
    _draw(p)


def test_panel_level_correction():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(ref_group=1, correction="fdr", panel_indep=True)
        + facet_grid(cols="cyl", scales="free")
    )
    _draw(p)


def test_unknown_correction_raises():
    p = (
        ggplot(mpg, aes("class", "displ"))
        + geom_boxplot()
        + stat_compare(correction="not-a-method")
    )
    with pytest.raises(ValueError):
        _draw(p)
