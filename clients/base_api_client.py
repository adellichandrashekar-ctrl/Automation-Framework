import logging
import requests

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Parent class for all API clients"""

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.time_out = timeout
        self.session = requests.Session()
        logger.info(f"BaseAPIClient Created for: {self.base_url}")

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
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("APIClient session is closed")

        