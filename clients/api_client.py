import logging
import requests

logger = logging.getLogger(__name__)

class APIClient:
    """
    Simple HTTP client that wraps requests.session
    """
    def __init__(self, base_url, time_out=10):
        self.base_url = base_url
        self.time_out = time_out
        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        logger.info(f"APIClient Created for: {self.base_url}")

    def get(self, endpoint, **kwargs):
        """Send a GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Get {url}")
        response = self.session.get(url, timeout=self.time_out, **kwargs)
        logger.info(f"Status Code: {response.status_code}")
        return response
    
    def post(self, endpoint, json=None, **kwargs):
        """Send a POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        response = self.session.post(url, json=json, timeout=self.time_out, **kwargs)
        logger.info(f"Status Code: {response.status_code}")
        return response
    
    def put(self, endpoint, json=None, **kwargs):
        """Send a PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        response = self.session.put(url, json=json, timeout=self.time_out, **kwargs)
        logger.info(f"Status Code: {response.status_code}")
        return response
    
    def patch(self, endpoint, json=None, **kwargs):
        """Send a PATCH request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url}")
        response = self.session.patch(url, json=json, timeout=self.time_out, **kwargs)
        logger.info(f"Status Code: {response.status_code}")
        return response
    
    def delete(self, endpoint, **kwargs):
        """Send a DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, timeout=self.time_out, **kwargs)
        logger.info(f"Status Code: {response.status_code}")
        return response
    
    def set_auth_token(self, token):
        """Store auth token in session header
          will automatically include this token for every request"""
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.info("Auth token set in session headers")

    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("APIClient session is closed")
