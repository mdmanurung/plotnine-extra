"""
``geom_text_repel`` / ``geom_label_repel``: text labels with
force-directed repulsion to avoid overlaps, inspired by R's
``ggrepel`` package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from plotnine.doctools import document
from plotnine.geoms.geom_text import geom_text
from scipy.spatial import cKDTree

from .._common import resolve_random_state

if TYPE_CHECKING:
    from typing import Any, Sequence

    import pandas as pd
    from matplotlib.axes import Axes
    from numpy.typing import NDArray
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import RandomStateLike


def _repel_labels(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    labels: Sequence[str],
    points: Sequence[str],
    *,
    box_padding: float,
    point_padding: float,
    force: float,
    max_iter: int,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    random_state: RandomStateLike,
    min_segment_length: float,
    direction: str,
    fontsize: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Force-directed label placement algorithm.

    Repeatedly pushes overlapping labels apart so they no
    longer occlude each other or the data points they annotate.

    Each iteration builds a KD-tree over the labels and the data points and
    enumerates only the pairs close enough to interact, then applies the
    resulting repulsion. A pair contributes no force once its boxes are
    clear, so the pair search can be restricted to a neighbourhood without
    changing the result -- that is what keeps this tractable, since the
    naive all-pairs form is quadratic in the number of labels.

    Parameters
    ----------
    x, y
        Label anchor positions in data coordinates.
    labels, points
        Label texts, and the point texts to repel from.
    box_padding
        Label box padding (fraction of axis range).
    point_padding
        Padding around data points (fraction of axis range).
    force
        Repulsion force multiplier.
    max_iter
        Maximum number of iterations.
    xlim, ylim
        Axis limits used to clamp labels inside the plot.
    random_state
        Seed or generator for reproducibility.
    min_segment_length
        Minimum segment length (fraction of x-range) below
        which no connector line is drawn.
    direction
        ``"both"``, ``"x"``, or ``"y"``: restricts which
        axes are affected by repulsion.
    fontsize
        Font size of the labels.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Adjusted *(x, y)* label positions.
    """
    n = len(x)
    if n == 0:
        return np.array([]), np.array([])

    rng = resolve_random_state(random_state)

    # Work on float copies
    lx = x.copy().astype(float)
    ly = y.copy().astype(float)

    # Small initial jitter to break exact ties
    lx += rng.uniform(-0.01, 0.01, n)
    ly += rng.uniform(-0.01, 0.01, n)

    x_range = xlim[1] - xlim[0] if xlim[1] > xlim[0] else 1.0
    y_range = ylim[1] - ylim[0] if ylim[1] > ylim[0] else 1.0

    # Approximate text dimensions in data coordinates
    char_w = x_range * 0.015
    text_h = y_range * 0.035

    widths = np.array(
        [len(str(l)) * char_w + 2 * box_padding * x_range for l in labels]
    )
    heights = np.array([text_h + 2 * box_padding * y_range for _ in labels])

    pt_pad_x = point_padding * x_range
    pt_pad_y = point_padding * y_range

    # Constants that do not change between iterations.
    move_x = direction != "y"
    move_y = direction != "x"
    half_w = widths / 2
    half_h = heights / 2

    n_points = len(x)
    # A pair only interacts when the two boxes overlap, which needs
    # |dx| < (w_i + w_j)/2 and |dy| < (h_i + h_j)/2, plus the point padding
    # against a data point. Bounding both with the largest box means a search
    # radius of hypot(...) can never miss a pair that would contribute force
    # -- it only adds extras, which are then filtered exactly below.
    radius = float(np.hypot(widths.max() + pt_pad_x, heights.max() + pt_pad_y))
    # Half-extents over labels-then-points, so a pair's overlap is the plain
    # sum of its two entries. Constant across iterations.
    half_x = np.concatenate([widths / 2, np.full(n_points, pt_pad_x)])
    half_y = np.concatenate([heights / 2, np.full(n_points, pt_pad_y)])
    all_x = np.concatenate([lx, x])
    all_y = np.concatenate([ly, y])

    for _iteration in range(max_iter):
        overlapping = False
        all_x[:n] = lx
        all_y[:n] = ly
        tree = cKDTree(np.column_stack([all_x, all_y]))
        pairs = tree.query_pairs(radius, output_type="ndarray")
        if not len(pairs):
            # Nothing is close enough to anything to push: settled.
            return lx, ly

        i = pairs[:, 0]
        j = pairs[:, 1]
        # A data point is never pushed, so point-point pairs cannot
        # contribute and are dropped.
        live = (i < n) | (j < n)
        i = i[live]
        j = j[live]

        both_labels = (i < n) & (j < n)
        # Visit a label-label pair once, from its lower-indexed member.
        owner = np.where(both_labels, np.minimum(i, j), np.where(i < n, i, j))
        # The other member: the partner label, or the data point.
        partner = np.where(
            both_labels, np.maximum(i, j), np.where(i < n, j, i)
        )

        dx = lx[owner] - all_x[partner]
        dy = ly[owner] - all_y[partner]

        # Two half-extents sum to both cases: (w_i + w_j) / 2 between
        # labels, and w_i / 2 + pad against a data point.
        ovlp_x = half_x[owner] + half_x[partner] - np.abs(dx)
        ovlp_y = half_y[owner] + half_y[partner] - np.abs(dy)
        hit = (ovlp_x > 0) & (ovlp_y > 0)
        if not hit.any():
            continue
        overlapping = True

        dist = np.maximum(np.sqrt(dx[hit] ** 2 + dy[hit] ** 2), 0.001)
        # Label-point pairs carry a weaker force than label-label pairs.
        weight = np.where(both_labels[hit], 1.0, 0.5)
        owner = owner[hit]
        partner = partner[hit]
        both = both_labels[hit]
        fx_pair = force * dx[hit] / dist * ovlp_x[hit] / x_range * weight
        fy_pair = force * dy[hit] / dist * ovlp_y[hit] / y_range * weight

        # A pair pushes its two label members in opposite directions.
        mv_idx = np.concatenate([owner, partner[both]])
        mv_fx = np.concatenate([fx_pair, -fx_pair[both]])
        mv_fy = np.concatenate([fy_pair, -fy_pair[both]])

        # np.bincount accumulates shared indices correctly, unlike
        # fancy-index "+=".
        fx = np.bincount(mv_idx, weights=mv_fx, minlength=n)
        fy = np.bincount(mv_idx, weights=mv_fy, minlength=n)

        moved = (np.abs(fx) > 1e-6) | (np.abs(fy) > 1e-6)
        if not moved.any():
            break

        lx += np.where(moved & move_x, fx * x_range * 0.1, 0.0)
        ly += np.where(moved & move_y, fy * y_range * 0.1, 0.0)
        np.clip(lx, xlim[0] + half_w, xlim[1] - half_w, out=lx)
        np.clip(ly, ylim[0] + half_h, ylim[1] - half_h, out=ly)

        # Nothing overlapped anywhere this iteration: the layout has settled.
        if not overlapping:
            break

    return lx, ly


