import requests
import git
import os

# Set your GitHub username and personal access token
username = 'TemuSoft'
token = 'your_tocken'

# Base URL for GitHub API
base_url = 'https://api.github.com'

# Endpoint for listing repositories
repos_endpoint = f'{base_url}/user/repos'

# Headers containing authentication information
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# List to store all private repositories
private_repos = []

# Function to fetch repositories recursively for pagination
def fetch_repositories(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        private_repos.extend([repo['name'] for repo in repos if repo['private']])
        # Check if there are more pages
        if 'next' in response.links:
            fetch_repositories(response.links['next']['url'])
    else:
        print(f"Failed to fetch repositories: {response.status_code} - {response.text}")

# Make the initial API request to get repository information
fetch_repositories(repos_endpoint)

# Print the list of private repository names
print("Private Repositories:")
for repo in private_repos:
    te_repo = repo
    if not os.path.exists(te_repo):
        os.makedirs(te_repo)
    repo = "https://github.com" + "/" + username + "/" + repo + ".git"
    #git.Git("").clone(repo)
    #git.Repo.clone_from(repo, "")
    print(f"Cloning {repo}")
    if repo.endswith('/'):
        repo = repo[:-1]
    try:
        git.Repo.clone_from(repo, te_repo)
    except git.exc.GitCommandError as e:
        # Handle specific error when repository is not found
        if 'repository not found' in str(e):
            print("Repository not found.")
    print(f"Cloning {repo} is done")
    print(repo)
