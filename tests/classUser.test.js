/**
**********************************************
* Unit test of class UIser
* @author Richard Fehling, MVT22 EC Utbildning
**********************************************
*/
//Setup class User dependency
const User = require("../src/js/classUser.js");

//Unittests of classUser.js
//*************************

describe('Checking validateUserID() in class User', () => {
  //Setup test arrays
  const goodUsers = ["bax1", "Bax2", "admin", "Admin", "Åäö20", "longUserID01234567890123456789"];
  const badUsers = ["", null, undefined, "axl", "richard", "adam1@", "pat rik", "tooLongID0123456789012345678901"];
  //Variables
  let adminID;   
  
  test('Validate "admin" User ID and this.admin = true', () => {
      let user = new User("admin", null, null);
      adminID = "admin";
      expect(user.validateUserID(adminID)).toBeTruthy();
      expect(user.admin).toBeTruthy();
    });

  test('Validate newAdminID User ID and this.admin = true', () => {
        let user = new User("my1admin", null, null);
        adminID = "my1admin";
        expect(user.validateUserID(adminID)).toBeTruthy();
        expect(user.admin).toBeTruthy();
      });

  test.each(goodUsers)('tested good User ID (%s)', (userID) => {
    let user = new User(userID, null, null);
    adminID = "admin";
    expect(user.validateUserID(adminID)).toBeTruthy(); 
  });

  test.each(badUsers)('tested bad User ID (%s)', (userID) => {
    let user = new User(userID, null, null);
    adminID = "admin";
    expect(user.validateUserID(adminID)).toBeFalsy(); 
  });
});

describe('Checking validatePassword() in class User', () => {
  //Setup test arrays  
  const goodPasswords = ["Bax1#", "2aX#", "Bax3%", "40bAx?", "20Åäö&", "LongPass##012345"];
  const badPasswords = ["", null, undefined, "P1#", "password1#", "Pass#", "Pass word1#", "TooLongPass#34567"];

  test.each(goodPasswords)('tested good password (%s)', (password) => {
    let user = new User(null, password, null);
    expect(user.validatePassword()).toBeTruthy(); 
  });
  
  test.each(badPasswords)('tested bad password (%s)', (password) => {
    let user = new User(null, password, null);
    expect(user.validatePassword()).toBeFalsy(); 
  });
});

describe('Checking checkUserInDB() in class User', () => {
  //Setup test arrays
  const goodUsers = ["bax1", "Bax2", "admin", "Admin", "Åäö20", "longUserID01234567890123456789"]; 
  const users = [];

  //Make a mock database
  goodUsers.forEach(userID => {
    let $user = new User(userID, null, null);
    users.push($user);  
  });

  test.each(users)('Check user ID (%s) in mockDB', (userID) => {
    expect(userID.checkUserInDB(users)).toBeTruthy(); 
  });
  
  test.each(users)('Check user ID "baluba5" not in mockDB', () => {
    let baluba5ID = new User("baluba5", null, null);
    expect(baluba5ID.checkUserInDB(users)).toBeFalsy(); 
  });

});

describe('Checking checkPassword() in class User', () => {
  //Setup test arrays
  const goodUsers = ["bax1", "Bax2", "admin", "Admin1", "Åäö20", "longUserID01234567890123456789"]; 
  const goodPasswords = ["Bax1#", "2aX#", "Bax3%", "40bAx?", "20Åäö&", "LongPass##012345"];
  const badPasswords = [" Password1#", "Pass word1#", "TooLongPass#34567", "Password1# "];
  const users = [];

  //Make a mock database
  goodUsers.forEach(userID => {
    let $user = new User(userID, null, null);
    users.push($user);  
  });
  for (let i = 0; i < users.length; i++){
    users[i].password = goodPasswords[i]
  };

  test.each(users)('Check password (%s) in mockDB', (password) => {
    expect(password.checkPassword(users)).toBeTruthy();
  });

  //Setup bad person with correct pass in mock database
  let badPerson = new User("bax1", "Baxen1#", null);
  let badPersUsers = [badPerson];

  //Do 4 bad logins with wrong pass
  let badTry = new User("bax1", null, null);
  test.each(badPasswords)('Check bad password (%s) against mockDB', (password) => {
    badTry.password = password;
    expect(badTry.checkPassword(badPersUsers)).toBeFalsy();
    expect(badPerson.nrOfAttempts).toBeLessThanOrEqual(3);
  });
  //After 3 bad logins with wrong pass user deleted
  test('Empty array after 3 bad pass', () => {
    expect(badPersUsers.length).toBe(0);
  });

});

