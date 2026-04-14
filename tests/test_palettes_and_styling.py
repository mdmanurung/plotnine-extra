"""Unit tests for palettes, p-value helpers and styling."""

import pytest

from plotnine_extra import (
    bgcolor,
    border,
    color_palette,
    create_p_label,
    fill_palette,
    font,
    format_p_value,
    get_p_format_style,
    get_palette,
    gradient_color,
    gradient_fill,
    grids,
    list_p_format_styles,
    rotate_x_text,
    rotate_y_text,
    rremove,
    show_line_types,
    show_point_shapes,
    xscale,
    yscale,
)
from plotnine_extra.palettes import GGSCI_PALETTES


def test_get_palette_named():
    cols = get_palette("npg", k=5)
    assert len(cols) == 5
    assert cols[0] == GGSCI_PALETTES["npg"][0]


def test_get_palette_interpolated():
    cols = get_palette("jama", k=20)
    assert len(cols) == 20
    assert all(c.startswith("#") for c in cols)


def test_get_palette_default():
    cols = get_palette("default", k=3)
    assert len(cols) == 3


def test_get_palette_unknown_raises():
    with pytest.raises(ValueError, match="Unknown palette"):
        get_palette("definitely-not-a-palette", k=2)


def test_color_fill_palette_return_scales():
    cs = color_palette("npg")
    fs = fill_palette("aaas")
    # plotnine scale objects expose a `palette` attribute
    assert cs is not None
    assert fs is not None


def test_gradient_color_fill():
    gc = gradient_color("viridis")
    gf = gradient_fill("viridis")
    assert gc is not None
    assert gf is not None


def test_format_p_value_default():
    assert "0.05" in format_p_value(0.05)


def test_format_p_value_signif_style():
    assert format_p_value(0.001, style="p.signif") == "***"


def test_format_p_value_accuracy():
    assert format_p_value(0.0001, accuracy=0.001) == "p < 0.001"


def test_create_p_label_scalar():
    assert create_p_label(0.001) == "***"
    assert create_p_label(0.5) == "ns"


def test_create_p_label_array():
    out = create_p_label([0.001, 0.04, 0.5])
    assert out == ["***", "*", "ns"]


def test_get_p_format_style_unknown():
    with pytest.raises(ValueError, match="Unknown"):
        get_p_format_style("not-a-style")


def test_list_p_format_styles_contains_default():
    styles = list_p_format_styles()
    assert "default" in styles


def test_styling_helpers_return_themes():
    assert bgcolor("white") is not None
    assert border("black") is not None
    assert grids("xy") is not None
    assert rotate_x_text(45) is not None
    assert rotate_y_text(45) is not None
    assert font("title", size=14, face="bold") is not None


def test_grids_invalid_axis():
    with pytest.raises(ValueError):
        grids("z")


def test_rremove_known_targets():
    assert rremove("axis.text") is not None
    assert rremove("legend") is not None
    with pytest.raises(ValueError):
        rremove("unknown")


def test_xscale_yscale_known():
    assert xscale("log10") is not None
    assert yscale("sqrt") is not None
    with pytest.raises(ValueError):
        xscale("nope")
    with pytest.raises(ValueError):
        yscale("nope")


def test_show_helpers_return_ggplots():
    assert show_point_shapes() is not None
    assert show_line_types() is not None
