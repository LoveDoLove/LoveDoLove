import os
import requests

# Use environment variables for secrets and inputs
username = os.environ['GH_ACCOUNT']
token = os.environ.get('GH_TOKEN')
if not token:
    raise RuntimeError('GH_TOKEN environment variable not set. Please add your Personal Access Token as a secret named GH_PAT.')
headers = {
    'Authorization': f"token {token}",
    'Accept': 'application/vnd.github+json'
}

# Fetch all forked repos for the user
repos = []
page = 1
while True:
    resp = requests.get(
        f'https://api.github.com/users/{username}/repos?type=forks&per_page=100&page={page}',
        headers=headers
    )
    if resp.status_code != 200:
        print(f"Error fetching repos: {resp.text}")
        break
    data = resp.json()
    if not data:
        break
    repos.extend(data)
    page += 1

print(f"Found {len(repos)} forked repos for {username}")

# Update each fork

# For each repo, fetch its details to ensure 'parent' is present if it's a fork
for repo in repos:
    owner = repo['owner']['login']
    name = repo['name']
    print(f"Processing {owner}/{name}")
    # Fetch full repo details
    repo_url = f"https://api.github.com/repos/{owner}/{name}"
    repo_resp = requests.get(repo_url, headers=headers)
    if repo_resp.status_code != 200:
        print(f"Error fetching repo details for {name}: {repo_resp.text}")
        continue
    repo_details = repo_resp.json()
    if not repo_details.get('parent'):
        print(f"Repo {name} has no upstream parent, skipping.")
        continue
    upstream_owner = repo_details['parent']['owner']['login']
    upstream_repo = repo_details['parent']['name']
    # Merge upstream default branch
    merge_url = f"https://api.github.com/repos/{owner}/{name}/merge-upstream"
    merge_resp = requests.post(
        merge_url,
        headers=headers,
        json={"branch": repo_details['default_branch']}
    )
    if merge_resp.status_code == 200:
        print(f"Updated {name} to upstream.")
    else:
        print(f"Failed to update {name}: {merge_resp.text}")

# Error handling: log summary and exit code
print("Workflow completed. See above for details.")

# In-text citation: [GitHub Docs, 2024]
