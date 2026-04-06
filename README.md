# plotnine-extra

Extra geoms, stats, scales, and more for [plotnine](https://github.com/has2k1/plotnine) — a Grammar of Graphics extension package.

## What is plotnine-extra?

`plotnine-extra` is a companion package for [plotnine](https://plotnine.readthedocs.io/) that provides additional ggplot2 features not yet available in the upstream plotnine library. It works as a drop-in extension: install it alongside plotnine, and you get extra geoms, stats, scales, coords, and guides.

Think of it as the "batteries included" extension for plotnine.

## Installation

```console
# Install plotnine (if not already installed) + plotnine-extra
pip install plotnine
pip install plotnine-extra

# Or install with optional spatial/extra dependencies
pip install 'plotnine-extra[extra]'
```

## Quick Start

### Option 1: Import everything (plotnine + extras)

```python
from plotnine_extra import *
# You now have ALL of plotnine plus all extra components
```

### Option 2: Import selectively

```python
from plotnine import *  # standard plotnine
from plotnine_extra.geoms import geom_hex  # just one extra
from plotnine_extra.stats import stat_contour  # another extra
```

## Example

```python
from plotnine_extra import *
import numpy as np
import pandas as pd

# Create hexbin plot
np.random.seed(42)
df = pd.DataFrame({"x": np.random.randn(1000), "y": np.random.randn(1000)})

(
    ggplot(df, aes("x", "y"))
    + geom_hex()
    + scale_fill_viridis_c()
    + theme_minimal()
)
```

## Extra Components

### Geoms
| Component | Description |
|-----------|-------------|
| `geom_contour` / `geom_contour_filled` | Contour lines and filled contour polygons from gridded data |
| `geom_curve` | Curved line segments between points (using `FancyArrowPatch`) |
| `geom_density_2d_filled` | Filled 2D density contours |
| `geom_function` | Draw a function as a continuous curve |
| `geom_hex` | Hexagonal binned heatmaps with custom hex rendering |
| `geom_sf` / `geom_sf_label` / `geom_sf_text` | Simple feature (GeoDataFrame) geometries, labels, and text |

### Stats
| Component | Description |
|-----------|-------------|
| `stat_contour` / `stat_contour_filled` | Contour computation from x, y, z grid data (via `contourpy`) |
| `stat_density_2d_filled` | Filled 2D kernel density contours |
| `stat_bin_hex` / `stat_summary_hex` | Hexagonal binning and hex-binned summaries |
| `stat_summary_2d` | 2D binned summaries with user-supplied functions |
| `stat_spoke` | Convert angle/radius to line segment endpoints |
| `stat_sf` / `stat_sf_coordinates` | Simple feature pass-through and centroid extraction |
| `stat_align` | Align observations across groups by interpolation |
| `stat_connect` | Connect observations in x-order |
| `stat_manual` | Explicit pass-through stat |

### Scales
| Component | Description |
|-----------|-------------|
| `scale_color_binned` / `scale_fill_binned` | Binned continuous color/fill scales |
| `scale_color_steps` / `scale_color_steps2` / `scale_color_stepsn` | Stepped gradient color scales (+ `fill` variants) |
| `scale_color_fermenter` / `scale_fill_fermenter` | ColorBrewer-based binned scales |
| `scale_color_viridis_c` / `scale_color_viridis_d` | Viridis convenience scales (+ `fill` variants) |
| `scale_linewidth` / `scale_linewidth_continuous` / `scale_linewidth_discrete` | Linewidth scales |
| `sec_axis` / `dup_axis` | Secondary axis specification (API compatibility) |

All color scales also have British spelling variants (`colour`).

### Coords
| Component | Description |
|-----------|-------------|
| `coord_polar` | Polar coordinate system (uses matplotlib polar projection) |
| `coord_radial` | Radial coordinates (extended polar with `r_axis_inside`) |
| `coord_quickmap` | Quick map coordinates with Mercator aspect ratio correction |
| `coord_sf` | Coordinate system for simple features with CRS-aware aspect ratio |

### Guides
| Component | Description |
|-----------|-------------|
| `guide_none` | Suppress legend/colorbar for an aesthetic |
| `guide_bins` | Binned legend guide |
| `guide_colorsteps` / `guide_coloursteps` | Stepped colorbar guide |
| `guide_custom` | Custom guide with user-provided matplotlib artists |

## How It Works

plotnine has a built-in **metaclass-based auto-registration system**. When you subclass `geom`, `stat`, `scale`, `coord`, or `guide`, the new class is automatically registered in plotnine's global `Registry`. This means that simply importing `plotnine_extra` makes all extra components available in ggplot pipelines.

## Relationship to plotnine

- **plotnine** (upstream): The core Grammar of Graphics implementation for Python by [Hassan Kibirige](https://github.com/has2k1/plotnine)
- **plotnine-extra** (this package): Additional components that extend plotnine

This package depends on plotnine and does not duplicate any of its code. We import base classes and utilities from plotnine and only implement new components here.

## Contributing

Contributions are welcome! If you have a new geom, stat, scale, or other component that would be useful, please open a PR.

## License

MIT License — see [LICENSE](LICENSE) for details.
