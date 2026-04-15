"""
Styling helper functions ported from ggpubr.

These return ``theme`` objects (or modified ``ggplot``s) that
tweak common styling elements without writing the full theme
declaration. They are intended to be added to a plot with the
``+`` operator just like any other plotnine theme.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine import (
    coord_flip,
    element_blank,
    element_line,
    element_rect,
    element_text,
    labs,
    scale_x_continuous,
    scale_x_log10,
    scale_x_sqrt,
    scale_y_continuous,
    scale_y_log10,
    scale_y_sqrt,
    theme,
)

if TYPE_CHECKING:
    from typing import Sequence

__all__ = (
    "ggpar",
    "bgcolor",
    "border",
    "grids",
    "rotate",
    "rotate_x_text",
    "rotate_y_text",
    "rremove",
    "xscale",
    "yscale",
    "font",
    "labs_pubr",
)


def bgcolor(color: str = "white"):
    """Set the panel and plot background colours."""
    return theme(
        panel_background=element_rect(fill=color, color=color),
        plot_background=element_rect(fill=color, color=color),
        legend_background=element_rect(fill=color, color=color),
    )


def border(
    color: str = "black",
    size: float = 0.5,
    linetype: str = "solid",
):
    """Add a panel border."""
    return theme(
        panel_border=element_rect(
            color=color,
            fill=None,
            size=size,
            linetype=linetype,
        )
    )


def grids(
    axis: str = "xy",
    color: str = "#EBEBEB",
    size: float = 0.4,
    linetype: str = "solid",
):
    """
    Add panel grid lines along the chosen axis.

    Parameters
    ----------
    axis : str, default ``"xy"``
        One of ``"x"``, ``"y"`` or ``"xy"``.
    """
    if axis not in {"x", "y", "xy"}:
        raise ValueError(f"axis must be 'x', 'y' or 'xy', got {axis!r}")
    line = element_line(color=color, size=size, linetype=linetype)
    kwargs = {}
    if axis in {"x", "xy"}:
        kwargs["panel_grid_major_x"] = line
    if axis in {"y", "xy"}:
        kwargs["panel_grid_major_y"] = line
    return theme(**kwargs)


def rotate():
    """Flip the coordinate system (alias of ``coord_flip``)."""
    return coord_flip()


def rotate_x_text(angle: float = 45, hjust: float = 1, vjust: float = 1):
    """Rotate x-axis tick labels."""
    return theme(
        axis_text_x=element_text(
            rotation=angle,
            ha="right" if hjust >= 0.5 else "left",
            va="top" if vjust >= 0.5 else "bottom",
        )
    )


def rotate_y_text(angle: float = 45, hjust: float = 1, vjust: float = 1):
    """Rotate y-axis tick labels."""
    return theme(
        axis_text_y=element_text(
            rotation=angle,
            ha="right" if hjust >= 0.5 else "left",
            va="top" if vjust >= 0.5 else "bottom",
        )
    )


_REMOVABLE = {
    "x.text": "axis_text_x",
    "y.text": "axis_text_y",
    "xy.text": ("axis_text_x", "axis_text_y"),
    "axis.text": ("axis_text_x", "axis_text_y"),
    "x.title": "axis_title_x",
    "y.title": "axis_title_y",
    "xy.title": ("axis_title_x", "axis_title_y"),
    "axis.title": ("axis_title_x", "axis_title_y"),
    "ticks": ("axis_ticks_x", "axis_ticks_y"),
    "x.ticks": "axis_ticks_x",
    "y.ticks": "axis_ticks_y",
    "axis": (
        "axis_text_x",
        "axis_text_y",
        "axis_title_x",
        "axis_title_y",
        "axis_line",
    ),
    "legend": "legend_position",
    "grid": ("panel_grid_major", "panel_grid_minor"),
    "panel.grid": ("panel_grid_major", "panel_grid_minor"),
}


def rremove(name: str):
    """
    Remove a named theme element.

    Parameters
    ----------
    name : str
        One of ``"x.text"``, ``"y.text"``, ``"xy.text"``,
        ``"axis.text"``, ``"x.title"``, ``"y.title"``,
        ``"xy.title"``, ``"axis.title"``, ``"x.ticks"``,
        ``"y.ticks"``, ``"ticks"``, ``"axis"``, ``"legend"``,
        ``"grid"``, ``"panel.grid"``.
    """
    if name not in _REMOVABLE:
        raise ValueError(
            f"Unknown rremove target {name!r}; expected one of "
            f"{sorted(_REMOVABLE)}"
        )
    target = _REMOVABLE[name]
    if name == "legend":
        return theme(legend_position="none")
    if isinstance(target, str):
        return theme(**{target: element_blank()})
    return theme(**{t: element_blank() for t in target})


_X_SCALES = {
    "none": scale_x_continuous,
    "log2": lambda **k: scale_x_continuous(trans="log2", **k),
    "log10": scale_x_log10,
    "sqrt": scale_x_sqrt,
}
_Y_SCALES = {
    "none": scale_y_continuous,
    "log2": lambda **k: scale_y_continuous(trans="log2", **k),
    "log10": scale_y_log10,
    "sqrt": scale_y_sqrt,
}


def xscale(type: str = "none", **kwargs):
    """
    Set the x-axis scale.

    Parameters
    ----------
    type : str
        One of ``"none"``, ``"log2"``, ``"log10"``, ``"sqrt"``.
    """
    if type not in _X_SCALES:
        raise ValueError(
            f"Unknown xscale type {type!r}; expected one of "
            f"{sorted(_X_SCALES)}"
        )
    return _X_SCALES[type](**kwargs)


def yscale(type: str = "none", **kwargs):
    """
    Set the y-axis scale. See :func:`xscale` for the list of
    valid ``type`` values.
    """
    if type not in _Y_SCALES:
        raise ValueError(
            f"Unknown yscale type {type!r}; expected one of "
            f"{sorted(_Y_SCALES)}"
        )
    return _Y_SCALES[type](**kwargs)


def font(
    which: str = "title",
    size: float | None = None,
    color: str | None = None,
    face: str | None = None,
    family: str | None = None,
):
    """
    Set the font of a named theme element.

    Parameters
    ----------
    which : str
        One of ``"title"``, ``"subtitle"``, ``"caption"``,
        ``"x"``, ``"y"``, ``"xy"``, ``"x.text"``, ``"y.text"``,
        ``"xy.text"``, ``"legend.title"``, ``"legend.text"``.
    size, color, family : optional
        Passed straight through to :class:`element_text`.
    face : str, optional
        One of ``"plain"``, ``"bold"``, ``"italic"``,
        ``"bold.italic"``.
    """
    weight = "normal"
    style = "normal"
    if face == "bold":
        weight = "bold"
    elif face == "italic":
        style = "italic"
    elif face == "bold.italic":
        weight = "bold"
        style = "italic"

    elem = element_text(
        size=size,
        color=color,
        weight=weight,
        style=style,
        family=family,
    )
    target_map = {
        "title": "plot_title",
        "subtitle": "plot_subtitle",
        "caption": "plot_caption",
        "x": "axis_title_x",
        "y": "axis_title_y",
        "xy": ("axis_title_x", "axis_title_y"),
        "x.text": "axis_text_x",
        "y.text": "axis_text_y",
        "xy.text": ("axis_text_x", "axis_text_y"),
        "legend.title": "legend_title",
        "legend.text": "legend_text",
    }
    if which not in target_map:
        raise ValueError(
            f"Unknown font target {which!r}; expected one of "
            f"{sorted(target_map)}"
        )
    target = target_map[which]
    if isinstance(target, str):
        return theme(**{target: elem})
    return theme(**{t: elem for t in target})


def labs_pubr(base_size: float = 12, base_family: str = ""):
    """
    A theme that bolds axis titles and increases their size.

    Mirrors the publication-style typography in
    ``ggpubr::labs_pubr``.
    """
    return theme(
        plot_title=element_text(
            size=base_size * 1.2,
            weight="bold",
            family=base_family,
        ),
        axis_title=element_text(
            size=base_size,
            weight="bold",
            family=base_family,
        ),
        axis_text=element_text(
            size=base_size * 0.9,
            family=base_family,
        ),
        legend_title=element_text(
            size=base_size,
            weight="bold",
            family=base_family,
        ),
        legend_text=element_text(
            size=base_size * 0.9,
            family=base_family,
        ),
    )


def ggpar(
    plot,
    title: str | None = None,
    subtitle: str | None = None,
    caption: str | None = None,
    xlab: str | None = None,
    ylab: str | None = None,
    legend: str | None = None,
    legend_title: str | None = None,
    palette: "str | Sequence[str] | None" = None,
    orientation: str | None = None,
    font_main: dict | None = None,
    font_x: dict | None = None,
    font_y: dict | None = None,
    font_legend: dict | None = None,
    x_text_angle: float | None = None,
    y_text_angle: float | None = None,
):
    """
    One-shot setter for plot title / labels / legend / palette.

    A subset of the kitchen-sink ggpubr ``ggpar`` interface. The
    most common arguments are supported; pass any further theme
    customisations as separate ``+ theme(...)`` layers.
    """
    out = plot
    label_kwargs = {}
    if title is not None:
        label_kwargs["title"] = title
    if subtitle is not None:
        label_kwargs["subtitle"] = subtitle
    if caption is not None:
        label_kwargs["caption"] = caption
    if xlab is not None:
        label_kwargs["x"] = xlab
    if ylab is not None:
        label_kwargs["y"] = ylab
    if label_kwargs:
        out = out + labs(**label_kwargs)

    if legend is not None:
        out = out + theme(legend_position=legend)
    if legend_title is not None:
        out = out + labs(color=legend_title, fill=legend_title)

    if palette is not None:
        from ..palettes import color_palette, fill_palette

        out = out + color_palette(palette) + fill_palette(palette)

    if orientation in {"horizontal", "horiz"}:
        out = out + coord_flip()

    if font_main is not None:
        out = out + font("title", **font_main)
    if font_x is not None:
        out = out + font("x", **font_x)
    if font_y is not None:
        out = out + font("y", **font_y)
    if font_legend is not None:
        out = out + font("legend.text", **font_legend)

    if x_text_angle is not None:
        out = out + rotate_x_text(angle=x_text_angle)
    if y_text_angle is not None:
        out = out + rotate_y_text(angle=y_text_angle)

    return out
