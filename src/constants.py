"""
Constants, weights, and thresholds for GitHub ranking and telemetry generation.
"""

# Median thresholds and weights for rank calculations
COMMITS_MEDIAN = 1000
COMMITS_WEIGHT = 2

PRS_MEDIAN = 50
PRS_WEIGHT = 3

ISSUES_MEDIAN = 25
ISSUES_WEIGHT = 1

REVIEWS_MEDIAN = 2
REVIEWS_WEIGHT = 1

STARS_MEDIAN = 50
STARS_WEIGHT = 4

FOLLOWERS_MEDIAN = 10
FOLLOWERS_WEIGHT = 1

TOTAL_WEIGHT = (
    COMMITS_WEIGHT
    + PRS_WEIGHT
    + ISSUES_WEIGHT
    + REVIEWS_WEIGHT
    + STARS_WEIGHT
    + FOLLOWERS_WEIGHT
)

RANK_THRESHOLDS = [1, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
RANK_LEVELS = ["S", "A+", "A", "A-", "B+", "B", "B-", "C+", "C"]

# Fallback stats if API token is unavailable or offline
FALLBACK_STATS = {
    'stars': 26,
    'commits': 6530,
    'prs': 6,
    'issues': 936,
    'reviews': 1,
    'followers': 15,
    'repos': 71,
    'rank': 'B',
    'percentile': 55.57,
    'langs': [
        {'name': 'Python', 'pct': 37.74, 'color': '#3572A5'},
        {'name': 'C++', 'pct': 32.25, 'color': '#f34b7d'},
        {'name': 'TypeScript', 'pct': 17.69, 'color': '#3178c6'},
        {'name': 'Jupyter Notebook', 'pct': 2.25, 'color': '#DA5B0B'},
        {'name': 'Rust', 'pct': 1.78, 'color': '#dea584'},
        {'name': 'HTML', 'pct': 1.14, 'color': '#e34c26'},
        {'name': 'C', 'pct': 1.12, 'color': '#555555'},
        {'name': 'JavaScript', 'pct': 1.12, 'color': '#f1e05a'},
        {'name': 'CMake', 'pct': 0.75, 'color': '#DA3434'},
        {'name': 'KiCad Layout', 'pct': 0.57, 'color': '#2f4aab'},
        {'name': 'Java', 'pct': 0.54, 'color': '#b07219'},
        {'name': 'CSS', 'pct': 0.51, 'color': '#663399'}
    ]
}
