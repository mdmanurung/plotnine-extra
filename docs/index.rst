plotnine-extra
==============

**plotnine-extra** is an extension package for
`plotnine <https://plotnine.org>`_ that provides additional geoms, stats,
plot composition operators, and animation support.

.. code-block:: python

   from plotnine_extra import *

This single import gives you the full plotnine API **plus** every extra
component shipped by plotnine-extra.

``plotnine-extra`` requires **plotnine 0.16** and **Python 3.11+**. Because it
re-exports plotnine's public API, everything plotnine 0.16 added is reachable
from ``plotnine_extra`` too, with no code of our own — ``coord_polar``,
``coord_radial``, ``sec_axis``, ``dup_axis``, ``geom_contour``,
``geom_contour_filled``, ``geom_density_2d_filled``, ``stat_contour``,
``stat_contour_filled``, ``stat_density_2d_filled``, and ``I(...)`` for
literal aesthetic values.

Extra Components
----------------

**Geoms**: ``geom_pointdensity``, ``geom_spoke``, ``geom_bracket``,
``annotation_stripes``

**Stats**: ``stat_pointdensity``, ``stat_mean``, ``stat_chull``,
``stat_stars``, ``stat_central_tendency``, ``stat_conf_ellipse``,
``stat_cor``, ``stat_regline_equation``,
``stat_overlay_normal_density``, ``stat_compare_means``,
``stat_anova_test``, ``stat_kruskal_test``, ``stat_welch_anova_test``,
``stat_friedman_test``, ``stat_pvalue_manual``, ``stat_pwc``

**Composition**: ``Compose``, ``Beside``, ``Stack``, ``Wrap``,
``plot_layout``, ``plot_annotation``, ``plot_spacer``, ``guide_area``,
``inset_element``

**Animation**: ``PlotnineAnimation``


.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   api/index
   vignettes/index
