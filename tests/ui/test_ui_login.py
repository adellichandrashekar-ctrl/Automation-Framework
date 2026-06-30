import time # for time being veiwing what is happening (not a standard thing to use)
import pytest
import logging
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

logger = logging.getLogger(__name__)

@pytest.mark.ui
@pytest.mark.smoke
class TestSauceDemoLogin:

    def test_login_success(self, driver):
        """Validate successful login with valid creds"""
        logger.info("Initializing Page Object")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        time.sleep(3) # for time being veiwing what is happening (not a standard thing to use in automation)

        logger.info("Attempting login as standard_user")
        login_page.login("standard_user", "secret_sauce")
        time.sleep(3) # for time being veiwing what is happening (not a standard thing to use in automation)

        logger.info("Verfying successful redirect to inventory page")
        assert inventory_page.is_header_displayed(), "Inventory header should be visible"
        assert inventory_page.get_header_text() == "Products"
        logger.info("Login Successful")

    def test_login_locked_user(self, driver):
        login_page = LoginPage(driver)
        logger.info("Attempting login as locked_out_user")
        time.sleep(3) # for time being veiwing what is happening (not a standard thing to use in automation)
        login_page.login("locked_out_user", "secret_sauce")
        time.sleep(3) # for time being veiwing what is happening (not a standard thing to use in automation)
        error_msg = login_page.get_error_message()
        assert "locked out" in error_msg.lower()
        logger.info(f"Verified error message: {error_msg}")

    def test_login_invalid_password(self, driver):
        """verify login with invalid password"""
        login_page = LoginPage(driver)
        time.sleep(3) # for time being veiwing what is happening (not a standard thing to use in automation)
        logger.info("Attempting login with invalid password")
        login_page.login("standard_user", "wrong_password")
        time.sleep(3) # for time being veiwing what is happening (not a standard thing to use in automation)

        error_msg = login_page.get_error_message()
        logger.info(f"error_msg = {error_msg}")
        assert "do not match" in error_msg.lower()
        logger.info(f"Verified Error Message: {error_msg}")
