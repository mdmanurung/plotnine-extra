"""
Public p-value formatting helpers, ported from ggpubr.

These wrap the internal :mod:`plotnine_extra.stats._p_format`
helpers and add a small registry of "format styles" so users
can switch between display conventions in one place.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ._p_format import (
    DEFAULT_CUTPOINTS,
    DEFAULT_SYMBOLS,
    p_to_signif,
)
from ._p_format import (
    format_p_value as _format_p_value_internal,
)

if TYPE_CHECKING:
    from typing import Sequence

__all__ = (
    "format_p_value",
    "create_p_label",
    "get_p_format_style",
    "list_p_format_styles",
    "ggadjust_pvalue",
)


# Each style is a callable that takes a single p-value and
# returns the formatted display string.
def _style_default(p, digits=3):
    return _format_p_value_internal(p, digits=digits)


def _style_scientific(p, digits=2):
    if np.isnan(p):
        return "NA"
    return f"p = {p:.{digits}e}"


def _style_exact(p, digits=4):
    if np.isnan(p):
        return "NA"
    return f"{p:.{digits}f}"


def _style_signif(p, digits=3):
    return p_to_signif(p)


def _style_p_signif(p, digits=3):
    if np.isnan(p):
        return "NA"
    return f"{_format_p_value_internal(p, digits=digits)} {p_to_signif(p)}"


_P_FORMAT_STYLES = {
    "default": _style_default,
    "scientific": _style_scientific,
    "exact": _style_exact,
    "signif": _style_signif,
    "p.signif": _style_signif,
    "p.format": _style_default,
    "p.format.signif": _style_p_signif,
}


def list_p_format_styles() -> list[str]:
    """Return all known p-value format style names."""
    return sorted(_P_FORMAT_STYLES)


def get_p_format_style(style: str = "default"):
    """
    Return the formatting callable registered for ``style``.
    """
    if style not in _P_FORMAT_STYLES:
        raise ValueError(
            f"Unknown p-value format style {style!r}; expected "
            f"one of {list_p_format_styles()}"
        )
    return _P_FORMAT_STYLES[style]


def format_p_value(
    p: float,
    digits: int = 3,
    style: str = "default",
    accuracy: float | None = None,
    leading_zero: bool = True,
) -> str:
    """
    Format a p-value for display.

    Parameters
    ----------
    p : float
        P-value to format.
    digits : int, default 3
        Number of decimal digits (default style only).
    style : str, default ``"default"``
        Name of the format style. See
        :func:`list_p_format_styles`.
    accuracy : float, optional
        If provided, p-values smaller than this threshold are
        rendered as ``"p < <accuracy>"``.
    leading_zero : bool, default True
        Whether to keep the leading ``0.``.
    """
    if accuracy is not None and not np.isnan(p) and p < accuracy:
        result = f"p < {accuracy:g}"
        if not leading_zero:
            result = result.replace("0.", ".", 1)
        return result
    fn = get_p_format_style(style)
    try:
        result = fn(p, digits=digits)
    except TypeError:
        result = fn(p)
    if not leading_zero:
        result = result.replace("0.", ".", 1)
    return result


def create_p_label(
    p,
    cutpoints: "Sequence[float] | None" = None,
    symbols: "Sequence[str] | None" = None,
):
    """
    Convert one or more p-values to significance symbols.

    Parameters
    ----------
    p : float or array-like
        P-values.
    cutpoints : sequence of float, optional
        Upper bounds for each significance level. Defaults to
        ``(0.0001, 0.001, 0.01, 0.05, 1.0)``.
    symbols : sequence of str, optional
        Symbols matching ``cutpoints``. Defaults to
        ``("****", "***", "**", "*", "ns")``.

    Returns
    -------
    str or list of str
        Significance label(s).
    """
    cps = tuple(cutpoints) if cutpoints is not None else DEFAULT_CUTPOINTS
    syms = tuple(symbols) if symbols is not None else DEFAULT_SYMBOLS
    if np.ndim(p) == 0:
        return p_to_signif(float(p), cps, syms)
    return [p_to_signif(float(v), cps, syms) for v in p]


def ggadjust_pvalue(
    plot,
    p_adjust_method: str = "holm",
    label: str | None = None,
):
    """
    Re-adjust p-values displayed on an existing plot.

    Walks ``plot.layers`` and updates the ``p_adjust_method``
    parameter of any ``stat_pwc`` / ``stat_compare_means`` /
    ``stat_pvalue_manual`` layer in place. The plot is then
    returned for chaining.

    Parameters
    ----------
    plot : ggplot
        The plot to mutate.
    p_adjust_method : str, default ``"holm"``
        New adjustment method. One of ``"bonferroni"``,
        ``"holm"``, ``"hochberg"``, ``"hommel"``, ``"BH"``,
        ``"BY"``, ``"fdr"``, ``"none"``.
    label : str, optional
        New label format (e.g. ``"p.adj.signif"``).
    """
    from .stat_compare_means import stat_compare_means
    from .stat_pvalue_manual import stat_pvalue_manual
    from .stat_pwc import stat_pwc

    targets = (stat_pwc, stat_compare_means, stat_pvalue_manual)
    for layer in plot.layers:
        st = getattr(layer, "stat", None)
        if isinstance(st, targets):
            params = getattr(st, "params", None)
            if params is not None:
                if "p_adjust_method" in params:
                    params["p_adjust_method"] = p_adjust_method
                if label is not None and "label" in params:
                    params["label"] = label
    return plot
