"""
GitHub GraphQL API client for retrieving developer metrics and language statistics.
"""

import json
import os
import subprocess
from typing import Dict, Any
from src.constants import FALLBACK_STATS
from src.rank_calculator import calculate_rank

GRAPHQL_QUERY = """query {
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
}"""

def fetch_user_stats(username: str = "ACFHarbinger") -> Dict[str, Any]:
    """
    Fetches user contribution data, repositories, and languages via GitHub GraphQL API.
    Falls back cleanly to cached data if offline or missing tokens.
    """
    token = (
        os.environ.get("GH_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
        or os.environ.get("PAT_TOKEN")
        or os.environ.get("GH_PAT")
    )
    
    cmd = ['gh', 'api', 'graphql', '-f', f'query={GRAPHQL_QUERY}']
    
    try:
        env = os.environ.copy()
        if token:
            env["GH_TOKEN"] = token
            env["GITHUB_TOKEN"] = token

        res = json.loads(subprocess.check_output(cmd, env=env, stderr=subprocess.DEVNULL))
        user = res['data']['user']
        commits = user['contributionsCollection']['totalCommitContributions']
        issues = user['contributionsCollection']['totalIssueContributions']
        prs = user['contributionsCollection']['totalPullRequestContributions']
        reviews = user['contributionsCollection']['totalPullRequestReviewContributions']
        followers = user['followers']['totalCount']
        stars = sum(r['stargazerCount'] for r in user['repositories']['nodes'])
        repos = user['repositories']['totalCount']
        
        level, percentile = calculate_rank(commits, prs, issues, reviews, stars, followers)
        
        # Calculate language distribution
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
            pct = (size / total_lang_size) * 100.0
            top_langs.append({
                'name': name,
                'pct': pct,
                'color': lang_colors[name]
            })

        return {
            'username': username,
            'name': user.get('name') or username,
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
        print(f"[Warning] Failed to fetch live metrics via GitHub API: {e}. Using fallback dataset.")
        return FALLBACK_STATS.copy()
