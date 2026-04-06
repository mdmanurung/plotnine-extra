"""
Label positioning and formatting utilities.

Provides functions for computing label positions from
normalized plot coordinates and formatting statistical
test labels.
"""

from __future__ import annotations

from typing import Any


def compute_label_position(
    data_min: float,
    data_max: float,
    npc: float | str,
) -> float:
    """
    Convert normalized plot coordinates to data coordinates.

    Parameters
    ----------
    data_min : float
        Minimum of the data range.
    data_max : float
        Maximum of the data range.
    npc : float or str
        Normalized position. Float in [0, 1] or one of
        ``"left"``, ``"center"``, ``"right"``, ``"top"``,
        ``"middle"``, ``"bottom"``.

    Returns
    -------
    float
        Position in data coordinates.
    """
    npc_map = {
        "left": 0.05,
        "center": 0.5,
        "middle": 0.5,
        "right": 0.95,
        "top": 0.95,
        "bottom": 0.05,
    }
    if isinstance(npc, str):
        npc = npc_map.get(npc, 0.5)

    data_range = data_max - data_min
    return data_min + npc * data_range


def format_stat_label(
    template: str,
    **values: Any,
) -> str:
    """
    Format a statistical test label using a template.

    Parameters
    ----------
    template : str
        Template string with ``{key}`` placeholders.
    **values
        Values to substitute into the template.

    Returns
    -------
    str
        Formatted label string.
    """
    return template.format(**values)
