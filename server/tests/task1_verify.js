async function test() {
  const rEmpty = await fetch('http://localhost:3001/api/diagnose', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '' })
  });
  const dEmpty = await rEmpty.json();
  console.log('=== EMPTY QUERY RESULT ===');
  console.log('Verdict:', dEmpty.validation?.overallStatus);
  console.log('Fail Reasons:', dEmpty.validation?.failureReasons);
  console.log('Action:', dEmpty.action?.action);
  console.log('Deeplink:', dEmpty.deeplink?.deeplink);

  const rRotate = await fetch('http://localhost:3001/api/diagnose', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: "My screen isn't rotating automatically." })
  });
  const dRotate = await rRotate.json();
  console.log('\n=== AUTO ROTATE QUERY RESULT ===');
  console.log('Verdict:', dRotate.validation?.overallStatus);
  console.log('Action:', dRotate.action?.action);
  console.log('Deeplink:', dRotate.deeplink?.deeplink);
  console.log('Verified:', dRotate.deeplink?.verified);
}
test();
