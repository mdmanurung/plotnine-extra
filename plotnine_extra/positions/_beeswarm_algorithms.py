"""
Beeswarm offset algorithms.

Pure-Python implementations of the beeswarm and quasirandom
jittering algorithms, ported from the R packages ``beeswarm``
and ``vipor``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .._common import resolve_random_state

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from plotnine.typing import RandomStateLike


# -------------------------------------------------------------------
# Van der Corput sequence (used by quasirandom)
# -------------------------------------------------------------------


def van_der_corput(n: int, base: int = 2) -> NDArray[np.float64]:
    """
    Generate the first *n* elements of the van der Corput
    low-discrepancy sequence in the given *base*.

    Values lie in (0, 1) and are well-distributed.
    """
    seq = np.zeros(n, dtype=np.float64)
    for i in range(n):
        q = 0.0
        denom = 1.0
        m = i + 1
        while m > 0:
            denom *= base
            q += (m % base) / denom
            m //= base
        seq[i] = q
    return seq


# -------------------------------------------------------------------
# Quasirandom offset (density-aware jitter)
# -------------------------------------------------------------------


def _kde_density(
    values: NDArray[np.float64],
    bandwidth: float = 0.5,
    nbins: int | None = None,
) -> NDArray[np.float64]:
    """
    Estimate density at each data point using a Gaussian KDE.

    Returns an array of density values the same length as *values*.

    The KDE is evaluated on an evenly spaced grid of *nbins* points and then
    interpolated back to the data. Evaluating it at every observation instead
    would build and multiply an n-by-n kernel matrix, which is quadratic in
    both time and peak memory; on a grid the cost is O(n * nbins).
    """
    from scipy.stats import gaussian_kde

    n = len(values)
    if n < 2:
        return np.ones_like(values)

    try:
        kde = gaussian_kde(values, bw_method=bandwidth)
    except np.linalg.LinAlgError:
        return np.ones_like(values)

    # How many points to evaluate on. Growing like sqrt(n) keeps the cost
    # near-linear while staying dense enough to resolve the density.
    n_grid = int(min(n, max(64, min(1024, np.sqrt(n) * 8))))
    if n_grid >= n:
        density = kde(values)
    else:
        # The KDE has support outside the data range, so extend the grid past
        # it; otherwise the interpolation would clamp at the edges and
        # flatten the tails.
        pad = 3 * float(kde.scotts_factor()) * float(np.std(values))
        lo = float(values.min()) - pad
        hi = float(values.max()) + pad
        grid = np.linspace(lo, hi, n_grid)
        density = np.interp(values, grid, kde(grid))

    # Normalize so max == 1
    dmax = density.max()
    if dmax > 0:
        density /= dmax
    return density


def offset_quasirandom(
    values: NDArray[np.float64],
    *,
    method: str = "quasirandom",
    width: float = 0.4,
    bandwidth: float = 0.5,
    nbins: int | None = None,
    varwidth: bool = False,
    group_count: int | None = None,
    total_count: int | None = None,
    random_state: RandomStateLike | None = None,
) -> NDArray[np.float64]:
    """
    Compute quasi-random x-offsets for a single group.

    Parameters
    ----------
    values
        The data-axis values (e.g. y in a vertical plot).
    method
        ``"quasirandom"`` (van der Corput) or ``"pseudorandom"``.
    width
        Maximum spread of the jitter.
    bandwidth
        Bandwidth adjustment for KDE.
    nbins
        Number of bins for the density estimate. *None* picks a grid from
        the group size.
    varwidth
        If *True*, scale width by relative group size.
    group_count
        Size of this group (for *varwidth*).
    total_count
        Total number of observations (for *varwidth*).

    Returns
    -------
    offsets
        Array of horizontal offsets, centred around 0.
    """
    n = len(values)
    if n == 0:
        return np.array([], dtype=np.float64)
    if n == 1:
        return np.zeros(1, dtype=np.float64)

    # Density at each point
    density = _kde_density(values, bandwidth=bandwidth, nbins=nbins)

    # Base jitter values in (-0.5, 0.5)
    if method == "pseudorandom":
        rng = resolve_random_state(random_state)
        jitter = rng.uniform(-0.5, 0.5, size=n)
    else:
        # quasirandom (default): van der Corput sequence
        vdc = van_der_corput(n)
        jitter = vdc - 0.5  # centre around 0

    # Scale by density so dense regions are wider
    offsets = jitter * density

    # Scale to desired width
    if varwidth and group_count and total_count and total_count > 0:
        scale = group_count / total_count
    else:
        scale = 1.0

    offsets *= width * scale
    return offsets


# -------------------------------------------------------------------
# Beeswarm offset (avoid-overlap placement)
# -------------------------------------------------------------------


def offset_beeswarm(
    values: NDArray[np.float64],
    *,
    method: str = "swarm",
    cex: float = 1.0,
    side: int = 0,
    priority: str = "ascending",
    point_size: float | None = None,
    random_state: RandomStateLike | None = None,
) -> NDArray[np.float64]:
    """
    Compute beeswarm x-offsets for a single group.

    Parameters
    ----------
    values
        Data-axis values (e.g. y-coordinates for a vertical plot).
    method
        ``"swarm"`` (default), ``"compactswarm"``, ``"center"``,
        ``"square"``, or ``"hex"``.
    cex
        Scaling factor for point spacing (higher = more spread).
    side
        ``0``: both sides, ``1``: right/up only,
        ``-1``: left/down only.
    priority
        Order in which points are placed: ``"ascending"`` (default),
        ``"descending"``, ``"density"``, ``"random"``, ``"none"``.
    point_size
        Physical size of a point in data units.  If *None* an
        estimate is derived from the data range.
    random_state
        Seed or generator for the RNG used when ``priority="random"``.  *None*
        means non-reproducible output.

    Returns
    -------
    offsets
        Horizontal offsets centred around 0.
    """
    n = len(values)
    if n == 0:
        return np.array([], dtype=np.float64)
    if n == 1:
        return np.zeros(1, dtype=np.float64)

    # Estimate point size in data-axis units
    if point_size is None:
        val_range = values.max() - values.min()
        point_size = 1.0 if val_range == 0 else val_range / max(n, 10)
    point_size *= cex

    if method in ("swarm", "compactswarm"):
        return _swarm(values, point_size, method, priority, side, random_state)
    if method in ("center", "centre"):
        return _grid(values, point_size, side, mode="center")
    if method == "hex":
        return _grid(values, point_size, side, mode="hex")
    # default: "square"
    return _grid(values, point_size, side, mode="square")


def _order_indices(
    values: NDArray[np.float64],
    priority: str,
    random_state: RandomStateLike | None = None,
) -> NDArray[np.intp]:
    """Return indices in the desired placement order."""
    if priority == "descending":
        return np.argsort(-values)
    if priority == "random":
        idx = np.arange(len(values))
        resolve_random_state(random_state).shuffle(idx)
        return idx
    if priority == "density":
        from scipy.stats import gaussian_kde

        try:
            kde = gaussian_kde(values)
            density = kde(values)
        except np.linalg.LinAlgError:
            density = np.ones_like(values)
        return np.argsort(-density)
    if priority == "none":
        return np.arange(len(values))
    # ascending (default)
    return np.argsort(values)


def _swarm(
    values: NDArray[np.float64],
    point_size: float,
    method: str,
    priority: str,
    side: int,
    random_state: RandomStateLike | None = None,
) -> NDArray[np.float64]:
    """
    Core swarm algorithm: place points one at a time, shifting
    sideways by the minimum amount needed to avoid overlap.
    """
    n = len(values)
    offsets = np.zeros(n, dtype=np.float64)
    order = _order_indices(values, priority, random_state)

    # Preallocate the "already placed" buffers and track a write cursor.
    # np.append() reallocates and copies both arrays on every one of the n
    # iterations, so the loop is quadratic in allocation traffic on top of
    # its quadratic scan.
    placed_y = np.empty(n, dtype=np.float64)
    placed_x = np.empty(n, dtype=np.float64)

    for n_placed, idx in enumerate(order):
        y_i = values[idx]

        if n_placed == 0:
            offsets[idx] = 0.0
        else:
            # Only the entries written so far are meaningful, so view the
            # buffers up to the cursor rather than the whole allocation.
            py = placed_y[:n_placed]
            # Find all previously placed points within point_size
            # distance on the data axis
            dy = np.abs(py - y_i)
            neighbours = dy < point_size

            if not neighbours.any():
                offsets[idx] = 0.0
            else:
                # For each overlapping neighbour, compute the
                # minimum horizontal distance needed
                neighbour_x = placed_x[:n_placed][neighbours]
                neighbour_dy = dy[neighbours]

                # From the overlap circle: dx² + dy² >= d²
                # => dx >= sqrt(d² - dy²)
                min_dx = np.sqrt(
                    np.maximum(point_size**2 - neighbour_dy**2, 0)
                )

                if method == "compactswarm":
                    x_i = _compact_place(neighbour_x, min_dx, side)
                else:
                    x_i = _swarm_place(neighbour_x, min_dx, side)
                offsets[idx] = x_i

        placed_y[n_placed] = y_i
        placed_x[n_placed] = offsets[idx]

    return offsets


def _candidates(
    neighbour_x: NDArray[np.float64],
    min_dx: NDArray[np.float64],
    side: int,
) -> NDArray[np.float64]:
    """
    Candidate x-positions: each neighbour's two touching positions, plus 0.
    """
    cands = np.empty(2 * len(neighbour_x) + 1, dtype=np.float64)
    cands[:-1:2] = neighbour_x + min_dx
    cands[1:-1:2] = neighbour_x - min_dx
    cands[-1] = 0.0

    # Filter by the side constraint.
    if side == 1:
        cands = cands[cands >= -1e-10]
    elif side == -1:
        cands = cands[cands <= 1e-10]

    if not len(cands):
        cands = np.array([0.0])
    return cands


def _outer_edge(
    neighbour_x: NDArray[np.float64],
    min_dx: NDArray[np.float64],
    side: int,
) -> float:
    """Where to place a point when no candidate position is clear."""
    if side >= 0:
        return float(np.max(neighbour_x + min_dx))
    return float(np.min(neighbour_x - min_dx))


def _clear_mask(
    cands: NDArray[np.float64],
    neighbour_x: NDArray[np.float64],
    min_dx: NDArray[np.float64],
) -> NDArray[np.bool_]:
    """
    For each candidate, whether it clears every neighbour.

    All candidates are tested in one (candidates x neighbours) comparison.
    The loop this replaces made that same comparison once per candidate, in
    its own NumPy call, so its cost was quadratic in the neighbour count.
    """
    clear = np.abs(neighbour_x[None, :] - cands[:, None]) >= (
        min_dx[None, :] - 1e-10
    )
    return clear.all(axis=1)


def _swarm_place(
    neighbour_x: NDArray[np.float64],
    min_dx: NDArray[np.float64],
    side: int,
) -> float:
    """
    Find the closest valid x-position to 0 that does not overlap
    with any neighbour.
    """
    cands = _candidates(neighbour_x, min_dx, side)
    good = cands[_clear_mask(cands, neighbour_x, min_dx)]
    if len(good):
        # Of the positions that clear, take the one nearest 0.
        return float(good[np.argmin(np.abs(good))])

    # Fallback: place at outer edge
    return _outer_edge(neighbour_x, min_dx, side)


def _compact_place(
    neighbour_x: NDArray[np.float64],
    min_dx: NDArray[np.float64],
    side: int,
) -> float:
    """
    Compact placement: find the position closest to 0 that
    does not overlap, searching outward from centre.
    """
    cands = _candidates(neighbour_x, min_dx, side)
    # Search outward from the centre. A stable sort keeps the candidate
    # order within a distance band, matching the original sort.
    cands = cands[np.argsort(np.abs(cands), kind="stable")]

    ok = _clear_mask(cands, neighbour_x, min_dx)
    if ok.any():
        return float(cands[np.argmax(ok)])

    # Fallback
    return _outer_edge(neighbour_x, min_dx, side)


def _grid(
    values: NDArray[np.float64],
    point_size: float,
    side: int,
    mode: str = "square",
) -> NDArray[np.float64]:
    """
    Place points on a regular grid (square, hex, or centred).
    """
    n = len(values)
    if n == 0:
        return np.array([], dtype=np.float64)

    # Bin the values
    val_min, val_max = values.min(), values.max()
    val_range = val_max - val_min

    if val_range == 0:
        # All same value: arrange in a line
        offsets = np.arange(n, dtype=np.float64) - (n - 1) / 2.0
        offsets *= point_size
        return _apply_side(offsets, side)

    n_bins = max(1, int(np.ceil(val_range / point_size)))
    bin_edges = np.linspace(val_min, val_max + 1e-10, n_bins + 1)
    bin_idx = np.digitize(values, bin_edges) - 1
    bin_idx = np.clip(bin_idx, 0, n_bins - 1)

    offsets = np.zeros(n, dtype=np.float64)

    for b in range(n_bins):
        mask = bin_idx == b
        count = mask.sum()
        if count == 0:
            continue

        positions = np.arange(count, dtype=np.float64)
        positions -= (count - 1) / 2.0  # centre around 0
        positions *= point_size

        if mode == "hex" and b % 2 == 1:
            positions += point_size * 0.5

        if mode == "center":
            # Re-centre so the swarm is symmetric
            positions -= positions.mean()

        offsets[mask] = positions

    return _apply_side(offsets, side)


def _apply_side(
    offsets: NDArray[np.float64], side: int
) -> NDArray[np.float64]:
    """Shift offsets to one side if requested."""
    if side == 1:
        offsets = np.abs(offsets)
    elif side == -1:
        offsets = -np.abs(offsets)
    return offsets


# -------------------------------------------------------------------
# Corral helpers
# -------------------------------------------------------------------


def corral_points(
    offsets: NDArray[np.float64],
    method: str = "none",
    width: float = 0.9,
    random_state: RandomStateLike | None = None,
) -> NDArray[np.float64]:
    """
    Handle runaway points that extend beyond the corral boundary.

    Parameters
    ----------
    offsets
        Horizontal offsets.
    method
        ``"none"``: no correction,
        ``"gutter"``: clamp to boundary,
        ``"wrap"``: periodic wrap,
        ``"random"``: random within boundary,
        ``"omit"``: set to NaN.
    width
        Half-width of the corral region.
    random_state
        Seed or generator for the RNG used when ``method="random"``.  *None*
        means non-reproducible output.
    """
    if method == "none":
        return offsets

    half = width / 2.0
    out_of_bounds = np.abs(offsets) > half

    if not out_of_bounds.any():
        return offsets

    offsets = offsets.copy()

    if method == "gutter":
        offsets = np.clip(offsets, -half, half)
    elif method == "wrap":
        offsets[out_of_bounds] = (
            (offsets[out_of_bounds] + half) % width
        ) - half
    elif method == "random":
        rng = resolve_random_state(random_state)
        n_out = out_of_bounds.sum()
        offsets[out_of_bounds] = rng.uniform(-half, half, size=n_out)
    elif method == "omit":
        offsets[out_of_bounds] = np.nan

    return offsets
