# selenium 4
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
# For Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# Python
import os
import json
import pytest


# Test variables
good_users = ["bax1", "Bax2", "admin", " spaces1 ", "Åäö20", "longUserID01234567890123456789"]
good_passwords = ["Bax1#", "2aX#", "Bax3%", "40bAx?", "20Åäö&", "LongPass##012345"]
bad_users = ["", "richard", "adam1@", "baxen1#", "pat rik", "tooLongID0123456789012345678901"]
bad_passwords = ["", "P1#", "password1#", "Password#", "Pass word1#", "TooLongPass#34567"]

# Invoke Chrome
# Experimental option to keep webpage open during development
#options_chrome = ChromeOptions()
#options_chrome.add_experimental_option("detach", True)
#driver_chrome = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options_chrome)
driver_chrome = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def test_1_setup():       
    # Get relative path to local html
    html_file = os.getcwd() + "//" + "..//src//html/index.html"
    driver_chrome.get("file:///" + html_file)
    assert driver_chrome.page_source, "No HTML page found"

def test_2_title_login():
    title_chrome = driver_chrome.title
    assert title_chrome == "Login", "Wrong page title"

def test_3_create_users():
    # function variables
    text = ''
    # Goto create
    driver_chrome.find_element(By.ID, "createOrLogin").click()
    # Create accounts
    for i in range(len(good_users)):
        driver_chrome.find_element(By.ID, "reset").click()
        # Set user
        driver_chrome.find_element(By.ID, "userID").send_keys(good_users[i])
        # Set password
        driver_chrome.find_element(By.ID, "password").send_keys(good_passwords[i])
        # Create
        driver_chrome.find_element(By.ID, "actionButton").click()
        try:
            WebDriverWait(driver_chrome, 0).until(EC.alert_is_present())
            alert = driver_chrome.switch_to.alert
            alert.accept()
            text += f'Bad user: {good_users[i]}, or bad pass: {good_passwords[i]}\n'
        except TimeoutException:
            continue
    assert text == '', text

def test_4_usersDB():
    users_json = driver_chrome.execute_script('return getUsers()')
    user_data = json.loads(users_json)
    assert len(good_users) == len(user_data)

def test_5_login_users():
    # function variables
    text = ''
    # Goto login
    driver_chrome.find_element(By.ID, "createOrLogin").click()
    # Login
    for i in range(len(good_users)):
        if good_users[i] == 'admin': continue
        driver_chrome.find_element(By.ID, "reset").click()
        # Set user
        driver_chrome.find_element(By.ID, "userID").send_keys(good_users[i])
        # Set password
        driver_chrome.find_element(By.ID, "password").send_keys(good_passwords[i])
        # Login
        driver_chrome.find_element(By.ID, "actionButton").click()
        try:
            WebDriverWait(driver_chrome, 0).until(EC.alert_is_present())
            alert = driver_chrome.switch_to.alert
            alert.accept()
            text += f'Bad user: {good_users[i]}, or bad pass: {good_passwords[i]}\n'
        except TimeoutException:
            continue
    assert text == '', text

def test_6_three_bad_attempts():
    # function variables
    text = ''  
    # Login, good_user with 3 bad_passwords
    for i in range(3):
        # Reset login page
        driver_chrome.find_element(By.ID, "reset").click()
        # Set user
        driver_chrome.find_element(By.ID, "userID").send_keys(good_users[5])
        # Set bad password
        driver_chrome.find_element(By.ID, "password").send_keys(bad_passwords[i])
        # Login
        driver_chrome.find_element(By.ID, "actionButton").click()
        try:
            WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
            alert = driver_chrome.switch_to.alert
            alert.accept()
            text += f'Good user: {good_users[5]} with bad pass: {bad_passwords[i]}\n'
        except TimeoutException:
            continue
    assert text != '', text
    # Check DB minus one
    users_json = driver_chrome.execute_script('return getUsers()')
    user_data = json.loads(users_json)
    assert len(good_users) -1 == len(user_data), "Checking list good_users against usersDB"

def test_7_admin():
    driver_chrome.find_element(By.ID, "reset").click()
    # Set user admin index 2 in good_users
    driver_chrome.find_element(By.ID, "userID").send_keys(good_users[2])
    # Set password
    driver_chrome.find_element(By.ID, "password").send_keys(good_passwords[2])
    # Login
    driver_chrome.find_element(By.ID, "actionButton").click()
    title_chrome = driver_chrome.title
    assert title_chrome == "Admin", "Wrong page title"

