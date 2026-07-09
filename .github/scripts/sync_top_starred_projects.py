import os
import requests

# Automatically detect GitHub username:
# 1. Use GITHUB_REPOSITORY (format: owner/repo) if available
# 2. Fallback to GITHUB_ACTOR (set by GitHub Actions)
# 3. Fallback to GITHUB_USERNAME env var (for local runs)
# If none are set, raise an error and exit.
def detect_github_username():
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo and "/" in repo:
        username = repo.split("/")[0]
        print(f"[INFO] Detected GitHub username from GITHUB_REPOSITORY: {username}")
        return username
    username = os.environ.get("GITHUB_ACTOR") or os.environ.get("GITHUB_USERNAME")
    if username:
        # Mask if it looks like a token or is from env
        if "token" in username.lower() or len(username) > 32:
            masked = username[:2] + "*" * (len(username) - 4) + username[-2:]
            print(f"[INFO] Detected GitHub username from environment variable: {masked} (masked)")
        else:
            print(f"[INFO] Detected GitHub username from environment variable: {username}")
        return username
    print("[ERROR] GITHUB_USERNAME could not be determined. Please set GITHUB_REPOSITORY, GITHUB_ACTOR, or GITHUB_USERNAME environment variable.")
    raise RuntimeError(
        "GITHUB_USERNAME could not be determined. Please set GITHUB_REPOSITORY, GITHUB_ACTOR, or GITHUB_USERNAME environment variable."
    )
GITHUB_USERNAME = detect_github_username()
# EXCLUDE_REPOS is set only via the EXCLUDE_REPOS environment variable (comma-separated).
# If the environment variable is not set, EXCLUDE_REPOS will be an empty list.
_exclude_env = os.environ.get("EXCLUDE_REPOS")

if _exclude_env:
    EXCLUDE_REPOS = [repo.strip() for repo in _exclude_env.split(",") if repo.strip()]
    print("[INFO] EXCLUDE_REPOS source: GitHub environment variable (EXCLUDE_REPOS)")
else:
    EXCLUDE_REPOS = []
    print("[INFO] EXCLUDE_REPOS not set; using empty list.")

print(f"[INFO] EXCLUDE_REPOS: {EXCLUDE_REPOS}")
README_PATH = "README.md"
FEATURED_START = "## 🚀 Featured Projects"
FEATURED_END = "---"
MAX_PROJECTS = 10

def fetch_repos():
    print("[STEP] Fetching repositories from GitHub API...")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&type=public&sort=updated"
    repos = []
    while url:
        resp = requests.get(url)
        resp.raise_for_status()
        repos.extend(resp.json())
        # Pagination
        url = resp.links.get('next', {}).get('url')
    filtered = [repo for repo in repos if not repo['fork'] and repo['name'] not in EXCLUDE_REPOS]
    print(f"[INFO] Total repos fetched: {len(repos)}")
    print(f"[INFO] Total repos after filtering (not forked, not excluded): {len(filtered)}")
    return filtered

def get_repo_languages(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
    resp = requests.get(url)
    if resp.status_code == 200:
        langs = list(resp.json().keys())
        return langs
    return []

def get_featured_md(repos):
    print("[STEP] Selecting featured repositories...")
    sorted_repos = sorted(repos, key=lambda r: r['stargazers_count'], reverse=True)[:MAX_PROJECTS]
    featured_names = [repo['name'] for repo in sorted_repos]
    print(f"[INFO] Featured repositories: {featured_names}")
    lines = []
    for repo in sorted_repos:
        name = repo['name']
        url = repo['html_url']
        desc = repo['description'] or ''
        badge = f"[![GitHub stars](https://img.shields.io/github/stars/{GITHUB_USERNAME}/{name}?style=social)]({url})"
        # Fetch all languages used in the repo
        langs = get_repo_languages(name)
        tech = f"<sub>Tech: {', '.join(langs)}</sub>" if langs else ""
        lines.append(f"### [{name}]({url}) {badge}\n\n{desc}<br>\n{tech}\n")
    return '\n'.join(lines)

def update_readme():
    print("[STEP] Updating README.md with featured projects...")
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()
    start = content.find(FEATURED_START)
    if start == -1:
        print("[ERROR] Could not find start marker in README.md")
        return
    end = content.find(FEATURED_END, start)
    if end == -1:
        print("[ERROR] Could not find end marker after featured section in README.md")
        return
    repos = fetch_repos()
    featured_md = get_featured_md(repos)
    new_content = content[:start] + FEATURED_START + "\n\n" + featured_md + "\n" + content[end:]
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[SUCCESS] README.md updated with top starred public repos.")

if __name__ == "__main__":
    print("[STEP] sync_top_starred_projects.py started.")
    update_readme()
    print("[STEP] sync_top_starred_projects.py completed.")