// sample-app/user_service.js
// LEGACY JavaScript — uses var, callbacks, and http.get.
// This is the TARGET file that the BobMigrate Lite skill modernizes.

var http = require('http');

function getUserData(userId, callback) {
  var options = {
    hostname: 'jsonplaceholder.typicode.com',
    path: '/users/' + userId,
    method: 'GET'
  };

  http.get(options, function(err, res) {
    if (err) {
      return callback(err, null);
    }
    var body = '';
    res.on('data', function(chunk) {
      body += chunk;
    });
    res.on('end', function() {
      var user = { id: userId, name: 'Demo User' };
      callback(null, user);
    });
  });
}

module.exports = { getUserData };
