"""
Regression tests for the performance-critical code paths.

The optimisations in this package (KD-tree repulsion, preallocated swarm
buffers, grid-evaluated KDE, pivot-once paired tests, vectorised
polygonraster) are only safe if they keep producing the same answers. These
tests pin that behaviour. Timings live in ``test_benchmarks.py``; what is
checked here is correctness, which is what actually regresses.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from plotnine_extra.geoms.geom_polygonraster import geom_polygonraster
from plotnine_extra.geoms.geom_text_repel import _repel_labels
from plotnine_extra.positions._beeswarm_algorithms import (
    _candidates,
    _kde_density,
    corral_points,
    offset_beeswarm,
    offset_quasirandom,
)
from plotnine_extra.stats._common import (
    pair_from_wide,
    paired_frame_by_wid,
    paired_values_by_wid,
)

# --------------------------------------------------------------------
# geom_text_repel: KD-tree neighbour search
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


def _labels(n: int) -> list[str]:
    return [f"label {i}" for i in range(n)]


def test_repel_stays_inside_the_axes_and_is_finite():
    n = 120
    rng = np.random.default_rng(0)
    x = rng.normal(size=n)
    y = rng.normal(size=n)
    lx, ly = _repel_labels(
        x, y, _labels(n), _labels(n), random_state=42, **_REPEL_KW
    )

    assert np.isfinite(lx).all()
    assert np.isfinite(ly).all()
    assert lx.min() >= _REPEL_KW["xlim"][0] - 1e-9
    assert lx.max() <= _REPEL_KW["xlim"][1] + 1e-9
    assert ly.min() >= _REPEL_KW["ylim"][0] - 1e-9
    assert ly.max() <= _REPEL_KW["ylim"][1] + 1e-9


def test_repel_reduces_overlapping_labels():
    """The point of the algorithm: fewer collisions than it began with."""
    n = 150
    rng = np.random.default_rng(0)
    x = rng.normal(size=n)
    y = rng.normal(size=n)
    labels = _labels(n)

    def collisions(px: np.ndarray, py: np.ndarray) -> int:
        # Same box model the implementation uses.
        w = np.array([len(v) * 6.0 * 0.015 + 2 * 0.01 * 6.0 for v in labels])
        h = np.full(n, 6.0 * 0.035 + 2 * 0.01 * 6.0)
        i, j = np.triu_indices(n, 1)
        ox = (w[i] + w[j]) / 2 - np.abs(px[i] - px[j])
        oy = (h[i] + h[j]) / 2 - np.abs(py[i] - py[j])
        return int(((ox > 0) & (oy > 0)).sum())

    before = collisions(x, y)
    lx, ly = _repel_labels(x, y, labels, labels, random_state=42, **_REPEL_KW)
    after = collisions(lx, ly)

    assert before > 0, "the fixture should start with collisions"
    assert after < before


def test_repel_is_reproducible_and_seed_sensitive():
    n = 60
    rng = np.random.default_rng(1)
    x = rng.normal(size=n)
    y = rng.normal(size=n)
    labels = _labels(n)

    a = _repel_labels(x, y, labels, labels, random_state=7, **_REPEL_KW)
    b = _repel_labels(x, y, labels, labels, random_state=7, **_REPEL_KW)
    c = _repel_labels(x, y, labels, labels, random_state=8, **_REPEL_KW)

    assert np.array_equal(a[0], b[0])
    assert np.array_equal(a[1], b[1])
    assert not np.array_equal(a[0], c[0])


def test_repel_handles_degenerate_inputs():
    # Empty input.
    empty = _repel_labels(
        np.array([]), np.array([]), [], [], random_state=1, **_REPEL_KW
    )
    assert len(empty[0]) == 0 and len(empty[1]) == 0

    # Every label on the same spot: the fully-degenerate case the pairwise
    # search has to survive.
    n = 40
    z = np.zeros(n)
    lx, ly = _repel_labels(
        z, z, _labels(n), _labels(n), random_state=3, **_REPEL_KW
    )
    assert np.isfinite(lx).all() and np.isfinite(ly).all()
    # They must have been pushed apart rather than left stacked.
    assert lx.std() > 0 or ly.std() > 0


# --------------------------------------------------------------------
# Beeswarm placement
# --------------------------------------------------------------------


def test_swarm_place_picks_the_clear_candidate_nearest_zero():
    from plotnine_extra.positions._beeswarm_algorithms import _swarm_place

    # Neighbours at +/-0.2 each needing 0.5 of clearance, so 0.0 is blocked
    # and only the touching points at -/+0.7 are clear. The tie is broken
    # towards the first of the two in candidate order, which is -0.7.
    neighbour_x = np.array([-0.2, 0.2])
    min_dx = np.array([0.5, 0.5])
    assert _swarm_place(neighbour_x, min_dx, 0) == pytest.approx(-0.7)

    # Widening the clearance pushes the answer out to the far touching
    # points.
    assert _swarm_place(neighbour_x, np.array([2.0, 2.0]), 0) == pytest.approx(
        -2.2
    )


def test_swarm_place_falls_back_to_the_outer_edge():
    from plotnine_extra.positions._beeswarm_algorithms import _swarm_place

    # A huge required separation means no candidate is clear.
    neighbour_x = np.array([0.0])
    min_dx = np.array([100.0])
    assert _swarm_place(neighbour_x, min_dx, 0) == pytest.approx(100.0)
    assert _swarm_place(neighbour_x, min_dx, -1) == pytest.approx(-100.0)


def test_compact_place_searches_outward_from_the_centre():
    from plotnine_extra.positions._beeswarm_algorithms import _compact_place

    # 0.0 is blocked, 0.4 is clear, 0.9 is also clear but further out.
    neighbour_x = np.array([0.0])
    min_dx = np.array([0.4])
    assert _compact_place(neighbour_x, min_dx, 0) == pytest.approx(0.4)


def test_candidates_respect_the_side_constraint():
    neighbour_x = np.array([-1.0, 1.0])
    min_dx = np.array([0.5, 0.5])

    right = _candidates(neighbour_x, min_dx, 1)
    assert (right >= -1e-10).all()

    left = _candidates(neighbour_x, min_dx, -1)
    assert (left <= 1e-10).all()

    both = _candidates(neighbour_x, min_dx, 0)
    assert len(both) == 2 * len(neighbour_x) + 1


def test_swarm_offsets_clear_every_neighbour():
    """Every placed point must respect the minimum separation it was given."""
    n, levels = 300, 6
    rng = np.random.default_rng(0)
    values = rng.integers(0, levels, size=n).astype(float)
    point_size = 1.0
    offsets = offset_beeswarm(
        values, method="swarm", side=0, point_size=point_size
    )

    for level in range(levels):
        at = values == level
        xs = np.sort(offsets[at])
        if len(xs) < 2:
            continue
        # Same y, so the required horizontal gap is the full point size.
        assert np.all(np.diff(xs) >= point_size - 1e-9)


def test_beeswarm_deterministic_for_every_method():
    n = 200
    rng = np.random.default_rng(0)
    values = rng.integers(0, 5, size=n).astype(float)
    for method in ("swarm", "compactswarm", "hex", "square", "center"):
        a = offset_beeswarm(values, method=method, point_size=0.5)
        b = offset_beeswarm(values, method=method, point_size=0.5)
        assert np.array_equal(a, b), method


def test_kde_density_is_normalised_and_tracks_the_data():
    rng = np.random.default_rng(0)
    # Dense cluster plus a sparse tail: density must be higher at the cluster.
    values = np.concatenate([rng.normal(0, 0.2, 800), rng.normal(4, 1.0, 200)])

    density = _kde_density(values)
    assert len(density) == len(values)
    assert density.max() == pytest.approx(1.0)
    assert (density >= 0).all()
    assert density[values < 2].mean() > density[values > 3].mean()


def test_kde_density_agrees_with_direct_evaluation():
    """The grid is an approximation; it must still be a close one."""
    from scipy.stats import gaussian_kde

    rng = np.random.default_rng(0)
    values = rng.normal(size=2000)
    direct = gaussian_kde(values, bw_method=0.5)(values)
    direct = direct / direct.max()

    assert np.abs(_kde_density(values) - direct).max() < 0.02


def test_kde_density_edge_cases():
    # Too few points for a KDE.
    assert np.array_equal(_kde_density(np.array([1.0])), np.array([1.0]))
    # Constant input is singular; must degrade to a flat estimate.
    flat = _kde_density(np.full(10, 2.0))
    assert np.isfinite(flat).all()


def test_quasirandom_width_is_bounded():
    rng = np.random.default_rng(0)
    values = rng.normal(size=500)
    offsets = offset_quasirandom(values, width=0.4)
    assert np.abs(offsets).max() <= 0.4 + 1e-9


def test_corral_gutter_keeps_points_inside_the_width():
    rng = np.random.default_rng(0)
    values = rng.normal(size=300)
    offsets = offset_beeswarm(values)
    corralled = corral_points(offsets, method="gutter", width=0.5)
    assert np.abs(corralled).max() <= 0.5 + 1e-9


# --------------------------------------------------------------------
# Paired-test pivot (hoisted out of the comparison loop)
# --------------------------------------------------------------------


def _complete_paired_frame(n_subj: int = 120, levels: int = 4) -> pd.DataFrame:
    rng = np.random.default_rng(0)
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


def test_pair_from_wide_matches_the_per_pair_pivot():
    df = _complete_paired_frame()
    for a, b in ((1.0, 2.0), (1.0, 4.0), (3.0, 4.0)):
        direct = paired_values_by_wid(df, a, b, "wid")
        wide, _wid, dup = paired_frame_by_wid(df, "wid")
        hoisted = pair_from_wide(wide, dup, df, a, b)

        assert np.array_equal(direct[0], hoisted[0])
        assert np.array_equal(direct[1], hoisted[1])
        # Subjects are aligned: row i of both arrays is the same subject.
        assert len(direct[0]) == len(direct[1]) == df["wid"].nunique()


def test_hoisted_pivot_still_rejects_incomplete_pairs():
    df = _complete_paired_frame()
    # Drop one subject's observation from level 4.
    partial = df[~((df["wid"] == "s0") & (df["x"] == 4.0))]
    with pytest.raises(ValueError, match="complete paired observations"):
        paired_values_by_wid(partial, 1.0, 4.0, "wid")


def test_hoisted_pivot_still_rejects_duplicate_subjects():
    df = _complete_paired_frame()
    wide, _wid, dup = paired_frame_by_wid(df, "wid")
    # No duplicates in the fixture.
    pair_from_wide(wide, dup, df, 1.0, 2.0)

    doubled = pd.concat([df, df.head(2)], ignore_index=True)
    wide2, _w2, dup2 = paired_frame_by_wid(doubled, "wid")
    with pytest.raises(ValueError, match="duplicate subject/group"):
        pair_from_wide(wide2, dup2, doubled, 1.0, 2.0)


def test_paired_frame_requires_a_wid_column():
    df = _complete_paired_frame()
    with pytest.raises(ValueError, match="wid"):
        paired_frame_by_wid(df, None)


# --------------------------------------------------------------------
# geom_polygonraster
# --------------------------------------------------------------------


def _raster_geom():
    geom = geom_polygonraster.__new__(geom_polygonraster)
    geom.params = {"hjust": 0.5, "vjust": 0.5}
    return geom


def test_polygonraster_emits_four_corners_per_cell():
    rng = np.random.default_rng(0)
    data = pd.DataFrame({"x": rng.normal(size=25), "y": rng.normal(size=25)})

    out = geom_polygonraster.setup_data(_raster_geom(), data)

    assert len(out) == 4 * len(data)
    # The four corners of each cell keep its group.
    for raster_id in range(len(data)):
        corners = out[out["_raster_group"] == raster_id]
        assert len(corners) == 4
        assert corners["x"].nunique() == 2
        assert corners["y"].nunique() == 2
        assert set(corners["group"]) == {raster_id}


def test_polygonraster_preserves_other_columns():
    rng = np.random.default_rng(0)
    data = pd.DataFrame(
        {
            "x": rng.normal(size=10),
            "y": rng.normal(size=10),
            "colour": ["red"] * 10,
        }
    )
    out = geom_polygonraster.setup_data(_raster_geom(), data)
    # Every row keeps the extra aesthetic, unlike the old dict-per-row form.
    assert set(out["colour"]) == {"red"}


def test_polygonraster_handles_empty_input():
    data = pd.DataFrame({"x": [], "y": []})
    out = geom_polygonraster.setup_data(_raster_geom(), data)
    assert len(out) == 0
