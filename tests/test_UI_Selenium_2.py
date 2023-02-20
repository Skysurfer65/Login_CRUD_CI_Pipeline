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
#from time import sleep
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
# source "venv/Scripts/activate" 
# pytest -rA --capture sys --verbose --html=tests/test_reports/selenium_test_report.html tests/test_UI_Selenium_2.py           
####################################################################################################

# Setup for webdrivers, scope set to class
@pytest.fixture(params=['chrome', 'edge'],scope="class")
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
    # This is a parent class for setups/teardowns and 
    # to be able to choose different drivers or no driver
    # for testcases/classes
    def function_setup(self):
        print('Function setup')
        self.driver.get("file:///" + LOGIN_HTML)
    
    def function_teardown(self):
        self.driver.delete_all_cookies()
        print('Function teardown')

    def delete_everything_selenium(self):
        print('Cleanup')
        self.driver.execute_script('deleteEverythingSelenium()')
    
#Testcase-1-Basic-startup-and-DB-checks--------------------------------------------------------------
class Testcase1(BasicTest):
 
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
        user_data = func.get_users(self.driver)
        my.assert_equal(0, len(user_data), "Users array not empty")
        self.function_teardown()

#Testcase-2-Creation-of-users-and-check-DB------------------------------------------------------------
class Testcase2(BasicTest):

    # Create good users with good passwords
    def test_1_create_users(self):
        # Arrange
        self.function_setup()
        # Goto create user
        func.goto_create(self.driver)
        # Act, add users
        print('Create users')
        bad_text, success, good_text = func.create_or_login_users(
            self.driver, good_users, good_passwords)      
        # Assert, check no errors but success
        my.assert_equal('', bad_text, bad_text)
        my.boolean_assert(success, 'Unable CREATE or Login with some users')
        print(good_text)
        # Cleanup
        # Leave localstorage for test_2_usersDB  
        self.function_teardown()
    
    # Check results in DB, test only after test 1 in Testcase2
    def test_2_usersDB(self):
        self.function_setup()
        print('Check DB from test_1_create_users')
        user_data = func.get_users(self.driver)
        my.assert_equal(len(good_users), len(user_data), "Testdata and database not equal")
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()
        

#Testcase-3-Logins-good-and-bad-----------------------------------------------------------------------
class Testcase3(BasicTest):

    # Login good users
    def test_1_login_good_users(self):
        # Arrange
        self.function_setup()
        print('Good users and passwords login')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        func.goto_login(self.driver)
        bad_text, success, good_text = func.create_or_login_users(
            self.driver, good_users, good_passwords)
        # Assert
        my.assert_equal('', bad_text, bad_text)
        if success:
            print(good_text)
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()

    # Login good users with bad passwords
    def test_2_login_good_users_with_bad_pass(self):
        # Arrange
        self.function_setup()
        print('Good users with bad pass login')   
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        func.goto_login(self.driver)
        bad_text, success, good_text = func.create_or_login_users(
            self.driver, good_users, bad_passwords)
        # Assert
        my.assert_not_equal('', bad_text, "No login errors!?")
        print(bad_text)
        if success:
            print(f'Some logins worked: {good_text}')
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()
     
    # Login bad users with good passwords
    def test_3_login_bad_users_with_good_pass(self):
        # Arrange
        self.function_setup()
        print('Bad users with good pass login')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        func.goto_login(self.driver)
        bad_text, success, good_text = func.create_or_login_users(
            self.driver, bad_users, good_passwords)
        # Assert
        my.assert_not_equal('', bad_text, "No login errors!?")
        print(bad_text)
        if success:
            print(f'Some logins worked: {good_text}')
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()

    # Three bad login attempts
    def test_4_three_bad_login_attempts(self):
        # Arrange
        self.function_setup()
        print('Users three bad login attempts')
        three_bad_passwords = bad_passwords[0:3]
        good_user_times_3 = [good_users[0], good_users[0], good_users[0]]
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login
        func.goto_login(self.driver)
        bad_text, success, good_text = func.create_or_login_users(
            self.driver, good_user_times_3, three_bad_passwords)
        # Assert
        my.boolean_assert(not success, good_text)
        print(bad_text)
        # Check DB minus one
        users_data = func.get_users(self.driver)
        my.assert_equal(len(good_users) -1, len(users_data), "Checking list good_users against usersDB")
        print(f'{good_users[0]} deleted from database!')
        self.delete_everything_selenium()
        self.function_teardown()


