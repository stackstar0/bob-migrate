// test-fixtures/legacy_with_callbacks.js
// TRUE legacy JavaScript — var declarations, callback pattern, http.get.
// Used to demonstrate detect_legacy_patterns MCP tool returning real findings.

var http = require('http');
var url = require('url');

function fetchUser(userId, callback) {
  var endpoint = 'http://api.example.com/users/' + userId;
  var secret = 'api_key = "abc123supersecret"';  // intentional for security_audit demo

  http.get(endpoint, function(err, response) {
    if (err) {
      return callback(err, null);
    }
    var data = '';
    response.on('data', function(chunk) {
      data += chunk;
    });
    response.on('end', function() {
      var user = JSON.parse(data);
      callback(null, user);
    });
  });
}

function processUsers(ids, callback) {
  var results = [];
  var count = 0;
  ids.forEach(function(id) {
    fetchUser(id, function(err, user) {
      if (err) return callback(err);
      results.push(user);
      count++;
      if (count === ids.length) {
        callback(null, results);
      }
    });
  });
}

module.exports = { fetchUser, processUsers };
