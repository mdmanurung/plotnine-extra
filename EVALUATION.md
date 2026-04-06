# Comprehensive Codebase Evaluation & Feature Proposals for plotnine-extra

## Context

plotnine-extra (v0.1.0) is a Python extension package for plotnine that adds extra geoms, stats, composition, facets, animation, and themes. It ports functionality from several R ggplot2 extension packages (ggpubr, ggbeeswarm, ggtext, patchwork) while adding some novel Python-specific features. This evaluation assesses the current state and proposes features to improve usability and novelty.

---

## Part 1: Codebase Evaluation

### Architecture: A (Excellent)

- Clean modular structure: `geoms/`, `stats/`, `positions/`, `composition/`, `facets/`, `themes/`, `utils/`, `data/`
- ~10K lines across 80+ modules, average 125 lines/module (well-decomposed)
- Proper separation of concerns: private helpers (`_*.py`), public API in `__init__.py`
- Good use of design patterns: template method (`_base_stat_test`), mixins (`_PositionGeomMixin`), factories
- Re-exports plotnine's entire API via `from plotnine import *` for seamless drop-in usage

### Code Quality: A-

**Strengths:**
- Comprehensive docstrings on all public classes/functions
- Modern Python: type hints with `TYPE_CHECKING` guards, `@dataclass`, f-strings
- Consistent use of plotnine conventions (`REQUIRED_AES`, `DEFAULT_AES`, `DEFAULT_PARAMS`, `@document`)
- Clean operator overloading in composition module (`|`, `/`, `+`, `-`, `&`, `*`)
- Good error handling with descriptive messages

**Weaknesses:**
- `_plotnine_version` imported but unused (line 67 of `__init__.py`)
- Some modules could benefit from more inline comments on non-obvious math (e.g., beeswarm algorithms)
- Markdown parser in `geom_richtext.py` uses regex - fragile for complex nested markup

### API Design: A

- Follows plotnine/ggplot2 conventions exactly - users familiar with R equivalents will feel at home
- Intuitive composition operators that mirror patchwork's API
- `stat_pvalue_manual` is a function (returns layers) rather than a stat class - inconsistent but pragmatic
- Good parameter naming and defaults throughout

### Test Coverage: B-

- 12 test files, 200+ test cases
- Strong algorithmic coverage (beeswarm, van der Corput, p-value formatting)
- Good visual regression infrastructure with baseline image comparison
- **Critical gap:** Facets module has ZERO test coverage (8 modules untested)
- **Missing:** No tests for `geom_bracket` rendering, limited edge cases
- 50% minimum coverage threshold is low for a library

### Documentation: B

- Good README with installation, usage examples, and composition operator documentation
- Sphinx docs with furo theme, deployed to GitHub Pages
- 3 Jupyter notebook vignettes (basic barplots, beeswarm, stat_pwc)
- **Missing:** No CHANGELOG, no CONTRIBUTING guide, no migration/upgrade notes
- **Gap:** Many components (facets, themes, utils, most stats) lack vignettes

### CI/CD: A

- Full pipeline: lint (ruff), test (Python 3.10-3.13), notebook execution, docs deployment
- OIDC trusted publishing to PyPI
- Proper matrix testing across Python versions

### Dependencies: A

- Minimal: only plotnine + scipy as core dependencies
- scipy is justified for statistical tests and KDE

---

## Part 2: Feature Proposals

### Priority 1: High Impact, Moderate Effort

#### 1. `geom_text_repel` / `geom_label_repel` (text/label repulsion) -- Port of ggrepel

- **What:** Automatically position text labels to avoid overlapping each other and data points
- **Why:** This is the #1 most-used ggplot2 extension in R. Currently plotnine has no label repulsion. This would be the single highest-impact addition
- **Approach:** Implement simulated annealing or force-directed algorithm for label placement
- **Files:** `plotnine_extra/geoms/geom_text_repel.py`, `plotnine_extra/geoms/geom_label_repel.py`
- **Effort:** High (algorithmic complexity), but enormous value

