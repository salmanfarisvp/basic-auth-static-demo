export const config = {
  // Protect everything except landing.html (which is always public)
  matcher: ["/((?!landing\\.html).*)"],
};

const USERNAME = "screenly";
const PASSWORD = "admin";
const COOKIE_NAME = "screenly_demo_auth";

export default function middleware(request) {
  // 1. Accept real HTTP Basic Auth (used by the Screenly player)
  const auth = request.headers.get("authorization") ?? "";
  const expected = "Basic " + btoa(`${USERNAME}:${PASSWORD}`);
  if (auth === expected) {
    return;
  }

  // 2. Accept session cookie (set by the browser login form on landing.html)
  const cookies = request.headers.get("cookie") ?? "";
  if (cookies.includes(`${COOKIE_NAME}=1`)) {
    return;
  }

  // 3. Neither valid — redirect to the public landing page
  const url = new URL(request.url);
  return Response.redirect(`${url.origin}/landing.html`, 302);
}
