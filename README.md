# KeeperApp Backend

FastAPI service for the Keeper notes application. It provides a database health check and note CRUD routes using SQLAlchemy and PostgreSQL.

## Requirements

- Python 3.10 or newer
- A reachable PostgreSQL database

## Local setup

Run these commands from the `KeeperAppBackend` directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `DATABASE_URL` to your PostgreSQL connection URL. This project uses Psycopg 3, so use the `postgresql+psycopg://` scheme. For Supabase, include `?sslmode=require`; URL-encode special characters in the password. Set `FRONTEND_ORIGINS` to the frontend origin, normally `http://localhost:5173`.

Do not commit `.env` or share a connection URL containing your password.

## Start the API

```powershell
uvicorn app.main:app --reload --port 8000
```

- Health check: `http://127.0.0.1:8000/api/health`
- Interactive API docs: `http://127.0.0.1:8000/docs`

## Current routes

- `GET /api/health` checks API-to-database connectivity.
- `GET /api/notes` lists notes; supports `status`, `q`, `limit`, and `offset` query parameters.
- `POST /api/notes` creates a note from a title and content.
- `GET /api/notes/{id}` retrieves one note.
- `PUT /api/notes/{id}` replaces a note's title and content.
- `PATCH /api/notes/{id}` updates supplied title, content, status, or pinned fields.
- `DELETE /api/notes/{id}` permanently deletes a note.

Note IDs are UUIDs. `createdAt` and `updatedAt` are Unix timestamps in milliseconds to match the frontend note type.

## Database status

The app does not create tables at startup. Do not create the tables manually. In the next phase, define the `users` and `notes` SQLAlchemy models and create the schema with Alembic migrations. Until those migrations are applied, the health check can verify the database connection, but note CRUD requires the notes table to exist.

Authentication and user-specific note access are not implemented yet. Keep this API restricted to local development until those protections are added.