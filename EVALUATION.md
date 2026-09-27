# Codebase Evaluation and Feature Notes for plotnine-extra

Historical note: the body of this document is an April 2026 planning snapshot,
kept for background. The **Test & Quality Metrics** table and **Part 5
(Performance)** are current as of the plotnine 0.16 sync; the rest should not be
read as the current release assessment. Use the API reference, vignettes, and
test suite for current behaviour.

## Context

plotnine-extra (v0.1.0 at the time of this snapshot) is a Python extension
package for plotnine that adds geoms, stats, positions, composition, facets,
animation, and themes. It ports functionality from several R ggplot2 extension
packages (ggpubr, ggbeeswarm, ggtext, ggrepel, gghalves, patchwork, ggh4x)
while adding Python-specific features.

---

## Part 1: Codebase Evaluation

### Architecture: A- (modular, with minor gaps)

- Modular structure: `geoms/`, `stats/`, `positions`, `composition/`, `facets/`, `themes/`, `utils/`, `data/`
- ~9.6K lines across 70 modules, average ~137 lines/module (well-decomposed)
- Separation of concerns: private helpers (`_*.py`), public API in `__init__.py`
- Uses established patterns: template method (`_base_stat_test`), mixins (`_PositionGeomMixin`), factories
- Re-exports plotnine's API via `from plotnine import *` for drop-in usage
- **Snapshot gap:** At this snapshot, the `facets/strips/` subpackage had 4 stub classes (`strip_nested`, `strip_split`, `strip_tag`, `strip_themed`) that were exported but had unimplemented `draw()`/`setup()` methods. The main facet classes were implemented.

### Code Quality: A-

**Strengths:**
- Docstrings on public classes/functions
- Modern Python: type hints with `TYPE_CHECKING` guards, `@dataclass`, f-strings
- Consistent use of plotnine conventions (`REQUIRED_AES`, `DEFAULT_AES`, `DEFAULT_PARAMS`, `@document`)
- Clean operator overloading in composition module (`|`, `/`, `+`, `-`, `&`, `*`)
- Error handling uses descriptive messages
- Version compatibility checking at import time warns about untested plotnine versions

**Weaknesses:**
- Markdown parser in `geom_richtext.py` uses regex; this is fragile for complex nested markup
- `geom_richtext` and `geom_textbox` share duplicated bbox construction and color handling logic (both files have near-identical code blocks rather than a shared utility)
- R-style dot-separated method names (`"wilcox.test"`, `"t.test"`, `"kruskal.test"`) are used instead of Python `snake_case` conventions. This preserves API parity with R/ggpubr but may confuse Python-native users.
- `geom_half_violin.draw_group()` has low test coverage (19.3%); most rendering paths were untested in this snapshot

### API Design: A

- Follows plotnine/ggplot2 conventions closely
- Intuitive composition operators that mirror patchwork's API
- `stat_pvalue_manual` is a function (returns layers) rather than a stat class. This is inconsistent with the name but practical for the returned layer set.
- Consistent parameter naming and defaults throughout
- 12 geoms, 16 stats, 2 positions, 5 themes, and full composition API exported

### Test Coverage: B+ (Improved)

- 13 test files, 331 test cases (297 passed, 34 skipped)
- Overall coverage: **68.4%** (up from estimated ~50%)
- Focused algorithmic coverage (beeswarm, van der Corput, p-value formatting)
- Visual regression infrastructure with baseline image comparison
- New `test_new_features.py` covers geom_text_repel, geom_label_repel, geom_half_boxplot, geom_half_violin, facets, themes, and Hommel correction
- **Remaining gaps:**
  - `facets/strips/` module: 0% coverage (all stubs)
  - `geom_half_violin`: 19.3% coverage (draw_group untested)
  - `facet_manual`: 12.0%, `facet_nested`: 13.0%, `facet_nested_wrap`: 19.2% (layout/rendering paths largely untested)
  - `facetted_pos_scales`: 29.7%, `scale_facet`: 24.2%
- CI enforces 50% minimum threshold via `--cov-fail-under=50`

### Documentation: B

- README with installation, usage examples, and composition operator documentation
- Sphinx docs with furo theme, deployed to GitHub Pages
- 3 Jupyter notebook vignettes (basic barplots, beeswarm, stat_pwc)
- **Missing:** No CHANGELOG, no CONTRIBUTING guide, no migration/upgrade notes
- **Gap:** Many components (facets, themes, repel geoms, half geoms, most stats) lack vignettes

