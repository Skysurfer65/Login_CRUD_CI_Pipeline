/**
**********************************************
* Login program with JSON Database
* @author Richard Fehling, MVT22 EC Utbildning
**********************************************
*/

/**
 * @function promptText
 * @description Textfiles for admins to be displayed as alert, prompted or help
 * @param {integer} x - Integer to select text from switch case
 * @returns string
 */
function promptText(x) {
    let text = "";
    switch (x) {
        case 1:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += 'Which "Data ID" do you want to UPDATE?\n';
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            break;
        case 2:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += 'Which "Data ID" do you want to DELETE?\n';
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            break;
        case 3:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += 'Which key field do you want to update, "User ID" \nor "Password"?\n';
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            break;
        case 4:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += " Prerequisites:                                                     \n";
            text += " User ID has to be unique and consist of minimum 4 characters, max 30.\n";
            text += " Only letters  and numbers and at least one of each, user ID is not \n";
            text += " case sensitive, no empty spaces are allowed.                       \n";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            break;
        case 5:
            text = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n";
            text += " Prerequisites:                                                     \n";
            text += " Password has to have a minimum of 4 characters and consist of at   \n";
            text += " least one letter, one number and one special character. Passwords  \n";
            text += " are case sensitive and need to consist of both upper and lower     \n";
            text += " case letters. Maximum 16 characters.                               \n";
            text += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            break;
        case 6:
            text = "                                           HOW-TO\n";
            text += " Admin as User ID can be changed with CRUD operations and is good\n";
            text += " practice. The new admin User ID will follow standard User ID criteria.\n";
            text += " Minimum 4 characters and max 30, atleast one letter and one number. \n";
            text += " After a CRUD operation is done click on \"Display Current Database\"\n";
            text += " to see changes. Database fields could be removed with browser update.\n";
            text += " Database is visual as JSON in browser dev tool as \"myLoginDB\" in \n";
            text += " Local storage. An updated admin User ID will be there as \"newAdminID\"\n";
            text += " Tests could be viewed in browser console.";
            break;
    }
    return text;
}
