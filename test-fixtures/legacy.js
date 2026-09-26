function getUserData(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: userId, name: "Hafiza" });
    }, 100);
  });
}

(async () => {
  try {
    const user = await getUserData(123);
    console.log(user);
  } catch (err) {
    console.error(err);
  }
})();

module.exports = { getUserData };
