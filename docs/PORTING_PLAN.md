# ggpubr & ggh4x Porting Plan

This document tracks a multi-feature port of ggpubr and ggh4x
functionality into `plotnine_extra`. It is the design rationale
behind the new modules added under this branch.

## Module layout

```
plotnine_extra/
  utils/
    summary.py            # mean_*, median_*, get_summary_stats,
                          # desc_statby, add_summary
  palettes/
    __init__.py
    _ggsci.py             # vendored color tables (NPG, AAAS,
                          # Lancet, JCO, NEJM, JAMA, etc.)
    palettes.py           # get_palette, color_palette,
                          # fill_palette, gradient_color,
                          # gradient_fill, set_palette,
                          # change_palette, show_*
  themes/
    theme_pub.py          # (existing) +
                          # theme_classic2, theme_pubclean,
                          # theme_cleveland, theme_transparent,
                          # clean_theme
    styling.py            # ggpar, bgcolor, border, grids,
                          # rotate, rotate_x_text, rotate_y_text,
                          # rremove, xscale, yscale, font,
                          # labs_pubr
  stats/
    _p_format.py          # (existing) extended with
                          # create_p_label, P_FORMAT_STYLES
    p_format.py           # public-facing wrappers
    stat_difference.py    # ggh4x: signed-difference ribbon
    stat_rle.py           # ggh4x: run-length encoding
    stat_centroid.py      # ggh4x: per-group XY centroid
    stat_midpoint.py      # ggh4x: per-group XY midpoint
    stat_funxy.py         # ggh4x: arbitrary fun(x), fun(y)
    stat_rollingkernel.py # ggh4x: rolling kernel smoother
    stat_theodensity.py   # ggh4x: theoretical density fit
  geoms/
    geom_signif.py        # ggpubr alias of geom_bracket
    geom_pwc.py           # ggpubr geom counterpart of stat_pwc
    geom_pointpath.py     # ggh4x: points + path combo
    geom_outline_point.py # ggh4x: points with halo outline
    geom_box.py           # ggh4x: rectangular highlight
    geom_text_aimed.py    # ggh4x: rotation-aware text
    geom_rectmargin.py    # ggh4x: marginal rectangles
    geom_tilemargin.py    # ggh4x: marginal tiles
  positions/
    position_lineartrans.py     # ggh4x
    position_disjoint_ranges.py # ggh4x
  scales/                 # NEW subpackage
    __init__.py
    scale_manual.py       # scale_x_manual, scale_y_manual
    scale_multi.py        # scale_colour_multi, scale_fill_multi,
                          # scale_listed
  guides/                 # NEW subpackage (documentation only)
    __init__.py           # explains why guide_axis_* family is
                          # not implementable as drop-in classes
  coords/                 # NEW subpackage
    __init__.py
    coord_axes_inside.py  # ggh4x; partial via post-render hook
```

## Implementation phases

### Phase 1 — pure Python (no plotnine internals)
Lowest risk, highest immediate value.

- ggpubr summary helpers (`utils/summary.py`)
- ggpubr p-value helpers (`stats/p_format.py`)
- ggpubr palettes (`palettes/`)
- ggpubr themes additions (`themes/theme_pub.py`)
- ggpubr styling helpers (`themes/styling.py`)

### Phase 2 — simple plotnine subclasses
Subclass `stat`, `geom`, `position`, `scale` directly. Each item
follows the patterns already established by `stat_central_tendency`,
`position_beeswarm`, etc.

- ggh4x stats (7 items)
- ggh4x positions (2 items)
- ggh4x simple geoms (6 items)
- ggh4x manual scales + multi colour scales (5 items)
- ggpubr `geom_signif` and `geom_pwc` wrappers

### Phase 3 — partial / documented gaps
Items where plotnine internals do not expose the necessary hook
points. We provide stubs with clear NotImplementedError or
limited functionality and document the workaround pattern.

- `coord_axes_inside`: limited implementation via subclassing
  `coord_cartesian` plus a post-build axes-tweak callback.
- ggh4x `guide_axis_*` family: documented as unsupported in
  `guides/__init__.py`. The reason is that plotnine 0.15/0.16's
  `guide_axis` is an empty stub class — tick rendering happens
  in `plotnine.facets.facet.set_breaks_and_labels` via direct
  matplotlib `ax.set_xticks(...)` calls. There is no extension
  point for arbitrary tick guides without monkey-patching that
  method or post-walking the figure axes.

### Phase 4 — wiring + tests
- Append every public symbol to `plotnine_extra/__init__.py`
  `_extra_all`.
- Update sub-package `__init__.py` re-exports.
- Add unit tests for all pure-Python helpers.
- Smoke tests (no baseline images) that construct the geom /
  stat / position / scale and add it to a `ggplot` to verify
  it doesn't blow up.

## New dependencies

None. The ggsci color tables are vendored as a small Python dict
in `palettes/_ggsci.py`. Everything else is covered by existing
deps (`scipy`, `numpy`, `pandas`, `plotnine`).

## Testing strategy

- Unit tests in `tests/test_summary_helpers.py`,
  `tests/test_palettes.py`, `tests/test_p_format.py`,
  `tests/test_styling.py`.
- Smoke tests in `tests/test_ggh4x_layers.py` that build a
  trivial `ggplot` for each new geom / stat / position / scale
  and call `.draw(show=False)` to catch import errors and
  schema mistakes. No baseline images on first pass — those
  can be added incrementally as the API stabilises.

## Known limitations (carry-over from R → Python port)

1. **`guide_axis_*` family is not portable** without
   monkey-patching `plotnine.facets.facet.set_breaks_and_labels`.
   The replacement pattern users should reach for is to subclass
   `facet_grid2` / `facet_wrap2` and override that method, or to
   walk the figure axes after `ggplot.draw()`.
2. **`scale_x_dendrogram` / `scale_y_dendrogram`** require a
   linkage matrix and a custom axis decoration. They are stubbed
   out for now; the discrete reordering portion is achievable
   via `scale_x_discrete(limits=ordered_labels)`.
3. **`ggadjust_pvalue`** rewrites layer params on an already
   constructed `ggplot`. The plotnine equivalent walks
   `plot.layers` and mutates each `stat_pwc` / `stat_compare_means`
   layer's `params` in place; it works but is sensitive to
   plotnine internals.
4. **matplotlib cannot render heterogeneously coloured tick
   labels** through the standard axis API in a single call,
   so `guide_axis_colour` would need a per-tick post-render
   pass. Not implemented.
