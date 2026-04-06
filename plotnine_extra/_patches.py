"""
Monkey-patches to plotnine internals required by plotnine_extra.

These patches are applied at import time and are necessary for
certain extra components (e.g., coord_polar) to work correctly.
"""

from __future__ import annotations

_patches_applied = False


def apply_patches():
    """
    Apply all necessary patches to plotnine internals.

    This function is idempotent — calling it multiple times
    has no additional effect.
    """
    global _patches_applied
    if _patches_applied:
        return
    _patches_applied = True

    _patch_facet_make_axes()


def _patch_facet_make_axes():
    """
    Patch facet._make_axes to support coord.projection attribute.

    The original plotnine facet._make_axes creates subplots without
    passing a projection kwarg. We patch it so that if the
    coordinate system has a ``projection`` attribute (e.g.,
    coord_polar.projection = "polar"), it is forwarded to
    ``figure.add_subplot()``.
    """
    import itertools

    import numpy as np
    from plotnine.facets.facet import facet

    _original_make_axes = facet._make_axes

    def _patched_make_axes(self):
        """
        Create axes for the facet, with projection support.
        """
        projection = getattr(
            self.plot.coordinates, "projection", None
        )

        if projection is None:
            # No projection needed, use original
            return _original_make_axes(self)

        # Replicate the original logic but with projection
        num_panels = len(self.layout.layout)
        axsarr = np.empty(
            (self.nrow, self.ncol), dtype=object
        )
        self._panels_gridspec = self._get_panels_gridspec()

        it = itertools.product(
            range(self.nrow), range(self.ncol)
        )
        for i, (row, col) in enumerate(it):
            axsarr[row, col] = self.figure.add_subplot(
                self._panels_gridspec[i],
                projection=projection,
            )

        # Rearrange axes (same logic as original)
        if self.dir == "h":
            order = "C"
            if not self.as_table:
                axsarr = axsarr[::-1]
        elif self.dir == "v":
            order = "F"
            if self.as_table:
                axsarr = axsarr[:, ::-1]

        axes = axsarr.ravel(order)

        # Match up panels and axes
        _axes = []
        for i in range(num_panels):
            _axes.append(axes[i])

        return _axes

    facet._make_axes = _patched_make_axes
