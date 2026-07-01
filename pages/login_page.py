from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")

    def login(self, username, password):
        """Perform the logic action"""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Retrive the text of the login error message"""
        return self.get_text(self.ERROR_MESSAGE)
