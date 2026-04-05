"""
Base class for binned scales.

Binned scales discretize continuous data into bins before mapping
to aesthetic values.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence, cast

import numpy as np
import pandas as pd
from mizani.bounds import rescale

from .._utils import match
from ._runtime_typing import (
    GuideTypeT,
)
from .scale_continuous import scale_continuous

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


@dataclass(kw_only=True)
class scale_binned(
    scale_continuous[GuideTypeT],
):
    """
    Base class for all binned scales

    Binned scales discretize continuous data into bins, then map
    each bin to a discrete aesthetic value.
    """

    n_breaks: int = 5
    """
    Number of bin boundaries (breaks). The number of bins
    will be `n_breaks - 1`.
    """

    nice_breaks: bool = True
    """
    If `True`{.py}, the breaks are adjusted to be "nice" numbers.
    """

    def map(
        self,
        x: FloatArrayLike,
        limits: Optional[tuple[float, float]] = None,
    ) -> FloatArrayLike:
        if limits is None:
            limits = self.final_limits

        breaks = self.get_breaks(limits)

        if len(breaks) == 0:
            return super().map(x, limits)

        # Bin the continuous values
        breaks = sorted(breaks)
        n_bins = len(breaks) - 1

        if n_bins <= 0:
            return super().map(x, limits)

        # Assign each value to a bin (0-indexed)
        bin_idx = np.digitize(np.asarray(x), breaks) - 1
        # Clamp to valid range
        bin_idx = np.clip(bin_idx, 0, n_bins - 1)

        # Map bin midpoints through the palette
        midpoints = np.array(
            [(breaks[i] + breaks[i + 1]) / 2 for i in range(n_bins)]
        )
        rescaled = rescale(midpoints, _from=limits)
        na_value = cast("float", self.na_value)

        uniq_rescaled = np.unique(rescaled)
        pal = np.asarray(self.palette(uniq_rescaled))
        mapped_midpoints = pal[match(rescaled, uniq_rescaled)]

        # Look up the mapped value for each bin
        result = np.asarray(mapped_midpoints)[bin_idx]

        # Handle NaN in input
        nan_mask = pd.isna(x)
        if np.any(nan_mask):
            if result.dtype.kind == "U":
                result = np.where(nan_mask, str(na_value), result)
            else:
                result = result.astype(float)
                result[nan_mask] = na_value

        return result

    def get_breaks(
        self, limits: Optional[tuple[float, float]] = None
    ) -> Sequence[float]:
        if limits is None:
            limits = self.final_limits

        if self.is_empty() or self.breaks is False or self.breaks is None:
            return []

        if self.breaks is True:
            from mizani.breaks import breaks_extended

            breaks = breaks_extended(n=self.n_breaks)(self.inverse(limits))
        elif callable(self.breaks):
            breaks = self.breaks(self.inverse(limits))
        else:
            breaks = self.breaks

        breaks = self.transform(breaks)
        return breaks

    def default_expansion(self, mult=0, add=0.5, expand=True):
        """
        Default expansion for binned scales is slightly different
        from continuous scales.
        """
        return super().default_expansion(mult=mult, add=add, expand=expand)