#Testcase-4-Admin-and-CRUD-functions------------------------------------------------------------------
class Testcase4(BasicTest):
    # Test admin page
    def test_1_login_as_admin(self):
        # Arrange
        self.function_setup()
        print('Login as admin')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login as admin, index 2 in good lists
        func.goto_login(self.driver)
        admin, password = [good_users[2]], [good_passwords[2]]
        bad_text, success, good_text = func.create_or_login_users(self.driver, admin, password)
        # Assert, login success and page title is Admin
        my.boolean_assert(success, bad_text)
        print(good_text)
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()

    def test_2_display_DB(self):
        # Arrange
        self.function_setup()
        print('Display database')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login as admin
        func.goto_login(self.driver)
        func.login_as_admin(self.driver)
        # Display database
        self.driver.find_element(*find.DISPLAY_DB).click()
        # Assert
        database_name = self.driver.find_element(*find.USER_ID_2)
        my.assert_equal('admin', database_name.text, 'Pagelist not showing correct user name')
        print('Pagelist of database displayed')
        # Cleanup
        self.driver.find_element(*find.LOGOUT).click()
        self.delete_everything_selenium()
        self.function_teardown()

    def test_3_update_admin(self):
        # Arrange
        self.function_setup()
        print('Update admin')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login as admin
        func.goto_login(self.driver)
        func.login_as_admin(self.driver)
        # Update admin user name (user ID)
        self.driver.find_element(*find.UPDATE_ENTRY).click()
        alert = self.driver.switch_to.alert
        alert.send_keys('2') # Choose entry to update
        alert.accept()
        alert.send_keys('User ID') # Choose field to update
        alert.accept()
        alert.send_keys('newadmin1') # Set new admin user ID
        alert.accept()
        # Refresh page and dispay DB
        self.driver.refresh()
        self.driver.find_element(*find.DISPLAY_DB).click()
        # Assert
        database_name = self.driver.find_element(*find.USER_ID_2)
        my.assert_equal('newadmin1', database_name.text, 'Pagelist not showing updated user name')
        print('Pagelist updated')
        # Check local storage
        self.driver.find_element(*find.LOGOUT).click()
        new_DB_name = func.get_new_admin_ID(self.driver)
        my.assert_equal('newadmin1', new_DB_name, 'Database not showing updated user name')
        print('Database updated')
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()

    def test_4_admin_update_user(self):
        # Arrange
        self.function_setup()
        print('Admin update user')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Act, goto login and login as admin
        func.goto_login(self.driver)
        func.login_as_admin(self.driver)
        # Update someones username (user ID)
        self.driver.find_element(*find.UPDATE_ENTRY).click()
        alert = self.driver.switch_to.alert
        alert.send_keys('0') # Choose entry to update
        alert.accept()
        alert.send_keys('password') # Choose field to update
        alert.accept()
        alert.send_keys('Bax100#') # Set new user password
        alert.accept()
        # Refresh page and dispay DB
        self.driver.refresh()
        self.driver.find_element(*find.DISPLAY_DB).click()
        # Assert
        new_pass = self.driver.find_element(*find.USER_PASS_0)
        my.assert_equal('Bax100#', new_pass.text, 'Database not showing updated password')
        print('Database updated!')
        # Cleanup
        self.driver.find_element(*find.LOGOUT).click()
        self.delete_everything_selenium()
        self.function_teardown()

    def test_5_admin_delete_user(self):
        # Arrange
        self.function_setup()
        print('Admin delete user')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Goto login and login as admin
        func.goto_login(self.driver)
        func.login_as_admin(self.driver)
        # Delete user
        self.driver.find_element(*find.DELETE_ENTRY).click()
        alert = self.driver.switch_to.alert
        alert.send_keys('5') # Choose entry to delete
        alert.accept()
        # Assert
        # Goto index page and check DB minus one
        self.driver.find_element(*find.LOGOUT).click()
        users_data = func.get_users(self.driver)
        my.assert_equal(len(good_users) -1, len(users_data), "Checking list good_users against usersDB")
        print(f'{good_users[5]} deleted from database!')
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()

    def test_6_admin_delete_all(self):
        # Arrange
        self.function_setup()
        print('Admin delete all')
        # Goto create user and add users
        func.goto_create(self.driver)
        func.create_or_login_users(self.driver, good_users, good_passwords)
        # Goto login and login as admin
        func.goto_login(self.driver)
        func.login_as_admin(self.driver)
        # Delete all
        self.driver.find_element(*find.DELETE_ALL).click()
        alert = self.driver.switch_to.alert
        alert.accept()
        # Assert
        # Goto index page and check DB empty
        self.driver.find_element(*find.LOGOUT).click()
        users_data = func.get_users(self.driver)
        my.assert_equal(0, len(users_data), "Checking database empty")
        print('Database empty!')
        # Cleanup
        self.delete_everything_selenium()
        self.function_teardown()  


