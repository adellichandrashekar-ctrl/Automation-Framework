import logging
from clients.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class APIClient(BaseAPIClient):
    """Simple HTTP client for our basic auth tests"""

    def __init__(self, base_url, timeout=10):
        super().__init__(base_url, timeout)

        self.session.headers.update({
            "Content-Type": "Application/json",
            "Accept": "application/json",
        })
        logger.info("APIClient setup complete")

    def set_auth_token(self, token):
        """store auth token in session header"""
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.info("Auth token set in session headers")
