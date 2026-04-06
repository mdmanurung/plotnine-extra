"""
Secondary axis specification.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


class sec_axis:
    """
    Specify a secondary axis

    Parameters
    ----------
    trans : callable
        A function that transforms values from the primary scale
        to the secondary scale. Should be a monotonic function.
    name : str, optional
        The name (label) for the secondary axis.
    breaks : callable or array_like, optional
        Break points for the secondary axis.
    labels : callable or array_like, optional
        Labels for the break points.

    Notes
    -----
    This is a data specification class. Secondary axis rendering
    is not yet integrated into the plotnine pipeline — the axis
    will not be drawn on plots. This class is provided for API
    compatibility with ggplot2.
    """

    def __init__(
        self,
        trans: Callable[[FloatArrayLike], FloatArrayLike],
        name: Optional[str] = None,
        breaks: Optional[Callable | list] = None,
        labels: Optional[Callable | list] = None,
    ):
        self.trans = trans
        self.name = name
        self.breaks = breaks
        self.labels = labels

    def transform(self, x: FloatArrayLike) -> FloatArrayLike:
        """Apply the transformation to data values."""
        return self.trans(x)


class dup_axis(sec_axis):
    """
    Duplicate the primary axis

    Creates a secondary axis that is identical to the primary axis.

    Parameters
    ----------
    name : str, optional
        The name (label) for the secondary axis.
    breaks : callable or array_like, optional
        Break points for the secondary axis.
    labels : callable or array_like, optional
        Labels for the break points.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        breaks: Optional[Callable | list] = None,
        labels: Optional[Callable | list] = None,
    ):
        super().__init__(
            trans=lambda x: x,
            name=name,
            breaks=breaks,
            labels=labels,
        )
