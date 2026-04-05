# plotnine <img width="20%" align="right" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/logo-512.png?raw=true">

[![Release](https://img.shields.io/pypi/v/plotnine.svg)](https://pypi.python.org/pypi/plotnine)
[![License](https://img.shields.io/pypi/l/plotnine.svg)](https://pypi.python.org/pypi/plotnine)
[![DOI](https://zenodo.org/badge/89276692.svg)](https://zenodo.org/badge/latestdoi/89276692)
[![Build Status](https://github.com/has2k1/plotnine/workflows/build/badge.svg?branch=main)](https://github.com/has2k1/plotnine/actions?query=branch%3Amain+workflow%3A%22build%22)
[![Coverage](https://codecov.io/github/has2k1/plotnine/coverage.svg?branch=main)](https://codecov.io/github/has2k1/plotnine?branch=main)

plotnine is an implementation of a *grammar of graphics* in Python
based on [ggplot2](https://github.com/tidyverse/ggplot2).
The grammar allows you to compose plots by explicitly mapping variables in a
dataframe to the visual characteristics (position, color, size etc.) of objects that make up the plot.

Plotting with a *grammar of graphics* is powerful. Custom (and otherwise
complex) plots are easy to think about and build incrementally, while the
simple plots remain simple to create.

To learn more about how to use plotnine, check out the
[documentation](https://plotnine.org). Since plotnine
has an API similar to ggplot2, where it lacks in coverage the
[ggplot2 documentation](http://ggplot2.tidyverse.org/reference/index.html)
may be helpful.


## Example

```python
from plotnine import *
from plotnine.data import mtcars
```

Building a complex plot piece by piece.

1. Scatter plot

   ```python
   (
       ggplot(mtcars, aes("wt", "mpg"))
       + geom_point()
   )
   ```

   <img width="90%" align="center" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/readme-image-1.png?raw=true">

2. Scatter plot colored according some variable

   ```python
   (
       ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
       + geom_point()
   )
   ```

   <img width="90%" align="center" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/readme-image-2.png?raw=true">

3. Scatter plot colored according some variable and
   smoothed with a linear model with confidence intervals.

   ```python
   (
       ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
       + geom_point()
       + stat_smooth(method="lm")
   )
   ```

   <img width="90%" align="center" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/readme-image-3.png?raw=true">

4. Scatter plot colored according some variable,
   smoothed with a linear model with confidence intervals and
   plotted on separate panels.

   ```python
   (
       ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
       + geom_point()
       + stat_smooth(method="lm")
       + facet_wrap("gear")
   )
   ```

   <img width="90%" align="center" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/readme-image-4.png?raw=true">

5. Adjust the themes


   I) Make it playful

   ```python
   (
       ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
       + geom_point()
       + stat_smooth(method="lm")
       + facet_wrap("gear")
       + theme_xkcd()
   )
   ```

   <img width="90%" align="center" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/readme-image-5.png?raw=true">

   II) Or professional

   ```python
   (
       ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
       + geom_point()
       + stat_smooth(method="lm")
       + facet_wrap("gear")
       + theme_tufte()
   )
   ```

   <img width="90%" align="center" src="https://github.com/has2k1/plotnine/blob/logos/doc/images/readme-image-5alt.png?raw=true">

## Additional Features (beyond upstream plotnine)

This fork extends plotnine with additional ggplot2 features not yet available
in the [upstream repository](https://github.com/has2k1/plotnine):

### New Geoms
- `geom_contour` / `geom_contour_filled` — Contour lines and filled contour polygons from gridded data
- `geom_curve` — Curved line segments between points (using `FancyArrowPatch`)
- `geom_density_2d_filled` — Filled 2D density contours
- `geom_function` — Draw a function as a continuous curve
- `geom_hex` — Hexagonal binned heatmaps with custom hex rendering
- `geom_sf` / `geom_sf_label` / `geom_sf_text` — Simple feature (GeoDataFrame) geometries, labels, and text

### New Stats
- `stat_contour` / `stat_contour_filled` — Contour computation from x, y, z grid data (via `contourpy`)
- `stat_density_2d_filled` — Filled 2D kernel density contours
- `stat_bin_hex` / `stat_summary_hex` — Hexagonal binning and hex-binned summaries
- `stat_summary_2d` — 2D binned summaries with user-supplied functions
- `stat_spoke` — Convert angle/radius to line segment endpoints
- `stat_sf` / `stat_sf_coordinates` — Simple feature pass-through and centroid extraction
- `stat_align` — Align observations across groups by interpolation
- `stat_connect` — Connect observations in x-order
- `stat_manual` — Explicit pass-through stat

### New Scales
- **Binned color/fill scales**: `scale_color_binned`, `scale_color_steps`, `scale_color_steps2`, `scale_color_stepsn`, `scale_color_fermenter` (and `fill` / British spelling variants)
- **Linewidth scales**: `scale_linewidth`, `scale_linewidth_continuous`, `scale_linewidth_discrete`, `scale_linewidth_ordinal`
- **Viridis convenience scales**: `scale_color_viridis_c`, `scale_color_viridis_d`, `scale_fill_viridis_c`, `scale_fill_viridis_d`
- **Secondary axis**: `sec_axis`, `dup_axis` (API specification; rendering not yet integrated)

### New Coords
- `coord_polar` — Polar coordinate system (uses matplotlib polar projection)
- `coord_radial` — Radial coordinates (extended polar with `r_axis_inside`)
- `coord_quickmap` — Quick map coordinates with Mercator aspect ratio correction
- `coord_sf` — Coordinate system for simple features with CRS-aware aspect ratio

### New Guides
- `guide_none` — Suppress legend/colorbar for an aesthetic
- `guide_bins` — Binned legend guide (API placeholder)
- `guide_colorsteps` / `guide_coloursteps` — Stepped colorbar guide (API placeholder)
- `guide_custom` — Custom guide with user-provided matplotlib artists

## Installation

Official release

```console
# Using pip
$ pip install plotnine             # 1. should be sufficient for most
$ pip install 'plotnine[extra]'    # 2. includes extra/optional packages
$ pip install 'plotnine[test]'     # 3. testing
$ pip install 'plotnine[doc]'      # 4. generating docs
$ pip install 'plotnine[dev]'      # 5. development (making releases)
$ pip install 'plotnine[all]'      # 6. everything

# Or using conda
$ conda install -c conda-forge plotnine

# Or using pixi
$ pixi init name-of-my-project
$ cd name-of-my-project
$ pixi add python plotnine
```

Development version

```console
$ pip install git+https://github.com/has2k1/plotnine.git
```

## Contributing

Our documentation could use some examples, but we are looking for something
a little bit special. We have two criteria:

1. Simple looking plots that otherwise require a trick or two.
2. Plots that are part of a data analytic narrative. That is, they provide
   some form of clarity showing off the `geom`, `stat`, ... at their
   differential best.

If you come up with something that meets those criteria, we would love to
see it. See [plotnine-examples](https://github.com/has2k1/plotnine-examples).

If you discover a bug checkout the [issues](https://github.com/has2k1/plotnine/issues)
if it has not been reported, yet please file an issue.

And if you can fix a bug, your contribution is welcome.

Testing
-------

Plotnine has tests that generate images which are compared to baseline images known
to be correct. There may be small differences in the text rendering that throw off the
image comparisons, and the tests allow some very small differences.
