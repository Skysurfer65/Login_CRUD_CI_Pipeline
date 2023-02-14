/**
**********************************************
* Login program with JSON Database
* @author Richard Fehling, MVT22 EC Utbildning
* @file store DB in Local storage
**********************************************
*/
class User{
    /**
     * @description Create user from class User.
     * nrOfAttempts is a variable to delete user if trying
     * to login with wrong pass 3 times during session.
     * @param {string} userID - From html form
     * @param {string} password - From html form
     * @param {string} admin - Set to YES || NO
     */   
    constructor( userID, password, admin){
        this.userID = userID;
        this.password = password;
        this.admin = admin;
        //Variable to check login attempts/session. Value not stored in database
        this.nrOfAttempts = 0;          
        }

    /**
     * @method valideUserID-UserClassMethod
     * @description Check to prerequisites
     * @param {string} adminID - Default or updated
     * @returns boolean
     */
    validateUserID(adminID) {
        let letter = false, number = false;
        let specialCharacters = " !#$%&'()*+,-./:;<=>?@[]^_`{|}";
        let numbers = "1234567890";
        
        //Check if userID empty, null, undefined, NaN etc.
        if(!this.userID) return false;
        
        //Check length of userID
        if (this.userID.length < 4 || this.userID.length > 30) return false;

        //No checks for admin. Will be checked later when updated in admin.js
        if (this.userID.toLocaleLowerCase() === adminID.toLocaleLowerCase()){ 
            this.admin = "YES";
            return true;
        } else this.admin = "NO";

        //Check for no empty space or special char, at least one letter and one number
        for (let i = 0; i < this.userID.length; i++) {
            if (specialCharacters.indexOf(this.userID[i]) > -1) return false;
            else if (numbers.indexOf(this.userID[i]) > -1) number = true;
            else letter = true;         
        }
        return (letter && number);
    }
    /**
     * @method validatePassword-UserClassMethod
     * @description Check to prerequisites
     * @returns boolean
     */
    validatePassword(){
        let specialChar = false, number = false, letter = false, upperCase = false;
        let specialCharacters = "!#$%&'()*+,-./:;<=>?@[]^_`{|}";
        let emptySpace = " ";
        let numbers = "1234567890";
        let capitalLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ";
            
        //Check if password is empty, null, undefined, NaN etc.
        if(!this.password) return false;
    
        //Check length
        if (this.password.length < 4 || this.password.length > 16) return false;
        
        //Check for no empty space but at least one letter, one number and one special character
        for (let i = 0; i < this.password.length; i++) {
            if (emptySpace.indexOf(this.password[i]) > -1) return false;
            else if (specialCharacters.indexOf(this.password[i]) > -1) specialChar = true;
            else if (numbers.indexOf(this.password[i]) > -1) number = true;
            else if (capitalLetters.indexOf(this.password[i]) > -1) upperCase = true;
            else letter = true;
        }  
        return (specialChar && number && upperCase && letter);
    }

    /**
     * @method checkUserInDB-UserClassMethod
     * @description User ID not case sensitive
     * @param {array} users - Array of User objects
     * @returns boolean
     */
    checkUserInDB(users){
        for (let i = 0; i < users.length; i++){
            if (users[i].userID.toLocaleLowerCase() === this.userID.toLocaleLowerCase()) return true;
        }
        return false;
    }

    /**
     * @method checkPassword-UserClassMethod
     * @description Also includes delete user if nrOfAttempts == 3
     * @param {array} users - array of User objects
     * @returns boolean
     */
    checkPassword(users){
        for (let i = 0; i < users.length; i++){
            //Check password to correct userID, not case sensitive
            if (users[i].userID.toLocaleLowerCase() === this.userID.toLocaleLowerCase()){
                //Password is case sensitive
                if (users[i].password === this.password) return true;
                //If not correct pass set nrOfAttempts
                else {
                    users[i].nrOfAttempts += 1;
                    if (users[i].nrOfAttempts == 3){
                        //Delete user from user array
                        users.splice(i, 1);
                    }
                }
            }
        }
        return false;
    }

    /**
     * @method addUserToUsers-UserClassMethod
     * @description Add user object to array users then stringify and save as DB in Local storage
     */
    addUserToUsers(){
        users.push(new User(this.userID, this.password, this.admin));
        //Save users to local storage
        let myLoginDB = JSON.stringify(users);
        localStorage.setItem("myLoginDB", myLoginDB); //Stored in browser local storage "kolla i utvecklarverktyg"
    } 
}
//For jest tests, will generate warning in browser debug, could be commented out for normal use
module.exports = User;        