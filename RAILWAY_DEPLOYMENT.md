# Railway Deployment Guide

## Creating a Superuser

Since this is a fresh deployment, you need to create a superuser account to login.

### Option 1: Using Railway CLI (Recommended)

1. Install Railway CLI if you haven't:
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. Link to your project:
   ```bash
   railway link
   ```

3. Run the createsuperuser command:
   ```bash
   railway run python manage.py createsuperuser
   ```

4. Follow the prompts:
   - Username: `deanna` (or your choice)
   - Email: `deanna.riddlespur@gmail.com`
   - Password: `Sunshine101!` (or your choice)

### Option 2: Using Railway Dashboard

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Deployments" tab
4. Click on the latest deployment
5. Open the "Shell" or "Console" tab
6. Run:
   ```bash
   python manage.py createsuperuser
   ```
7. Follow the prompts to create your user

## Login

Once you've created the superuser:

1. Go to your Railway app URL (something like: `https://your-app-name.up.railway.app`)
2. Click on `/login/` or go directly to the login page
3. Login with:
   - Email: `deanna.riddlespur@gmail.com` OR Username: `deanna`
   - Password: `Sunshine101!` (or whatever you set)

## Environment Variables

Make sure these are set in Railway:

- `SECRET_KEY` - Django secret key (generate a new one for production!)
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Your Railway domain (e.g., `your-app-name.up.railway.app`)

## Troubleshooting

If you can't login:
- Make sure you created the superuser successfully
- Check that migrations ran: `railway run python manage.py migrate`
- Verify environment variables are set correctly
- Check Railway logs for any errors

