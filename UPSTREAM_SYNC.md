# Staying in sync with plotnine

`plotnine-extra` is an **extension package**, not a fork of plotnine. There
is no `plotnine/` source tree in this repository — plotnine is an ordinary
runtime dependency (see `pyproject.toml`). That is the single most important
fact for staying in sync: **"integrating new plotnine commits" is a dependency
version bump, not a git merge.** There is nothing to rebase and nothing of ours
to clobber.

This document explains how to keep up with plotnine safely, and why the one
place we broke is the one place we had diverged from that rule.

## The failure we fixed, and the lesson

Plot composition used to be **vendored**: `plotnine_extra/composition/` held a
copy of plotnine's composition code. plotnine then shipped composition natively
— the `|`, `/`, `-`, `+` operators live on `plotnine.ggplot`, so `p1 | p2`
builds a *plotnine* `Beside`. Our vendored `plot_layout`/`Wrap` were a separate
lineage that could never own those operators, so mixing them crashed.

The fix was to stop vendoring and re-export from `plotnine.composition`
(`plotnine_extra/composition/__init__.py`). Now the operators and the objects
they build come from the same source and cannot disagree. Syncing composition
from upstream is therefore automatic: it rides along with the installed plotnine.

**Lesson: don't vendor plotnine code. Delegate to it.** Copying upstream code is
what creates a divergent branch you then have to merge.

Animation is delegated the same way: plotnine ships `PlotnineAnimation`, so
`plotnine_extra/animation.py` re-exports it and inherits its fixes for free.

## Version policy

**We require plotnine 0.16.** There is no stable 0.16 on PyPI yet — the latest
stable is 0.15.8, and 0.16 exists only as alphas. That has a direct consequence
for the dependency specifier:

```toml
dependencies = ["plotnine>=0.16.0a15"]
```

Not `plotnine>=0.16`: that specifier is **unsatisfiable** (there is no such
release), and `pip install plotnine-extra` would fail outright. PEP 440 only
permits pre-releases when the specifier itself names one, which is what
`>=0.16.0a15` does. So a plain `pip install` works with no `--pre` flag.

- **plotnine floor:** `>=0.16.0a15`
- **Python floor:** `>=3.11` (upstream bumped this in a11, via `039dc674d`).
  The CI matrix is 3.11/3.12/3.13.
- **When 0.16.0 ships stable:** change the floor to `>=0.16`, and nothing else
  in the package has to move — the code already targets 0.16 internals.

Because we sit on an alpha, CI carries a non-blocking `prerelease` job that
installs the newest pre-release plotnine and runs the suite. It is
`continue-on-error: true` so it never blocks the stable lane. That job is how
the *next* internal break surfaces on our schedule rather than after plotnine
releases.

## Where we are still coupled (the real sync risk)

Delegation solves composition and animation, but several extension modules
reach into plotnine's **internal (underscore) APIs**, which plotnine changes
without notice between releases. These are the surfaces to watch on every
plotnine bump.

The 0.15 → 0.16 transition is the worked example. Three things broke, all
between a11 and a14:

| What plotnine changed | Where we relied on it | How it is handled now |
| --- | --- | --- |
| `Facet.compute_layout()` gained a required `scales` argument (a14; it feeds `scales.axis_positions`, the moved-axis feature) | `facet_manual`, `facet_grid2`, `facet_wrap2` overrode it as `compute_layout(self, data)` | Signature updated and `scales` forwarded to `super()`. `facet_manual` also uses `scales.axis_positions` to place the primary axes. |
| `Facet.set_limits_breaks_and_labels()` **removed** in a12; the work moved to `coord.setup_ax(ax, panel_params, layout_info)` | 5 facet classes overrode it to run `apply_axis_guides` per panel | Axis guides now hang off a coord mixin (`guides/_AxisGuideCoord`), installed by `facets/_axis_guides.py::AxisGuideFacet.setup`. The old overrides were **silent dead code** — nothing crashed, the guides just stopped rendering. |
| `Facet._get_panels_gridspec()` → `_make_gridspec()` | `facet_manual` defined the old name, so it was never called | Renamed. `panel_tools` no longer probes for either spelling. |

a15 broke four more couplings. `at_panel` silently filtered nothing, which is
the silent failure mode again.

| What plotnine changed | Where we relied on it | How it is handled now |
| --- | --- | --- |
| `ggplot.build()` works on a **copy**; `_build()` stores it as `plot.built` | `at_panel` read `plot._build_objs.layout` mid-build, `get_breaks` read `plot.layout` after `_build()`, tests read `plot.layers[i].data` and `plot.facet.nrow` | `at_panel` reads `plot.layout` on the build copy. `get_breaks` uses `plot.build()`. Tests use `plot.layer_data(i)` and `plot.built`. |
| `guide` and `guide_legend` lost `__post_init__`; `_elements_cls` became a read-only property | `guide_stringlegend` set `_elements_cls` and `kind` in `__post_init__`, which no longer ran | `@dataclass` on the subclass so `__post_init__` runs; `_elements_cls` is an overriding property. |
| `Compose` is no longer a dataclass (`__init__(items)`) | Downstream `ggann` subclasses `Beside`/`Stack` with `@dataclass` | Fixed in ggann, not here. |

