import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # declared default 10 seconds explicit wait

    def wait_for_element_visible(self, locator):
        """Wait untill an element visibile on screen"""
        try:
            logger.info(f"Wait for element to be visible: {locator}")
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for element to be visible: {locator}")
            False
        
    def wait_for_element_clickable(self, locator):
        """Wait until an element is clickable then click it"""
        try:
            logger.info(f"waiting for element to be clickable: {locator}")
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logger.info(f"Timeout waiting for element to clickable: {locator}")
            False

    def click(self, locator):
        """wait for element to clickable and then click it"""
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.info(f"Clicked element: {locator}")

    def type_text(self, locator, text):
        """Wait for element visible then clear it and type text"""
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Typed tex into element: {locator}")

    def get_text(self, locator):
        """Wait for element to be visible and return its text"""
        element = self.wait_for_element_visible(locator)
        text = element.text
        logger.info(f"Got text '{text}' from element: {locator}")
        return text
    
    def is_element_displayed(self, locator):
        """Check if an element is currently displayed on the page"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False
