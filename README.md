# viewer

Lightweight FastAPI backend for authenticated data access and scraping helpers.

**Project type:** FastAPI app (Python >= 3.11) using PyMongo and PyJWT.

**Quick start:**

```bash
python main.py
```

**Repository layout (key files):**

- `main.py` — FastAPI app bootstrap and router wiring.
- `config.ini` — canonical config (DB URI, JWT secret). Keep secrets out of VCS.
- `src/viewer/auth/router.py` — authentication routes (`/auth/token`, `/auth/sign-in`, `/auth/sign-up`, `/auth/me`).
- `src/viewer/auth/service.py` — token creation and auth helpers (uses `jwt`, `bcrypt`).
- `src/viewer/public/*` — utilities: `database.py`, `dependencies.py`, `utils.py`, `models.py`.

**Important conventions:**

- OAuth2 password flow token URL: `auth/token` (used by `OAuth2PasswordBearer(tokenUrl="auth/token")`).
- Database selection: `get_collection(...)` maps specific collections to the `scraper` DB; others use `viewer` DB.

**Configuration:**

- Edit `config.ini` at repository root to set `AUTH.SECRET_KEY` and `DB` connection string.
