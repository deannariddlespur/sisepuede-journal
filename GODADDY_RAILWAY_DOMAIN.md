# Connect Your GoDaddy Domain to Railway

Use this guide to point the domain you pay for at GoDaddy to your Me Defino journal app on Railway.

---

## What you need

- Your GoDaddy domain (e.g. `yourdomain.com` or `medefino.com`)
- Your Railway project: [railway.app/dashboard](https://railway.app/dashboard)
- About 5–15 minutes (DNS can take a few minutes to update)

---

## Step 1: Add the custom domain in Railway

1. Go to [railway.app](https://railway.app) and open your **sisepuede-journal** project.
2. Click your **service** (the app that’s deployed).
3. Open the **Settings** tab.
4. Find **Networking** or **Domains**.
5. Click **Add custom domain** (or **Generate domain** / **Custom domain**).
6. Enter your domain in one or both forms:
   - **Root:** `yourdomain.com`
   - **www:** `www.yourdomain.com`
7. Save. Railway will show you the **DNS target** for each (usually a CNAME like `1txbr6dw.up.railway.app` or a similar `*.up.railway.app` host). **Keep this page open** — you’ll use this in GoDaddy.

---

## Step 2: Point GoDaddy DNS to Railway

Log in at [godaddy.com](https://www.godaddy.com) → **My Products** → your domain → **DNS** (or **Manage DNS**).

### Option A: Use **www** (easiest on GoDaddy)

- **Type:** CNAME  
- **Name:** `www`  
- **Value:** the Railway CNAME target from Step 1 (e.g. `1txbr6dw.up.railway.app`)  
- **TTL:** 600 or 1 Hour  

Save. Your site will be at **https://www.yourdomain.com**.

### Option B: Use root domain (**yourdomain.com** without www)

GoDaddy does **not** allow a CNAME on the root (`@`). You have two choices:

**B1 – Redirect in GoDaddy (simplest)**  
- In GoDaddy DNS, add or edit a **forwarding** rule: `yourdomain.com` → `https://www.yourdomain.com` (permanent 301).  
- Then set up only **www** in Railway and in Step 3 below. Visitors to `yourdomain.com` will be sent to `www.yourdomain.com`.

**B2 – Use Cloudflare for DNS**  
- Add your domain to [Cloudflare](https://cloudflare.com) (free).  
- In GoDaddy, change the domain’s **nameservers** to the ones Cloudflare gives you.  
- In Cloudflare DNS, add the CNAME record Railway gives you; Cloudflare can “flatten” it so the root domain works.  
- Then add both `yourdomain.com` and `www.yourdomain.com` in Railway and in Step 3.

---

## Step 3: Tell Django to accept your domain (Railway env vars)

So Django and HTTPS work correctly, set these in **Railway** for your service:

1. Railway project → your service → **Variables** (or **Environment**).
2. Add or edit:

**ALLOWED_HOSTS**  
- If you only use **www**:  
  `www.yourdomain.com,1txbr6dw.up.railway.app`  
- If you use **root + www**:  
  `yourdomain.com,www.yourdomain.com,1txbr6dw.up.railway.app`  
- Use your real domain; no `https://`, no spaces (comma-separated).

**CSRF_TRUSTED_ORIGINS**  
- If you only use **www**:  
  `https://www.yourdomain.com,https://1txbr6dw.up.railway.app`  
- If you use **root + www**:  
  `https://yourdomain.com,https://www.yourdomain.com,https://1txbr6dw.up.railway.app`  
- Include `https://` and no spaces (comma-separated).

3. Save. Railway will redeploy; the app will then accept requests to your GoDaddy domain.

---

## Step 4: Wait for DNS and test

- DNS can take **5–30 minutes** (sometimes up to 48 hours).
- Then open:
  - **https://www.yourdomain.com** (or **https://yourdomain.com** if you set that up).
- If you see “connection not private” or certificate errors, wait a bit longer; Railway issues SSL for your custom domain automatically.

---

## Quick checklist

- [ ] Custom domain added in Railway (www and/or root).
- [ ] CNAME in GoDaddy: `www` → Railway’s CNAME target (and root handled by redirect or Cloudflare if needed).
- [ ] Railway env: `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` include your GoDaddy domain(s).
- [ ] Redeploy finished; tested in browser after DNS propagated.

If you tell me your exact domain (e.g. `medefino.com`), I can fill in the exact values for **ALLOWED_HOSTS** and **CSRF_TRUSTED_ORIGINS** for you.
