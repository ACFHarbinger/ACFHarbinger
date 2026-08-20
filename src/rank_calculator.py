"""
Mathematical rank scoring and percentile evaluation using log-normal distributions.
"""

import math
from typing import Tuple
from src.constants import (
    COMMITS_MEDIAN, COMMITS_WEIGHT,
    PRS_MEDIAN, PRS_WEIGHT,
    ISSUES_MEDIAN, ISSUES_WEIGHT,
    REVIEWS_MEDIAN, REVIEWS_WEIGHT,
    STARS_MEDIAN, STARS_WEIGHT,
    FOLLOWERS_MEDIAN, FOLLOWERS_WEIGHT,
    TOTAL_WEIGHT, RANK_THRESHOLDS, RANK_LEVELS
)

def exponential_cdf(x: float) -> float:
    """Computes exponential cumulative distribution function."""
    return 1 - (2 ** -x)

def log_normal_cdf(x: float) -> float:
    """Computes simplified log-normal CDF approximation."""
    if x <= 0:
        return 0.0
    return x / (1.0 + x)

def calculate_rank(commits: int, prs: int, issues: int, reviews: int, stars: int, followers: int) -> Tuple[str, float]:
    """
    Computes developer rank tier and exact percentile according to GitHub Readme Stats algorithm.
    """
    rank_score = (
        COMMITS_WEIGHT * log_normal_cdf(commits / COMMITS_MEDIAN)
        + PRS_WEIGHT * log_normal_cdf(prs / PRS_MEDIAN)
        + ISSUES_WEIGHT * log_normal_cdf(issues / ISSUES_MEDIAN)
        + REVIEWS_WEIGHT * log_normal_cdf(reviews / REVIEWS_MEDIAN)
        + STARS_WEIGHT * log_normal_cdf(stars / STARS_MEDIAN)
        + FOLLOWERS_WEIGHT * log_normal_cdf(followers / FOLLOWERS_MEDIAN)
    ) / TOTAL_WEIGHT

    percentile = (1.0 - rank_score) * 100.0

    level = "C"
    for i, threshold in enumerate(RANK_THRESHOLDS):
        if percentile <= threshold:
            level = RANK_LEVELS[i]
            break

    return level, percentile
