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

    def __radd__(self, other: Any) -> Any:
        """
        Allow ``ggplot() + scale_x_facet(...)``.

        Stores this object on the plot so that compatible facets
        can consume it when initialising per-panel scales.
        """
        if not hasattr(other, "_scale_facets"):
            other._scale_facets = []
        other._scale_facets.append(self)
        return other

    def matches(self, layout_row: Any) -> bool:
        """
        Test whether a layout row matches this scale's selector.

        Parameters
        ----------
        layout_row : dict-like
            A row from the layout DataFrame (or a dict of facet
            variable values for a panel).

        Returns
        -------
        bool
            ``True`` if the panel should use this scale.
        """
        expr = self.expr
        if callable(expr):
            return bool(expr(layout_row))
        if isinstance(expr, str):
            # Evaluate the expression string against the
            # layout row values as local variables.
            try:
                return bool(eval(expr, {}, dict(layout_row)))  # noqa: S307
            except Exception:
                return False
        return False


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
