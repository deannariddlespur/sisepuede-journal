# Why images show as broken on Railway (and how to fix it)

## What’s going on

The **image path is stored in the database** (e.g. `diary/2026/02/photo.jpg`). The **file itself** is stored on the server’s disk in `media/`.

On Railway, the app filesystem is **ephemeral**: every redeploy gets a fresh container. So:

- After a deploy, `media/` is empty.
- The database still has the path, so Django still generates URLs like `/media/diary/photo.jpg`.
- The browser requests that URL, but the file no longer exists → **broken image**.

So “my image is in the database” is correct — the **reference** is there; the **file** was lost on redeploy.

## Fix: persistent media with a Railway volume

Use a **Railway Volume** so `media/` lives on a disk that survives redeploys.

### 1. Create a volume in Railway

1. Open your project on [Railway](https://railway.app).
2. Select the service that runs the Django app.
3. Go to **Variables** or **Settings** and find **Volumes**, or add a new **Volume** from the dashboard.
4. Create a volume and **mount path**: e.g. `/data` (Railway will show the exact mount path).

### 2. Set the env var

Add a variable so Django uses that path for uploads:

- **Name:** `RAILWAY_VOLUME_MOUNT_PATH`  
- **Value:** the mount path (e.g. `/data`)

The app is already configured to use it: when `RAILWAY_VOLUME_MOUNT_PATH` is set, `MEDIA_ROOT` becomes `{mount_path}/media`, so all uploads go to the volume.

### 3. Redeploy

Redeploy the service so it starts with the new variable. After that, new uploads will be stored on the volume and will still be there after future deploys.

### 4. Existing broken images

Records that point to files **uploaded before** the volume was set are still broken (those files are gone). You can:

- Re-upload those images in the admin (or via your app), or  
- Leave them as-is; the site will hide broken images so they don’t show a broken icon.

---

**Summary:** The DB only stores paths. The real files must live on a persistent disk (e.g. a Railway volume). Set `RAILWAY_VOLUME_MOUNT_PATH` and redeploy so new uploads persist.