# ----- aesthetic / parameter helpers -----

_text_repel_aes = geom_text.DEFAULT_AES.copy()
_text_repel_aes.update(
    {
        "color": "black",
        "alpha": 1,
        "size": 8,
        "angle": 0,
    }
)

_text_repel_params = geom_text.DEFAULT_PARAMS.copy()
_text_repel_params.update(
    {
        "box_padding": 0.01,
        "point_padding": 0.01,
        "force": 1.0,
        "max_iter": 500,
        "random_state": 42,
        "min_segment_length": 0.01,
        "segment_color": "grey",
        "segment_alpha": 0.6,
        "segment_size": 0.5,
        "direction": "both",
    }
)


def _draw_repelled_text(
    data: pd.DataFrame,
    panel_params: panel_view,
    coord: coord,
    ax: Axes,
    params: dict[str, Any],
    *,
    use_bbox: bool = False,
) -> None:
    """
    Shared drawing logic for *geom_text_repel* and
    *geom_label_repel*.
    """
    data = coord.transform(data, panel_params)

    if len(data) == 0:
        return

    x = data["x"].to_numpy(dtype=float)
    y = data["y"].to_numpy(dtype=float)
    labels = data["label"].to_numpy()

    mask = np.array([bool(str(l).strip()) for l in labels])
    if not mask.any():
        return

    x = x[mask]
    y = y[mask]
    labels = labels[mask]

    colors = data["color"].to_numpy()[mask]
    alphas = data["alpha"].to_numpy(dtype=float)[mask]
    sizes = data["size"].to_numpy(dtype=float)[mask]

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    fontsize = float(np.mean(sizes))

    new_x, new_y = _repel_labels(
        x,
        y,
        labels,
        ax,
        fontsize=fontsize,
        box_padding=params["box_padding"],
        point_padding=params["point_padding"],
        force=params["force"],
        max_iter=params["max_iter"],
        xlim=xlim,
        ylim=ylim,
        random_state=params["random_state"],
        min_segment_length=params["min_segment_length"],
        direction=params["direction"],
    )

    seg_color = params["segment_color"]
    seg_alpha = params["segment_alpha"]
    seg_size = params["segment_size"]
    min_seg = params["min_segment_length"]
    zorder = params.get("zorder", 3)
    ha = params.get("ha", "center")
    va = params.get("va", "center")

    x_range = xlim[1] - xlim[0] if xlim[1] > xlim[0] else 1.0

    # Optional label-box settings
    if use_bbox:
        fills = (
            data["fill"].to_numpy()[mask]
            if "fill" in data.columns
            else np.array(["white"] * int(mask.sum()))
        )
        label_pad = params.get("label_padding", 0.25)
        fill_alpha = params.get("fill_alpha", 0.8)

    for i in range(len(labels)):
        # --- connector segment ---
        dist = np.sqrt((new_x[i] - x[i]) ** 2 + (new_y[i] - y[i]) ** 2)
        if dist > min_seg * x_range:
            ax.plot(
                [x[i], new_x[i]],
                [y[i], new_y[i]],
                color=seg_color,
                alpha=seg_alpha,
                linewidth=seg_size,
                zorder=zorder - 0.1,
            )

        # --- text kwargs ---
        kw: dict[str, Any] = {
            "ha": ha,
            "va": va,
            "fontsize": sizes[i],
            "color": colors[i],
            "alpha": alphas[i],
            "zorder": zorder,
            "clip_on": True,
        }

        if use_bbox:
            kw["bbox"] = {
                "boxstyle": f"round,pad={label_pad}",
                "facecolor": fills[i],
                "edgecolor": colors[i],
                "alpha": fill_alpha,
                "linewidth": 0.5,
            }

        ax.text(
            new_x[i],
            new_y[i],
            str(labels[i]),
            **kw,
        )


