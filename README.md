# Screenly Basic Auth Demo

A static demo site showcasing [Screenly Basic Authentication](https://www.screenly.io/developers/authentication/). HTTP Basic Auth is enforced via Vercel Edge Middleware — no backend required.

## Credentials

```
Username: screenly
Password: admin
```

## Pages

- **`/landing.html`** — Public. Shown when not authenticated.
- **`/`** — Protected dashboard. Shown after successful auth.

## Deploy

Push to GitHub and import at [vercel.com/new](https://vercel.com/new). No configuration needed.

## Local dev

```bash
python3 server.py
# open http://localhost:8080
```

## Screenly setup

When adding the asset, click **+ Add Basic Auth** and enter the credentials above. The player sends the `Authorization` header automatically.
