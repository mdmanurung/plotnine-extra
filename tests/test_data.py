"""Tests for plotnine_extra.data datasets."""

import pandas as pd

from plotnine_extra.data import ToothGrowth


class TestToothGrowth:
    """Tests for the ToothGrowth dataset."""

    def test_shape(self):
        assert ToothGrowth.shape == (60, 3)

    def test_columns(self):
        assert list(ToothGrowth.columns) == ["len", "supp", "dose"]

    def test_dtypes(self):
        assert ToothGrowth["len"].dtype == "float64"
        assert ToothGrowth["supp"].dtype.name == "category"
        assert ToothGrowth["dose"].dtype == "float64"

    def test_supp_categories(self):
        assert set(ToothGrowth["supp"].cat.categories) == {"OJ", "VC"}

    def test_dose_values(self):
        assert set(ToothGrowth["dose"].unique()) == {0.5, 1.0, 2.0}

    def test_is_dataframe(self):
        assert isinstance(ToothGrowth, pd.DataFrame)
