"""
Manual panel layout using a design string or matrix.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
from plotnine.facets.facet import facet

if TYPE_CHECKING:
    from typing import Optional, Sequence, Union


def _parse_design(design: str) -> np.ndarray:
    """
    Parse a design string into a 2-D array of panel labels.

    Parameters
    ----------
    design : str
        Multi-line string where each character is a panel
        label. Use ``#`` for empty cells.

    Returns
    -------
    numpy.ndarray
        2-D character array of panel identifiers.

    Examples
    --------
    >>> _parse_design("AB\\nCD")
    array([['A', 'B'],
           ['C', 'D']], dtype='<U1')
    """
    rows = [list(line) for line in design.strip().splitlines()]
    return np.array(rows)


class facet_manual(facet):
    """
    Manually specify panel layout via a design matrix.

    Allows arbitrary placement of facet panels using a text
    design string or a 2-D array. Use ``#`` to denote empty
    cells in the layout.

    Parameters
    ----------
    facets : str or list of str, optional
        Variables to facet by. Each unique combination is
        assigned a panel label from the design.
    design : str or array-like, optional
        Layout specification. A multi-line string like
        ``"AB\\n#C"`` or a 2-D list / numpy array.
    scales : str
        Whether scales are fixed ("fixed"), free ("free",
        "free_x", "free_y").
    shrink : bool
        Whether to shrink scales to fit output of statistics.
    labeller : str
        Labelling function for strip text.
    as_table : bool
        If True, facets are laid out like a table.
    drop : bool
        Whether to drop unused factor levels.
    respect : bool
        If True, panel sizes respect the aspect ratio.
    """

    def __init__(
        self,
        facets: Optional[str | Sequence[str]] = None,
        *,
        design: Optional[Union[str, list, np.ndarray]] = None,
        scales: Literal[
            "fixed", "free", "free_x", "free_y"
        ] = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
        respect: bool = False,
    ):
        super().__init__(
            scales=scales,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
        )
        self.facets = facets
        self.design = design
        self.respect = respect
        self._design_matrix: Optional[np.ndarray] = None

        if design is not None:
            if isinstance(design, str):
                self._design_matrix = _parse_design(design)
            else:
                self._design_matrix = np.asarray(design)

    # TODO: Override compute_layout to place panels according
    # to the design matrix. Map panel labels from the design
    # to facet variable combinations.
