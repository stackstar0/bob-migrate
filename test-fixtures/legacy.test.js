(async () => {
  const { getUserData } = require('./legacy');

  // 1. Call getUserData and capture the result
  const result = getUserData(123);

  // 2. Assert the result is a Promise
  if (result instanceof Promise) {
    console.log('PASS: getUserData(123) returns a Promise');
  } else {
    console.error('FAIL: getUserData(123) did not return a Promise');
    process.exit(1);
  }

  // 3. Await and assert the resolved value
  const user = await result;

  if (user.id === 123) {
    console.log('PASS: user.id === 123');
  } else {
    console.error(`FAIL: expected user.id === 123, got ${user.id}`);
    process.exit(1);
  }

  if (user.name === 'Hafiza') {
    console.log('PASS: user.name === "Hafiza"');
  } else {
    console.error(`FAIL: expected user.name === "Hafiza", got ${user.name}`);
    process.exit(1);
  }

  console.log('\n✅ All tests passed.');
  process.exit(0);
})().catch((err) => {
  console.error('FAIL: Unexpected error —', err);
  process.exit(1);
});
