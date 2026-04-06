"""
Tests for plotnine_extra package.

Verifies that all extra components can be imported and are
properly registered in plotnine's Registry.
"""


class TestImports:
    """Test that all components can be imported."""

    def test_import_plotnine_extra(self):
        import plotnine_extra

        assert hasattr(plotnine_extra, "__version__")

    def test_import_star_includes_plotnine(self):
        """from plotnine_extra import * should include plotnine symbols."""
        import plotnine_extra

        # Check core plotnine symbols are available
        assert hasattr(plotnine_extra, "ggplot")
        assert hasattr(plotnine_extra, "aes")
        assert hasattr(plotnine_extra, "geom_point")
        assert hasattr(plotnine_extra, "theme_minimal")

    def test_import_star_includes_extras(self):
        """from plotnine_extra import * should include extra symbols."""
        import plotnine_extra

        # Coords
        assert hasattr(plotnine_extra, "coord_polar")
        assert hasattr(plotnine_extra, "coord_quickmap")
        assert hasattr(plotnine_extra, "coord_radial")
        assert hasattr(plotnine_extra, "coord_sf")

        # Geoms
        assert hasattr(plotnine_extra, "geom_contour")
        assert hasattr(plotnine_extra, "geom_contour_filled")
        assert hasattr(plotnine_extra, "geom_curve")
        assert hasattr(plotnine_extra, "geom_density_2d_filled")
        assert hasattr(plotnine_extra, "geom_function")
        assert hasattr(plotnine_extra, "geom_hex")
        assert hasattr(plotnine_extra, "geom_sf")
        assert hasattr(plotnine_extra, "geom_sf_label")
        assert hasattr(plotnine_extra, "geom_sf_text")

        # Stats
        assert hasattr(plotnine_extra, "stat_align")
        assert hasattr(plotnine_extra, "stat_bin_hex")
        assert hasattr(plotnine_extra, "stat_binhex")
        assert hasattr(plotnine_extra, "stat_connect")
        assert hasattr(plotnine_extra, "stat_contour")
        assert hasattr(plotnine_extra, "stat_contour_filled")
        assert hasattr(plotnine_extra, "stat_density_2d_filled")
        assert hasattr(plotnine_extra, "stat_manual")
        assert hasattr(plotnine_extra, "stat_sf")
        assert hasattr(plotnine_extra, "stat_sf_coordinates")
        assert hasattr(plotnine_extra, "stat_spoke")
        assert hasattr(plotnine_extra, "stat_summary_2d")
        assert hasattr(plotnine_extra, "stat_summary_hex")

        # Scales
        assert hasattr(plotnine_extra, "scale_color_binned")
        assert hasattr(plotnine_extra, "scale_color_steps")
        assert hasattr(plotnine_extra, "scale_color_viridis_c")
        assert hasattr(plotnine_extra, "scale_color_viridis_d")
        assert hasattr(plotnine_extra, "scale_linewidth")
        assert hasattr(plotnine_extra, "sec_axis")
        assert hasattr(plotnine_extra, "dup_axis")

        # Guides
        assert hasattr(plotnine_extra, "guide_none")
        assert hasattr(plotnine_extra, "guide_bins")
        assert hasattr(plotnine_extra, "guide_colorsteps")
        assert hasattr(plotnine_extra, "guide_coloursteps")
        assert hasattr(plotnine_extra, "guide_custom")


