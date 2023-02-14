/**
**********************************************
* Login program with JSON Database
* @author Richard Fehling, MVT22 EC Utbildning
* @file store DB in Local storage
**********************************************
*/
//Array for users
let users = [];
//Admin user ID to be updated
let adminID = "";
//Boolean for create account
let accountCreation = false;

//DOM variables
const helpTxt = document.getElementById("help");
const createOrLogin = document.getElementById("createOrLogin");
const reset = document.getElementById("reset");
const actionButton = document.getElementById("actionButton");
const header = document.getElementById("header");
const form = document.getElementById("login");

//Clear text
const clearTextID = document.getElementById("userID");
const clearTextPass = document.getElementById("password");

//Outputs text
const output1 = document.getElementById("output1");
const output2 = document.getElementById("output2");

//Button functions
helpTxt.onclick = help;
createOrLogin.onclick = createAccount;
reset.onclick = resetSuccess;
clearTextID.onclick = resetSuccess;
clearTextPass.onclick = resetSuccess;
actionButton.onclick = login;

//Put prerequsites info on page
resetSuccess();
//Check if database is available
setUpDB();
setUpAdmin();    

/**
 * @function  setUpDB
 * @description Check if DB available and load into users[]
 */
//Functions
function setUpDB(){
    if (localStorage.getItem("myLoginDB") !== null) {
        let textDB = localStorage.getItem("myLoginDB");
        users = JSON.parse(textDB);
        }
}

/**
 * @function setUpAdmin
 * @description Check if admin User ID has been changed and load into adminID
 */
function setUpAdmin(){
    if (localStorage.getItem("newAdminID") === null) {
        adminID = "admin";
        } else {
            adminID = localStorage.getItem("newAdminID");
        }
}

/**
 * @function login
 * @description Main function for login or create account, reads object of User class.
 */
function login() {
    //Make object of User        
    let user = new User(form.userID.value.trim(), form.password.value.trim());

    if (accountCreation){
        if (!user.checkUserInDB(users) && user.validateUserID(adminID) && user.validatePassword()){
            //Add to user ArrayList
            user.addUserToUsers();
            output1.innerHTML = "Login credentials<br>succesfully created!";
        } else alert(errors(1));

    } else {
        if (user.checkUserInDB(users)){
            //If you're admin
            let thisIsAdmin = false;
            if (user.userID.toLocaleLowerCase() === adminID.toLocaleLowerCase()){
                thisIsAdmin = true;
            }           
            //Check password
            if (user.checkPassword(users)){
                //Redirect to Admin page
                if (thisIsAdmin){
                    pageRedirect();
                }
                output1.innerHTML = "CORRECT<br>You're logged in";
                output2.innerHTML = "Reset to remove this message";
            } else {
                let outOfAttempts = true;
                users.forEach(userObject => {
                    if (userObject.userID.toLocaleLowerCase() === user.userID.toLocaleLowerCase()){
                        outOfAttempts = false;
                        alert(errors(3));
                    }             
                });       
                if (outOfAttempts){
                    //Update database  
                    let myLoginDB = JSON.stringify(users);
                    localStorage.setItem("myLoginDB", myLoginDB);
                    //If admin with own User ID
                    if (thisIsAdmin){
                        localStorage.removeItem("newAdminID");
                        setUpAdmin(); 
                    }
                    alert(errors(4));                      
                }      
            }
        } else alert(errors(2));                
    }
}

/**
 * @function createAccount
 * @description GUI setup for creating account
 */
function createAccount(){
    accountCreation = true;
    //Change GUI
    header.innerHTML = "Create Account";
    actionButton.value = "CREATE";
    createOrLogin.value = "Go To Login";
    createOrLogin.onclick = goToLogin;
}

/**
 * @function goToLogin
 * @description GUI setup for login
 */
function goToLogin(){
    accountCreation = false;
    //Change GUI
    resetSuccess();
    header.innerHTML = "Login";
    actionButton.value = "Login";
    createOrLogin.value = "Create Account";
    createOrLogin.onclick = createAccount;
}

/**
 * @function help
 * @description Display help file
 */
function help() {
   alert(errors(6)); 
}

/**
 * @function resetSuccess
 * @description Cleans up GUI after creation or login
 */
function resetSuccess(){
    output1.innerHTML = "";
    output2.innerHTML = errors(5);
}

/**
 * @function pageRedirect
 * @description Redirect admin after login
 */
function pageRedirect() {
    window.location.replace("admin.html");
}

/**
 * @function getUsers
 * @description Experimental function for Selenium (måste köras med js executor)
 * @returns string presentation of objects in users
 */
function getUsers(){
    getUsersStr = JSON.stringify(users, null, 1);
    return getUsersStr;
}
