"""
Shared helpers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from plotnine.typing import RandomStateLike


def resolve_random_state(
    random_state: RandomStateLike | None,
) -> np.random.RandomState | np.random.Generator:
    """
    Turn a seed, a generator, or *None* into a usable random generator.

    Mirrors plotnine's own seed handling so a seeded plotnine-extra position
    and a seeded plotnine position (e.g. ``position_jitter``) draw from the
    same family:

    - an integer becomes a seeded ``RandomState``, so the result is
      reproducible;
    - an existing ``RandomState``/``Generator`` is passed through unchanged;
    - ``None`` yields a freshly seeded generator, i.e. a different layout on
      every draw.

    plotnine keeps its own version of the first rule in
    ``plotnine._utils.normalise_random_state``, which is private. It is two
    lines, so it is inlined here rather than imported -- see
    ``UPSTREAM_SYNC.md``: prefer plotnine's public API, since every
    underscore-prefixed name is a future sync break.
    """
    if random_state is None:
        return np.random.RandomState()
    if isinstance(random_state, int):
        return np.random.RandomState(random_state)
    return random_state
