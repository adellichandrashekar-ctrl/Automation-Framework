import pytest
import logging
from utils.helpers import Validators

logger = logging.getLogger(__name__)


@pytest.mark.oauth
class TestUnitOAuthCLient:
    """Unit Tests - verify the client object is constructed correctly"""

    def test_client_has_token(self, github_client):
        logger.info("UNIT TestCase1: Verify the token was set in this client")
        assert github_client.token is not None, "Token Should not be None"
        assert len(github_client.token) > 0, "Token Should not be empty"
        logger.info("Token is present in the client")

    def test_client_has_auth_header(self, github_client):
        logger.info("UNIT TestCase2: Verify Bearer Token is in the Session Headers")
        auth_header = github_client.session.headers.get("Authorization")
        assert auth_header is not None, "Authorization header should be set"
        assert auth_header.startswith("Bearer "), "Should user Bearer Token scheme"
        logger.info("Authorization header is correctly formatted")

    def test_client_base_url(self, github_client):
        logger.info("UNIT TestCase3: Verify Base URL Loaded from Config")
        assert "github.com" in github_client.base_url, "Base URL should point to GitHub"
        logger.info(f"BASE URL is {github_client.base_url}")

@pytest.mark.oauth
class TestIntegrationGitHubAPI:
    """INTEGRATION Tests - Verify token works with real GitHub API"""

    def test_authenticated_user(self, github_client):
        logger.info("INTEGRATION TestCase1: Verify token gives us access to user profile")
        response = github_client.get_authenticated_user()
        Validators.check_status(response, 200)
        data = response.json()
        assert "login" in data, "Response should contain GitHub Username"
        assert "email" in data, "Response should contain email"
        logger.info(f"Authenticated as: {data['login']}")

    def test_list_my_repos(self, github_client):
        logger.info("INTEGRATION TestCase2: Verify we can list the user's repositories")
        response = github_client.get_my_repos()
        Validators.check_status(response, 200)
        repos = response.json()
        assert isinstance(repos, list), "Should return a list if repos"
        logger.info(f"Found {len(repos)} Repositories")

        for repo in repos[:3]:
            logger.info(f" Repo: {repo['name']} | Stars: {repo.get('startgazers_count', 0)}")

    def test_get_specific_repo(self, github_client):
        logger.info("INTEGRATION TestCase3: Fetch our automation framework repo details")
        response = github_client.get_repo("adelli-chandrashekar", "simple-automation-framework")
        Validators.check_status(response, 200)
        data = response.json()
        assert data["name"] == "simple-automation-framework"
        logger.info(f"Repo: '{data['name']}' has {data.get('stargazers_count', 0)} stars")

@pytest.mark.oauth
class TestEndToEndGitHubLifeCycle:
    """End-to-End LifeCycle using OAuth Token""" 

    def test_issue_lifecycle(self, github_client):
        logger.info("E2E: Create an issue, read it, verify it, then close it")
        owner = "adelli-chandrashekar"
        repo = "simple-automation-framework"

        # Create
        create_resp = github_client.create_issue(
            owner, repo, title="[Automated] OAuth 2.0 Test Issue",
            body="This issue was created by the automation framework to test OAuth 2.0 E2E flow"
        )
        Validators.check_status(create_resp, 201)
        issue_data = create_resp.json()
        issue_number = issue_data["number"]
        logger.info(f"E2E: Created issue #{issue_number}")

        # READ
        get_resp = github_client.get(f"/repos/{owner}/{repo}/issues/{issue_number}")
        Validators.check_status(get_resp, 200)
        read_data = get_resp.json()
        assert read_data["title"] == "[Automated] OAuth 2.0 Test Issue"
        assert read_data["state"] == "open"
        logger.info(f"E2E: READ issue #{issue_number} - title verified")

        # Upated
        close_resp = github_client.patch(f"/repos/{owner}/{repo}/issues/{issue_number}", json={"state": "closed"})
        Validators.check_status(close_resp, 200)
        assert close_resp.json()["state"] == "closed"
        logger.info(f"E2E: Closed issue #{issue_number} - Full lifecycle complete.")
