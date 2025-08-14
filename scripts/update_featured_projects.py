#!/usr/bin/env python3
"""Update featured projects either in an HTML file (between markers) or README.md.

Features:
- Auto-detect GitHub username from GITHUB_REPOSITORY / GITHUB_ACTOR / GITHUB_USERNAME.
- Support EXCLUDE_REPOS env var (comma-separated) to ignore repos.
- Use GITHUB_TOKEN if provided for higher API rate limits.
- Modes:
  * --file <path> : update HTML file between <!-- FEATURED_PROJECTS_START --> and <!-- FEATURED_PROJECTS_END -->
  * --readme       : update README.md between '## 🚀 Featured Projects' and the next '---'

Usage examples:
  python scripts/update_featured.py --user LoveDoLove --file portfolio-website/public/index.html --top 6
  python scripts/update_featured.py --readme
"""
import os
import sys
import argparse
import requests
from html import escape


def detect_github_username():
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo and "/" in repo:
        username = repo.split("/")[0]
        print(f"[INFO] Detected GitHub username from GITHUB_REPOSITORY: {username}")
        return username
    username = os.environ.get("GITHUB_ACTOR") or os.environ.get("GITHUB_USERNAME")
    if username:
        if "token" in username.lower() or len(username) > 32:
            masked = username[:2] + "*" * (len(username) - 4) + username[-2:]
            print(f"[INFO] Detected GitHub username from environment variable: {masked} (masked)")
        else:
            print(f"[INFO] Detected GitHub username from environment variable: {username}")
        return username
    print("[ERROR] GITHUB_USERNAME could not be determined. Please set GITHUB_REPOSITORY, GITHUB_ACTOR, or GITHUB_USERNAME environment variable.")
    raise RuntimeError("GITHUB_USERNAME could not be determined. Please set GITHUB_REPOSITORY, GITHUB_ACTOR, or GITHUB_USERNAME environment variable.")


_exclude_env = os.environ.get("EXCLUDE_REPOS")
if _exclude_env:
    EXCLUDE_REPOS = [repo.strip() for repo in _exclude_env.split(",") if repo.strip()]
    print("[INFO] EXCLUDE_REPOS source: GitHub environment variable (EXCLUDE_REPOS)")
else:
    EXCLUDE_REPOS = []
    print("[INFO] EXCLUDE_REPOS not set; using empty list.")

print(f"[INFO] EXCLUDE_REPOS: {EXCLUDE_REPOS}")


def get_repos(user, token=None, per_page=100):
    url = f"https://api.github.com/users/{user}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    repos = []
    page = 1
    while True:
        r = requests.get(url, params={"per_page": per_page, "page": page, "type": "public"}, headers=headers)
        if r.status_code != 200:
            raise SystemExit(f"GitHub API error: {r.status_code} {r.text}")
        batch = r.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    # Filter out forks and excluded names
    filtered = [repo for repo in repos if not repo.get("fork") and repo.get("name") not in EXCLUDE_REPOS]
    return filtered


def get_repo_languages(user, repo_name, token=None):
    url = f"https://api.github.com/repos/{user}/{repo_name}/languages"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return list(r.json().keys())
    return []


def build_list_html(repos, top_n=6):
    # sort primarily by stars (stargazers_count) descending, tie-breaker by forks_count descending
    print("[INFO] Sorting repositories by stars (desc) and forks (desc) for HTML list")
    repos_sorted = sorted(
        repos,
        key=lambda r: (r.get("stargazers_count", 0), r.get("forks_count", 0)),
        reverse=True,
    )
    items = []
    for r in repos_sorted[:top_n]:
        name = escape(r.get("name", ""))
        url = r.get("html_url")
        desc = escape((r.get("description") or "").strip())
        lang = escape((r.get("language") or "").strip())
        badge = f" — {lang}" if lang else ""
        text = f"<a href=\"{url}\" target=\"_blank\">{name}</a>{badge}"
        if desc:
            text += f" — {desc}"
        items.append(f"<li>{text}</li>")
    return "\n".join(items)


