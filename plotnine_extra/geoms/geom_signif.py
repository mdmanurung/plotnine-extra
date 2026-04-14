"""
``geom_signif`` is the ggsignif-style equivalent of
``geom_bracket``. It is implemented as a thin subclass that
keeps the parameter names familiar to ggsignif users.
"""

from __future__ import annotations

from .geom_bracket import geom_bracket


class geom_signif(geom_bracket):
    """
    Significance brackets with labels (ggsignif-style alias).

    This class is identical in behaviour to
    :class:`geom_bracket`. It exists so that ggsignif and
    ggpubr users can continue to write ``geom_signif(...)``
    without rewriting their code.

    Parameters
    ----------
    Same as :class:`geom_bracket`. The ``y_position`` and
    ``annotations`` arguments accepted by R's ``geom_signif``
    map onto the ``y`` and ``label`` aesthetics respectively.
    """
