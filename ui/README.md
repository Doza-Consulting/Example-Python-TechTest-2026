# UI

React + Vite + TypeScript front end for Escape Queue, a booking app for a
chain of escape room venues. It currently shows the API's status, the list of
rooms, and an About page explaining the company and what the app is for.

## Running locally

The UI needs the API running. From the repo root:

```bash
make install
make dev            # API on :3000 and UI on :5173 together
# or just the UI:
make dev-ui         # npm run dev -w ui
```

Open <http://localhost:5173>. The status badge in the header shows whether the
API is reachable.

The UI always calls relative `/api/...` URLs. In dev, Vite proxies them to
`http://localhost:3000` and strips the `/api` prefix (see
[vite.config.ts](vite.config.ts)). When deployed, CloudFront does the same
routing, so there is no CORS setup anywhere.

## Scripts

Run from the repo root with `-w ui`, or from this folder without it.

| Script | What it does |
|---|---|
| `npm run dev` | Vite dev server with hot reload |
| `npm test` | run Vitest once |
| `npm run test:watch` | Vitest in watch mode |
| `npm run build` | type-check, then build static files to `dist/` |
| `npm run preview` | serve the built `dist/` locally |

## Folder structure

```
ui/
├── index.html
├── vite.config.ts         dev proxy + Vitest config
├── tsconfig.json
└── src/
    ├── main.tsx           entry point (HashRouter)
    ├── App.tsx            layout, nav and routes
    ├── api.ts             API client and response types
    ├── styles.css         global styles
    ├── pages/
    │   ├── Rooms.tsx      room list (calls GET /rooms)
    │   └── About.tsx      company and app context
    ├── components/
    │   └── HealthBadge.tsx  API online/offline indicator
    └── test/
        └── setup.ts       Vitest setup (jest-dom matchers, cleanup)
```

Tests sit next to the code they cover as `*.test.tsx`.

## Testing

Vitest + React Testing Library in a jsdom environment.

- `pages/About.test.tsx`: a simple render test.
- `pages/Rooms.test.tsx`: stubs `fetch` so a component that calls the API can
  be tested without a server (success and error cases).
- `App.test.tsx`: routing and navigation using `MemoryRouter`.

## Good to know

- **Routing uses `HashRouter`** (URLs look like `/#/about`). The deployed site
  is static files on S3 behind CloudFront with no SPA fallback, so history-style
  URLs would 404 on refresh. Tests use `MemoryRouter` instead.
- Only `GET /health` and `GET /rooms` are implemented in the API, so booking
  and availability features have nothing to call yet.
- `api.ts` holds the response types by hand. They are not generated from the
  OpenAPI spec, so keep them in sync with [../api/openapi.yaml](../api/openapi.yaml).
- Deployed with `scripts/deploy-ui.sh`, which builds this app, uploads `dist/`
  to S3 and invalidates the CDN cache. See [../terraform](../terraform).
