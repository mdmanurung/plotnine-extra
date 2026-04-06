"""
Per-panel scale adjustment functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from typing import Any


class ScaleFacet:
    """
    Apply a scale modification to specific facet panels.

    Parameters
    ----------
    axis : str
        Which axis this scale targets ("x" or "y").
    expr : str or callable
        Expression or predicate identifying which panels
        to apply the scale to.
    *args : Any
        Positional arguments forwarded to the scale.
    **kwargs : Any
        Keyword arguments forwarded to the scale.
    """

    def __init__(
        self,
        axis: Literal["x", "y"],
        expr: Any,
        *args: Any,
        **kwargs: Any,
    ):
        self.axis = axis
        self.expr = expr
        self.args = args
        self.kwargs = kwargs

    # TODO: Integrate with facet layout to apply the scale
    # only to panels matching the expression.


def scale_x_facet(
    expr: Any,
    *args: Any,
    **kwargs: Any,
) -> ScaleFacet:
    """
    Apply x-axis scale to specific facet panels.

    Parameters
    ----------
    expr : str or callable
        Expression identifying which panels to target.
    *args : Any
        Forwarded to the underlying scale constructor.
    **kwargs : Any
        Forwarded to the underlying scale constructor.

    Returns
    -------
    ScaleFacet
        Object that can be added to a ggplot.
    """
    return ScaleFacet("x", expr, *args, **kwargs)


def scale_y_facet(
    expr: Any,
    *args: Any,
    **kwargs: Any,
) -> ScaleFacet:
    """
    Apply y-axis scale to specific facet panels.

    Parameters
    ----------
    expr : str or callable
        Expression identifying which panels to target.
    *args : Any
        Forwarded to the underlying scale constructor.
    **kwargs : Any
        Forwarded to the underlying scale constructor.

    Returns
    -------
    ScaleFacet
        Object that can be added to a ggplot.
    """
    return ScaleFacet("y", expr, *args, **kwargs)
