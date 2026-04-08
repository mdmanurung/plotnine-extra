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


# ---------------------------------------------------------------
# Assertion-based tests calling compute_panel directly with
# synthetic, deterministic data. These guard against silent
# regressions that a "draws without error" smoke test would miss.
# ---------------------------------------------------------------


def _fixture(seed=0, n_per=25):
    """Three-group fixture with clearly different means."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "y": np.concatenate(
                [
                    rng.normal(0.0, 1.0, n_per),
                    rng.normal(2.0, 1.0, n_per),
                    rng.normal(4.0, 1.0, n_per),
                ]
            ),
            "x": np.repeat([1.0, 2.0, 3.0], n_per),
        }
    )
    df["group"] = df["x"]
    df["PANEL"] = 1
    return df


def test_compute_panel_global_mode_matches_kruskal():
    df = _fixture()
    s = stat_compare()
    out = s.compute_panel(df, scales=None)
    assert len(out) == 1
    expected = sps.kruskal(
        df["y"][df["x"] == 1].to_numpy(),
        df["y"][df["x"] == 2].to_numpy(),
        df["y"][df["x"] == 3].to_numpy(),
    )
    assert out["p"].iloc[0] == pytest.approx(float(expected.pvalue))
    assert "Kruskal" in out["method"].iloc[0]


def test_compute_panel_parametric_matches_anova():
    df = _fixture()
    s = stat_compare(parametric=True)
    out = s.compute_panel(df, scales=None)
    expected = sps.f_oneway(
        df["y"][df["x"] == 1].to_numpy(),
        df["y"][df["x"] == 2].to_numpy(),
        df["y"][df["x"] == 3].to_numpy(),
    )
    assert out["p"].iloc[0] == pytest.approx(float(expected.pvalue))
    assert "ANOVA" in out["method"].iloc[0]


def test_compute_panel_ref_group_matches_wilcoxon():
    df = _fixture()
    s = stat_compare(ref_group=1)
    out = s.compute_panel(df, scales=None)
    # Two pairwise comparisons: 2 vs 1, 3 vs 1
    assert len(out) == 2
    ref = df["y"][df["x"] == 1].to_numpy()
    g2 = df["y"][df["x"] == 2].to_numpy()
    g3 = df["y"][df["x"] == 3].to_numpy()
    exp_21 = sps.mannwhitneyu(g2, ref, alternative="two-sided")
    exp_31 = sps.mannwhitneyu(g3, ref, alternative="two-sided")
    ps = sorted(out["p"].to_list())
    assert ps[0] == pytest.approx(
        min(float(exp_21.pvalue), float(exp_31.pvalue))
    )
    assert ps[1] == pytest.approx(
        max(float(exp_21.pvalue), float(exp_31.pvalue))
    )


def test_compute_panel_explicit_comparisons():
    df = _fixture()
    s = stat_compare(comparisons=[(1, 3)])
    out = s.compute_panel(df, scales=None)
    assert len(out) == 1
    expected = sps.mannwhitneyu(
        df["y"][df["x"] == 1].to_numpy(),
        df["y"][df["x"] == 3].to_numpy(),
        alternative="two-sided",
    )
    assert out["p"].iloc[0] == pytest.approx(float(expected.pvalue))


def test_compute_panel_overall_mode():
    df = _fixture()
    s = stat_compare(overall=True)
    out = s.compute_panel(df, scales=None)
    # One row per unique x
    assert len(out) == 3
    for xv in [1.0, 2.0, 3.0]:
        in_group = df["y"][df["x"] == xv].to_numpy()
        others = df["y"][df["x"] != xv].to_numpy()
        expected = sps.mannwhitneyu(in_group, others, alternative="two-sided")
        row_p = out["p"][out["x"] == xv].iloc[0]
        assert row_p == pytest.approx(float(expected.pvalue))


def test_panel_level_correction_actually_corrects():
    """Regression for audit MAJOR #5.

    When ``panel_indep=True``, ``compute_panel`` must apply the
    correction per panel so that ``q >= p`` and ``q`` differs
    from the raw ``p`` (when multiple tests are present).
    """
    df = _fixture()
    s = stat_compare(ref_group=1, correction="fdr", panel_indep=True)
    out = s.compute_panel(df, scales=None)
    assert len(out) == 2
    p = out["p"].to_numpy()
    q = out["q"].to_numpy()
    assert (q >= p - 1e-12).all()
    # At least one q should differ from its p (fdr on 2 tests)
    assert np.any(np.abs(q - p) > 1e-12)


def test_layer_level_correction_differs_from_panel_level():
    """Regression for audit MAJOR #5, counterpart.

    Layer-level correction should aggregate p-values across
    panels before adjusting, so the adjusted q-values differ
    from the panel-level variant whenever more than one panel
    contributes comparisons.
    """
    d1 = _fixture(seed=10)
    d1["PANEL"] = 1
    d2 = _fixture(seed=11)
    d2["PANEL"] = 2
    data = pd.concat([d1, d2], ignore_index=True)

    # Panel-level
    s_panel = stat_compare(ref_group=1, correction="fdr", panel_indep=True)
    panel_rows = []
    for _, sub in data.groupby("PANEL"):
        panel_rows.append(s_panel.compute_panel(sub, scales=None))
    panel_out = pd.concat(panel_rows, ignore_index=True)

    # Layer-level
    s_layer = stat_compare(ref_group=1, correction="fdr", panel_indep=False)
    layer_rows = []
    for _, sub in data.groupby("PANEL"):
        layer_rows.append(s_layer.compute_panel(sub, scales=None))
    layer_panel_stage = pd.concat(layer_rows, ignore_index=True)
    # Simulate the layer-level re-adjustment
    from plotnine_extra.stats.stat_compare import _adjust_pvalues

    layer_q = _adjust_pvalues(layer_panel_stage["p"].to_numpy(), "fdr")
    # With 4 pooled tests vs 2 tests per panel, the adjusted
    # q-values should differ somewhere.
    assert np.any(np.abs(layer_q - panel_out["q"].to_numpy()) > 1e-12)


def test_cutoff_shifts_hidden_brackets():
    """Regression for audit MAJOR #2.

    When the cutoff hides some labels, the visible brackets
    should be shifted down by ``space`` to close the gap.
    """
    from plotnine_extra.stats.stat_compare import (
        _shift_hidden_brackets,
    )

    # Simulate three consecutive brackets; the middle one is
    # hidden. The topmost should drop by one ``space``.
    df = pd.DataFrame(
        {
            "PANEL": [1, 1, 1],
            "label": ["a", "", "c"],
            "p": [0.001, 0.05, 0.02],
            "ymin": [10.0, 11.0, 12.0],
            "ymax": [10.5, 11.5, 12.5],
            "space": [1.0, 1.0, 1.0],
        }
    )
    out = _shift_hidden_brackets(df).sort_values("label")
    # "a" at ymin=10 is below the hidden "b"; it should stay at 10
    # "c" at ymin=12 should drop by 1 to 11
    # The hidden "" row also gets shifted (to 10) but is invisible
    a_row = out[out["label"] == "a"].iloc[0]
    c_row = out[out["label"] == "c"].iloc[0]
    assert a_row["ymin"] == pytest.approx(10.0)
    assert c_row["ymin"] == pytest.approx(11.0)


def test_horizontal_orientation_raises():
    """Regression for audit MAJOR #3.

    Horizontal plots (continuous x, discrete y) are not yet
    supported; the stat should refuse rather than silently
    produce nonsense brackets.
    """
    p = ggplot(mpg, aes("displ", "class")) + geom_boxplot() + stat_compare()
    with pytest.raises(NotImplementedError, match="horizontal"):
        _draw(p)


def test_is_horizontal_vertical_passthrough():
    from plotnine_extra.stats.stat_compare import _is_horizontal

    # Typical vertical data: x is small integer set, y continuous
    df = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0, 1.0, 2.0, 3.0],
            "y": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6],
        }
    )
    assert _is_horizontal(df) is False

    # Horizontal: y is small integer set, x continuous
    df2 = pd.DataFrame(
        {
            "x": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6],
            "y": [1.0, 2.0, 3.0, 1.0, 2.0, 3.0],
        }
    )
    assert _is_horizontal(df2) is True
