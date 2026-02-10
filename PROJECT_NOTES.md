# Project notes – Me Defino

**Start here when you come back after a break.** This file tracks what the app does, where things are documented, and what we’ve changed over time.

---

## Quick links

| What | Where |
|------|--------|
| **Live site** | https://www.medefino.com |
| **Login** | https://www.medefino.com/login/ |
| **Admin** | https://www.medefino.com/admin/ |
| **Define Your Path (events)** | https://www.medefino.com/define-your-path/ |
| **DeAnna's Diary** | https://www.medefino.com/deannas-diary/ |

---

## Docs in this project

| File | What it’s for |
|------|----------------|
| **README.md** | Setup, run locally, high-level overview. |
| **PROJECT_NOTES.md** | This file – “what we built” and changelog. |
| **GODADDY_RAILWAY_DOMAIN.md** | Pointing medefino.com (GoDaddy) at Railway. |
| **RAILWAY_MIGRATE.md** | Running migrations from your Mac (venv + public DB URL). |
| **RAILWAY_DEPLOYMENT.md** | Creating superuser, env vars, deployment on Railway. |
| **MUSIC_SETUP.md** | Background music on the site. |
| **BEHAVIOR_LOG.md** | (If you use it) Behavior / design notes. |

---

## What the app does (features)

- **Journal entries** – Create, edit, delete entries with images. Staff can publish/unpublish. Others can comment when logged in.
- **Define Your Path** – Event calendar (runs, hikes, adventures, etc.). Each event has **start** and **optional end** date/time, location, image, max participants.
- **DeAnna's Diary** – Diary pages (draft/public). Staff-only create/edit/delete.
- **Auth** – Login (email or username), logout, admin at `/admin/`. Custom logout at `/logout/` (no 405).
- **Theme** – Starry-night look: deep blue background, gold/amber accents (no pink). Nav highlights current page in gold.
- **Persistence** – PostgreSQL on Railway (via `DATABASE_URL`). Local dev can use `.env` + `python-dotenv` for migrate/createsuperuser.

---

## When you come back: run locally

```bash
cd /Users/deannariddlespur/personal/sisepuede-journal
source venv/bin/activate
pip install -r requirements.txt   # if needed
python manage.py migrate          # if there are new migrations
python manage.py runserver
```

Open http://127.0.0.1:8000/

---

## When you add new features

1. **Code** – Models, views, forms, templates, static files as usual.
2. **Migrations** – If you changed models: `python manage.py makemigrations` then `python manage.py migrate`. On Railway, run migrate with the public DB URL (see RAILWAY_MIGRATE.md) or let the release command do it.
3. **This file** – Add a short entry under “Changelog” below with the date and what you did, so next time you don’t forget.

---

## Changelog (what we accomplished)

*Add a line or two here whenever we add something meaningful. Date format: YYYY-MM-DD.*

- **2026-02-09** – GoDaddy (medefino.com) pointed at Railway. Custom domain + env vars (ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS). Root shows “coming soon”; www.medefino.com is the app.
- **2026-02-09** – PostgreSQL on Railway for persistent data. DATABASE_URL from Postgres service. Migrations/createsuperuser from Mac using public URL (see RAILWAY_MIGRATE.md). `.env` + python-dotenv for local migrate/createsuperuser.
- **2026-02-09** – Login fix: removed `form.add_error()` on unbound form; use `error_message` in context instead. Logout fix: custom `logout_view` (GET) at `/logout/` so nav “Logout” works (no 405).
- **2026-02-09** – README: live links table (site, login, admin). PROJECT_NOTES.md added (this file).
- **2026-02-09** – Starry-night theme: replaced pink with gold/amber (#d4a84b, #c9a227, #e8c547) and soft blue/lavender where needed. Nav “active” state only on current page; yellow/gold accent for current nav item.
- **2026-02-09** – Path events: added **End date & time** (optional). Form has “Start date & time” and “End date & time (optional)”. Migration: `0006_pathevent_event_end_date`. Detail page shows end date when set.
- **2026-02-09** – Admin static: WhiteNoise added; start command runs collectstatic before gunicorn so admin CSS/JS load in production.
