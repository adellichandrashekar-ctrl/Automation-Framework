import logging
from clients.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class GitHubClient(BaseAPIClient):
    """GitHub API Client using OAuth Token"""

    def __init__(self, base_url, token, timeout=10):
        super().__init__(base_url, timeout)

        self.token = token
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        })

        logger.info("GitHubClient Setup Complete.")

    def get_authenticated_user(self):
        return self.get("/user")

    def get_my_repos(self):
        return self.get("/user/repos", params={"sort": "updated", "per_age": 5})
    
    def get_repo(self, owner, repo_name):
        return self.get(f"/repos/{owner}/{repo_name}")
    
    def create_issue(self, owner, repo_name, title, body=""):
        return self.post(f"/repos/{owner}/{repo_name}/issues", json={
            "title": title,
            "body": body
        })
    
    def close(self):
        self.session.close()
        logger.info("GitHubClient Session Closed.")
