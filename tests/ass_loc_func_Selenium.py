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
    def create_or_login_users(self, object, users, passwords):
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
    
    def create_or_login_users_WIP(self, object, users, passwords):
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
            # Create or login
            driver.find_element(*loc.ACTION_BUTTON).click()
            if driver.find_element(*loc.OUTPUT_1):
                # If success
                text_frame = driver.find_element(*loc.OUTPUT_1).get_attribute('innerHTML')
            elif not driver.find_element(*loc.OUTPUT_1) :
                alert = driver.switch_to.alert
                alert.accept()
                text += f'Bad user: {users[i]}, or bad pass: {passwords[i]}\n'
            else:
                page_title = driver.title
                driver.find_element(*loc.LOGOUT).click()
  
            '''
            try:
                
                WebDriverWait(driver, 0).until(EC.presence_of_element_located(By.ID, 'output1'))
                # If success
                text_frame = driver.find_element(*loc.OUTPUT_1).get_attribute('innerHTML')
            except UnexpectedAlertPresentException:
                alert = driver.switch_to.alert
                alert.accept()
            except TimeoutError:
                pass   
                
            except Exception as e: 
                
                if e == UnexpectedAlertPresentException: # Something went wrong
                    alert = driver.switch_to.alert
                    alert.accept()
                    text += f'Bad user: {users[i]}, or bad pass: {passwords[i]}\n'
                elif e.__class__ == TimeoutException: # Admin page
                    page_title = driver.title
                    driver.find_element(*loc.LOGOUT).click()
                else: # Some other Exception
                    print(e)
                '''
                

                #if ('successfully' or 'CORRECT' in text_frame) or ('Admin' in page_title):
                #success = True             
        return text, success

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