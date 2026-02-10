# Run Migrations on Railway (from your computer)

Your Mac can’t use Railway’s private database URL. Use the **public** URL once to run migrations.

---

## Step A: Get your public database URL

1. Go to **railway.app** → your project.
2. Click the **Postgres** service (the database).
3. Open **Variables** or **Connect**.
4. Find **DATABASE_PUBLIC_URL** (or the connection string that has a host like `xxx.railway.app` or `xxx.proxy.rlwy.net` — **not** `postgres.railway.internal`).
5. Click to **copy** that full URL (starts with `postgresql://` or `postgres://`).

---

## Step B: One-time setup (venv + install)

Copy everything below, paste into Terminal, press Enter. Do this from your project folder.

```bash
cd /Users/deannariddlespur/personal/sisepuede-journal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step C: Run migrations (copy, paste your URL, run)

1. Replace **YOUR_PUBLIC_URL_HERE** in the command below with the URL you copied in Step A (paste between the single quotes).
2. Copy the full line.
3. In Terminal (with venv active: you should see `(venv)`), paste and press Enter.

```bash
DATABASE_URL='YOUR_PUBLIC_URL_HERE' python manage.py migrate --noinput
```

Wait until you see “OK” for each migration.

---

## Step D: Create your admin user again

Same idea: replace **YOUR_PUBLIC_URL_HERE** with your public URL, then run.

```bash
DATABASE_URL='YOUR_PUBLIC_URL_HERE' python manage.py createsuperuser
```

Enter username, email, and password when prompted.

---

## Step E: Reload the site

Open **https://www.medefino.com** and log in with that user.
