// Modernized ES2022 Service — async/await, const/let, Promise
const fs = require('fs');

async function getUserData(userId) {
  if (!userId) {
    throw new Error("User ID is required");
  }
  const user = { id: userId, role: "admin" };
  await new Promise((resolve) => setTimeout(resolve, 100));
  return user;
}

module.exports = { getUserData };
