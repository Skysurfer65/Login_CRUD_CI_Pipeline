from selenium.webdriver.common.by import By

class Assertions:
    def assert_equal(self,expected, actual):
        assert expected == actual, "Equals"

    def assert_not_equal(self,expected, actual):
        assert expected != actual, "Not equal"

class Locators:
    LOGIN = (By.LINK_TEXT, 'Login')