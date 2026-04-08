"""
Summary-statistic helpers ported from ggpubr.

These functions return tidy dictionaries (or DataFrames) with the
``y``, ``ymin`` and ``ymax`` columns expected by
``stat_summary``. They can be passed directly via the
``fun_data`` parameter::

    stat_summary(fun_data=mean_sd)

Each function accepts a 1-D array-like and returns a dict with at
least the ``y`` key. The ``mean_*`` and ``median_*`` variants are
named to match ggpubr exactly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from scipy import stats as _sps

if TYPE_CHECKING:
    from typing import Sequence


__all__ = (
    "mean_ci",
    "mean_sd",
    "mean_se_",
    "mean_range",
    "median_iqr",
    "median_mad",
    "median_q1q3",
    "median_range",
    "median_hilow_",
    "get_summary_stats",
    "desc_statby",
    "add_summary",
)


def _as_array(x):
    a = np.asarray(x, dtype=float)
    return a[~np.isnan(a)]


def mean_ci(x, ci: float = 0.95) -> dict:
    """
    Return the mean and confidence-interval bounds.

    Parameters
    ----------
    x : array-like
        Input values.
    ci : float, default 0.95
        Confidence level (between 0 and 1).
    """
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.mean(a))
    se = float(np.std(a, ddof=1) / np.sqrt(a.size)) if a.size > 1 else 0.0
    t = float(_sps.t.ppf(0.5 + ci / 2, a.size - 1)) if a.size > 1 else 0.0
    return {"y": m, "ymin": m - t * se, "ymax": m + t * se}


def mean_sd(x, mult: float = 1.0) -> dict:
    """
    Return the mean and ``mean ± mult * sd``.

    Parameters
    ----------
    x : array-like
        Input values.
    mult : float, default 1.0
        Standard-deviation multiplier.
    """
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.mean(a))
    s = float(np.std(a, ddof=1)) if a.size > 1 else 0.0
    return {"y": m, "ymin": m - mult * s, "ymax": m + mult * s}


def mean_se_(x, mult: float = 1.0) -> dict:
    """
    Return the mean and ``mean ± mult * se``.

    The trailing underscore mirrors the R name to avoid clashing
    with Python's ``mean`` builtins.
    """
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.mean(a))
    se = float(np.std(a, ddof=1) / np.sqrt(a.size)) if a.size > 1 else 0.0
    return {"y": m, "ymin": m - mult * se, "ymax": m + mult * se}


def mean_range(x) -> dict:
    """Return the mean and the data minimum / maximum."""
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    return {
        "y": float(np.mean(a)),
        "ymin": float(np.min(a)),
        "ymax": float(np.max(a)),
    }


def median_iqr(x, mult: float = 1.0) -> dict:
    """
    Return the median and ``median ± mult * IQR``.
    """
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.median(a))
    q1, q3 = np.percentile(a, [25, 75])
    iqr = float(q3 - q1)
    return {"y": m, "ymin": m - mult * iqr, "ymax": m + mult * iqr}


def median_mad(x, mult: float = 1.0) -> dict:
    """
    Return the median and ``median ± mult * MAD``.

    The MAD (median absolute deviation) is scaled by the usual
    consistency constant ``1.4826``.
    """
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.median(a))
    mad = float(1.4826 * np.median(np.abs(a - m)))
    return {"y": m, "ymin": m - mult * mad, "ymax": m + mult * mad}


def median_q1q3(x) -> dict:
    """Return the median and the first / third quartiles."""
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.median(a))
    q1, q3 = np.percentile(a, [25, 75])
    return {"y": m, "ymin": float(q1), "ymax": float(q3)}


def median_range(x) -> dict:
    """Return the median and the data minimum / maximum."""
    a = _as_array(x)
    if a.size == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    return {
        "y": float(np.median(a)),
        "ymin": float(np.min(a)),
        "ymax": float(np.max(a)),
    }


def median_hilow_(x, conf_int: float = 0.95) -> dict:
    """
    Return the median and the lower/upper confidence bounds.

    Uses the order-statistic interval based on the binomial
    distribution, matching the behaviour of
    ``ggpubr::median_hilow_``.
    """
    a = _as_array(x)
    n = a.size
    if n == 0:
        return {"y": np.nan, "ymin": np.nan, "ymax": np.nan}
    m = float(np.median(a))
    if n < 2:
        return {"y": m, "ymin": m, "ymax": m}
    alpha = 1 - conf_int
    # Order-statistic indices that bracket the median CI
    a_sorted = np.sort(a)
    lo_idx = int(_sps.binom.ppf(alpha / 2, n, 0.5))
    hi_idx = int(_sps.binom.ppf(1 - alpha / 2, n, 0.5))
    lo_idx = max(0, min(n - 1, lo_idx))
    hi_idx = max(0, min(n - 1, hi_idx))
    return {
        "y": m,
        "ymin": float(a_sorted[lo_idx]),
        "ymax": float(a_sorted[hi_idx]),
    }


_SUMMARY_FUNS = {
    "mean": np.mean,
    "sd": lambda v: np.std(v, ddof=1),
    "median": np.median,
    "min": np.min,
    "max": np.max,
    "n": len,
    "q1": lambda v: np.percentile(v, 25),
    "q3": lambda v: np.percentile(v, 75),
    "iqr": lambda v: np.percentile(v, 75) - np.percentile(v, 25),
    "mad": lambda v: 1.4826 * np.median(np.abs(v - np.median(v))),
    "se": lambda v: np.std(v, ddof=1) / np.sqrt(len(v)),
}

_SUMMARY_PROFILES = {
    "common": ("n", "min", "max", "median", "q1", "q3", "iqr", "mean", "sd"),
    "robust": ("n", "median", "iqr", "mad"),
    "five_number": ("min", "q1", "median", "q3", "max"),
    "mean_sd": ("n", "mean", "sd"),
    "mean_se": ("n", "mean", "se"),
    "mean_ci": ("n", "mean", "se"),
    "median_iqr": ("n", "median", "iqr"),
    "median_mad": ("n", "median", "mad"),
    "median_range": ("n", "median", "min", "max"),
    "quantile": ("n", "min", "q1", "median", "q3", "max"),
    "full": tuple(_SUMMARY_FUNS.keys()),
}


def get_summary_stats(
    data: pd.DataFrame,
    columns: "str | Sequence[str] | None" = None,
    type: str = "common",
    groupvars: "str | Sequence[str] | None" = None,
) -> pd.DataFrame:
    """
    Compute summary statistics for one or more numeric columns.

    Parameters
    ----------
    data : DataFrame
        Input data.
    columns : str or list of str, optional
        Numeric columns to summarise. If ``None`` all numeric
        columns are used.
    type : str, default ``"common"``
        Profile of statistics. One of ``"common"``, ``"robust"``,
        ``"five_number"``, ``"mean_sd"``, ``"mean_se"``,
        ``"mean_ci"``, ``"median_iqr"``, ``"median_mad"``,
        ``"median_range"``, ``"quantile"`` or ``"full"``.
    groupvars : str or list of str, optional
        Grouping columns. If supplied, the summary is computed
        within each group.
    """
    if type not in _SUMMARY_PROFILES:
        raise ValueError(
            f"Unknown summary type {type!r}; expected one of "
            f"{sorted(_SUMMARY_PROFILES)}"
        )
    stats = _SUMMARY_PROFILES[type]
    if columns is None:
        columns = list(data.select_dtypes(include="number").columns)
    elif isinstance(columns, str):
        columns = [columns]
    if isinstance(groupvars, str):
        groupvars = [groupvars]

    def _summarise(df: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for col in columns:
            v = df[col].dropna().to_numpy(dtype=float)
            row = {"variable": col}
            for s in stats:
                row[s] = float(_SUMMARY_FUNS[s](v)) if v.size else np.nan
            rows.append(row)
        return pd.DataFrame(rows)

    if not groupvars:
        return _summarise(data)

    pieces = []
    for keys, df in data.groupby(list(groupvars), dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        out = _summarise(df)
        for name, val in zip(groupvars, keys):
            out.insert(0, name, val)
        pieces.append(out)
    return pd.concat(pieces, ignore_index=True)


def desc_statby(
    data: pd.DataFrame,
    measurevar: str,
    groupvars: "str | Sequence[str]",
) -> pd.DataFrame:
    """
    Per-group descriptive statistics for ``measurevar``.

    Returns one row per group with columns ``length``, ``min``,
    ``max``, ``median``, ``mean``, ``iqr``, ``mad``, ``sd``,
    ``se`` and ``ci``.
    """
    if isinstance(groupvars, str):
        groupvars = [groupvars]
    rows = []
    for keys, df in data.groupby(list(groupvars), dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        v = df[measurevar].dropna().to_numpy(dtype=float)
        n = v.size
        if n == 0:
            row = dict.fromkeys(
                [
                    "length",
                    "min",
                    "max",
                    "median",
                    "mean",
                    "iqr",
                    "mad",
                    "sd",
                    "se",
                    "ci",
                ],
                np.nan,
            )
        else:
            mean = float(np.mean(v))
            sd = float(np.std(v, ddof=1)) if n > 1 else 0.0
            se = sd / np.sqrt(n) if n > 0 else 0.0
            tcrit = float(_sps.t.ppf(0.975, n - 1)) if n > 1 else 0.0
            row = {
                "length": n,
                "min": float(np.min(v)),
                "max": float(np.max(v)),
                "median": float(np.median(v)),
                "mean": mean,
                "iqr": float(np.percentile(v, 75) - np.percentile(v, 25)),
                "mad": float(1.4826 * np.median(np.abs(v - np.median(v)))),
                "sd": sd,
                "se": se,
                "ci": tcrit * se,
            }
        for name, val in zip(groupvars, keys):
            row[name] = val
        rows.append(row)
    cols = list(groupvars) + [
        "length",
        "min",
        "max",
        "median",
        "mean",
        "iqr",
        "mad",
        "sd",
        "se",
        "ci",
    ]
    return pd.DataFrame(rows, columns=cols)


_FUN_DATA_ALIASES = {
    "mean_se": mean_se_,
    "mean_se_": mean_se_,
    "mean_sd": mean_sd,
    "mean_ci": mean_ci,
    "mean_range": mean_range,
    "median_iqr": median_iqr,
    "median_mad": median_mad,
    "median_q1q3": median_q1q3,
    "median_range": median_range,
    "median_hilow": median_hilow_,
    "median_hilow_": median_hilow_,
}


def add_summary(
    plot,
    fun: "str | callable" = "mean_se",
    error_plot: str = "pointrange",
    color: str = "black",
    fill: str = "white",
    size: float = 1.0,
    width: float | None = None,
    shape: int = 19,
    linetype: str = "solid",
    show_legend: bool = False,
    **kwargs,
):
    """
    Add a summary layer to an existing ``ggplot`` object.

    Parameters
    ----------
    plot : ggplot
        The plot to add the layer to.
    fun : str or callable, default ``"mean_se"``
        Either a name from the ggpubr ``fun.data`` family
        (``"mean_se"``, ``"mean_sd"``, ``"mean_ci"``,
        ``"median_iqr"``, ...) or a callable returning a
        dict with ``y``, ``ymin`` and ``ymax``.
    error_plot : str, default ``"pointrange"``
        Geom to use. One of ``"pointrange"``, ``"linerange"``,
        ``"crossbar"``, ``"errorbar"``, ``"upper_errorbar"``,
        ``"lower_errorbar"``, ``"upper_pointrange"``,
        ``"lower_pointrange"``.
    """
    from plotnine import stat_summary

    if isinstance(fun, str):
        if fun not in _FUN_DATA_ALIASES:
            raise ValueError(
                f"Unknown summary function {fun!r}; expected one "
                f"of {sorted(_FUN_DATA_ALIASES)}"
            )
        fun_data = _FUN_DATA_ALIASES[fun]
    else:
        fun_data = fun

    geom_map = {
        "pointrange": "pointrange",
        "linerange": "linerange",
        "crossbar": "crossbar",
        "errorbar": "errorbar",
        "upper_errorbar": "errorbar",
        "lower_errorbar": "errorbar",
        "upper_pointrange": "pointrange",
        "lower_pointrange": "pointrange",
    }
    if error_plot not in geom_map:
        raise ValueError(
            f"Unknown error_plot {error_plot!r}; expected one of "
            f"{sorted(geom_map)}"
        )

    layer_kwargs = dict(
        geom=geom_map[error_plot],
        fun_data=fun_data,
        color=color,
        fill=fill,
        size=size,
        shape=shape,
        linetype=linetype,
        show_legend=show_legend,
    )
    if width is not None:
        layer_kwargs["width"] = width
    layer_kwargs.update(kwargs)

    return plot + stat_summary(**layer_kwargs)
