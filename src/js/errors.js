/**
**********************************************
* Login program with JSON Database
* @author Richard Fehling, MVT22 EC Utbildning
**********************************************
*/

/**
 * @function errors
 * @description Textfiles to be displayed as alert, prerequisites or help
 * @param {integer} x - number of text in switch case 
 * @returns string
 */
function errors(x) {
    let text = "";
    switch (x) {
        case 1:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += "                                  ERROR                             \n";
            text += " Prerequisites:                                                     \n";
            text += " User ID has to be unique and consist of minimum 4 characters, max 30.\n";
            text += " Only letters  and numbers and at least one of each, user ID is not \n";
            text += " case sensitive, no empty spaces are allowed.                       \n";
            text += "                                                                    \n";
            text += " Password has to have a minimum of 4 characters and consist of at   \n";
            text += " least one letter, one number and one special character. Passwords  \n";
            text += " are case sensitive and need to consist of both upper and lower     \n";
            text += " case letters. Maximum 16 characters.                               \n";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            break;
        case 2:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += "                                 ERROR                              \n";
            text += " User ID not in database, check your typing or                      \n";
            text += " create new account.                                                \n";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            break;
        case 3:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += "                                 ERROR                              \n";
            text += " Password not in database, check your typing, you have              \n";
            text += " three attempts.                                                    \n";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            break;
        case 4:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += "                                WARNING                             \n";
            text += " You have tried to reach this userID three times with invalid       \n";
            text += " password, this user Will be deleted. You may create new user.      \n";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            break;
        case 5:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!<br>";
            text += " <h3>Prerequisites:</h3><br>";
            text += " User ID has to be unique and consist of minimum 4 characters, max 30.<br>";
            text += " Only letters  and numbers and at least one of each, user ID is not <br>";
            text += " case sensitive, no empty spaces are allowed.                       <br>";
            text += "                                                                    <br>";
            text += " Password has to have a minimum of 4 characters and consist of at   <br>";
            text += " least one letter, one number and one special character. Passwords  <br>";
            text += " are case sensitive and need to consist of both upper and lower     <br>";
            text += " case letters. Maximum 16 characters.                               <br>";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!<br>";
            break;
        case 6:
            text = "                                           HOW-TO\n";
            text += " !!! You cannot login without first creating an account !!!\n";
            text += " To create an account:\n";
            text += " Click on \"Create Account\" \n";
            text += " write User ID and Password according to prerequisites and click \"CREATE\"\n";
            text += " Click on \"Go To Login\" and test your login, create a bunch of logins!\n";
            text += "                                                                    \n";
            text += " Create an Admin account to be able to perform CRUD operations:     \n";
            text += " Create account with \"admin\" as User ID. Admin as User ID can be\n";
            text += " changed with CRUD operations after login as admin on \"Admin page\"\n";
            text += " Database is visual as JSON in browser dev tool as \"myLoginDB\" in \n";
            text += " Local storage.";
            break;
    }
    return text;
}