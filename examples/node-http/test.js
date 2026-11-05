import assert from 'node:assert/strict';
import test from 'node:test';
import { createServer } from './server.js';

function start() {
  return new Promise((resolve) => {
    const server = createServer().listen(0, '127.0.0.1', () => resolve(server));
  });
}

test('serves the home page and a health check', async () => {
  const server = await start();
  const base = `http://127.0.0.1:${server.address().port}`;
  const health = await fetch(`${base}/healthz`);
  assert.equal(health.status, 200);
  assert.deepEqual(await health.json(), { status: 'ok' });
  const home = await (await fetch(base)).text();
  assert.match(home, /Internal app/);
  server.close();
});
