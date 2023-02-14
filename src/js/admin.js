/**
**********************************************
* Login program with JSON Database
* @author Richard Fehling, MVT22 EC Utbildning
* @file store DB in Local storage
**********************************************
*/

//Page variables
let adminLocalDB = [];

//DOM objects
const dispDB = document.getElementById("displayDB");
const logOut = document.getElementById("logout");
const updEntry = document.getElementById("updateEntry");
const delEntry = document.getElementById("deleteEntry");
const delEverything = document.getElementById("deleteEverything");
const helpAdminTxt = document.getElementById("helpAdmin");

//For test
const testOutput = document.getElementById("testOutput");

//Get data from database
retrievingData();

//Button actions
dispDB.onclick = displayDB;
logOut.onclick = logout;
updEntry.onclick = updateEntry;
delEntry.onclick = deleteEntry;
delEverything.onclick = deleteEverything;
helpAdminTxt.onclick = helpAdmin;

//Functions
/**
 * @function retrievingData 
 * @description Database from Local storage
 * stored locally in "adminLocalDB"
 */
function retrievingData(){
    let textDB = localStorage.getItem("myLoginDB");
    adminLocalDB = JSON.parse(textDB);
}

/**
 * @function displayDB 
 * @description Dynamic table for display of database
 */
function displayDB(){
    let counter = 0;
    let myTable = document.getElementById("tableDB");
    
    //Make static header
    let tr = document.createElement('TR');
    myTable.appendChild(tr);
    let th1 = document.createElement('TH');
    tr.appendChild(th1);
    th1.appendChild(document.createTextNode("Data ID"));       
    let th2 = document.createElement('TH');
    tr.appendChild(th2);
    th2.appendChild(document.createTextNode("*** User ID ***"));             
    let th3 = document.createElement('TH');
    tr.appendChild(th3);
    th3.appendChild(document.createTextNode("** Password **"));
    let th4 = document.createElement('TH');
    tr.appendChild(th4);
    th4.appendChild(document.createTextNode("** Admin **"));

    //Make dynamic table of data
    retrievingData();     
    adminLocalDB.forEach(user => {
        let tr = document.createElement('TR');
        myTable.appendChild(tr);
        let td1 = document.createElement('TD');
        tr.appendChild(td1);
        td1.appendChild(document.createTextNode(counter));       
        let td2 = document.createElement('TD');
        tr.appendChild(td2);
        td2.appendChild(document.createTextNode(user.userID));             
        let td3 = document.createElement('TD');
        tr.appendChild(td3);
        td3.appendChild(document.createTextNode(user.password));
        let td4 = document.createElement('TD');
        tr.appendChild(td4);
        td4.appendChild(document.createTextNode(user.admin));        
        counter++ 
    });
}

/**
 * @function helpAdmin
 * @description HTML alert with helptext
 */
function helpAdmin(){
    alert(promptText(6));
}

/**
 * @function logout
 * @description Back to index page when logout
 */
function logout(){
    window.location.replace("index.html");
}

/**
 * @function promptIntInput
 * @description Parse input string to integer, take prompt text as param.
 * @param {string} text - from promptText.js
 * @returns integer 
 */
function promptIntInput(text){
    let input = parseInt(prompt(promptText(text)), 10);
    return input;
}

/**
 * @function promptTxtInput
 * @description take prompt text as param
 * @param {string} text - from promptText.js
 * @returns string 
 */
function promptTxtInput(text){
    let input = prompt(promptText(text));
    //Regex to remove spaces
    input = input.replace(/ /g, "");
    return input;    
}

/**
 * @function updateEntry 
 * @description Either User ID or Password.
 * Update default admin User ID to new ID according
 * to prerequisites
 */
function updateEntry(){
    let n = promptIntInput(1);
    if (n >= 0 && n < adminLocalDB.length){
        let inputTxt = promptTxtInput(3);
        let valid = false;
        //Update user ID, truncate input enough to write "user"
        if (inputTxt.toLowerCase().substring(0, 4) === "user"){
            do {
                var newUserID = promptTxtInput(4); //"var" selected to reach outside block
                //TODO använda class User metoder istället
                valid = validateUserID(newUserID);
                if (!valid) alert("!!! NOT A VALID SELECTION !!!");       
            } while (!valid);
            //If admin changes his/her user ID
            if (adminLocalDB[n].userID.toLocaleLowerCase() === "admin" ||
            adminLocalDB[n].userID.toLocaleLowerCase() === localStorage.getItem("newAdminID").toLocaleLowerCase()){
                //Set newAdminID in local storage
                localStorage.setItem("newAdminID", newUserID);
            }
            //Save to adminLocalDB
            adminLocalDB[n].userID = newUserID;
            saveToDB(adminLocalDB);
        }

        //Update password, truncate input enough to write "pass"
        else if (inputTxt.toLowerCase().substring(0, 4) === "pass"){
            let newPassword;
            do {
                newPassword = promptTxtInput(5);
                //TODO använda class User metoder istället 
                valid = validatePassword(newPassword);
                if (!valid) alert("!!! NOT A VALID SELECTION !!!");              
            } while (!valid);
            adminLocalDB[n].password = newPassword;
            saveToDB(adminLocalDB);           
        }
        else { 
            alert("!!! NOT A VALID SELECTION !!!")
        }
        
    } else {
        alert("!!! NOT A VALID SELECTION !!!")
    }

}

