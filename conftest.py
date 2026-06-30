import os
import sys
import time
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from base.api_client import APIClient

logger = logging.getLogger(__name__)

# fixture 0
@pytest.fixture(scope="function")
def driver(config):
    """Function scoped- A new browser for each test, to ensure clean slate"""
    logger.info("Starting Chrome Browser...")
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    options.add_argument("--headless") # to run invisibly
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get(config.ui_url)

    yield driver

    logger.info("Closing Chrome Browser...")
    driver.quit()

# fixture 1
@pytest.fixture(scope="session")
def config():
    return Config()

# fixture 2
@pytest.fixture(scope="session")
def api_client(config):
    """Session scoped that authenticate once and shares the session across all tests"""
    client = APIClient(base_url=config.base_url, time_out=config.timeout)
    login_data = {
        "username": config.auth_username,
        "password": config.auth_password
    }
    logger.info("Authenticating with DummyJson...")
    response = client.post("/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json().get("accessToken")
        client.set_auth_token(token)
        logger.info("Login Successful. Auth session ready.")
    else:
        logger.error(f"Login Failed: {response.text}")
        pytest.fail("Failed to authenticate API Client")
    
    yield client

    client.close()

@pytest.fixture(autouse=True)
def test_logger(request):
    test_name = request.node.name
    logger.info(f"{'='*50}")
    logger.info(f"TEST START: {test_name}")
    logger.info(f"{'='*50}")

    yield

    logger.info(f"TEST END: {test_name}")
    logger.info(f"{'='*50}")

def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join("logs", f"automation_{timestamp}.log")

    config.option.log_file = log_file_path

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    skipped = len(terminalreporter.stats.get("skipped", []))

    logger.info(f"\n{'='*50}")
    logger.info("TOTAL TESTS SUMMARY")
    logger.info(f" PASSED: {passed}")
    logger.info(f" FAILED: {failed}")
    logger.info(f" SKIPPED: {skipped}")
    logger.info(f" Total: {passed + failed + skipped}")
    logger.info(f"\n{'='*50}")

# @pytest.fixture(autouse=True)
# def setup_test_logging(request):
#     test_name = request.node.name
#     # create a logs folder if it doesn't exist
#     os.makedirs("logs", exist_ok=True)

#     # create dynamic along with dat and time
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     log_file = f"logs/{test_name}_{timestamp}.log"

#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     file_handler = logging.FileHandler(log_file)
#     file_handler.setLevel(logging.INFO)
#     formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s")
#     file_handler.setFormatter(formatter)

#     logger.addHandler(file_handler)

#     yield

#     logger.removeHandler(file_handler)
#     file_handler.close()

