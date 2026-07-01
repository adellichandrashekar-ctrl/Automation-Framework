import logging

logger = logging.getLogger(__name__)


class Validators:
    """
    Reusable assertion helpers
    """
    @staticmethod
    def check_status(response, expected):
        """validate HTTP status code"""
        actual = response.status_code
        assert actual == expected, (f" Expected Status {expected}, but got {actual}."
                                    f"Body: {response.text[:200]}")
        logger.info(f"Status Code: {actual}")

    @staticmethod
    def check_key_exists(response, key):
        """validate key is in json response"""
        data = response.json()
        assert key in data, f"Key '{key}' not found. Available: {list(data.keys())}"
        logger.info(f"Key '{key}' found in response")

    @staticmethod
    def check_value(response, key, expected):
        """validate a json key as expected value"""
        data = response.json()
        actual = data.get(key)
        assert actual == expected, f"Expected '{key}'={expected}, got {actual}"
        logger.info(f"{key} = {expected}")

def generate_user_payload(first_name="Chandra", last_name="Shekar", role="QA Engineer"):
    """Generate a JSON payload for creating user in DummyJson"""
    return {"firstName": first_name, "lastName": last_name, "role": role}
