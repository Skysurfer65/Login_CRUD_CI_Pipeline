from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC

import json

class Assertions:
    def assert_equal(self,expected, actual, message):
        assert expected == actual, message

    def assert_not_equal(self,expected, actual, message):
        assert expected != actual, message

    def boolean_assert(self, value, message):
        assert value, message


class Locators:
    LOGIN = (By.LINK_TEXT, 'Login')
    HEADER = (By.ID, 'header')
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
    USER_PASS_0 = (By.XPATH, '//*[@id="tableDB"]/tr[2]/td[3]')
    DELETE_ENTRY = (By.ID, 'deleteEntry')
    DELETE_ALL = (By.ID, 'deleteEverything')
    LOGOUT = (By.ID, 'logout')
    OUTPUT_1 = (By.ID, 'output1')

class Functions:
    def goto_create(self, object):
        driver = object
        loc = Locators()
        header = driver.find_element(*loc.HEADER)
        if header.text == 'Login':
            driver.find_element(*loc.CREATE_OR_LOGIN).click()
        else:
            pass
        
    def goto_login(self, object):
        driver = object
        loc = Locators()
        header = driver.find_element(*loc.HEADER)
        if header.text == 'Create Account':
            driver.find_element(*loc.CREATE_OR_LOGIN).click()
        else:
            pass

    def create_or_login_users_Original(self, object, users, passwords):
        driver = object
        loc = Locators()
        text = ''
        success = False
        for i in range(len(users)):
            driver.find_element(*loc.RESET).click()
            # Set user
            driver.find_element(*loc.USER_ID).send_keys(users[i])
            # Set password
            driver.find_element(*loc.PASSWORD).send_keys(passwords[i])
            # Create
            driver.find_element(*loc.ACTION_BUTTON).click() 
            try:
                WebDriverWait(driver, 0).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                text += f'Bad user: {users[i]}, or bad pass: {passwords[i]}\n'
            except TimeoutException:
                try:
                    WebDriverWait(driver, 0).until(lambda d: d.find_element(*loc.OUTPUT_1))
                    text_frame = driver.find_element(*loc.OUTPUT_1).get_attribute('innerHTML')
                except TimeoutException:
                    page_title = driver.title
                    driver.find_element(*loc.LOGOUT).click()
                if ('successfully' or 'CORRECT' in text_frame) or ('Admin' in page_title):
                    success = True
                continue
        return text, success
    
    
    def create_or_login_users(self, object, users, passwords):
        driver = object
        loc = Locators()
        bad_users_text = ''
        good_users_text = ''
        success = False
        for i in range(len(users)):
            driver.find_element(*loc.RESET).click()
            # Set user
            driver.find_element(*loc.USER_ID).send_keys(users[i])
            # Set password
            driver.find_element(*loc.PASSWORD).send_keys(passwords[i])
            # Create or login
            try:
                driver.find_element(*loc.ACTION_BUTTON).click()
                WebDriverWait(driver, 0).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                bad_users_text += f'Bad user: {users[i]}, or bad pass: {passwords[i]}\n'
            
            except TimeoutException:
                if driver.find_elements(*loc.OUTPUT_1):
                    text_frame = driver.find_element(*loc.OUTPUT_1).get_attribute('innerHTML')
                    good_users_text += f'Good user: {users[i]}, with good pass: {passwords[i]}\n'
                elif driver.title == 'Admin':
                    driver.find_element(*loc.LOGOUT).click()
                    good_users_text += f'Good user: {users[i]}, with good pass: {passwords[i]}\n'

                if ('successfully' or 'CORRECT' in text_frame) or ('Admin' in driver.title):
                    success = True    
        return bad_users_text, success, good_users_text
        

    def login_as_admin(self, object):
        driver = object
        loc = Locators()
        driver.find_element(*loc.RESET).click()
        driver.find_element(*loc.USER_ID).send_keys('admin')
        driver.find_element(*loc.PASSWORD).send_keys('Bax3%')
        driver.find_element(*loc.ACTION_BUTTON).click()

    def get_users(self, object):
        driver = object
        users_json = driver.execute_script('return getUsers()')
        user_data = json.loads(users_json)
        return user_data
    
    def get_new_admin_ID(self, object):
        driver = object
        newAdminID = driver.execute_script('return getNewAdmin()')
        # user_data = json.loads(users_json)
        return newAdminID