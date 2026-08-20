#!/usr/bin/env python3
"""
ACFHarbinger GitHub Statistics & Telemetry Generator

Orchestrates live telemetry retrieval via GitHub GraphQL API,
evaluates ranking percentiles, and renders modular SVG cards.
"""

import os
from pathlib import Path
from src.github_api import fetch_user_stats
from src.svg_renderer import render_stats_svg, render_languages_svg

def main() -> None:
    output_dir = Path("profile")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching user telemetry from GitHub API...")
    stats = fetch_user_stats("ACFHarbinger")
    print(f"Calculated Developer Rank: {stats['rank']} (Percentile: {stats['percentile']:.2f}%)")

    # Render Stats SVG
    stats_svg = render_stats_svg(stats)
    stats_file = output_dir / "stats.svg"
    stats_file.write_text(stats_svg, encoding="utf-8")
    print(f"Rendered: {stats_file}")

    # Render Languages SVG
    langs_svg = render_languages_svg(stats)
    langs_file = output_dir / "languages.svg"
    langs_file.write_text(langs_svg, encoding="utf-8")
    print(f"Rendered: {langs_file}")

    print("All profile telemetry cards generated successfully.")

if __name__ == "__main__":
    main()
