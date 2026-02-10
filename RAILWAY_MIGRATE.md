# Run Migrations on Railway (from your computer)

Railway doesn’t always show a Shell in the dashboard. Use the **Railway CLI** from your laptop so migrations and createsuperuser run against your live database.

## 1. Install Railway CLI

**Mac (Homebrew):**
```bash
brew install railway
```

**Or with npm:**
```bash
npm i -g @railway/cli
```

## 2. Log in and link the project

In a terminal:

```bash
cd /Users/deannariddlespur/personal/sisepuede-journal
railway login
```

A browser window will open to log you in. Then:

```bash
railway link
```

- Choose your **Railway account** (if asked).
- Choose the **sisepuede-journal** project.
- Choose the **app** service (the one that runs Django), **not** Postgres.

## 3. Run migrations

```bash
railway run python manage.py migrate --noinput
```

Wait until you see “OK” for each migration. When it’s done, the `django_session` error should be fixed.

## 4. Create your admin user again (new DB = no users)

```bash
railway run python manage.py createsuperuser
```

Enter username (e.g. `deanna`), email, and password when prompted.

## 5. Reload the site

Open https://www.medefino.com (or your Railway URL) and log in with that user.

---

**Summary:**  
`railway link` → point at your **app** service. Then `railway run python manage.py migrate --noinput` and `railway run python manage.py createsuperuser`.
