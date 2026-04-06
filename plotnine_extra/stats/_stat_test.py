"""
Statistical test wrappers.

Provides a unified interface for running common statistical
tests using scipy.stats.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
from scipy import stats as sp_stats

TestMethod = Literal[
    "t.test",
    "wilcox.test",
    "anova",
    "kruskal.test",
    "friedman.test",
    "welch.anova",
    "pearson",
    "spearman",
    "kendall",
]


@dataclass
class StatTestResult:
    """Standardized result from a statistical test."""

    statistic: float
    p_value: float
    method: str
    df: float | None = None
    df2: float | None = None
    estimate: float | None = None
    alternative: str = "two-sided"
    extra: dict[str, Any] = field(default_factory=dict)


def run_stat_test(
    groups: list[np.ndarray],
    method: TestMethod,
    paired: bool = False,
    alternative: str = "two-sided",
    **kwargs: Any,
) -> StatTestResult:
    """
    Run a statistical test on groups of data.

    Parameters
    ----------
    groups : list of array-like
        Data groups to compare.
    method : str
        Test method name.
    paired : bool
        Whether the test is paired.
    alternative : str
        Alternative hypothesis direction.
    **kwargs
        Additional arguments passed to the test function.

    Returns
    -------
    StatTestResult
        Standardized test result.
    """
    if method == "t.test":
        return _run_ttest(groups, paired, alternative)
    elif method == "wilcox.test":
        return _run_wilcox(groups, paired, alternative)
    elif method == "anova":
        return _run_anova(groups)
    elif method == "kruskal.test":
        return _run_kruskal(groups)
    elif method == "friedman.test":
        return _run_friedman(groups)
    elif method == "welch.anova":
        return _run_welch_anova(groups)
    else:
        raise ValueError(f"Unknown test method: {method}")


def _run_ttest(
    groups: list[np.ndarray],
    paired: bool,
    alternative: str,
) -> StatTestResult:
    """Run t-test (independent or paired)."""
    if len(groups) != 2:
        raise ValueError("t-test requires exactly 2 groups")

    if paired:
        result = sp_stats.ttest_rel(
            groups[0], groups[1], alternative=alternative
        )
        method = "Paired t-test"
    else:
        result = sp_stats.ttest_ind(
            groups[0], groups[1], alternative=alternative
        )
        method = "Welch Two Sample t-test"

    df = len(groups[0]) + len(groups[1]) - 2
    return StatTestResult(
        statistic=result.statistic,
        p_value=result.pvalue,
        method=method,
        df=df,
        alternative=alternative,
    )


def _run_wilcox(
    groups: list[np.ndarray],
    paired: bool,
    alternative: str,
) -> StatTestResult:
    """Run Wilcoxon / Mann-Whitney U test."""
    if len(groups) != 2:
        raise ValueError(
            "Wilcoxon test requires exactly 2 groups"
        )

    if paired:
        result = sp_stats.wilcoxon(
            groups[0], groups[1], alternative=alternative
        )
        method = "Wilcoxon signed-rank test"
    else:
        result = sp_stats.mannwhitneyu(
            groups[0], groups[1], alternative=alternative
        )
        method = "Wilcoxon rank sum test"

    return StatTestResult(
        statistic=result.statistic,
        p_value=result.pvalue,
        method=method,
        alternative=alternative,
    )


def _run_anova(groups: list[np.ndarray]) -> StatTestResult:
    """Run one-way ANOVA."""
    result = sp_stats.f_oneway(*groups)
    df1 = len(groups) - 1
    df2 = sum(len(g) for g in groups) - len(groups)
    return StatTestResult(
        statistic=result.statistic,
        p_value=result.pvalue,
        method="One-way ANOVA",
        df=df1,
        df2=df2,
    )


def _run_kruskal(groups: list[np.ndarray]) -> StatTestResult:
    """Run Kruskal-Wallis test."""
    result = sp_stats.kruskal(*groups)
    df = len(groups) - 1
    return StatTestResult(
        statistic=result.statistic,
        p_value=result.pvalue,
        method="Kruskal-Wallis",
        df=df,
    )


def _run_friedman(groups: list[np.ndarray]) -> StatTestResult:
    """Run Friedman test."""
    result = sp_stats.friedmanchisquare(*groups)
    df = len(groups) - 1
    return StatTestResult(
        statistic=result.statistic,
        p_value=result.pvalue,
        method="Friedman test",
        df=df,
    )


def _run_welch_anova(
    groups: list[np.ndarray],
) -> StatTestResult:
    """
    Run Welch's ANOVA (does not assume equal variances).

    Uses the Welch-Satterthwaite approximation.
    """
    k = len(groups)
    ns = np.array([len(g) for g in groups])
    means = np.array([np.mean(g) for g in groups])
    variances = np.array(
        [np.var(g, ddof=1) for g in groups]
    )
    weights = ns / variances

    # Weighted grand mean
    grand_mean = np.sum(weights * means) / np.sum(weights)

    # Welch's F statistic
    numerator = np.sum(weights * (means - grand_mean) ** 2) / (
        k - 1
    )

    # Lambda values for denominator correction
    lambdas = (1 - weights / np.sum(weights)) ** 2 / (ns - 1)
    denominator = 1 + 2 * (k - 2) / (k**2 - 1) * np.sum(
        lambdas
    )

    f_stat = numerator / denominator
    df1 = k - 1
    df2 = (k**2 - 1) / (3 * np.sum(lambdas))
    p_value = 1 - sp_stats.f.cdf(f_stat, df1, df2)

    return StatTestResult(
        statistic=f_stat,
        p_value=p_value,
        method="Welch's ANOVA",
        df=df1,
        df2=df2,
    )
