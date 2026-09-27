// sample-app/test.js
// Bob Shell test runner — validates that user_service.js exports a Promise-based function.
// Run: node sample-app/test.js
// Exit 0 = PASS (modernized), Exit 1 = FAIL (still legacy callback).

const service = require('./user_service');

console.log("=== Running Bob Shell Automated Test Runner ===");

async function runTest() {
  try {
    const result = service.getUserData(101);

    // Asserts that the refactored function returns a Promise
    if (result && typeof result.then === 'function') {
      const data = await result;
      if (data && data.id === 101) {
        console.log("✅ TEST PASSED: getUserData returns an async Promise with correct id.");
        process.exit(0);
      }
      console.error("❌ TEST FAILED: Promise resolved but data.id !== 101. Got:", data);
      process.exit(1);
    }

    console.error("❌ TEST FAILED: getUserData did not return a Promise — still uses legacy callback pattern.");
    process.exit(1);
  } catch (err) {
    console.error("❌ TEST ERROR:", err.message);
    process.exit(1);
  }
}

runTest();
