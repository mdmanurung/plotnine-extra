# CLAUDE.md

## Project Overview

plotnine-extra is a Python extension package for [plotnine](https://github.com/has2k1/plotnine) that adds extra geoms, stats, positions, themes, plot composition, and animation support. It targets plotnine 0.15.x-0.16.x and Python >= 3.10.

## Repository Structure

```
plotnine_extra/
  __init__.py          # Re-exports plotnine's API + all extras
  animation.py         # PlotnineAnimation class
  composition/         # Plot composition (Beside, Stack, Wrap, plot_layout, etc.)
  data/                # Bundled CSV datasets
  facets/              # Extended faceting (facet_nested, facet_grid2, etc.)
  geoms/               # Extra geoms (pointdensity, spoke, beeswarm, richtext, etc.)
  positions/           # Beeswarm and quasirandom positioning
  stats/               # Statistical layers (compare_means, anova, correlation, etc.)
  themes/              # Publication-ready themes (theme_pubr, theme_clean, etc.)
  utils/               # Utility functions
tests/
  conftest.py          # Test fixtures, image comparison helpers
  baseline_images/     # Reference images for visual regression tests
  test_*.py            # Test modules
docs/
  vignettes/           # Jupyter notebook tutorials
```

## Development Commands

```bash
# Install in development mode with all extras
pip install -e ".[all]"

# Run tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ -v --cov=plotnine_extra --cov-report=term-missing --cov-fail-under=50

# Lint
ruff check plotnine_extra/
ruff format --check plotnine_extra/

# Auto-fix lint issues
ruff check --fix plotnine_extra/
ruff format plotnine_extra/
```

## Code Style

- Line length: 79 characters (configured in pyproject.toml)
- Linter: ruff with rules E, F, I, TCH, Q, PIE, PTH, PD, PYI, RSE, SIM, B904, FLY, NPY, PERF102
- Import style: `from plotnine_extra import *` re-exports everything; internal modules use explicit imports
- All public symbols must be added to `_extra_all` in `__init__.py`

## Testing

- Tests use image comparison via matplotlib's `compare_images`
- `conftest.py` monkey-patches `ggplot.__eq__` and `Compose.__eq__` to compare against baseline images in `tests/baseline_images/`
- To create a new visual test: save the result image, then copy it to the appropriate `baseline_images/` subdirectory
- Default tolerance: 2 (RMS), DPI: 72
- CI runs tests on Python 3.10-3.13

## Architecture Notes

- Composition and animation modules use plotnine's internal APIs (may break with plotnine updates)
- Stats that perform hypothesis tests inherit from `_base_stat_test.py`
- Geoms that need position adjustment use `_position_geom_mixin.py`
- The `facets/strips/` subpackage handles strip label customization for extended facets

## CI/CD

- GitHub Actions: `ci.yml` runs lint + tests on push/PR to main
- `docs.yml` deploys Sphinx documentation to GitHub Pages
- `publish.yml` publishes to PyPI/TestPyPI via trusted publishing (OIDC)