def test_8_admin_update():
    # On admin page from previous test
    driver_chrome.find_element(By.ID, "displayDB").click()
    user_id_2 = driver_chrome.find_element(By.XPATH, '//*[@id="tableDB"]/tr[4]/td[2]')
    # Check admin as user name
    assert good_users[2] == user_id_2.text
    # Choose update
    driver_chrome.find_element(By.ID, "updateEntry").click()
    WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
    alert = driver_chrome.switch_to.alert
    alert.send_keys('2')
    alert.accept()
    WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
    alert.send_keys('User ID')
    alert.accept()
    WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
    alert.send_keys('newadmin1')
    alert.accept()
    # Refresh webpage
    driver_chrome.refresh()
    driver_chrome.find_element(By.ID, "displayDB").click()
    user_id_2 = driver_chrome.find_element(By.XPATH, '//*[@id="tableDB"]/tr[4]/td[2]')
    # Check newadmin1 as admin name
    assert 'newadmin1' == user_id_2.text

def test_9_user_update():
    # On admin page from previuos test and refresh
    driver_chrome.refresh()
    # Choose update
    driver_chrome.find_element(By.ID, "updateEntry").click()
    WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
    alert = driver_chrome.switch_to.alert
    alert.send_keys('0')
    alert.accept()
    WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
    alert.send_keys('User ID')
    alert.accept()
    WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
    alert.send_keys('baluba1')
    alert.accept()
    driver_chrome.find_element(By.ID, "displayDB").click()
    user_id_0 = driver_chrome.find_element(By.XPATH, '//*[@id="tableDB"]/tr[2]/td[2]')
    # Check baluba1 as new user name
    assert 'baluba1' == user_id_0.text

def test_10_admin_delete_all():
    driver_chrome.find_element(By.ID, "deleteEverything").click()
    try:
        WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
        alert = driver_chrome.switch_to.alert
        alert.accept()
        assert True
    except TimeoutException:
        assert False, "No delete all Alert shown"
    
def test_11_empty_DB():
    # Return to start page
    driver_chrome.find_element(By.ID, "logout").click()
    # Check empty DB
    users_json = driver_chrome.execute_script('return getUsers()')
    user_data = json.loads(users_json)
    assert 0 == len(user_data)

def test_12_create_bad_users():
    # Test bad usernames with good passwords
    # function variables
    text = ''
    # Goto create
    driver_chrome.find_element(By.ID, "createOrLogin").click()
    # Create accounts
    for i in range(len(bad_users)):
        driver_chrome.find_element(By.ID, "reset").click()
        # Set bad user
        driver_chrome.find_element(By.ID, "userID").send_keys(bad_users[i])
        # Set good password
        driver_chrome.find_element(By.ID, "password").send_keys(good_passwords[i])
        # Create
        driver_chrome.find_element(By.ID, "actionButton").click()
        try:
            WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
            alert = driver_chrome.switch_to.alert
            alert.accept()    
        except TimeoutException:
            text += f'No Alert for user: {bad_users[i]} with pass: {good_passwords[i]}\n'
    assert text == '', text    

def test_13_create_bad_passwords():
    # Test good usernames with bad passwords
    # function variables
    text = ''
    # Create accounts
    for i in range(len(good_users)):
        driver_chrome.find_element(By.ID, "reset").click()
        # Set good user
        driver_chrome.find_element(By.ID, "userID").send_keys(good_users[i])
        # Set bad password
        driver_chrome.find_element(By.ID, "password").send_keys(bad_passwords[i])
        # Create
        driver_chrome.find_element(By.ID, "actionButton").click()
        try:
            WebDriverWait(driver_chrome, 2).until(EC.alert_is_present())
            alert = driver_chrome.switch_to.alert
            alert.accept()    
        except TimeoutException:
            text += f'No Alert for user: {good_users[i]} with pass: {bad_passwords[i]}\n'
    assert text == '', text 

def test_14_empty_DB_and_teardown():
    # Check empty DB
    users_json = driver_chrome.execute_script('return getUsers()')
    user_data = json.loads(users_json)
    assert 0 == len(user_data)
    # Quit
    driver_chrome.quit()




    
    
        