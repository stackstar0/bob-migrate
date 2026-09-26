// sample-app/legacy_user_service.js
// Modernized JavaScript — async/await, const/let, arrow functions.

async function getUserData(userId) {
    const user = {
        id: userId,
        name: "Demo User"
    };

    await new Promise((resolve) => setTimeout(resolve, 100));
    return user;
}

module.exports = { getUserData };
