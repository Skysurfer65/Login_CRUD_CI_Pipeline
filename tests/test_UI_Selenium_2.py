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
from ass_loc_func_Selenium import Assertions, Locators, Functions

### Test variabels and constants ##################################################################
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
func = Functions()
####################################################################################################

@pytest.fixture(params=["chrome"],scope="class")
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
    def function_setup(self):
        print('Function setup')
        self.driver.get("file:///" + LOGIN_HTML)
    
    def function_teardown(self):
        self.driver.delete_all_cookies()
        print('Function teardown')

    def delete_everything_selenium(self):
        self.driver.execute_script('deleteEverythingSelenium()')
    

class Testcase1(BasicTest):
    # Function for development
    def to_find_driver_functions(self):
        # To help IDE find type of driver
        driver : webdriver.Edge = self.driver 
     
    
    def test_1_source_found(self):
        self.function_setup()
        print('Check HTML source')
        my.boolean_assert(self.driver.page_source, 'No HTML source')         
        self.function_teardown()

    def test_2_correct_url(self):
        self.function_setup()        
        my.assert_equal(LOGIN_TITLE, self.driver.title, f'Title: {LOGIN_TITLE} not found')
        print(self.driver.title)
        self.function_teardown()

    def test_3_check_DB_empty(self):
        self.function_setup()
        print('Check empty database')
        self.delete_everything_selenium()
        user_data = func.get_users(self.driver)
        my.assert_equal(0, len(user_data), "Users array not empty")
        self.function_teardown()

class Testcase2(BasicTest):
    # Create good users with good passwords
    def test_1_create_users(self):
        # Arrange
        self.function_setup()
        self.delete_everything_selenium()
        # Goto create user
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        # Act, add users
        print('Add user to users')
        text, success = func.create_or_login_users(self.driver, good_users, good_passwords)      
        # Assert, check no errors but success
        my.assert_equal('', text, text)
        my.boolean_assert(success, 'No CREATE or Login success')
        # Cleanup   
        self.function_teardown()

    def test_2_usersDB(self):
        self.function_setup()
        user_data = func.get_users(self.driver)
        my.assert_equal(len(good_users), len(user_data), "Testdata and database not equal")
        self.delete_everything_selenium()
        self.function_teardown()

class Testcase3(BasicTest):
    # Login good users
    def test_1_login_good_users(self):
        # Arrange
        self.function_setup()
        print('Good users login')
        # Goto create user and add users
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        text, success = func.create_or_login_users(self.driver, good_users, good_passwords)
        my.boolean_assert(success, text)
        self.delete_everything_selenium()
        self.function_teardown()

    # Login good users with bad passwords
    def test_2_login_good_users_with_bad_pass(self):
        # Arrange
        self.function_setup()
        print('Good users with bad pass login')
        # Goto create user and add users
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        text, success = func.create_or_login_users(self.driver, good_users, bad_passwords)
        my.assert_not_equal('', text, "No login errors!?")
        print(text)
        my.boolean_assert(not success, 'One or more logins had no errors')
        self.delete_everything_selenium()
        self.function_teardown()

        
    # Login bad users with good passwords
    def test_2_login_bad_users_with_good_pass(self):
        # Arrange
        self.function_setup()
        print('Good users with bad pass login')
        # Goto create user and add users
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        self.driver.find_element(*find.CREATE_OR_LOGIN).click()
        text, success = func.create_or_login_users(self.driver, bad_users, good_passwords)
        my.assert_not_equal('', text, "No login errors!?")
        print(text)
        my.boolean_assert(not success, 'One or more logins had no errors')
        self.delete_everything_selenium()
        self.function_teardown()

    # Three bad login attempts
    def test_3_bad_login_attempts():
        pass    

class Testcase4(BasicTest):
    # Test admin page
    pass   


