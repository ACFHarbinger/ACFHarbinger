#!/usr/bin/env python3
import json
import os
import subprocess

def get_stats():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_PAT") or os.environ.get("PAT_TOKEN")
    cmd = ['gh', 'api', 'graphql', '-f', '''query=query {
  user(login: "ACFHarbinger") {
    name
    login
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
    repositories(first: 100, ownerAffiliations: OWNER) {
      totalCount
      nodes { stargazerCount }
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
        stars = sum(r['stargazerCount'] for r in user['repositories']['nodes'])
        repos = user['repositories']['totalCount']
        return {
            'stars': stars,
            'commits': commits,
            'prs': prs,
            'issues': issues,
            'reviews': reviews,
            'repos': repos
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            'stars': 25,
            'commits': 5373,
            'prs': 6,
            'issues': 705,
            'reviews': 1,
            'repos': 64
        }

def generate_svg(stats):
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
    .icon {{
      fill: #f8d000;
    }}
    .stk {{
      stroke: #e4e2e2;
      stroke-width: 1;
    }}
    .rank-text {{
      font: 800 24px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #38bdf8;
    }}
    .rank-circle {{
      stroke: #38bdf8;
      stroke-width: 4;
      fill: none;
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
    <circle cx="0" cy="0" r="40" class="rank-circle"/>
    <text x="0" y="8" text-anchor="middle" class="rank-text">A+</text>
  </g>
</svg>
'''
    return svg

if __name__ == "__main__":
    stats = get_stats()
    svg_content = generate_svg(stats)
    os.makedirs("profile", exist_ok=True)
    with open("profile/stats.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Successfully generated profile/stats.svg")
