# Selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# Pytest
import pytest
import pytest_html
# Python
import os
import json
from time import sleep
# Local
from asserts_locators_Selenium import Assertions, Locators

### Test variabels and constants ###
good_users = ["bax1", "Bax2", "admin", " spaces1 ", "Åäö20", "longUserID01234567890123456789"]
good_passwords = ["Bax1#", "2aX#", "Bax3%", "40bAx?", "20Åäö&", "LongPass##012345"]
bad_users = ["", "richard", "adam1@", "baxen1#", "pat rik", "tooLongID0123456789012345678901"]
bad_passwords = ["", "P1#", "password1#", "Password#", "Pass word1#", "TooLongPass#34567"]
LOGIN_TITLE = 'Login'
ADMIN_TITLE = 'Admin'
# Local 'URL' for html page
LOGIN_HTML = os.getcwd() + "//" + "..//src//html/index.html"
# Instance of help classes
my = Assertions()
find = Locators()

@pytest.fixture(params=["chrome", "edge"],scope="class")
def invoke_driver(request):
    print('Class setup')
    if request.param == "chrome":
        web_driver = webdriver.Chrome()
    if request.param == "edge":
        web_driver = webdriver.Edge()
    request.cls.driver = web_driver
    yield
    print('Class teardown')
    web_driver.quit()


@pytest.mark.usefixtures("invoke_driver")
class BasicTest:
    # To be able to choose driver use and setups for test classes
    def my_setup_1(self):
        print('Function setup')
        self.driver.get("file:///" + LOGIN_HTML)
    
    def my_teardown_1(self):
        self.driver.delete_all_cookies()
        print('Function teardown')

    def delete_DB(self):
        self.driver.execute_script("deleteEverything()")
    
    def delete_everything(self):
        self.driver.find_element(*find.RESET).click()
        # Log in as admin
        self.driver.find_element(*find.USER_ID).send_keys(good_users[2])
        self.driver.find_element(*find.PASSWORD).send_keys(good_passwords[2])
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        self.driver.find_element(*find.ACTION_BUTTON).click()
        # Select delete everything
        self.driver.find_element(*find.DELETE_ALL).click()
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except TimeoutException:
            assert False, "No delete all Alert shown"
        self.driver.find_element(*find.LOGOUT).click()
    

class Testcase1(BasicTest):
    # Function for development
    def to_find_driver_functions(self):
        # To help IDE find type of driver
        driver : webdriver.Edge = self.driver 
        driver.execute_script('localStorage.removeItem("myLoginDB");')
    
    def test_1_source_found(self):
        self.my_setup_1()
        my.boolean_assert(self.driver.page_source, 'No HTML source')         
        self.my_teardown_1()

    def test_2_correct_url(self):
        self.my_setup_1()        
        my.assert_equal(LOGIN_TITLE, self.driver.title, f'Title: {LOGIN_TITLE} not found')
        print(self.driver.title)
        self.my_teardown_1()


class Testcase2(BasicTest):


    def test_1_create_users(self):
        # function variables
        text = ''
        # Arrange
        self.my_setup_1()
        # Goto create user
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        # Act, add users
        for i in range(len(good_users)):
            self.driver.find_element(*find.RESET).click()
            # Set user
            self.driver.find_element(*find.USER_ID).send_keys(good_users[i])
            # Set password
            self.driver.find_element(*find.PASSWORD).send_keys(good_passwords[i])
            # Create
            self.driver.find_element(*find.ACTION_BUTTON).click() 
            try:
                WebDriverWait(self.driver, 0).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                text += f'Bad user: {good_users[i]}, or bad pass: {good_passwords[i]}\n'
            except TimeoutException:
                success = self.driver.find_element(*find.OUTPUT_1).get_attribute('innerHTML')
                my.boolean_assert('successfully' in success, 'No CREATE success')
                continue             
        # Check no errors
        my.assert_equal('', text, text)   
        #self.delete_DB()# TODO doesn't work
        self.delete_everything()
        self.my_teardown_1()

    def test_2_check_DB(self):
        users_json = self.driver.execute_script('return getUsers()')
        user_data = json.loads(users_json)
        assert 0 == len(user_data)
    


