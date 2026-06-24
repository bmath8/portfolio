export const config = { matcher: "/((?!favicon.ico|robots.txt).*)" };

const PASSWORD = "brian2026";

export default function middleware(request) {
  const auth = request.headers.get("authorization");
  if (auth && auth.startsWith("Basic ")) {
    try {
      const decoded = atob(auth.slice(6));
      const pwd = decoded.slice(decoded.indexOf(":") + 1);
      if (pwd === PASSWORD) return;
    } catch (e) {}
  }
  return new Response("Authentication required.", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="Private preview"' },
  });
}