# Login_CRUD_CI_Pipeline
## Login with admin CRUD. Javascript and HTML. Tested with JEST and Selenium in GitHub Actions.

# Continous Integration
In this setup I'm trying to get GitHub Actions to automate my tests
when the user push to the repository.<br/>
Unit and integrationtests are done on the javascript with **JEST** test package. Since javascript is a scripted language that needs an environment to be interpret (as it's normally done in the browser), I have to setup my VM to run Node. In this simulated back-end mode I can run my tests.
UI tests are done directly on the DOM by using **Selenium** to automate and **pytest** for assertions. This part of the project is written in **Python**. 
To see testresults you need to look into the logfiles under Actions.

-------------------------------------------------------------------------------------
If you want to try the app follow these instructions
# HOW-TO
!!! You cannot login without first creating an account !!!
- To create an account:
Click on "Create Account"
write User ID and Password according to prerequisites and click "CREATE",
create a bunch of logins!
- Login:
Click on "Go To Login" and test your login
- Admin account:
Create an Admin account to be able to perform CRUD operations.
Create account with "admin" as User ID. Admin as User ID can be
changed with CRUD operations after login as admin on "Admin page".

# Database
The pseudo database is visual as JSON in browser dev tool as "myLoginDB" in
Local storage. If you've changed "admin" User ID it will be stored
in Local storage as "newAdminID".

# Installation
No installation is necessary. Copy all folders and files under **src**
and place them in a folder on your computer. Open "index.html" from Edge
browser.

# Disclaimer
This is not aimed to be a secure login, only for javascript practice, CRUD
and testing purposes. It has been designed for Microsoft Edge but should work
fine in other browsers aswell.

# Author
Richard Fehling, student at EC Utbildning, MVT22<br/>
richard.fehling@learnet.se