"""
Multi-variable colour / fill scales.

``scale_colour_multi`` and ``scale_fill_multi`` are simplified
ports of ``ggh4x::scale_colour_multi`` / ``scale_fill_multi``.
They take a *dict* of palette assignments keyed by aesthetic
suffix and return a list of plotnine scale layers, so a single
``+ scale_colour_multi(...)`` adds several aesthetic-specific
colour scales at once.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine import (
    scale_color_gradientn,
    scale_color_manual,
    scale_fill_gradientn,
    scale_fill_manual,
)

from ..palettes.palettes import _resolve_palette

if TYPE_CHECKING:
    from typing import Mapping, Sequence


__all__ = (
    "scale_colour_multi",
    "scale_color_multi",
    "scale_fill_multi",
    "scale_listed",
)


def _build_scales(
    palettes: "Mapping[str, str | Sequence[str]]",
    aesthetic: str,
    discrete: bool,
):
    layers = []
    if aesthetic == "color":
        manual_cls = scale_color_manual
        gradient_cls = scale_color_gradientn
    else:
        manual_cls = scale_fill_manual
        gradient_cls = scale_fill_gradientn

    for aes_name, pal in palettes.items():
        cols = list(_resolve_palette(pal))
        if discrete:
            layers.append(
                manual_cls(
                    values=cols,
                    aesthetics=aes_name,
                )
            )
        else:
            layers.append(
                gradient_cls(
                    colors=cols,
                    aesthetics=aes_name,
                )
            )
    return layers


def scale_colour_multi(
    palettes: "Mapping[str, str | Sequence[str]]",
    discrete: bool = True,
):
    """
    Build several colour scales for different aesthetics.

    Parameters
    ----------
    palettes : mapping
        Maps aesthetic names (e.g. ``"colour"``,
        ``"colour_alt"``) to palette names or sequences of
        colours.
    discrete : bool, default True
        If ``True`` use discrete (manual) scales; otherwise
        continuous gradient scales.

    Returns
    -------
    list
        A list of plotnine scale objects ready to be added to
        a ggplot via the ``+`` operator. Adding the list adds
        each scale in turn.
    """
    return _build_scales(palettes, aesthetic="color", discrete=discrete)


# Alias for the American spelling
scale_color_multi = scale_colour_multi


def scale_fill_multi(
    palettes: "Mapping[str, str | Sequence[str]]",
    discrete: bool = True,
):
    """
    Build several fill scales for different aesthetics.
    See :func:`scale_colour_multi` for parameter docs.
    """
    return _build_scales(palettes, aesthetic="fill", discrete=discrete)


def scale_listed(
    scales: "Sequence",
    replaces: "Sequence[str] | None" = None,
):
    """
    Combine several already-constructed scales into one list.

    Parameters
    ----------
    scales : sequence
        Already-constructed plotnine scale objects.
    replaces : sequence of str, optional
        Aesthetic names that the listed scales should replace.
        Currently informational; the function returns the
        list as-is so it can be added to a ggplot in one go.
    """
    return list(scales)
