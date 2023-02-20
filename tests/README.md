# Unit tests with Jest
Testing classUser functions:
- validateUserID()
- validatePassword()
- checkUserInDB()
- checkPassword()

# To run
# Jest unit-tests
In console write: **npm run testcov**<br/>
Of course, all node modules for jest has to be installed first.<br/>
npm install jest -D<br/>

# Selenium tests
Testing application on with Chrome and Edge browsers.<br/>
test_UI_Selenium_2.py is the valid script written in python and validated by **pytest**
Run froom root with **pytest -rA --verbose tests/test_UI_Selenium_2.py**
Run single tests **pytest -rA --verbose tests/test_UI_Selenium_2.py::Testcase2::test_1_create_users**
If you want a HTML test report:<br/> 
**pytest -rA --capture sys --verbose --html=tests/test_reports/selenium_test_report.html tests/test_UI_Selenium_2.py** 

# Author
Richard Fehling, student at EC Utbildning, MVT22<br/>
richard.fehling@learnet.se