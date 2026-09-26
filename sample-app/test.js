// sample-app/test.js
// Verifies that the modernized getUserData returns a Promise that resolves
// with the expected user object.  Exit 0 on success, 1 on failure.

const { getUserData } = require("./legacy_user_service");

async function run() {
    console.log("--- BobMigrate Lite Test Suite ---\n");

    // 1. Result must be a Promise
    const result = getUserData(101);

    if (!(result instanceof Promise)) {
        console.error("FAIL: getUserData(101) did not return a Promise.");
        console.error(`      Got: ${Object.prototype.toString.call(result)}`);
        process.exit(1);
    }
    console.log("PASS: getUserData(101) returns a Promise.");

    // 2. Promise must resolve with the correct user object
    const user = await result;

    if (user.id !== 101) {
        console.error(`FAIL: expected user.id === 101, got ${user.id}`);
        process.exit(1);
    }
    console.log(`PASS: user.id === ${user.id}`);

    if (user.name !== "Demo User") {
        console.error(`FAIL: expected user.name === "Demo User", got "${user.name}"`);
        process.exit(1);
    }
    console.log(`PASS: user.name === "${user.name}"`);

    console.log("\n✅ All tests passed.");
    process.exit(0);
}

run().catch((err) => {
    console.error("FAIL: Unhandled error —", err.message);
    process.exit(1);
});