/**
 * @function deleteEntry
 * @description Row in database identified by Data ID
 * If admin deletes own entry and admin User ID has been
 * changed it will also delete "newAdminID" in Local storage
 */
function deleteEntry(){
    let n = promptIntInput(2);
    if (n >= 0 && n < adminLocalDB.length){
        //If admin wants to delete his/her entry
        if (adminLocalDB[n].userID === "admin" || adminLocalDB[n].userID === localStorage.getItem("newAdminID")){
            //Delete newAdminID in localstorage
            localStorage.removeItem("newAdminID");
        }
        adminLocalDB.splice(n, 1);
        saveToDB(adminLocalDB);
    } else {
        alert("!!! NOT A VALID SELECTION !!!")
    }
}

/**
 * @function deleteEverything
 * @description Delete all stored data in Local storage
 */
function deleteEverything(){
    if (confirm("!!! Are you shure to delete the whole list !!!")) {
        //Delete database
        localStorage.removeItem("myLoginDB");
        //Delete stored new admin User ID
        localStorage.removeItem("newAdminID");
      } //Else return to Admin page
}

/**
 * @function saveToDB
 * @description Stringify array and save to database
 * @param {array} adminLocalDB - Objects of User
 */
function saveToDB(adminLocalDB){
    let myLoginDB = JSON.stringify(adminLocalDB);
    localStorage.setItem("myLoginDB", myLoginDB);
}

/**
 * @function validateUserID
 * @description Check updated User ID according to prerequisites
 * @param {string} newUserID - spaces removed
 * @returns true || false
 */
function validateUserID(newUserID){
    let letter = false, number = false;
    let specialCharacters = " !#$%&'()*+,-./:;<=>?@[]^_`{|}";
    let numbers = "1234567890";
    
    //Check if userID empty
    if(!newUserID) return false;
    // if (newUserID == null) return false;
    // if (newUserID.isEmpty) return false;
    //Check length
    if (newUserID.length < 4 || newUserID.length > 30) return false;
    //Check if userID already exists
    for (let i = 0; i < adminLocalDB.length; i++){
        //UserID not case sensitive
        if (adminLocalDB[i].userID.toLocaleLowerCase() === newUserID.toLocaleLowerCase()) return false;
    }
    
    //Check for no empty space or special char, at least one letter and one number
    for (let i = 0; i < newUserID.length; i++) {
        if (specialCharacters.indexOf(newUserID[i]) > -1) return false;
        else if (numbers.indexOf(newUserID[i]) > -1) number = true;
        else letter = true;         
    }
    return (letter && number);
}

/**
 * @function validatePassword
 * @description Check updated Password according to prerequisites
 * @param {string} newPassword - spaces removed
 * @returns true || false
 */
function validatePassword(newPassword){
    let specialChar = false, number = false, letter = false, upperCase = false;
    let specialCharacters = "!#$%&'()*+,-./:;<=>?@[]^_`{|}";
    let emptySpace = " ";
    let numbers = "1234567890";
    let capitalLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ";
        
    //Check if password is empty
    if(!newPassword) return false;
    // if (newPassword == null) return false;
    // if (newPassword.isEmpty) return false;
    //Check length
    if (newPassword.length < 4 || newPassword.length > 16) return false;
    
    //Check for no empty space but at least one letter, one number and one special character
    for (let i = 0; i < newPassword.length; i++) {
        if (emptySpace.indexOf(newPassword[i]) > -1) return false;
        else if (specialCharacters.indexOf(newPassword[i]) > -1) specialChar = true;
        else if (numbers.indexOf(newPassword[i]) > -1) number = true;
        else if (capitalLetters.indexOf(newPassword[i]) > -1) upperCase = true;
        else letter = true;
    }  
    return (specialChar && number && upperCase && letter);
}


