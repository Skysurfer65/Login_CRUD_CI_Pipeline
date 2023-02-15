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
    # To be able to choose driver use for test class
    pass
class Test_URL(BasicTest):
    # Function for development
    def to_find_driver_functions(self):
        # To help IDE find type of driver
        driver : webdriver.Edge = self.driver
      
    def test_open_url(self):
        self.driver.get(lamb_url)
        print(self.driver.title)
        my.assert_equal('Most Powerful Cross Browser Testing Tool Online | LambdaTest',self.driver.title )
        
    def test_login(self):
        login = self.driver.find_element(*find.LOGIN)
        login.click()
        print(self.driver.title)
        my.assert_equal('Log in', self.driver.title)          