The recurring lesson from that list: **two of the three breakages were silent.**
A removed base method leaves the override as dead code, and a renamed method
leaves it uncalled. Neither raises. So the two failure modes to watch for are
crashes (signature/arity changes) *and* features quietly doing nothing.

Every remaining coupling is listed here. Prefer plotnine's **public** API; every
underscore-prefixed plotnine name is a future sync break.

| Module | Internal it uses |
| --- | --- |
| `facets/facet_manual.py` | `plotnine._utils.{join_keys, match}`, `plotnine.facets.facet.{add_missing_facets, combine_vars, eval_facet_vars}`, `plotnine.facets.strips.{Strips, strip}`, `plotnine._mpl.gridspec.p9GridSpec`, `ggplot._gridspec`, `Facet.{plot, free, environment, _make_axes}` |
| `facets/facet_nested.py`, `facet_nested_wrap.py` | subclass `plotnine.facets.strips.strip` (5-arg `__init__`), write `strip.label_info.variables` |
| `facets/panel_tools.py` | patches `Layer.compute_aesthetics` and `Facet._make_gridspec`, reads `plot._build_objs.layout.layout` |
| `facets/{facet_grid2, facet_wrap2}.py` | override `Facet.{compute_layout, init_scales, set_limits_breaks_and_labels}`; `facet_wrap._ncol`/`_nrow` |
| `guides/__init__.py` | `plotnine.guides.guide_legend.{GuideElementsLegend, guide_legend._calculate_rows_and_cols, _elements_cls}`, `guide._bind_source`, `legend.elements.text.has/.vas`, `guide._layer_parameters` |
| `stats/_common.py` | `Stat._raw_kwargs` (was `_kwargs` before 0.16) |
| `stats/*` (20 stat subclasses) | `compute_panel(self, data, scales)` / `compute_layer(self, data, layout)` arity |
| `stats/stat_pointdensity.py` | `plotnine.stats.density.{get_var_type, kde}` |
| `positions/position_beeswarm.py`, `position_quasirandom.py` | `plotnine._utils.{groupby_apply, resolution}`, `Position.{setup_params, compute_panel}` |
| `geoms/*` | `Geom.{setup_data, draw_group, draw_panel}`, `Layout.{layout, panel_params, axs}`, `Parameters.aes_params` |
| `coords/coord_axes_inside.py` | patches `plot.draw`, `coord_cartesian.__init__(expand=…)` |

### Version-tolerant code

A handful of helpers exist to absorb upstream renames rather than track them:

- `_common.py::resolve_random_state` — the same int-seed → generator conversion
  plotnine does, inlined so it does not depend on a private name.
- `positions/*.py` — the `random_state=` parameter (not `seed=`) typed with
  plotnine's public `RandomStateLike`, matching `position_jitter`.
- `guides/__init__.py::install_axis_guide_hook` — installs the axis-guide hook
  on a plot's coord at draw time, so it does not matter when a `+ coord_*()` or
  `+ facet_*()` was applied.

## Image baselines track one plotnine

Image-comparison baselines (`tests/baseline_images/`) are pixel-exact, so they
are pinned to whatever plotnine and matplotlib render. Both are now fixed:
plotnine is 0.16-only, and the `test` extra caps matplotlib at `>=3.10,<3.12`.

That cap matters. Without it, a matplotlib minor bump silently re-diffs all 44
images. The old `-mpl311` filename-suffix scheme existed to span two matplotlib
versions at once; with a single supported plotnine there is nothing to span, so
the 44 `-mpl311` files were deleted and `conftest.select_baseline_image` went
away.

To upgrade matplotlib deliberately: widen the cap in `pyproject.toml`, then
regenerate the baselines in an environment matching CI (Linux).

## Routine sync workflow

Fetch upstream (the `upstream` remote already points at `has2k1/plotnine`):

```bash
git fetch upstream --tags
```

1. **See what changed.** Compare the supported version against the latest tag,
   and skim its changelog for the coupled surfaces:
   ```bash
   git log --oneline v0.16.0a14..v0.16.0a15 -- plotnine/stats plotnine/guides \
       plotnine/facets plotnine/coords plotnine/layer.py
   ```
2. **Bump and test.** Change the floor in `pyproject.toml`, then run the suite
   against the new plotnine in a throwaway venv (see below). No code merge.
3. **Fix coupling, not composition.** Composition and animation ride the
   dependency. If tests fail, they will point at the internal-API surfaces in
   the table above.
4. **Regenerate image baselines** only if rendering legitimately changed, and do
   it in an environment matching CI.

### Test against an unreleased plotnine without touching your env

```bash
uv venv --python 3.12 .venv-pre && source .venv-pre/bin/activate
uv pip install -e ".[test]"
uv pip install --pre --upgrade "plotnine>=0.16.0a15"
uv pip install pytest && python -m pytest tests/ -q --ignore=tests/test_benchmarks.py
```

The same sequence runs as the non-blocking `prerelease` CI job, so it is worth
running locally only when a break is suspected.

## What the `upstream` remote is *not* for

The `upstream` remote is handy for reading plotnine's source, diffing internals
across versions, and cherry-picking a specific fix into a local patch. It is
**not** a branch to merge into `main`. Do not merge plotnine's source tree into
this package — that recreates the vendoring problem this whole document exists
to prevent.
