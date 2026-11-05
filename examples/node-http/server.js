// A minimal internal app that follows the platform rules:
// - listens on 0.0.0.0 and on the PORT the platform provides
// - has a health check
// - reads configuration from environment variables, never from the source
import http from 'node:http';
import { pathToFileURL } from 'node:url';

export function createServer() {
  const title = process.env.APP_TITLE ?? 'Internal app';
  return http.createServer((req, res) => {
    if (req.url === '/healthz') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ok' }));
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`<!doctype html><title>${title}</title><h1>${title}</h1><p>Deployed with the EOS CLI.</p>`);
  });
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const port = Number(process.env.PORT ?? 8080); // the platform supplies PORT at run time
  createServer().listen(port, '0.0.0.0', () => console.log(`listening on 0.0.0.0:${port}`));
}