@document
class geom_text_repel(geom_text):
    """
    Repulsive text labels that avoid overlapping

    Labels are repositioned using a force-directed algorithm
    to avoid overlapping each other and data points.
    Connector segments are drawn from the original data point
    to the repositioned label.

    {usage}

    Parameters
    ----------
    {common_parameters}
    box_padding : float
        Padding around text boxes (fraction of axis range).
    point_padding : float
        Padding around data points (fraction of axis range).
    force : float
        Repulsion force multiplier.
    max_iter : int
        Maximum repulsion iterations.
    random_state : int or numpy.random.RandomState or numpy.random.Generator
        Seed or generator for reproducibility.
    min_segment_length : float
        Minimum segment length (fraction of x-range) below
        which no connector line is drawn.
    segment_color : str
        Colour of connector segments.
    segment_alpha : float
        Alpha of connector segments.
    segment_size : float
        Line width of connector segments.
    direction : str
        ``"both"``, ``"x"``, or ``"y"``: restricts which
        axes are affected by repulsion.

    See Also
    --------
    plotnine.geom_text
    geom_label_repel
    """

    REQUIRED_AES = {"x", "y", "label"}
    DEFAULT_AES = _text_repel_aes
    DEFAULT_PARAMS = _text_repel_params

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        _draw_repelled_text(
            data,
            panel_params,
            coord,
            ax,
            self.params,
            use_bbox=False,
        )


# ----- label variant -----

_label_repel_aes = _text_repel_aes.copy()
_label_repel_aes["fill"] = "white"

_label_repel_params = _text_repel_params.copy()
_label_repel_params.update(
    {
        "label_padding": 0.25,
        "fill_alpha": 0.8,
    }
)


@document
class geom_label_repel(geom_text_repel):
    """
    Repulsive text labels with a background box

    Like :class:`geom_text_repel` but draws a filled rectangle
    behind each label for improved readability.

    {usage}

    Parameters
    ----------
    {common_parameters}
    box_padding : float
        Padding around text boxes (fraction of axis range).
    point_padding : float
        Padding around data points (fraction of axis range).
    force : float
        Repulsion force multiplier.
    max_iter : int
        Maximum repulsion iterations.
    random_state : int or numpy.random.RandomState or numpy.random.Generator
        Seed or generator for reproducibility.
    min_segment_length : float
        Minimum connector length (fraction of x-range).
    segment_color : str
        Connector segment colour.
    segment_alpha : float
        Connector segment alpha.
    segment_size : float
        Connector line width.
    direction : str
        ``"both"``, ``"x"``, or ``"y"``.
    label_padding : float
        Padding inside the label box.
    fill_alpha : float
        Alpha for the background fill.

    See Also
    --------
    plotnine.geom_label
    geom_text_repel
    """

    DEFAULT_AES = _label_repel_aes
    DEFAULT_PARAMS = _label_repel_params

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        _draw_repelled_text(
            data,
            panel_params,
            coord,
            ax,
            self.params,
            use_bbox=True,
        )
