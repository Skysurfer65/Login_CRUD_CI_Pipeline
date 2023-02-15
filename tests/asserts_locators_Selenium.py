from selenium.webdriver.common.by import By

class Assertions:
    def assert_equal(self,expected, actual, message):
        assert expected == actual, message

    def assert_not_equal(self,expected, actual, message):
        assert expected != actual, message
    
    def boolean_assert(self, value, message):
        assert value, message

class Locators:
    LOGIN = (By.LINK_TEXT, 'Login')
    CREATE = (By.CSS_SELECTOR, '[value="CREATE"]')
    ACTION_BUTTON = (By.ID, 'actionButton')
    CREATE_OR_LOGIN = (By.ID, 'createOrLogin')
    RESET = (By.ID, 'reset')
    USER_ID = (By.ID, 'userID')
    PASSWORD = (By.ID, 'password')
    DISPLAY_DB = (By.ID, 'displayDB')
    USER_ID_2 = (By.XPATH, '//*[@id="tableDB"]/tr[4]/td[2]') # Not dynamic, admin in good_users
    UPDATE_ENTRY = (By.ID, 'updateEntry')
    USER_ID_0 = (By.XPATH, '//*[@id="tableDB"]/tr[2]/td[2]')
    DELETE_ALL = (By.ID, 'deleteEverything')
    LOGOUT = (By.ID, 'logout')
    OUTPUT_1 = (By.ID, 'output1')