### CI/CD: A

- Full pipeline: lint (ruff), test (Python 3.10-3.13), notebook execution, docs deployment
- OIDC trusted publishing to PyPI
- Proper matrix testing across Python versions

### Dependencies: A

- Minimal: only plotnine + scipy as core dependencies
- scipy is justified for statistical tests and KDE

---

## Part 2: Bugs and Issues to Fix

The issues below were current for this snapshot and may have changed in later
releases.

### Resolved Bugs (from previous evaluation)

| Bug | Status | Details |
|-----|--------|---------|
| Facets module entirely unimplemented | **Fixed** | All 8 main facet/scale classes are now fully implemented with `compute_layout()`, `init_scales()`, `make_strips()`, etc. |
| `geom_bracket` bypasses `coord.transform()` | **Fixed** | `draw_group()` now calls `coord.transform()` on both bracket and label data before drawing |
| `stat_pwc` silently falls back to Bonferroni for Hommel | **Fixed** | Hommel correction is fully implemented with a proper step-down procedure (no silent fallback) |
| Unused `_plotnine_version` import | **Fixed** | Now used at import time to warn about untested plotnine versions |

### Current Issues

#### Issue 1: Strip classes are unimplemented stubs
- **Files:** `plotnine_extra/facets/strips/strip_nested.py`, `strip_split.py`, `strip_tag.py`, `strip_themed.py`
- **Issue:** Each class has `__init__()` but `draw()` and/or `setup()` methods contain only `# TODO` comments. All 4 are exported in the public API but non-functional.
- **Coverage:** 0% across all strip files
- **Priority:** Medium: either implement or remove from public API

#### Issue 2: Duplicated bbox construction between geom_richtext and geom_textbox
- **Files:** `plotnine_extra/geoms/geom_richtext.py` (lines ~182-196), `plotnine_extra/geoms/geom_textbox.py` (lines ~110-124)
- **Issue:** Near-identical bbox construction and color handling code duplicated across both files. `geom_textbox` imports `_parse_markdown` from `geom_richtext` but bbox logic is copy-pasted.
- **Priority:** Low: refactor into shared utility

#### Issue 3: Low coverage on facet rendering paths
- **Files:** `facet_manual.py` (12.0%), `facet_nested.py` (13.0%), `facet_nested_wrap.py` (19.2%)
- **Issue:** Facet classes are implemented but their `compute_layout()`, `map()`, `make_strips()` methods are largely untested. Regressions could go undetected.
- **Priority:** Medium: add rendering/layout tests

#### Issue 4: geom_half_violin rendering untested
- **File:** `plotnine_extra/geoms/geom_half_violin.py` (19.3% coverage)
- **Issue:** `draw_group()` (lines 63-140) is not exercised by tests. The half-clipping and polygon construction logic is unverified.
- **Priority:** Medium: add visual regression test

#### Issue 5: Regex-based markdown parser is fragile
- **File:** `plotnine_extra/geoms/geom_richtext.py` (lines 48-108)
- **Issue:** The `_parse_markdown()` function uses regex for `<br>`, `<sup>`, `<sub>`, `**bold**`, `*italic*` parsing. Nested markup or edge cases (e.g., `**bold *and italic***`) may produce incorrect results.
- **Priority:** Low: works for common cases, but fragile for complex input

---

## Part 3: Feature Proposals

### Features Already Implemented (from previous proposals)

The following previously proposed features have been completed:

| Feature | Status | Files |
|---------|--------|-------|
| `geom_text_repel` / `geom_label_repel` | **Implemented** | `geoms/geom_text_repel.py` (464 lines, force-directed algorithm) |
| `geom_half_violin` / `geom_half_boxplot` | **Implemented** | `geoms/geom_half_violin.py` (140 lines), `geoms/geom_half_boxplot.py` (86 lines) |
| Publication themes gallery | **Implemented** | `themes/theme_pub.py`: `theme_pubr`, `theme_clean`, `theme_scientific`, `theme_nature`, `theme_poster` |
| Version compatibility layer | **Implemented** | `__init__.py` warns at import time for untested plotnine versions |

### Remaining Feature Proposals

#### Priority 1: High Impact, Moderate Effort

##### 1. `stat_density_ridges` / `geom_ridgeline`: Port of ggridges