def build_featured_md(user, repos, token=None, max_projects=10):
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:max_projects]
    lines = []
    featured_names = [repo["name"] for repo in sorted_repos]
    print(f"[INFO] Featured repositories: {featured_names}")
    for repo in sorted_repos:
        name = repo.get("name")
        url = repo.get("html_url")
        desc = repo.get("description") or ""
        badge = f"[![GitHub stars](https://img.shields.io/github/stars/{user}/{name}?style=social)]({url})"
        langs = get_repo_languages(user, name, token=token)
        tech = f"<sub>Tech: {', '.join(langs)}</sub>" if langs else ""
        lines.append(f"### [{name}]({url}) {badge}\n\n{desc}<br>\n{tech}\n")
    return "\n".join(lines)


def replace_section_in_file(file_path, start_marker, end_marker, new_inner_html):
    with open(file_path, "r", encoding="utf-8") as f:
        s = f.read()
    start = s.find(start_marker)
    end = s.find(end_marker, start + 1)
    if start == -1 or end == -1:
        raise SystemExit("Markers not found in file")
    before = s[:start + len(start_marker)]
    after = s[end:]
    new_content = before + "\n" + new_inner_html + "\n" + after
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def update_readme(user, token=None, max_projects=10):
    README_PATH = "README.md"
    FEATURED_START = "## 🚀 Featured Projects"
    FEATURED_END = "---"
    print("[STEP] Updating README.md featured section...")
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()
    start = content.find(FEATURED_START)
    if start == -1:
        raise SystemExit("Could not find start marker in README.md")
    end = content.find(FEATURED_END, start)
    if end == -1:
        raise SystemExit("Could not find end marker after featured section in README.md")
    repos = get_repos(user, token=token)
    featured_md = build_featured_md(user, repos, token=token, max_projects=max_projects)
    new_content = content[:start] + FEATURED_START + "\n\n" + featured_md + "\n" + content[end:]
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[SUCCESS] README.md updated with top starred public repos.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=False, help="GitHub username (overrides env detection)")
    parser.add_argument("--file", required=False, help="HTML file to update between FEATURED markers")
    parser.add_argument("--top", type=int, default=6, help="Number of top repos to include")
    parser.add_argument("--readme", action="store_true", help="Update README.md featured section instead of HTML file")
    parser.add_argument("--max-projects", type=int, default=10, help="Max projects for README mode")
    parser.add_argument("--exclude", required=False, help="Comma-separated list of repo names to exclude (merged with EXCLUDE_REPOS env var)")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    user = args.user or detect_github_username()

    # Merge CLI exclude with environment EXCLUDE_REPOS
    cli_exclude = []
    if args.exclude:
        cli_exclude = [r.strip() for r in args.exclude.split(",") if r.strip()]
        if cli_exclude:
            print(f"[INFO] EXCLUDE_REPOS (from --exclude): {cli_exclude}")
    # global EXCLUDE_REPOS defined earlier from env
    if cli_exclude:
        # merge unique
        merged = list(dict.fromkeys(EXCLUDE_REPOS + cli_exclude))
        EXCLUDE_REPOS.clear()
        EXCLUDE_REPOS.extend(merged)
    print(f"[INFO] Final EXCLUDE_REPOS: {EXCLUDE_REPOS}")

    if args.readme:
        update_readme(user, token=token, max_projects=args.max_projects)
        return

    if not args.file:
        raise SystemExit("No target file provided. Use --file to specify the HTML file to update or --readme to update README.md.")

    # fetch repos and build HTML list
    repos = get_repos(user, token=token)
    new_html_items = build_list_html(repos, top_n=args.top)
    new_inner = f"<ul id=\"featured-projects\">\n{new_html_items}\n</ul>"
    start_marker = "<!-- FEATURED_PROJECTS_START -->"
    end_marker = "<!-- FEATURED_PROJECTS_END -->"
    replace_section_in_file(args.file, start_marker, end_marker, new_inner)
    print(f"[SUCCESS] Updated {args.file} with top {args.top} repos for user {user}.")


if __name__ == "__main__":
    main()
