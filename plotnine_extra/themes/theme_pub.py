"""
Publication-ready themes for common journals and styles.

Provides ready-to-use themes that produce figures suitable
for scientific publications, presentations, and posters.
"""

from __future__ import annotations

from plotnine import (
    element_blank,
    element_line,
    element_rect,
    element_text,
    theme,
    theme_bw,
    theme_minimal,
)


class theme_pubr(theme_bw):
    """
    Publication-ready theme inspired by ggpubr.

    A clean theme with no grid lines, axis lines on
    the bottom and left, and a white background. Suitable
    for most journal submissions.

    Parameters
    ----------
    base_size : float
        Base font size in points.
    base_family : str
        Base font family.
    """

    def __init__(
        self,
        base_size: float = 12,
        base_family: str = "",
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        self += theme(
            panel_border=element_blank(),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            axis_line=element_line(color="black", size=0.5),
            axis_ticks=element_line(color="black", size=0.5),
            legend_key=element_rect(fill="white"),
            legend_background=element_rect(fill="white"),
            strip_background=element_rect(
                fill="#F2F2F2",
                color="transparent",
            ),
        )


class theme_clean(theme_minimal):
    """
    Minimal clean theme for presentations.

    Light grid lines, no axis lines, generous spacing.
    Good for slides and posters.

    Parameters
    ----------
    base_size : float
        Base font size in points.
    base_family : str
        Base font family.
    """

    def __init__(
        self,
        base_size: float = 14,
        base_family: str = "",
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        self += theme(
            panel_grid_major=element_line(color="#EBEBEB", size=0.4),
            panel_grid_minor=element_blank(),
            axis_ticks=element_blank(),
            plot_title=element_text(
                weight="bold",
                size=base_size * 1.3,
            ),
            plot_subtitle=element_text(
                color="#555555",
                size=base_size * 1.0,
            ),
            legend_position="bottom",
        )


class theme_scientific(theme_bw):
    """
    Theme for scientific figures.

    Thin axis lines, minimal decoration, serif-friendly.
    Follows common scientific journal style guidelines.

    Parameters
    ----------
    base_size : float
        Base font size in points.
    base_family : str
        Base font family.
    """

    def __init__(
        self,
        base_size: float = 10,
        base_family: str = "",
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        self += theme(
            panel_border=element_rect(color="black", size=0.3),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            axis_ticks=element_line(color="black", size=0.3),
            axis_text=element_text(
                color="black",
                size=base_size * 0.9,
            ),
            axis_title=element_text(
                size=base_size,
            ),
            legend_key=element_rect(fill="white", color="transparent"),
            strip_background=element_rect(
                fill="white",
                color="black",
                size=0.3,
            ),
        )


class theme_nature(theme_bw):
    """
    Theme approximating Nature journal style.

    Small font sizes, no grid, thin black axis lines,
    and minimal decoration.

    Parameters
    ----------
    base_size : float
        Base font size in points.
    base_family : str
        Base font family.
    """

    def __init__(
        self,
        base_size: float = 7,
        base_family: str = "Arial",
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        self += theme(
            panel_border=element_blank(),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            axis_line=element_line(color="black", size=0.4),
            axis_ticks=element_line(color="black", size=0.4),
            axis_text=element_text(color="black", size=base_size),
            axis_title=element_text(
                size=base_size,
            ),
            legend_key_size=10,
            legend_text=element_text(size=base_size),
            strip_background=element_blank(),
            strip_text=element_text(weight="bold", size=base_size),
        )


class theme_classic2(theme_bw):
    """
    A classic theme with axis lines and no panel border.

    Port of ``ggpubr::theme_classic2``: white background, no
    grid, axis lines on the left and bottom only.
    """

    def __init__(
        self,
        base_size: float = 12,
        base_family: str = "",
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        self += theme(
            panel_border=element_blank(),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            axis_line=element_line(color="black", size=0.5),
            axis_ticks=element_line(color="black", size=0.5),
        )


class theme_pubclean(theme_bw):
    """
    Port of ``ggpubr::theme_pubclean``.

    A minimal theme with horizontal grid lines and a clean
    background. Useful for bar / dot charts.
    """

    def __init__(
        self,
        base_size: float = 12,
        base_family: str = "",
        flip: bool = False,
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        if flip:
            major = theme(
                panel_grid_major_x=element_line(color="#CCCCCC", size=0.4),
                panel_grid_major_y=element_blank(),
            )
        else:
            major = theme(
                panel_grid_major_y=element_line(color="#CCCCCC", size=0.4),
                panel_grid_major_x=element_blank(),
            )
        self += theme(
            panel_border=element_blank(),
            panel_grid_minor=element_blank(),
            axis_line=element_line(color="black", size=0.4),
            axis_ticks=element_line(color="black", size=0.4),
            legend_position="bottom",
            legend_key=element_rect(fill="white"),
            legend_background=element_rect(fill="white"),
        )
        self += major


class theme_cleveland(theme_bw):
    """
    Port of ``ggpubr::theme_cleveland``.

    A theme suited to Cleveland-style dot plots, with horizontal
    grid lines and no axis ticks on the y-axis.
    """

    def __init__(
        self,
        base_size: float = 12,
        base_family: str = "",
        flip: bool = True,
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        if flip:
            self += theme(
                panel_grid_major_y=element_line(
                    color="#B3B3B3",
                    size=0.4,
                    linetype="dashed",
                ),
                panel_grid_minor=element_blank(),
                panel_border=element_blank(),
                axis_ticks_y=element_blank(),
            )
        else:
            self += theme(
                panel_grid_major_x=element_line(
                    color="#B3B3B3",
                    size=0.4,
                    linetype="dashed",
                ),
                panel_grid_minor=element_blank(),
                panel_border=element_blank(),
                axis_ticks_x=element_blank(),
            )


class theme_transparent(theme):
    """
    Port of ``ggpubr::theme_transparent``.

    Sets every panel / plot / legend background element to
    transparent. Useful when overlaying plots on slides.
    """

    def __init__(self):
        super().__init__(
            panel_background=element_rect(fill="none", color="none"),
            plot_background=element_rect(fill="none", color="none"),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            legend_background=element_rect(fill="none", color="none"),
            legend_box_background=element_rect(fill="none", color="none"),
        )


class clean_theme(theme):
    """
    Port of ``ggpubr::clean_theme``.

    Removes axis text, ticks, titles and grid lines while
    keeping the data ink. Used to declutter ridge plots and
    summary panels.
    """

    def __init__(self):
        super().__init__(
            axis_text=element_blank(),
            axis_title=element_blank(),
            axis_ticks=element_blank(),
            axis_line=element_blank(),
            panel_grid=element_blank(),
        )


class theme_poster(theme_minimal):
    """
    High-visibility theme for posters.

    Large fonts, bold titles, generous spacing.
    Designed for readability at a distance.

    Parameters
    ----------
    base_size : float
        Base font size in points.
    base_family : str
        Base font family.
    """

    def __init__(
        self,
        base_size: float = 20,
        base_family: str = "",
    ):
        super().__init__(
            base_size=base_size,
            base_family=base_family,
        )
        self += theme(
            panel_grid_major=element_line(color="#DDDDDD", size=0.5),
            panel_grid_minor=element_blank(),
            axis_text=element_text(
                size=base_size * 0.8,
            ),
            axis_title=element_text(
                size=base_size * 1.1,
                weight="bold",
            ),
            plot_title=element_text(
                weight="bold",
                size=base_size * 1.5,
            ),
            plot_subtitle=element_text(
                size=base_size * 1.0,
            ),
            legend_text=element_text(
                size=base_size * 0.8,
            ),
            legend_title=element_text(
                size=base_size * 0.9,
                weight="bold",
            ),
        )