- **What:** Ridgeline plots (joy plots): stacked density curves offset by a grouping variable
- **Why:** Popular for comparing distributions across many groups (time series, categories)
- **Approach:** Compute KDE per group, offset y-position, handle overlap/fill
- **Files:** `plotnine_extra/geoms/geom_ridgeline.py`, `plotnine_extra/stats/stat_density_ridges.py`

##### 2. `scale_color_paletteer` / `scale_fill_paletteer`: Expanded color palettes

- **What:** Access to 2000+ color palettes (viridis, journal palettes, ColorBrewer, etc.)
- **Why:** plotnine has limited built-in palettes; scientists often need specific journal-style palettes
- **Approach:** Bundle palette definitions as data, create scale wrappers for Nature, Science, JAMA, Lancet, etc.
- **Files:** `plotnine_extra/scales/`, `plotnine_extra/data/palettes/`

##### 3. `geom_mark_ellipse` / `geom_mark_hull` / `geom_mark_rect`: Port of ggforce marks

- **What:** Annotate groups of points with enclosing shapes (ellipses, convex hulls, rectangles) with labels
- **Why:** Useful for highlighting clusters in scatter plots. `stat_chull` and `stat_conf_ellipse` exist but lack polished annotation layers
- **Approach:** Build on existing `stat_chull` and `stat_conf_ellipse`, add label placement and styling
- **Files:** `plotnine_extra/geoms/geom_mark_ellipse.py`, `geom_mark_hull.py`, `geom_mark_rect.py`

#### Priority 2: High Impact, Lower Effort

##### 4. Implement strip classes

- **What:** Complete the 4 stub strip classes: `strip_nested`, `strip_split`, `strip_tag`, `strip_themed`
- **Why:** These are exported in the public API but non-functional, and facet customization is incomplete without them
- **Approach:** Implement `draw()` and `setup()` methods following the existing `Strip` base class contract
- **Files:** `plotnine_extra/facets/strips/strip_*.py`

##### 5. `annotation_custom`: Arbitrary grob/artist placement

- **What:** Place arbitrary matplotlib artists (images, tables, inset plots) at specific coordinates
- **Why:** Enables inset plots, logo placement, and image annotations, which are common in publication figures
- **Approach:** Wrap matplotlib's `add_artist()` with ggplot-style coordinate system
- **Files:** `plotnine_extra/geoms/annotation_custom.py`

##### 6. `geom_signif`: Simplified significance brackets

- **What:** A simpler alternative to `stat_pwc` for adding significance brackets between groups
- **Why:** `stat_pwc` has many options, while many plots only need a bracket with a star between two groups
- **Approach:** Wrapper around existing `geom_bracket` with automatic y-positioning and stacking
- **Files:** Could be a convenience function in `utils/`

#### Priority 3: Novel Python-Specific Features

##### 7. Interactive plot export: HTML/Plotly bridge

- **What:** `to_plotly()` or `to_interactive()` method that converts a plotnine plot to an interactive Plotly figure
- **Why:** Python users often expect interactive output, and a plotnine-to-Plotly bridge would address that workflow
- **Approach:** Extract data and aesthetics from built plot, reconstruct in Plotly
- **Effort:** High

##### 8. `stat_smooth_gam`: GAM smoothing

- **What:** Generalized Additive Model smoothing using pyGAM or scipy
- **Why:** plotnine's `stat_smooth` supports lm/loess but not GAMs. Scientists need non-linear smoothing
- **Approach:** Integrate with pyGAM (optional dependency)
- **Files:** `plotnine_extra/stats/stat_smooth_gam.py`

##### 9. `geom_waffle`: Waffle charts

- **What:** Waffle/square pie charts as an alternative to pie charts
- **Why:** Popular for showing proportions in an accessible way; no plotnine implementation
- **Approach:** Grid of colored squares using geom_tile internally
- **Files:** `plotnine_extra/geoms/geom_waffle.py`

##### 10. `stat_slabinterval` / `geom_slabinterval`: Port of ggdist

- **What:** Slab+interval plots, eye plots, half-eye plots for distributional visualization
- **Why:** Useful for Bayesian analysis workflows in Python
- **Files:** `plotnine_extra/stats/stat_slabinterval.py`, `plotnine_extra/geoms/geom_slabinterval.py`

##### 11. `geom_sankey` / `geom_alluvial`: Flow diagrams

- **What:** Sankey/alluvial flow diagrams showing categorical transitions
- **Why:** Increasingly used in data journalism and scientific papers
- **Effort:** High, but unique in the plotnine ecosystem

##### 12. DataFrame `.plot_gg` accessor: Python API

