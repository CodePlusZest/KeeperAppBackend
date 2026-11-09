# KeeperApp Backend

FastAPI and SQLAlchemy backend for the Keeper notes app. This first backend phase provides PostgreSQL persistence, a database health check, and note CRUD. Authentication and per-user access are intentionally deferred to the next phase; do not expose this unauthenticated API publicly.

## Setup

Use Python 3.10 or newer. From this directory:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `DATABASE_URL` to the PostgreSQL connection string for the database you created. For a Supabase connection, use its PostgreSQL connection string and keep `sslmode=require`. Do not commit `.env` or paste database credentials into source files.

Run the API:

```powershell
uvicorn app.main:app --reload
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

- `GET /api/health` checks API and database connectivity.
- `GET /api/notes` lists notes, optionally filtered by `status` (`active`, `archived`, or `trash`) and `q`; supports `limit` and `offset`.
- `POST /api/notes` creates a note from `{ "title": "...", "content": "..." }`.
- `GET /api/notes/{id}` retrieves one note.
- `PUT /api/notes/{id}` replaces a note's title and content.
- `PATCH /api/notes/{id}` updates any supplied title, content, status, or pinned fields.
- `DELETE /api/notes/{id}` permanently deletes a note. Set status to `trash` with PATCH to move it to trash instead.

Response IDs are UUID strings. `createdAt` and `updatedAt` are Unix timestamps in milliseconds to match the current frontend type.

The app does not create database tables on startup. In the next phase, define the `users` and `notes` tables with SQLAlchemy and create them through versioned Alembic migrations; do not create them manually. Until those migrations are added and applied, note CRUD endpoints require the tables to already exist. Authentication and per-user ownership should be added before exposing the API publicly.