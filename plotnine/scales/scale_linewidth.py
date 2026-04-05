"""
Linewidth scales.
"""

from __future__ import annotations

from dataclasses import KW_ONLY, InitVar, dataclass
from typing import Literal
from warnings import warn

import numpy as np

from .._utils.registry import alias
from ..exceptions import PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_discrete import scale_discrete


@dataclass
class scale_linewidth_continuous(
    scale_continuous[Literal["legend"] | None],
):
    """
    Continuous linewidth scale

    Maps continuous data to line widths.
    """

    _aesthetics = ["linewidth"]
    range: InitVar[tuple[float, float]] = (0.25, 3)
    """
    Range ([Minimum, Maximum]) of output linewidth values.
    """
    _: KW_ONLY
    guide: Literal["legend"] | None = "legend"

    def __post_init__(self, range):
        from mizani.palettes import rescale_pal

        super().__post_init__()
        self.palette = rescale_pal(range)


@dataclass
class scale_linewidth_ordinal(scale_discrete):
    """
    Ordinal linewidth scale
    """

    _aesthetics = ["linewidth"]
    range: InitVar[tuple[float, float]] = (0.25, 3)
    """
    Range ([Minimum, Maximum]) of output linewidth values.
    """

    def __post_init__(self, range):
        super().__post_init__()

        def palette(n: int):
            return np.linspace(range[0], range[1], n)

        self.palette = palette


@dataclass
class scale_linewidth_discrete(scale_linewidth_ordinal):
    """
    Discrete linewidth scale
    """

    _aesthetics = ["linewidth"]

    def __post_init__(self, range):
        warn(
            "Using linewidth for a discrete variable is not advised.",
            PlotnineWarning,
        )
        super().__post_init__(range)


@alias
class scale_linewidth(scale_linewidth_continuous):
    pass
