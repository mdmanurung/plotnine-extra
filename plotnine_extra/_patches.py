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
    Patch facet.make_axes to support coord.projection attribute.

    The original plotnine facet.make_axes creates subplots without
    passing a projection kwarg. We patch it so that if the
    coordinate system has a ``projection`` attribute (e.g.,
    coord_polar.projection = "polar"), it is forwarded to
    ``figure.add_subplot()``.
    """
    import itertools

    from plotnine.facets.facet import facet

    _original_make_axes = facet.make_axes

    def _patched_make_axes(self):
        """
        Create axes for the facet, with projection support.
        """
        # Call original to set up the gridspec, figure, etc.
        # But we need to intercept the add_subplot calls.
        # The simplest approach: replicate the relevant logic.

        # Check if the original method has already been patched
        # by looking for projection support
        import inspect

        src = inspect.getsource(_original_make_axes)
        if "projection" in src:
            # Already has projection support (shouldn't happen
            # since we check _patches_applied, but be safe)
            return _original_make_axes(self)

        # Call the original method
        _original_make_axes(self)

        # Now re-create axes with projection if needed
        projection = getattr(
            self.plot.coordinates, "projection", None
        )
        if projection is not None:
            from plotnine._mpl.gridspec import p9GridSpec

            gs = self.figure._p9_gridspec
            axsarr = self.figure._p9_axsarr

            it = itertools.product(
                range(self.nrow), range(self.ncol)
            )
            for i, (row, col) in enumerate(it):
                # Remove old axis and create new one with projection
                old_ax = axsarr[row, col]
                self.figure.delaxes(old_ax)
                axsarr[row, col] = self.figure.add_subplot(
                    gs[i], projection=projection
                )

    facet.make_axes = _patched_make_axes
