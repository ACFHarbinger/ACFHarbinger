# Contributing to ACFHarbinger Profile & Projects

Thank you for your interest in contributing to my profile repository, open-source projects, and research tools!

---

## 💡 Ways to Contribute

1. **Suggesting Improvements**: Propose new ideas, aesthetic tweaks, or metrics telemetry plugins by opening an [Issue](https://github.com/ACFHarbinger/ACFHarbinger/issues).
2. **Bug Reports**: Notice a broken badge, broken link, or failing workflow? Open a detailed issue describing the expected vs. actual behavior.
3. **Research & Collaboration**: If you're interested in collaborating on Deep RL, Combinatorial Optimization, or Game Development projects, reach out via [Email](mailto:afonso.fernandes100@gmail.com) or [LinkedIn](https://linkedin.com/in/afonso-cruz-fernandes-31a38612a).

---

## 🛠️ Local Development & Testing

### Submodules Setup
To clone this repository along with all submodules (`markdown-badges` and `metrics`):

```bash
git clone --recurse-submodules https://github.com/ACFHarbinger/ACFHarbinger.git
# Or if already cloned:
git submodule update --init --recursive
```

### Running Stats Generator Locally
To generate the latest `profile/stats.svg` and `profile/languages.svg`:

```bash
# Ensure GitHub CLI (gh) is authenticated or set GITHUB_TOKEN environment variable
python3 generate_stats.py
```

### Automated Metrics (GitHub Actions)
The [metrics workflow](.github/workflows/github-stats.yaml) uses the **local** `submodules/metrics` action (not the remote `lowlighter/metrics` marketplace action).

For richer GraphQL plugins (isocalendar, habits, languages, activity), add a classic Personal Access Token as a repository secret named `METRICS_TOKEN` (fallbacks: `PAT_TOKEN`, `GH_PAT`, then `GITHUB_TOKEN`). No scopes are required for public profile metrics; `read:user` / `repo` unlock private and in-depth data.

Trigger a refresh from the Actions tab (`workflow_dispatch`) or wait for the `00:00` / `12:00` UTC schedules.

---

## 📋 Pull Request Process

1. Fork the repository and create a descriptive feature branch (`git checkout -b feature/aesthetic-upgrade`).
2. Adhere to the existing code and documentation style.
3. Commit with clear, conventional commit messages (`feat: ...`, `fix: ...`, `docs: ...`, `style: ...`).
4. Ensure any generated SVGs or markdown formatting renders properly.
5. Submit your PR with a clear summary of changes.

---

## 📜 Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to abide by its terms.
