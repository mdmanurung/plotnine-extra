"""Unit tests for ggpubr-style summary helpers."""

import numpy as np
import pandas as pd
import pytest

from plotnine_extra import (
    desc_statby,
    get_summary_stats,
    mean_ci,
    mean_range,
    mean_sd,
    mean_se_,
    median_hilow_,
    median_iqr,
    median_mad,
    median_q1q3,
    median_range,
)


@pytest.fixture
def x():
    return np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])


def test_mean_sd(x):
    out = mean_sd(x)
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] < out["y"] < out["ymax"]
    assert out["ymax"] - out["y"] == pytest.approx(out["y"] - out["ymin"])


def test_mean_se_(x):
    out = mean_se_(x)
    assert out["y"] == pytest.approx(5.5)
    se = float(np.std(x, ddof=1) / np.sqrt(len(x)))
    assert out["ymax"] - out["y"] == pytest.approx(se)


def test_mean_ci(x):
    out = mean_ci(x, ci=0.95)
    assert out["y"] == pytest.approx(5.5)
    assert out["ymax"] > out["y"] > out["ymin"]


def test_mean_range(x):
    out = mean_range(x)
    # ggpubr: range = max - min = 9, mean = 5.5, so
    # ymin = 5.5 - 9 = -3.5, ymax = 5.5 + 9 = 14.5
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] == pytest.approx(-3.5)
    assert out["ymax"] == pytest.approx(14.5)


def test_median_iqr(x):
    out = median_iqr(x)
    assert out["y"] == pytest.approx(5.5)
    iqr = float(np.percentile(x, 75) - np.percentile(x, 25))
    assert out["ymax"] - out["y"] == pytest.approx(iqr)


def test_median_mad(x):
    out = median_mad(x)
    assert out["y"] == pytest.approx(5.5)
    assert out["ymax"] > out["ymin"]


def test_median_q1q3(x):
    out = median_q1q3(x)
    assert out["ymin"] == pytest.approx(np.percentile(x, 25))
    assert out["ymax"] == pytest.approx(np.percentile(x, 75))


def test_median_range(x):
    out = median_range(x)
    # ggpubr: range = max - min = 9, median = 5.5
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] == pytest.approx(-3.5)
    assert out["ymax"] == pytest.approx(14.5)


def test_median_hilow_quantile_definition(x):
    out = median_hilow_(x, conf_int=0.95)
    # ggpubr: ymin = quantile(x, 0.025), ymax = quantile(x, 0.975)
    assert out["y"] == pytest.approx(5.5)
    assert out["ymin"] == pytest.approx(np.quantile(x, 0.025))
    assert out["ymax"] == pytest.approx(np.quantile(x, 0.975))


def test_median_hilow(x):
    out = median_hilow_(x)
    assert out["ymin"] <= out["y"] <= out["ymax"]


def test_empty_input_returns_nan():
    out = mean_sd([])
    assert np.isnan(out["y"])


def test_get_summary_stats_common():
    df = pd.DataFrame(
        {
            "y": [1, 2, 3, 4, 5],
            "g": ["a", "a", "b", "b", "b"],
        }
    )
    out = get_summary_stats(df, columns="y", type="common")
    assert "mean" in out.columns
    assert out["mean"].iloc[0] == pytest.approx(3.0)


def test_get_summary_stats_grouped():
    df = pd.DataFrame(
        {
            "y": [1, 2, 3, 4, 5],
            "g": ["a", "a", "b", "b", "b"],
        }
    )
    out = get_summary_stats(df, columns="y", groupvars="g")
    assert set(out["g"]) == {"a", "b"}
    rows_a = out[out["g"] == "a"]
    assert rows_a["mean"].iloc[0] == pytest.approx(1.5)


def test_get_summary_stats_unknown_type():
    df = pd.DataFrame({"y": [1, 2, 3]})
    with pytest.raises(ValueError, match="Unknown summary type"):
        get_summary_stats(df, columns="y", type="bogus")


def test_desc_statby():
    df = pd.DataFrame(
        {
            "y": [1, 2, 3, 4, 5],
            "g": ["a", "a", "b", "b", "b"],
        }
    )
    out = desc_statby(df, "y", "g")
    assert set(out["g"]) == {"a", "b"}
    assert out.loc[out["g"] == "b", "mean"].iloc[0] == pytest.approx(4.0)
    assert "ci" in out.columns
