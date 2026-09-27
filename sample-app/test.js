const service = require('./user_service');

console.log("=== Running Bob Shell Automated Test Runner ===");

async function runTest() {
  try {
    const result = service.getUserData(101);

    // Asserts that the refactored function returns a Promise
    if (result && typeof result.then === 'function') {
      const data = await result;
      if (data && data.id === 101) {
        console.log("✅ TEST PASSED: Function converted to Async/Await Promise successfully!");
        process.exit(0);
      }
    }

    console.error("❌ TEST FAILED: Function still uses legacy callback pattern or returns undefined.");
    process.exit(1);
  } catch (err) {
    console.error("❌ TEST ERROR:", err.message);
    process.exit(1);
  }
}

runTest();
