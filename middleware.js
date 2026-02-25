export const config = {
  matcher: "/:path*",
};

const USERNAME = "screenly";
const PASSWORD = "admin";

const UNAUTHORIZED_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>401 – Unauthorized</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #ffffff;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      text-align: center;
      padding: 48px 40px;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.06);
      max-width: 360px;
      width: 100%;
    }
    .logo-mark {
      width: 40px; height: 40px;
      background: #0d6efd;
      border-radius: 9px;
      display: flex; align-items: center; justify-content: center;
      margin: 0 auto 20px;
    }
    .logo-mark svg { width: 22px; height: 22px; fill: #fff; }
    h1 { font-size: 20px; font-weight: 700; margin-bottom: 8px; color: #1a1a1a; }
    p  { font-size: 14px; color: #6b7280; line-height: 1.5; }
    .code {
      display: inline-block;
      font-size: 11px;
      font-family: monospace;
      background: #f3f4f6;
      border: 1px solid #e5e7eb;
      border-radius: 5px;
      padding: 2px 7px;
      margin-top: 16px;
      color: #374151;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo-mark">
      <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="3" width="16" height="11" rx="1.5"/>
        <rect x="7" y="15" width="6" height="1.5" rx=".75"/>
        <rect x="9.25" y="14" width="1.5" height="2" rx=".75"/>
      </svg>
    </div>
    <h1>401 Unauthorized</h1>
    <p>This page is protected by Screenly Basic Auth.<br/>Valid credentials are required.</p>
    <span class="code">WWW-Authenticate: Basic realm="Screenly Demo"</span>
  </div>
</body>
</html>`;

export default function middleware(request) {
  const auth = request.headers.get("authorization") ?? "";
  const expected = "Basic " + btoa(`${USERNAME}:${PASSWORD}`);

  if (auth === expected) {
    return; // valid — pass the request through to the static file
  }

  return new Response(UNAUTHORIZED_HTML, {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="Screenly Demo"',
      "Content-Type": "text/html; charset=utf-8",
    },
  });
}
