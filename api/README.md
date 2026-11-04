# API

FastAPI (Python) REST API for Escape Queue, a booking engine for a chain of
escape room venues. Customers can see room availability publicly; venue staff
manage bookings and game-master assignments. The full contract is in
[openapi.yaml](openapi.yaml) (paste it into <https://editor.swagger.io> to
browse it).

## Running locally

From the repo root:

```bash
make install          # creates api/.venv and installs dependencies
make dev-api          # or: cd api && .venv/bin/python -m uvicorn app.main:create_app --factory --reload
```

The API listens on <http://localhost:3000>. Check it with:

```bash
curl http://localhost:3000/health     # {"status":"ok"}
curl http://localhost:3000/rooms
```

It reloads on save (uvicorn `--reload`). Set `PORT` to use a different port.
FastAPI also serves interactive docs at <http://localhost:3000/docs>.

Requires Python 3.12+. SQLite uses Python's built-in `sqlite3`, so there is
nothing native to compile.

## Commands

Run from the repo root.

| Command | What it does |
|---|---|
| `make dev-api` | run with hot reload |
| `make test-api` | run the pytest tests |
| `make build-lambda` | bundle for AWS Lambda into `api/dist-lambda/` |

Dependencies live in `requirements-lambda.txt` (what the deployed function
needs), `requirements.txt` (adds the local server and boto3) and
`requirements-dev.txt` (adds test tools).

## Folder structure

```
api/
├── openapi.yaml           API contract
├── requirements*.txt
├── pytest.ini
├── app/
│   ├── main.py            app factory: create_app(store=None)
│   ├── lambda_handler.py  AWS Lambda entry point (same app, via Mangum)
│   ├── models.py          Room, GameMaster, Booking models (Pydantic)
│   ├── seed.py            seed rooms and game masters
│   ├── deps.py            FastAPI dependencies (get_store)
│   ├── errors.py          error response helpers
│   ├── routes/            one router per resource
│   │   ├── health.py
│   │   ├── auth.py
│   │   ├── rooms.py
│   │   └── bookings.py
│   └── store/             storage layer
│       ├── base.py        the Store interface the routes use
│       ├── __init__.py    picks an implementation from env vars
│       ├── sqlite.py      local dev + tests
│       └── dynamodb.py    deployed on AWS
└── tests/                 pytest tests
```

## Endpoints

| Method | Path | Status |
|---|---|---|
| GET | `/health` | ✅ Implemented (reference pattern) |
| GET | `/rooms` | ✅ Implemented |
| POST | `/auth/register` | 🔲 Stubbed (`501`) |
| POST | `/auth/login` | 🔲 Stubbed (`501`) |
| GET | `/rooms/:id/availability` | 🔲 Stubbed (`501`) |
| GET | `/bookings` | 🔲 Stubbed (`501`) |
| POST | `/bookings` | 🔲 Stubbed (`501`) |
| GET | `/bookings/:id` | 🔲 Stubbed (`501`) |
| PATCH | `/bookings/:id` | 🔲 Stubbed (`501`) |
| POST | `/bookings/:id/assign` | 🔲 Stubbed (`501`) |

Errors use the shape `{ "error": { "code": "...", "message": "..." } }`.
Stubs return it with code `NOT_IMPLEMENTED`. Each stub has a `TODO` in its
docstring describing what it should do.

## Domain

- **Room**: has a name, theme, min/max party size and a running time
  (`duration_minutes`, `durationMinutes` in JSON). Three are seeded: The Vault
  (2–6 players, 60 min), Cursed Manor (3–8, 75 min) and Lost Signal (2–4,
  45 min).
- **Booking**: a party's reservation of a room for a time window. It has a
  `status` (`confirmed` or `cancelled`) and an optional game master. Times are
  ISO 8601 strings. `endTime` is derived from the room's duration.
- **Game master**: a staff member who runs a session. Two are seeded.

Models are written with snake_case field names and exposed as camelCase JSON
(see `app/models.py`).

## Storage

Routes use the `Store` in [app/store/base.py](app/store/base.py) and never
touch a database directly. Inject it into a route with
`store: Store = Depends(get_store)`. The implementation is chosen by
environment variable:

| Variable | Default | Meaning |
|---|---|---|
| `STORAGE` | `sqlite` | `sqlite` or `dynamodb` |
| `SQLITE_PATH` | `./data/escapequeue.db` | SQLite file (when `STORAGE=sqlite`) |
| `TABLE_PREFIX` | none | DynamoDB table prefix (required when `STORAGE=dynamodb`) |
| `PORT` | `3000` | local server port |

- Rooms and game masters are seeded on first start if their tables are empty.
  Bookings start empty.
- Local data is a file in `api/data/` (git-ignored). Delete the folder to reset.
- Each repo has `list`, `get` and, for bookings, `insert` and `update`. Any
  method you add must be added to the interface **and** to both
  implementations.
- Deployed, the tables are created by Terraform (see [../terraform](../terraform)).

## Testing

Tests use pytest and FastAPI's `TestClient` and live in `tests/`. Build the
app with a throwaway in-memory store and call it in-process, with no server or
port needed:

```python
from fastapi.testclient import TestClient

from app.main import create_app
from app.store.sqlite import create_sqlite_store

client = TestClient(create_app(create_sqlite_store(":memory:")))
res = client.get("/rooms")
```

Each test that builds its own store starts from a clean seeded database. See
`test_health.py` and `test_rooms.py` for examples.

## Good to know

- There is **no authentication** and **no request validation** yet. Every
  route is open.
- The router-per-resource layout is a starting point, not a requirement.
- On AWS the same FastAPI app runs in Lambda behind CloudFront, which sends
  `/api/*` to it. `lambda_handler.py` strips the `/api` prefix, so routes are
  identical locally and deployed.