#### 2. `geom_half_violin` / `geom_half_boxplot` / `geom_half_point` -- Port of gghalves

- **What:** Split geoms that show half of a distribution (e.g., half violin + half boxplot side-by-side)
- **Why:** Raincloud plots (half-violin + jitter + boxplot) are increasingly popular in scientific publications; no Python ggplot solution exists
- **Approach:** Modify existing plotnine geom_violin to clip at midpoint, combine with position adjustments
- **Files:** `plotnine_extra/geoms/geom_half_violin.py`, `plotnine_extra/geoms/geom_half_boxplot.py`

#### 3. `stat_density_ridges` / `geom_ridgeline` -- Port of ggridges

- **What:** Ridgeline plots (joy plots) - stacked density curves offset by a grouping variable
- **Why:** Popular for comparing distributions across many groups (e.g., time series, categories)
- **Approach:** Compute KDE per group, offset y-position, handle overlap/fill
- **Files:** `plotnine_extra/geoms/geom_ridgeline.py`, `plotnine_extra/stats/stat_density_ridges.py`

#### 4. `scale_color_paletteer` / `scale_fill_paletteer` -- Expanded color palettes

- **What:** Access to 2000+ color palettes from R's paletteer package (viridis, scientific journal palettes, ColorBrewer, etc.)
- **Why:** plotnine has limited built-in palettes; scientists often need specific journal-style palettes
- **Approach:** Bundle palette definitions as data, create scale wrappers. Palettes for Nature, Science, JAMA, Lancet, etc.
- **Files:** `plotnine_extra/scales/`, `plotnine_extra/data/palettes/`

### Priority 2: High Impact, Lower Effort

#### 5. `geom_mark_ellipse` / `geom_mark_hull` / `geom_mark_rect` -- Port of ggforce marks

- **What:** Annotate groups of points with enclosing shapes (ellipses, convex hulls, rectangles) with labels
- **Why:** Useful for highlighting clusters in scatter plots. `stat_chull` and `stat_conf_ellipse` exist but lack the polished annotation layer
- **Approach:** Build on existing `stat_chull` and `stat_conf_ellipse`, add label placement and styling
- **Files:** `plotnine_extra/geoms/geom_mark_ellipse.py`, `geom_mark_hull.py`, `geom_mark_rect.py`

#### 6. `annotation_custom` -- Arbitrary grob/artist placement

- **What:** Place arbitrary matplotlib artists (images, tables, inset plots) at specific data or normalized coordinates
- **Why:** Enables inset plots, logo placement, image annotations - common in publication figures
- **Approach:** Wrap matplotlib's `add_artist()` with ggplot-style coordinate system
- **Files:** `plotnine_extra/geoms/annotation_custom.py`

#### 7. `geom_signif` -- Simplified significance brackets

- **What:** A simpler alternative to `stat_pwc` for adding significance brackets between groups
- **Why:** `stat_pwc` is powerful but complex; many users just want "add a bracket with a star between group A and B"
- **Approach:** Wrapper around existing `geom_bracket` with automatic y-positioning and stacking
- **Files:** Could be a convenience function in `utils/`

#### 8. Pre-built theme gallery -- `theme_pubr`, `theme_scientific`, `theme_nature`, etc.

- **What:** Publication-ready themes matching journal style guides
- **Why:** ggpubr's `theme_pubr()` is extremely popular; scientists want one-line publication formatting
- **Approach:** Define themes using plotnine's theme system with appropriate fonts, sizes, grid lines
- **Files:** `plotnine_extra/themes/theme_pubr.py`, `theme_scientific.py`, etc.

### Priority 3: Novel Python-Specific Features

#### 9. Interactive plot export -- HTML/Plotly bridge