- **What:** Register a pandas accessor: `df.plot_gg.scatter("x", "y", color="group")`
- **Why:** Uses pandas' accessor pattern for a Python-native API
- **Files:** `plotnine_extra/pandas_accessor.py`

##### 13. `coord_radar`: Radar/spider charts

- **What:** Radar chart coordinate system for multi-variate comparison
- **Why:** Commonly requested, no plotnine solution exists

---

## Part 4: Quality & Infrastructure Improvements

| # | Improvement | Impact | Effort | Details |
|---|-------------|--------|--------|---------|
| Q1 | Implement or remove strip stubs | High | Medium | 4 strip classes with TODO-only methods are exported publicly |
| Q2 | Raise coverage to 70%+ | Medium | Medium | Current: 68.4%. Add tests for facet rendering paths (12-19%), geom_half_violin (19%), strip classes (0%) |
| Q3 | Raise CI threshold | Low | Trivial | Currently `--cov-fail-under=50`; raise to 65% or 70% to match actual coverage |
| Q4 | Add facet visual regression tests | High | Medium | `facet_manual`, `facet_nested`, `facet_nested_wrap` rendering is largely untested |
| Q5 | Extract shared bbox utilities | Low | Low | Deduplicate bbox construction between `geom_richtext` and `geom_textbox` |
| Q6 | Expand vignettes | High | Medium | Add vignettes for composition layouts, facets, repel geoms, half geoms, themes, and statistical annotations |
| Q7 | Add CHANGELOG.md | Medium | Low | No release notes exist; important for library consumers |
| Q8 | Add CONTRIBUTING.md | Medium | Low | No contribution guide; would help onboard contributors |

---

## Implementation Priority Summary

### Current Issues (Fix First)

| Issue | Severity | Effort | Coverage |
|-------|----------|--------|----------|
| Strip classes are stubs | Medium | Medium | 0% |
| Facet rendering paths untested | Medium | Medium | 12-19% |
| `geom_half_violin` rendering untested | Medium | Low | 19.3% |
| Duplicated bbox code | Low | Low | N/A |
| Regex markdown parser fragile | Low | Medium | N/A |

### New Features

| # | Feature | Impact | Effort | Category |
|---|---------|--------|--------|----------|
| 1 | Ridgeline plots | High | Medium | Geom/Stat |
| 2 | Expanded color palettes | High | Low | Scale |
| 3 | Mark geoms (ellipse/hull/rect) | Medium | Medium | Geom |
| 4 | Complete strip classes | Medium | Medium | Facet |
| 5 | `annotation_custom` (inset plots) | Medium | Medium | Geom |
| 6 | Simplified significance brackets | Medium | Low | Util |
| 7 | Interactive Plotly bridge | Very High | Very High | Python API |
| 8 | GAM smoothing | Medium | Medium | Stat |
| 9 | Waffle charts | Medium | Low | Geom |
| 10 | `stat_slabinterval` (ggdist) | High | Large | Stat |
| 11 | Sankey/alluvial diagrams | Medium | High | Geom |
| 12 | DataFrame `.plot_gg` accessor | Medium | Small | Python API |
| 13 | `coord_radar` | Medium | Medium | Coord |

### Test & Quality Metrics

Refreshed after the plotnine 0.16 sync. The numbers in the April 2026 body of
this document are superseded by the table below.

| Metric | Current | Previous snapshot |
|--------|---------|-------------------|
| Test cases | 595 passing, 0 skipped | 331 (297 pass, 34 skip) |
| Test functions | 583 | 331 |
| Test files | 26 | 13 |
| Overall coverage | 79.9% | 68.4% |
| CI coverage threshold | 50% | 50% |
| CI Python matrix | 3.11, 3.12, 3.13 | 3.10 - 3.13 |
| Vignettes | 7 | 3 |
| Package size | ~16,800 lines | ~9,600 lines |

## Part 5: Performance

This section did not exist in the previous evaluation, which rated
"Dependencies: A" on the strength of having only two core dependencies and
never measured anything. There was no benchmark suite, no profiling script, and
no timing code anywhere in the repository; `.benchmarks/` was an empty,
untracked directory and the `benchmarks` entry in `.gitignore` was inherited
verbatim from plotnine.

Nothing was slow *visibly* because **no test in the suite drew more than
n=100 points**, which is small enough that every quadratic path in the package
looks instantaneous. The costs were found by reading the implementations.

### Fixed

