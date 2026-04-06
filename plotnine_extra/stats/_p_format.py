"""
P-value formatting utilities.

Provides functions for formatting p-values and converting
them to significance symbols.
"""

from __future__ import annotations

import numpy as np

# Default significance cutoffs matching ggpubr conventions
DEFAULT_CUTPOINTS = (0.0001, 0.001, 0.01, 0.05, 1.0)
DEFAULT_SYMBOLS = ("****", "***", "**", "*", "ns")


def format_p_value(
    p: float,
    digits: int = 3,
    leading_zero: bool = True,
) -> str:
    """
    Format a p-value for display.

    Parameters
    ----------
    p : float
        The p-value to format.
    digits : int
        Number of significant digits.
    leading_zero : bool
        Whether to include the leading zero.

    Returns
    -------
    str
        Formatted p-value string.
    """
    if np.isnan(p):
        return "NA"

    threshold = 10 ** (-digits)
    if p < threshold:
        result = f"p < {threshold:.{digits}f}"
    else:
        result = f"p = {p:.{digits}f}"

    if not leading_zero:
        result = result.replace("0.", ".", 1)

    return result


def p_to_signif(
    p: float,
    cutpoints: tuple[float, ...] = DEFAULT_CUTPOINTS,
    symbols: tuple[str, ...] = DEFAULT_SYMBOLS,
) -> str:
    """
    Convert a p-value to a significance symbol.

    Parameters
    ----------
    p : float
        The p-value to convert.
    cutpoints : tuple of float
        Upper bounds for each significance level.
    symbols : tuple of str
        Symbols corresponding to each significance level.

    Returns
    -------
    str
        Significance symbol.
    """
    if np.isnan(p):
        return "NA"

    for cutpoint, symbol in zip(cutpoints, symbols):
        if p <= cutpoint:
            return symbol

    return symbols[-1]
