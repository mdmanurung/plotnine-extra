"""
Manual panel layout using a design string or matrix.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd
from plotnine._utils import join_keys, match
from plotnine.facets.facet import (
    add_missing_facets,
    combine_vars,
    eval_facet_vars,
    facet,
)
from plotnine.facets.strips import Strips, strip

if TYPE_CHECKING:
    from typing import Optional, Sequence, Union

    from matplotlib.axes import Axes
    from plotnine.iapi import layout_details


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
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
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

        # Normalize facets to a list
        if facets is None:
            self.vars: list[str] = []
        elif isinstance(facets, str):
            self.vars = [facets]
        else:
            self.vars = list(facets)

    def compute_layout(
        self,
        data: list[pd.DataFrame],
    ) -> pd.DataFrame:
        if self._design_matrix is None:
            msg = "facet_manual requires a 'design' argument"
            raise ValueError(msg)

        design = self._design_matrix

        # Extract unique panel labels from design, preserving order,
        # excluding '#' (empty cells)
        labels: list[str] = []
        for row in design:
            for cell in row:
                if cell != "#" and cell not in labels:
                    labels.append(cell)

        # Get facet variable combinations from data
        if self.vars:
            base = combine_vars(
                data, self.environment, self.vars, drop=self.drop
            )
        else:
            base = pd.DataFrame({"_dummy_": [1]})

        n_panels = min(len(labels), len(base))

        rows_list = []
        for i in range(n_panels):
            label = labels[i]
            # Find position of this label in the design matrix
            r_pos, c_pos = 1, 1
            for r_idx in range(design.shape[0]):
                for c_idx in range(design.shape[1]):
                    if design[r_idx, c_idx] == label:
                        r_pos = r_idx + 1
                        c_pos = c_idx + 1
                        break
                else:
                    continue
                break

            row_data: dict = {
                "PANEL": i + 1,
                "ROW": r_pos,
                "COL": c_pos,
                "SCALE_X": i + 1 if self.free["x"] else 1,
                "SCALE_Y": i + 1 if self.free["y"] else 1,
                "AXIS_X": True,
                "AXIS_Y": True,
            }
            # Add facet variable values
            if self.vars and i < len(base):
                for var in self.vars:
                    row_data[var] = base.iloc[i][var]

            rows_list.append(row_data)

        layout = pd.DataFrame(rows_list)
        layout["PANEL"] = pd.Categorical(
            layout["PANEL"],
            categories=range(1, n_panels + 1),
        )

        # Remove helper column if no facet vars
        if "_dummy_" in layout.columns:
            layout = layout.drop(columns=["_dummy_"])

        self.nrow = int(design.shape[0])
        self.ncol = int(design.shape[1])
        return layout

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        if not len(data):
            data["PANEL"] = pd.Categorical(
                [],
                categories=layout["PANEL"].cat.categories,
                ordered=True,
            )
            return data

        if not self.vars:
            # No facet variables: all data goes to panel 1
            data["PANEL"] = pd.Categorical(
                [1] * len(data),
                categories=layout["PANEL"].cat.categories,
                ordered=True,
            )
            return data

        facet_vals = eval_facet_vars(data, self.vars, self.environment)
        data, facet_vals = add_missing_facets(
            data, layout, self.vars, facet_vals
        )

        # Assign each data point to a panel
        if len(facet_vals) and len(facet_vals.columns):
            keys = join_keys(facet_vals, layout, self.vars)
            data["PANEL"] = match(keys["x"], keys["y"], start=1)
        else:
            data["PANEL"] = 1

        data["PANEL"] = pd.Categorical(
            data["PANEL"],
            categories=layout["PANEL"].cat.categories,
            ordered=True,
        )
        data.reset_index(drop=True, inplace=True)
        return data

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        if not self.vars:
            return Strips([])
        s = strip(self.vars, layout_info, self, ax, "top")
        return Strips([s])
