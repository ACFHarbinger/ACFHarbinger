#!/usr/bin/env python3
import json
import math
import os
import subprocess

def exponential_cdf(x):
    return 1 - (2 ** -x)

def log_normal_cdf(x):
    return x / (1 + x)

def calculate_rank(commits, prs, issues, reviews, stars, followers):
    COMMITS_MEDIAN, COMMITS_WEIGHT = 1000, 2
    PRS_MEDIAN, PRS_WEIGHT = 50, 3
    ISSUES_MEDIAN, ISSUES_WEIGHT = 25, 1
    REVIEWS_MEDIAN, REVIEWS_WEIGHT = 2, 1
    STARS_MEDIAN, STARS_WEIGHT = 50, 4
    FOLLOWERS_MEDIAN, FOLLOWERS_WEIGHT = 10, 1

    TOTAL_WEIGHT = (
        COMMITS_WEIGHT
        + PRS_WEIGHT
        + ISSUES_WEIGHT
        + REVIEWS_WEIGHT
        + STARS_WEIGHT
        + FOLLOWERS_WEIGHT
    )

    rank_score = (
        COMMITS_WEIGHT * log_normal_cdf(commits / COMMITS_MEDIAN)
        + PRS_WEIGHT * log_normal_cdf(prs / PRS_MEDIAN)
        + ISSUES_WEIGHT * log_normal_cdf(issues / ISSUES_MEDIAN)
        + REVIEWS_WEIGHT * log_normal_cdf(reviews / REVIEWS_MEDIAN)
        + STARS_WEIGHT * log_normal_cdf(stars / STARS_MEDIAN)
        + FOLLOWERS_WEIGHT * log_normal_cdf(followers / FOLLOWERS_MEDIAN)
    ) / TOTAL_WEIGHT

    percentile = (1 - rank_score) * 100

    THRESHOLDS = [1, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
    LEVELS = ["S", "A+", "A", "A-", "B+", "B", "B-", "C+", "C"]

    level = "C"
    for i, threshold in enumerate(THRESHOLDS):
        if percentile <= threshold:
            level = LEVELS[i]
            break

    return level, percentile

def get_stats():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_PAT") or os.environ.get("PAT_TOKEN")
    cmd = ['gh', 'api', 'graphql', '-f', '''query=query {
  user(login: "ACFHarbinger") {
    name
    login
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
    repositories(first: 100, ownerAffiliations: OWNER) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
}''']
    try:
        env = os.environ.copy()
        if token:
            env["GH_TOKEN"] = token
        res = json.loads(subprocess.check_output(cmd, env=env))
        user = res['data']['user']
        commits = user['contributionsCollection']['totalCommitContributions']
        issues = user['contributionsCollection']['totalIssueContributions']
        prs = user['contributionsCollection']['totalPullRequestContributions']
        reviews = user['contributionsCollection']['totalPullRequestReviewContributions']
        followers = user['followers']['totalCount']
        stars = sum(r['stargazerCount'] for r in user['repositories']['nodes'])
        repos = user['repositories']['totalCount']
        
        level, percentile = calculate_rank(commits, prs, issues, reviews, stars, followers)
        
        # Calculate language stats
        lang_sizes = {}
        lang_colors = {}
        for r in user['repositories']['nodes']:
            if not r.get('languages'):
                continue
            for edge in r['languages']['edges']:
                name = edge['node']['name']
                color = edge['node']['color'] or "#858585"
                size = edge['size']
                lang_sizes[name] = lang_sizes.get(name, 0) + size
                lang_colors[name] = color
                
        total_lang_size = sum(lang_sizes.values()) or 1
        top_langs = []
        for name, size in sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True)[:12]:
            pct = (size / total_lang_size) * 100
            top_langs.append({
                'name': name,
                'pct': pct,
                'color': lang_colors[name]
            })

        return {
            'stars': stars,
            'commits': commits,
            'prs': prs,
            'issues': issues,
            'reviews': reviews,
            'followers': followers,
            'repos': repos,
            'rank': level,
            'percentile': percentile,
            'langs': top_langs
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        level, percentile = calculate_rank(5373, 6, 705, 1, 23, 15)
        return {
            'stars': 23,
            'commits': 5373,
            'prs': 6,
            'issues': 705,
            'reviews': 1,
            'followers': 15,
            'repos': 40,
            'rank': level,
            'percentile': percentile,
            'langs': [
                {'name': 'Python', 'pct': 77.18, 'color': '#3572A5'},
                {'name': 'TypeScript', 'pct': 9.37, 'color': '#3178c6'},
                {'name': 'Rust', 'pct': 4.44, 'color': '#dea584'},
                {'name': 'C++', 'pct': 3.13, 'color': '#f34b7d'},
                {'name': 'HTML', 'pct': 0.99, 'color': '#e34c26'},
                {'name': 'CSS', 'pct': 0.97, 'color': '#563d7c'},
                {'name': 'QML', 'pct': 0.91, 'color': '#44a51c'},
                {'name': 'Kotlin', 'pct': 0.72, 'color': '#A97BFF'},
                {'name': 'TeX', 'pct': 0.51, 'color': '#3D6117'},
                {'name': 'JavaScript', 'pct': 0.42, 'color': '#f1e05a'}
            ]
        }

def generate_stats_svg(stats):
    rank_level = stats['rank']
    percentile = stats['percentile']
    stroke_dasharray = 251.2  # 2 * pi * 40
    stroke_dashoffset = (percentile / 100.0) * stroke_dasharray

    svg = f'''<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Afonso Cruz Fernandes's GitHub Stats">
  <title>Afonso Cruz Fernandes's GitHub Stats</title>
  <style>
    .header {{
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #38bdf8;
      animation: fadeInAnimation 0.8s ease-in-out forwards;
    }}
    .stat {{
      font: 600 14px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif;
      fill: #a9fef7;
    }}
    .bold {{ font-weight: 700 }}
    .rank-text {{
      font: 800 24px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #38bdf8;
    }}
    .rank-circle-bg {{
      stroke: rgba(255, 255, 255, 0.1);
      stroke-width: 4;
      fill: none;
    }}
    .rank-circle {{
      stroke: #38bdf8;
      stroke-width: 4;
      fill: none;
      stroke-dasharray: {stroke_dasharray:.1f};
      stroke-dashoffset: {stroke_dashoffset:.1f};
      stroke-linecap: round;
      transform: rotate(-90deg);
      transform-origin: center;
    }}
    @keyframes fadeInAnimation {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
  </style>

  <rect x="0.5" y="0.5" rx="4.5" width="494" height="194" fill="#141321" stroke="#e4e2e2" stroke-opacity="0.2"/>

  <g transform="translate(25, 35)">
    <text x="0" y="0" class="header">Afonso Cruz Fernandes's GitHub Stats</text>
  </g>

  <g transform="translate(25, 55)">
    <g transform="translate(0, 0)">
      <svg x="0" y="0" width="16" height="16" viewBox="0 0 16 16" fill="#f8d000">
        <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
      </svg>
      <text x="25" y="12.5" class="stat bold">Total Stars:</text>
      <text x="200" y="12.5" class="stat">{stats['stars']}</text>
    </g>
    <g transform="translate(0, 25)">
      <svg x="0" y="0" width="16" height="16" viewBox="0 0 16 16" fill="#f8d000">
        <path d="M10.5 5a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm.01 4.5A4.5 4.5 0 0115 14a.75.75 0 01-1.5 0 3 3 0 00-6 0 .75.75 0 01-1.5 0 4.5 4.5 0 014.51-4.5zM3.5 4a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"/>
      </svg>
      <text x="25" y="12.5" class="stat bold">Total Commits:</text>
      <text x="200" y="12.5" class="stat">{stats['commits']:,}</text>
    </g>
    <g transform="translate(0, 50)">
      <svg x="0" y="0" width="16" height="16" viewBox="0 0 16 16" fill="#f8d000">
        <path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm0 9.5a.75.75 0 100 1.5.75.75 0 000-1.5z"/>
      </svg>
      <text x="25" y="12.5" class="stat bold">Total PRs:</text>
      <text x="200" y="12.5" class="stat">{stats['prs']}</text>
    </g>
    <g transform="translate(0, 75)">
      <svg x="0" y="0" width="16" height="16" viewBox="0 0 16 16" fill="#f8d000">
        <path d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm9 3a1 1 0 11-2 0 1 1 0 012 0zm-.25-6.25a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0v-3.5z"/>
      </svg>
      <text x="25" y="12.5" class="stat bold">Total Issues:</text>
      <text x="200" y="12.5" class="stat">{stats['issues']}</text>
    </g>
    <g transform="translate(0, 100)">
      <svg x="0" y="0" width="16" height="16" viewBox="0 0 16 16" fill="#f8d000">
        <path d="M2 2.5A1.5 1.5 0 013.5 1h9A1.5 1.5 0 0114 2.5v11a1.5 1.5 0 01-1.5 1.5h-9A1.5 1.5 0 012 13.5v-11z"/>
      </svg>
      <text x="25" y="12.5" class="stat bold">Contributed to:</text>
      <text x="200" y="12.5" class="stat">{stats['repos']}</text>
    </g>
  </g>

  <g transform="translate(400, 110)">
    <circle cx="0" cy="0" r="40" class="rank-circle-bg"/>
    <circle cx="0" cy="0" r="40" class="rank-circle"/>
    <text x="0" y="8" text-anchor="middle" class="rank-text">{rank_level}</text>
  </g>
</svg>
'''
    return svg

def generate_languages_svg(stats):
    langs = stats.get('langs', [])
    card_height = 80 + len(langs) * 40
    
    items_svg = ""
    for idx, l in enumerate(langs):
        y_pos = idx * 40
        pct_str = f"{l['pct']:.2f}%"
        bar_width = max(2, int((l['pct'] / 100.0) * 205))
        items_svg += f'''
    <g transform="translate(0, {y_pos})">
      <text x="25" y="15" class="lang-name">{l['name']}</text>
      <text x="270" y="15" text-anchor="end" class="lang-pct">{pct_str}</text>
      <svg width="245" x="25" y="22">
        <rect rx="4" ry="4" x="0" y="0" width="245" height="8" fill="rgba(255,255,255,0.1)"/>
        <rect rx="4" ry="4" x="0" y="0" width="{bar_width}" height="8" fill="{l['color']}"/>
      </svg>
    </g>'''

    svg = f'''<svg width="300" height="{card_height}" viewBox="0 0 300 {card_height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Most Used Languages">
  <title>Most Used Languages</title>
  <style>
    .header {{
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #38bdf8;
    }}
    .lang-name {{
      font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #a9fef7;
    }}
    .lang-pct {{
      font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #858585;
    }}
  </style>

  <rect x="0.5" y="0.5" rx="4.5" width="299" height="{card_height - 1}" fill="#141321" stroke="#e4e2e2" stroke-opacity="0.2"/>

  <g transform="translate(25, 35)">
    <text x="0" y="0" class="header">Most Used Languages</text>
  </g>

  <g transform="translate(0, 55)">
    {items_svg}
  </g>
</svg>
'''
    return svg

if __name__ == "__main__":
    stats = get_stats()
    print(f"Calculated Rank: {stats['rank']} (Percentile: {stats['percentile']:.2f}%)")
    os.makedirs("profile", exist_ok=True)
    
    with open("profile/stats.svg", "w", encoding="utf-8") as f:
        f.write(generate_stats_svg(stats))
        
    with open("profile/languages.svg", "w", encoding="utf-8") as f:
        f.write(generate_languages_svg(stats))
        
    print("Successfully generated profile/stats.svg and profile/languages.svg")
