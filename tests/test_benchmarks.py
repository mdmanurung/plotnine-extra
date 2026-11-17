"""
Benchmarks for the code paths that dominate plotting time.

Run them with::

    pytest tests/test_benchmarks.py --benchmark-only

Or compare against a saved baseline::

    pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare

Cap the calibration time if you only want a rough reading::

    pytest tests/test_benchmarks.py --benchmark-only \
        --benchmark-min-rounds=1 --benchmark-max-time=0.2

Sizes go up to 10,000 because that is where the algorithms differ. The
regular test suite tops out around n=100, which is small enough that every
quadratic path in this package looks instantaneous -- which is exactly how
the repulsion and swarm costs went unnoticed. The correctness of these paths
is pinned in ``test_performance_paths.py``; this file only measures them.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from plotnine_extra.geoms.geom_polygonraster import geom_polygonraster
from plotnine_extra.geoms.geom_text_repel import _repel_labels
from plotnine_extra.positions._beeswarm_algorithms import (
    _kde_density,
    offset_beeswarm,
    offset_quasirandom,
)
from plotnine_extra.stats import stat_compare, stat_compare_means, stat_pwc
from plotnine_extra.stats._common import pair_from_wide, paired_frame_by_wid

# 10,000 is the largest size used here on purpose: it is big enough to
# separate a near-linear implementation from a quadratic one, and small
# enough that the suite still runs in CI.
SIZES = [100, 1_000, 10_000]

# Repulsion is the slowest path by a wide margin, so it gets its own, much
# smaller sizes. Each of these is a multi-second call, and pytest-benchmark
# runs a benchmark many times over, so a single 10,000-label repulsion would
# dominate the whole run.
REPEL_SIZES = [100, 500, 1_000]


def _tied_values(n: int, levels: int, seed: int = 0) -> np.ndarray:
    """Discrete y values, which is what beeswarm and repel are for."""
    return (
        np.random.default_rng(seed).integers(0, levels, size=n).astype(float)
    )


# --------------------------------------------------------------------
# geom_text_repel
# --------------------------------------------------------------------

_REPEL_KW = {
    "box_padding": 0.01,
    "point_padding": 0.01,
    "force": 1.0,
    "max_iter": 500,
    "xlim": (-3.0, 3.0),
    "ylim": (-3.0, 3.0),
    "min_segment_length": 0.01,
    "direction": "both",
    "fontsize": 8,
}


@pytest.mark.parametrize("n", REPEL_SIZES)
def test_bench_repel(benchmark, n):
    """Force-directed repulsion. Was Theta(1000 * n^2) Python iterations."""
    rng = np.random.default_rng(0)
    x = rng.normal(size=n)
    y = rng.normal(size=n)
    labels = [f"label {i}" for i in range(n)]

    def run():
        return _repel_labels(
            x, y, labels, labels, random_state=42, **_REPEL_KW
        )

    lx, ly = benchmark(run)
    assert np.isfinite(lx).all()
    assert np.isfinite(ly).all()


# --------------------------------------------------------------------
# Beeswarm / quasirandom offsets
# --------------------------------------------------------------------


@pytest.mark.parametrize("n", SIZES)
@pytest.mark.parametrize("method", ["swarm", "compactswarm", "hex", "square"])
def test_bench_beeswarm(benchmark, n, method):
    """Swarm placement. The dense-cluster case is the expensive one."""
    values = _tied_values(n, levels=max(2, n // 20))
    result = benchmark(
        lambda: offset_beeswarm(values, method=method, point_size=1.0)
    )
    assert len(result) == n


@pytest.mark.parametrize("n", SIZES)
@pytest.mark.parametrize("method", ["quasirandom", "pseudorandom"])
def test_bench_quasirandom(benchmark, n, method):
    values = _tied_values(n, levels=max(2, n // 20))
    result = benchmark(lambda: offset_quasirandom(values, method=method))
    assert len(result) == n


@pytest.mark.parametrize("n", SIZES)
def test_bench_kde_density(benchmark, n):
    """Density estimate behind quasirandom; was evaluated at every point."""
    values = np.random.default_rng(0).normal(size=n)
    density = benchmark(lambda: _kde_density(values, bandwidth=0.5))
    assert len(density) == n


# --------------------------------------------------------------------
# Statistical annotations
# --------------------------------------------------------------------


def _paired_frame(n_subj: int, levels: int, seed: int = 0):
    rng = np.random.default_rng(seed)
    rows = []
    for s in range(n_subj):
        for lv in range(levels):
            rows.append(
                {
                    "x": float(lv + 1),
                    "y": float(rng.normal()),
                    "wid": f"s{s}",
                }
            )
    return pd.DataFrame(rows)


@pytest.mark.parametrize("n_subj", [200, 4_000])
@pytest.mark.parametrize("levels", [4, 8])
def test_bench_stat_pwc_paired(benchmark, n_subj, levels):
    """Pairwise comparisons. The wide pivot is hoisted out of the pair loop."""
    df = _paired_frame(n_subj, levels)
    result = benchmark(
        lambda: stat_pwc(
            paired=True, wid="wid", method="t.test"
        ).compute_panel(df, None)
    )
    assert len(result) == levels * (levels - 1) // 2


@pytest.mark.parametrize("n_subj", [200, 4_000])
def test_bench_paired_pivot_once(benchmark, n_subj):
    """The pivot itself, versus one per comparison pair."""
    df = _paired_frame(n_subj, 8)
    pairs = [(1.0, 2.0)] * 10

    def run():
        wide, _wid, dup = paired_frame_by_wid(df, "wid")
        return [pair_from_wide(wide, dup, df, a, b) for a, b in pairs]

    assert len(benchmark(run)) == len(pairs)


@pytest.mark.parametrize("n_subj", [500, 5_000])
def test_bench_stat_compare_overall(benchmark, n_subj):
    """Overall tests. Used to deep-copy the frame once per level."""
    df = _paired_frame(n_subj, 6)
    result = benchmark(
        lambda: stat_compare(overall=True, method="t.test").compute_panel(
            df, None
        )
    )
    assert len(result) == 6


@pytest.mark.parametrize("n_subj", [500, 5_000])
def test_bench_stat_compare_pairs(benchmark, n_subj):
    """Pairwise tests. The per-comparison filter was rebuilt each time."""
    df = _paired_frame(n_subj, 6)
    result = benchmark(
        lambda: stat_compare(
            method="t.test", comparisons=[(1.0, 2.0), (3.0, 4.0)]
        ).compute_panel(df, None)
    )
    assert len(result) == 2


@pytest.mark.parametrize("n_subj", [200, 2_000])
def test_bench_stat_compare_means_paired(benchmark, n_subj):
    # A paired *global* test is only defined for exactly two groups.
    df = _paired_frame(n_subj, 2)
    result = benchmark(
        lambda: stat_compare_means(
            method="t.test", paired=True, wid="wid"
        ).compute_panel(df, None)
    )
    assert len(result) > 0


@pytest.mark.parametrize("n_subj", [200, 2_000])
def test_bench_stat_compare_means_pairs_paired(benchmark, n_subj):
    """The pairwise path, which does the per-pair pivot lookups."""
    df = _paired_frame(n_subj, 6)
    result = benchmark(
        lambda: stat_compare_means(
            method="t.test",
            paired=True,
            wid="wid",
            comparisons=[(1.0, 2.0), (3.0, 4.0)],
        ).compute_panel(df, None)
    )
    assert len(result) == 2


# --------------------------------------------------------------------
# Geoms
# --------------------------------------------------------------------


@pytest.mark.parametrize("n", [100, 5_000, 20_000])
def test_bench_polygonraster_setup(benchmark, n):
    """Raster to polygon. Was a dict materialised per cell."""
    data = pd.DataFrame(
        {
            "x": np.random.default_rng(0).normal(size=n),
            "y": np.random.default_rng(1).normal(size=n),
        }
    )
    geom = geom_polygonraster.__new__(geom_polygonraster)
    geom.params = {"hjust": 0.5, "vjust": 0.5}

    out = benchmark(lambda: geom_polygonraster.setup_data(geom, data))
    assert len(out) == 4 * n
