import os
import requests

GITHUB_USERNAME = "LoveDoLove"
EXCLUDE_REPOS = [
    # Add repo names (not URLs) to exclude from featured list
    "portfolio",
    "YoutubeSourceCodes"
]
README_PATH = "README.md"
FEATURED_START = "## 🚀 Featured Projects"
FEATURED_END = "---"
MAX_PROJECTS = 10

def fetch_repos():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&type=public&sort=updated"
    repos = []
    while url:
        resp = requests.get(url)
        resp.raise_for_status()
        repos.extend(resp.json())
        # Pagination
        url = resp.links.get('next', {}).get('url')
    return [repo for repo in repos if not repo['fork'] and repo['name'] not in EXCLUDE_REPOS]

def get_repo_languages(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
    resp = requests.get(url)
    if resp.status_code == 200:
        langs = list(resp.json().keys())
        return langs
    return []

def get_featured_md(repos):
    sorted_repos = sorted(repos, key=lambda r: r['stargazers_count'], reverse=True)[:MAX_PROJECTS]
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
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()
    start = content.find(FEATURED_START)
    if start == -1:
        print("Could not find start marker in README.md")
        return
    end = content.find(FEATURED_END, start)
    if end == -1:
        print("Could not find end marker after featured section in README.md")
        return
    repos = fetch_repos()
    featured_md = get_featured_md(repos)
    new_content = content[:start] + FEATURED_START + "\n\n" + featured_md + "\n" + content[end:]
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated with top starred public repos.")

if __name__ == "__main__":
    update_readme()
