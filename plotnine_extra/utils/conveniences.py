"""
Convenience utilities ported from ggh4x's ``conveniences.R``.

Provides helpers for distributing theme-element arguments,
weaving categorical factors, and building symmetric limits.
"""

from __future__ import annotations

import inspect
from itertools import product
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from plotnine.themes.elements import element_rect, element_text

if TYPE_CHECKING:
    from typing import Any, Callable


def distribute_args(
    *,
    fun: Callable[..., Any] = element_text,
    cull: bool = True,
    **kwargs: Any,
) -> list[Any]:
    """
    Distribute vectorised keyword arguments across calls.

    Each keyword argument should be a scalar or a sequence.
    The *i*-th element of every kwarg is forwarded to the
    *i*-th invocation of *fun*.  ``None`` values are silently
    dropped before calling *fun*.

    Parameters
    ----------
    fun : callable
        Constructor / factory to call (default `element_text`).
    cull : bool
        If ``True``, only pass keyword arguments whose names
        match a parameter of *fun*.
    **kwargs
        Keyword arguments whose values are scalars or lists.

    Returns
    -------
    list
        One result of *fun* per position.
    """
    if cull:
        sig = inspect.signature(fun)
        valid = set(sig.parameters.keys())
        has_var_kw = any(
            p.kind == inspect.Parameter.VAR_KEYWORD
            for p in sig.parameters.values()
        )
        if not has_var_kw:
            kwargs = {k: v for k, v in kwargs.items() if k in valid}

    # Drop keys with empty sequences
    kwargs = {k: v for k, v in kwargs.items() if _has_length(v)}

    if not kwargs:
        return [fun()]

    # Normalise every value to a list
    kwargs = {
        k: v if isinstance(v, (list, tuple)) else [v]
        for k, v in kwargs.items()
    }

    names = list(kwargs.keys())
    values = list(kwargs.values())
    n = max(len(v) for v in values)

    results: list[Any] = []
    for i in range(n):
        call_kwargs: dict[str, Any] = {}
        for name, vals in zip(names, values):
            if i < len(vals):
                val = vals[i]
            else:
                # Recycle: positions beyond the vector length
                # get nothing (mirroring R behaviour).
                continue
            if val is None or _is_na(val):
                continue
            call_kwargs[name] = val
        results.append(fun(**call_kwargs))
    return results


def elem_list_text(**kwargs: Any) -> list[Any]:
    """
    Convenience wrapper: ``distribute_args(fun=element_text)``.

    Parameters
    ----------
    **kwargs
        Forwarded to :func:`distribute_args`.

    Returns
    -------
    list
        A list of :class:`element_text` instances.
    """
    return distribute_args(fun=element_text, **kwargs)


def elem_list_rect(**kwargs: Any) -> list[Any]:
    """
    Convenience wrapper: ``distribute_args(fun=element_rect)``.

    Parameters
    ----------
    **kwargs
        Forwarded to :func:`distribute_args`.

    Returns
    -------
    list
        A list of :class:`element_rect` instances.
    """
    return distribute_args(fun=element_rect, **kwargs)


def weave_factors(
    *args: Any,
    drop: bool = True,
    sep: str = ".",
    replace_na: bool = True,
) -> pd.Categorical:
    """
    Combine categorical / array-like columns into one factor.

    Levels are ordered lexicographically over the input
    factors' levels (Cartesian product, then filtered to
    observed combinations when *drop* is ``True``).

    Parameters
    ----------
    *args : array-like
        Series, arrays, or lists to combine.
    drop : bool
        Drop unobserved level combinations.
    sep : str
        Separator placed between level components.
    replace_na : bool
        If ``True``, replace ``NaN`` / ``None`` with the
        string ``"NA"`` before combining.

    Returns
    -------
    pd.Categorical
        A single categorical with combined levels.
    """
    if not args:
        return pd.Categorical([])

    series_list: list[pd.Categorical] = []
    for a in args:
        s = pd.Series(a)
        if replace_na:
            s = s.fillna("NA")
        cat = pd.Categorical(s)
        series_list.append(cat)

    lengths = [len(c) for c in series_list]
    if len(set(lengths)) != 1:
        msg = f"All arguments must have the same length, got {lengths}"
        raise ValueError(msg)

    n = lengths[0]

    # Build all possible levels (Cartesian product)
    all_levels = [list(c.categories) for c in series_list]
    all_combos = [
        sep.join(str(x) for x in combo) for combo in product(*all_levels)
    ]

    # Build observed values
    codes = [
        sep.join(str(series_list[j][i]) for j in range(len(args)))
        for i in range(n)
    ]

    if drop:
        observed = set(codes)
        categories = [c for c in all_combos if c in observed]
    else:
        categories = all_combos

    return pd.Categorical(codes, categories=categories)


def center_limits(
    around: float = 0,
) -> Callable[[tuple[float, float]], tuple[float, float]]:
    """
    Factory that returns a limits-centering function.

    The returned callable accepts a ``(min, max)`` tuple and
    produces symmetric limits centred on *around*.

    Parameters
    ----------
    around : float
        Centre point for the limits.

    Returns
    -------
    callable
        A function ``(min, max) -> (new_min, new_max)``.

    Examples
    --------
    >>> center_limits(0)((3, 8))
    (-8, 8)
    """

    def _center(
        limits: tuple[float, float],
    ) -> tuple[float, float]:
        max_dev = max(abs(limits[0] - around), abs(limits[1] - around))
        return (around - max_dev, around + max_dev)

    return _center


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _is_na(x: Any) -> bool:
    """Return ``True`` for NA-like scalars."""
    if x is None:
        return True
    try:
        return bool(np.isnan(x))
    except (TypeError, ValueError):
        return False


def _has_length(v: Any) -> bool:
    """Return ``True`` when *v* is non-empty."""
    if isinstance(v, (list, tuple)):
        return len(v) > 0
    return True
