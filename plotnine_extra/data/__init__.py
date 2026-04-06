"""
Extra datasets for plotnine_extra
=================================

Datasets included here complement those in ``plotnine.data`` and are
primarily useful for replicating examples from *ggpubr*.

Datasets
--------
ToothGrowth
    The Effect of Vitamin C on Tooth Growth in Guinea Pigs.

    The response is the length of odontoblasts (cells responsible
    for tooth growth) in 60 guinea pigs.  Each animal received one
    of three dose levels of vitamin C (0.5, 1, and 2 mg/day) by
    one of two delivery methods: orange juice (OJ) or ascorbic
    acid (VC).

    ========  ===========  ==========================================
    Column    Type         Description
    ========  ===========  ==========================================
    len       float64      Tooth length
    supp      category     Supplement type (OJ = orange juice,
                           VC = ascorbic acid)
    dose      float64      Dose in milligrams/day (0.5, 1.0, 2.0)
    ========  ===========  ==========================================

    **Shape:** 60 rows × 3 columns

    **Source:** C. I. Bliss (1952). *The Statistics of Bioassay*.
    Academic Press.

    **References:** McNeil, D. R. (1977). *Interactive Data
    Analysis*. Wiley.
"""

from pathlib import Path

import pandas as pd

__all__ = ("ToothGrowth",)

_DATA_DIR = Path(__file__).parent

ToothGrowth = pd.read_csv(_DATA_DIR / "toothgrowth.csv")
ToothGrowth["supp"] = pd.Categorical(
    ToothGrowth["supp"], categories=["OJ", "VC"], ordered=False
)
