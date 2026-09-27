// Legacy ES5 Callback Service
var fs = require('fs');

function getUserData(userId, callback) {
  var user = { id: userId, role: "admin" };
  setTimeout(function() {
    if (!userId) {
      return callback(new Error("User ID is required"), null);
    }
    return callback(null, user);
  }, 100);
}

module.exports = { getUserData: getUserData };
