# Me Defino - Define Yourself

A beautiful Django journaling application with image upload support.

---

## 🔗 Live site links (medefino.com)

| What        | URL |
|------------|-----|
| **Site**   | https://www.medefino.com |
| **Login**  | https://www.medefino.com/login/ |
| **Admin**  | https://www.medefino.com/admin/ |

Use your superuser username + password to log in. Admin is for managing entries, users, and content in the Django backend.

**Coming back after a while?** See **[PROJECT_NOTES.md](PROJECT_NOTES.md)** for what we’ve built, where docs live, and a short changelog so you don’t forget.

---

## Features

- 📝 Create, edit, and delete journal entries
- 🖼️ Upload images with your entries
- 🎨 Starry-night theme (deep blue, gold accents)
- 🔐 Secure user authentication
- 📱 Responsive design

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sisepuede-journal
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Deployment

### For Production

1. **Set environment variables**
   - `SECRET_KEY` - Django secret key
   - `DEBUG=False`
   - `ALLOWED_HOSTS` - Your domain(s)

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Configure media files**
   - Set up proper media file storage (AWS S3, etc.)
   - Update `MEDIA_ROOT` and `MEDIA_URL` in settings.py

4. **Set up database**
   - Use PostgreSQL or MySQL for production
   - Update `DATABASES` in settings.py

5. **Configure web server**
   - Use Gunicorn or uWSGI with Nginx
   - Example Gunicorn command:
     ```bash
     gunicorn journal.wsgi:application --bind 0.0.0.0:8000
     ```

## Project Structure

```
sisepuede-journal/
├── entries/          # Main journal app
│   ├── models.py     # JournalEntry model
│   ├── views.py      # Views for CRUD operations
│   ├── forms.py      # Forms for entries
│   └── templates/    # HTML templates
├── journal/          # Django project settings
│   ├── settings.py   # Project configuration
│   └── urls.py       # URL routing
├── media/            # User uploaded files
├── staticfiles/      # Collected static files
└── manage.py         # Django management script
```

## Technologies

- Django 6.0.1
- Python 3.12+
- Pillow (for image processing)
- SQLite (development) / PostgreSQL (production)

## License

MIT License
