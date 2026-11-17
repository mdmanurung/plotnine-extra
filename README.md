# plotnine-extra

Extension package for [plotnine](https://github.com/has2k1/plotnine) that adds extra geoms, stats, plot composition, and animation support.

## Installation

```bash
pip install "plotnine-extra @ git+https://github.com/mdmanurung/plotnine-extra"
```

The current version (0.3.1) is not on PyPI yet.

### Requirements

`plotnine-extra` requires **plotnine 0.16** and **Python 3.11+**.

There is no stable plotnine 0.16 on PyPI yet — the latest stable is 0.15.8 and
0.16 exists only as alphas. The dependency is therefore pinned as
`plotnine>=0.16.0a15`, which lets `pip` install the pre-release without a
`--pre` flag. In other words: **installing this package puts you on a plotnine
alpha.** That is a deliberate trade for the composition, coordinate, contour
and secondary-axis features it unlocks; if you would rather stay on stable
plotnine, use plotnine directly.

This also installs `plotnine` itself as a dependency.

## Claude Code Skill

`plotnine-extra` includes a Claude Code skill with package-specific notes for
the extra geoms and stats, ggpubr-style statistical annotations, ggh4x-style
facets and guides, patchwork-style composition, and animation helpers.

The skill is bundled with the Python package. Claude Code does not scan
installed Python packages for skills, so install it once after installing or
upgrading `plotnine-extra`:

```bash
plotnine-extra-install-skills --target claude
```

This copies the skill to `~/.claude/skills/plotnine-extra/`, where it is
available to Claude Code in every project. Re-run with `--force` after upgrading
`plotnine-extra` to refresh the installed copy. Then Claude Code can use the
plotnine-extra references for tasks such as "add pairwise p-value brackets with
`stat_pwc`", "use `facet_manual` for this layout", or "compose these plots with
`plot_layout`".

The skill is a router (`SKILL.md`) that points to detailed reference files
loaded when needed. To use the bundled copy without copying files into your home
directory, point Claude Code at the package path:

```bash
export CLAUDE_SKILLS_PATH="$(plotnine-extra-install-skills --print-path)"
```

For Codex, run `plotnine-extra-install-skills --target codex`. Running
`plotnine-extra-install-skills` without `--target` installs both Claude Code and
Codex copies.

## Usage

```python
from plotnine_extra import *
```

This imports all of plotnine's public API plus the extra components provided by this package. You can also import from `plotnine` and `plotnine_extra` separately:

```python
from plotnine import ggplot, aes, geom_point
from plotnine_extra import geom_pointdensity, annotation_stripes
```

## Extra Components

### Geoms

- **`geom_pointdensity`**: Scatterplot with density estimation at each point
- **`geom_spoke`**: Line segments parameterised by location, direction, and distance
- **`annotation_stripes`**: Alternating background stripes, useful with `geom_jitter`

### Stats

- **`stat_pointdensity`**: Compute density estimation for each point

### Facets, Guides, and Strips

```python
from plotnine import ggplot, aes, geom_point, scale_x_continuous
from plotnine_extra import facet_wrap2, guide_axis_manual

(
    ggplot(df, aes("x", "y"))
    + geom_point()
    + facet_wrap2("group", scales="free_x", axes="all")
    + scale_x_continuous(
        guide=guide_axis_manual(
            breaks=[0, 5, 10],
            labels=["low", "mid", "high"],
            label_colour=["#1b9e77", "#7570b3", "#d95f02"],
        )
    )
)
```

- **`facet_grid2`**, **`facet_wrap2`**, **`facet_manual`**: Extended facet layouts with inner-axis and per-panel-scale support
- **`scale_x_facet`**, **`scale_y_facet`**: Selector-based per-panel position scales
- **`guide_axis_manual`**, **`guide_axis_colour`**, **`guide_axis_minor`**, **`guide_axis_logticks`**, **`guide_axis_truncated`**, **`guide_axis_scalebar`**, **`guide_axis_nested`**, **`guide_dendro`**: Matplotlib-backed axis guides for the extended facets
- **`guide_stringlegend`**: Text-only color/fill legend
- **`strip_nested`**, **`strip_themed`**, **`strip_split`**, **`strip_tag`**: Constructor-compatible strip descriptors; direct strip drawing is partial where plotnine does not expose the required strip-side hooks

### Plot Composition

Plot composition is provided by plotnine itself; `plotnine_extra` re-exports it
so these names are importable from one place. The composing operators come from
plotnine's own `ggplot`, so they never conflict with the composition objects.

All of it is available: plotnine 0.16 is this package's minimum, so there is no
version gating to work around.

Compose multiple plots using operators:

- `|`: Arrange plots side by side (`Beside`)
- `/`: Arrange plots vertically (`Stack`)
- `+`: Arrange plots in a 2D grid (`Wrap`)
- `-`: Arrange plots side by side at the same nesting level
- `&`: Add to all plots in a composition
- `*`: Add to top-level plots only

```python
from plotnine import ggplot, aes, geom_point
from plotnine.data import mtcars
from plotnine_extra import plot_layout, plot_annotation

p1 = ggplot(mtcars, aes("wt", "mpg")) + geom_point()
p2 = ggplot(mtcars, aes("hp", "mpg")) + geom_point()

# Side by side
p1 | p2

# Stacked
p1 / p2

# With layout control
(p1 | p2) + plot_layout(widths=[1, 2])

# With annotation
(p1 | p2) + plot_annotation(title="My Composition")
```

Additional composition classes and functions:
- **`Compose`**: Base class for compositions
- **`Beside`**, **`Stack`**, **`Wrap`**: Composition subclasses
- **`plot_layout`**: Customise composition layout (nrow, ncol, widths, heights)
- **`plot_annotation`**: Add title, subtitle, caption, footer to compositions
- **`plot_spacer`**: Add blank space in compositions
- **`guide_area`**: Reserve space in a composition for a guide
- **`inset_element`**: Place an inset axes inside a composition

### Animation

```python
from plotnine import ggplot, aes, geom_point, lims
from plotnine_extra import PlotnineAnimation

plots = [
    ggplot(data_frame_i, aes("x", "y")) + geom_point() + lims(x=(0, 10), y=(0, 10))
    for data_frame_i in frames
]

ani = PlotnineAnimation(plots, interval=200)
ani.save("animation.gif")
```

### Inherited from plotnine 0.16

Because the package re-exports plotnine's whole public API, everything plotnine
0.16 added is available from `plotnine_extra` too, with no code of our own:

- **Coordinates**: `coord_polar`, `coord_radial`
- **Secondary axes**: `sec_axis`, `dup_axis`
- **Contours**: `geom_contour`, `geom_contour_filled`, `geom_density_2d_filled`,
  `stat_contour`, `stat_contour_filled`, `stat_density_2d_filled`
- **Literal aesthetic values**: `I(...)`

## Compatibility

- Requires Python ≥ 3.11
- Requires plotnine ≥ 0.16.0a15 (there is no stable 0.16 yet; see
  [Requirements](#requirements))

> **Note:** Composition and animation delegate to plotnine's own implementations,
> so they track upstream automatically. Some stat/guide/facet helpers still use
> plotnine's internal APIs and need adjustment across plotnine releases — see
> [`UPSTREAM_SYNC.md`](UPSTREAM_SYNC.md) for the current list and how syncing
> works. Private plotnine names are gathered in `plotnine_extra/_compat.py` and
> checked by `pytest -m canary`.

## Development

```bash
git clone https://github.com/mdmanurung/plotnine-extra.git
cd plotnine-extra
pip install -e ".[all]"
```

### Testing

```bash
python -m pytest tests/ --ignore=tests/test_benchmarks.py
python -m pytest -m canary   # fast checks of the plotnine coupling
```

See [`UPSTREAM_SYNC.md`](UPSTREAM_SYNC.md) for `plotnine_extra/_compat.py` and
the `downstream` CI job.

## Publishing to PyPI

This project uses [trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC) via GitHub Actions. No API tokens are needed.

### One-time setup

1. **Create accounts** on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)

2. **Add trusted publishers** on both PyPI and TestPyPI:
   - Go to your account → Publishing → Add a new pending publisher
   - Fill in:
     - **PyPI project name:** `plotnine-extra`
     - **Owner:** `mdmanurung`
     - **Repository:** `plotnine-extra`
     - **Workflow name:** `publish.yml`
     - **Environment name:** `pypi` (for PyPI) or `testpypi` (for TestPyPI)

3. **Create GitHub environments** in your repository settings:
   - Go to Settings → Environments
   - Create two environments: `pypi` and `testpypi`

### How to publish

- **To TestPyPI:** Go to Actions → "Publish to PyPI / TestPyPI" → Run workflow → select `testpypi`
- **To PyPI:** Create a GitHub Release tagged exactly as `vX.Y.Z` for the version in `pyproject.toml` (for this release candidate, `v0.3.1`). Publishing starts after artifact validation.

### Version bumping

Before publishing a new version, update the version in both:
- `pyproject.toml` → `version = "X.Y.Z"`
- `plotnine_extra/__init__.py` → `__version__ = "X.Y.Z"`

## License

MIT License (same as plotnine)
