// sample-app/legacy_user_service.js
// This is the MODERNIZED reference copy — async/await, const/let, no callbacks.
// After the BobMigrate Lite skill runs on user_service.js, it should look like this.

const http = require('http');

async function getUserData(userId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'jsonplaceholder.typicode.com',
      path: '/users/' + userId,
      method: 'GET'
    };

    http.get(options, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        const user = { id: userId, name: 'Demo User' };
        resolve(user);
      });
    }).on('error', reject);
  });
}

module.exports = { getUserData };