| Path | Problem | Complexity | Result |
| --- | --- | --- | --- |
| `geoms/geom_text_repel.py` | Triple-nested Python loop (`max_iter` x labels x labels), with `np.sqrt` on NumPy scalars in the innermost body | Theta(1000 * n^2) Python iterations | KD-tree neighbour search + vectorised force accumulation. **41x at n=40, 177x at n=200**; n=1500 dropped from minutes to ~3s |
| `geoms/geom_polygonraster.py` | `data.iloc[[i]].to_dict("records")[0]` per raster cell, then 4 dict copies, then a DataFrame built from 4n dicts | Linear, ~30-60 us per cell | Broadcast the shared columns. **33.3s -> 19.5ms (1700x) at n=50,000**, identical output |
| `positions/_beeswarm_algorithms.py` `_swarm` | `np.append` inside the placement loop reallocated and copied both buffers on every one of the n iterations | Theta(n^2) time *and* Theta(n^2) allocation traffic | Preallocated buffers with a write cursor |
| `positions/_beeswarm_algorithms.py` `_swarm_place` / `_compact_place` | 2k+1 candidates, each tested in its own NumPy call against all k neighbours | Theta(n^3) worst case | One broadcast (candidates x neighbours) comparison. **4-22x on tied data**, bit-identical output |
| `positions/_beeswarm_algorithms.py` `_kde_density` | `gaussian_kde` evaluated at every observation, materialising an n x n kernel matrix | Theta(n^2) time and peak memory, per group | Evaluate on a grid growing like sqrt(n), then interpolate. **8x at n=10,000**, max error < 1e-4 |
| `stats/_common.py` `paired_values_by_wid` | A full `pivot_table` plus a full-frame `isin` copy re-done once per comparison pair | Theta(C * n * pivot) | Pivot once, index per pair. **~10x for 28 pairs over 32,000 rows**, identical results |
| `stats/stat_compare.py` (`overall=True`) | `data.copy()` -- a full deep copy -- inside the per-level loop | Theta(G * n) deep copies | Group once and slice |
| `stats/stat_compare.py` (pairwise) | `data["x"] == a` mask rebuilt per comparison, each group re-extracted once per pair | Theta(C * n) | Group once |
| `stats/stat_compare.py` `_run_test` | `d["y"].dropna()` evaluated twice per group | Theta(2n) | Materialise once |
| `geoms/geom_textbox.py`, `geom_richtext.py` | `data.iloc[i]` built a whole pandas Series per label | Linear, large constant | Pre-extract the columns once |

The beeswarm, `stat_compare`, and `geom_polygonraster` changes are all verified
**bit-identical** to the previous output. The repulsion rewrite is the one place
where output legitimately differs: it converges to a different local optimum,
resolving slightly fewer label collisions at n=40 (18 vs 12 of 73) and
noticeably more at n >= 200.

### Infrastructure added

- `pytest-benchmark` in the `test` extra, and `tests/test_benchmarks.py`: 41
  benchmarks over the paths above, at n = 100 / 1,000 / 10,000 (repulsion uses
  100 / 500 / 1,000, since it is seconds per call).
  ```bash
  pytest tests/test_benchmarks.py --benchmark-only
  ```
  CI runs these into a `bench.json` artifact.
- `tests/test_performance_paths.py`: 22 correctness tests pinning the optimised
  paths, since a fast wrong answer is worse than a slow right one. It also pins
  the error behaviour of the paired-test pivot (incomplete pairs, duplicate
  subjects), which the pivot hoist could plausibly have changed.
- Matplotlib is now capped at `>=3.10,<3.12` in the `test` extra. The image
  baselines are pixel-exact, so an unpinned matplotlib silently re-diffs all 44
  of them. This replaces the old `-mpl311` filename-suffix scheme, which existed
  only to span two matplotlib versions at once.
- The benchmark suite is excluded from the main CI lane (`--ignore=
  tests/test_benchmarks.py`) so calibration cannot make the gating job flaky.

### Still slow, deliberately

- `_repel_labels` remains superlinear in the number of labels: a KD-tree bounds
  each query to a neighbourhood, but with many labels packed into one panel the
  neighbourhood is large, so cost still grows faster than linearly. n=3000 takes
  ~140s. Making that faster needs a real collision-resolution scheme (e.g.
  simulated annealing with a Barnes-Hut approximation), not a tighter loop.
- `geom_text_repel` creates two Matplotlib artists per label, which slows
  `savefig` and interactive redraw independently of the layout algorithm.