- **What:** `to_plotly()` or `to_interactive()` method that converts a plotnine plot to an interactive Plotly figure
- **Why:** This would be genuinely novel - no R package does ggplot2-to-plotly as cleanly. Python users expect interactivity
- **Approach:** Extract data and aesthetics from built plot, reconstruct in Plotly
- **Effort:** High, but very differentiating

#### 10. `stat_smooth_gam` -- GAM smoothing

- **What:** Generalized Additive Model smoothing using pyGAM or scipy
- **Why:** plotnine's `stat_smooth` supports lm/loess but not GAMs. Scientists need non-linear smoothing
- **Approach:** Integrate with pyGAM (optional dependency) for flexible smoothing
- **Files:** `plotnine_extra/stats/stat_smooth_gam.py`

#### 11. `geom_waffle` -- Waffle charts

- **What:** Waffle/square pie charts as an alternative to pie charts
- **Why:** Popular for showing proportions in an accessible way; no plotnine implementation
- **Approach:** Grid of colored squares using geom_tile internally
- **Files:** `plotnine_extra/geoms/geom_waffle.py`

#### 12. `stat_summary_bin2d` -- 2D binned summaries

- **What:** Apply arbitrary summary functions to 2D bins (not just count)
- **Why:** Useful for large datasets where per-point rendering is impractical
- **Approach:** Extend plotnine's stat_bin_2d with custom summary functions
- **Files:** `plotnine_extra/stats/stat_summary_bin2d.py`

#### 13. `geom_sankey` / `geom_alluvial` -- Flow diagrams

- **What:** Sankey/alluvial flow diagrams showing categorical transitions
- **Why:** Increasingly used in data journalism and scientific papers
- **Effort:** High, but unique in the plotnine ecosystem

### Priority 4: Quality & Infrastructure Improvements

#### 14. Facets module test coverage

- Add tests for `facet_grid2`, `facet_wrap2`, `facet_manual`, `facet_nested`, `facet_nested_wrap`
- Add tests for `facetted_pos_scales`, `scale_facet`, and all strip variants
- Currently the only major module with ZERO tests

#### 15. Raise test coverage threshold to 70%+

- Current minimum is 50% - should be higher for a library
- Add visual regression tests for `geom_bracket`, `geom_richtext`, `geom_textbox`
- Add edge case tests (empty data, single observations, NaN handling)

#### 16. Expand vignettes and documentation

- Add vignettes for: composition advanced usage, facets, statistical annotations workflow, animation
- Add a gallery page showing every geom/stat with output images
- Add CHANGELOG.md and CONTRIBUTING.md

#### 17. Version compatibility layer

- The README warns about internal API usage. Add `plotnine_version_check()` at import time that warns about untested plotnine versions
- The `_plotnine_version` import exists but is unused - wire it up

---

## Implementation Priority Summary

| # | Feature | Impact | Effort | Category |
|---|---------|--------|--------|----------|
| 1 | `geom_text_repel` / `geom_label_repel` | Very High | High | Geom |
| 2 | Half geoms (raincloud plots) | High | Medium | Geom |
| 3 | Ridgeline plots | High | Medium | Geom/Stat |
| 4 | Expanded color palettes | High | Low | Scale |
| 5 | Mark geoms (ellipse/hull/rect) | Medium | Medium | Geom |
| 6 | `annotation_custom` (inset plots) | Medium | Medium | Geom |
| 7 | Simplified significance brackets | Medium | Low | Util |
| 8 | Publication themes gallery | High | Low | Theme |
| 9 | Interactive Plotly bridge | Very High | Very High | Novel |
| 10 | GAM smoothing | Medium | Medium | Stat |
| 11 | Waffle charts | Medium | Low | Geom |
| 12 | 2D binned summaries | Low | Low | Stat |
| 13 | Sankey/alluvial diagrams | Medium | High | Geom |
| 14 | Facets test coverage | High | Medium | Testing |
| 15 | Raise coverage to 70%+ | Medium | Medium | Testing |
| 16 | Expand vignettes | High | Medium | Docs |
| 17 | Version compatibility | Low | Low | Infra |