class TestRegistry:
    """Test that extra components register in plotnine's Registry."""

    def test_geoms_registered(self):
        from plotnine._utils.registry import Registry

        import plotnine_extra  # noqa: F401

        geom_names = [
            "geom_contour",
            "geom_contour_filled",
            "geom_curve",
            "geom_density_2d_filled",
            "geom_function",
            "geom_hex",
            "geom_sf",
            "geom_sf_label",
            "geom_sf_text",
        ]
        for name in geom_names:
            assert name in Registry, f"{name} not in Registry"

    def test_stats_registered(self):
        from plotnine._utils.registry import Registry

        import plotnine_extra  # noqa: F401

        stat_names = [
            "stat_align",
            "stat_bin_hex",
            "stat_connect",
            "stat_contour",
            "stat_contour_filled",
            "stat_density_2d_filled",
            "stat_manual",
            "stat_sf",
            "stat_sf_coordinates",
            "stat_spoke",
            "stat_summary_2d",
            "stat_summary_hex",
        ]
        for name in stat_names:
            assert name in Registry, f"{name} not in Registry"

    def test_guides_registered(self):
        from plotnine._utils.registry import Registry

        import plotnine_extra  # noqa: F401

        guide_names = [
            "guide_bins",
            "guide_colorsteps",
            "guide_coloursteps",
            "guide_custom",
            "guide_none",
        ]
        for name in guide_names:
            assert name in Registry, f"{name} not in Registry"

    def test_scales_registered(self):
        from plotnine._utils.registry import Registry

        import plotnine_extra  # noqa: F401

        scale_names = [
            "scale_color_binned",
            "scale_fill_binned",
            "scale_color_steps",
            "scale_color_steps2",
            "scale_color_stepsn",
            "scale_color_fermenter",
            "scale_color_viridis_c",
            "scale_color_viridis_d",
            "scale_linewidth_continuous",
            "scale_linewidth_ordinal",
        ]
        for name in scale_names:
            assert name in Registry, f"{name} not in Registry"

    def test_coords_registered(self):
        from plotnine._utils.registry import Registry

        import plotnine_extra  # noqa: F401

        coord_names = [
            "coord_polar",
            "coord_quickmap",
            "coord_radial",
            "coord_sf",
        ]
        for name in coord_names:
            assert name in Registry, f"{name} not in Registry"


class TestSubpackageImports:
    """Test selective imports from subpackages."""

    def test_import_geoms_subpackage(self):
        from plotnine_extra.geoms import geom_hex

        assert geom_hex is not None

    def test_import_stats_subpackage(self):
        from plotnine_extra.stats import stat_contour

        assert stat_contour is not None

    def test_import_scales_subpackage(self):
        from plotnine_extra.scales import scale_color_binned

        assert scale_color_binned is not None

    def test_import_coords_subpackage(self):
        from plotnine_extra.coords import coord_polar

        assert coord_polar is not None

    def test_import_guides_subpackage(self):
        from plotnine_extra.guides import guide_none

        assert guide_none is not None


class TestComponentInstantiation:
    """Test that extra components can be instantiated."""

    def test_sec_axis(self):
        from plotnine_extra.scales import sec_axis

        sa = sec_axis(trans=lambda x: x * 2, name="Secondary")
        assert sa.name == "Secondary"

    def test_dup_axis(self):
        from plotnine_extra.scales import dup_axis

        da = dup_axis(name="Dup")
        assert da.name == "Dup"

    def test_guide_none(self):
        from plotnine_extra.guides import guide_none

        g = guide_none()
        result = g.train(scale=None)
        assert result is None

    def test_stat_manual(self):
        from plotnine_extra.stats import stat_manual

        s = stat_manual()
        assert s.REQUIRED_AES == set()

    def test_stat_connect(self):
        from plotnine_extra.stats import stat_connect

        s = stat_connect()
        assert "x" in s.REQUIRED_AES
        assert "y" in s.REQUIRED_AES


class TestAllList:
    """Test __all__ is correct."""

    def test_all_contains_plotnine_symbols(self):
        import plotnine_extra

        all_symbols = plotnine_extra.__all__
        assert "ggplot" in all_symbols
        assert "aes" in all_symbols
        assert "geom_point" in all_symbols

    def test_all_contains_extra_symbols(self):
        import plotnine_extra

        all_symbols = plotnine_extra.__all__
        assert "geom_hex" in all_symbols
        assert "stat_contour" in all_symbols
        assert "scale_color_binned" in all_symbols
        assert "coord_polar" in all_symbols
        assert "guide_none" in all_symbols

    def test_no_import_cycles(self):
        """Ensure no circular import issues."""
        import importlib

        importlib.reload(__import__("plotnine_extra"))
