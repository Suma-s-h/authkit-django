# AuthKit — Django Authentication Starter Kit

A production-ready Django authentication starter with Bootstrap 5 UI, full user management, and a clean, extensible project structure.

---

## Features

| Feature | Details |
|---|---|
| Registration | Custom form with first/last name, email uniqueness check, terms agreement |
| Login | Remember-me (30-day session), safe `next`-URL redirect, error messages |
| Logout | POST-only with confirmation page |
| Dashboard | Profile card, account stats, quick-action buttons |
| Profile | Edit name, email, bio, location, phone, website, gender, avatar colour |
| Password change | Secure change with session preservation (no re-login required) |
| Password reset | Full 4-step email flow; never reveals whether an email is registered |
| Admin panel | Inline profile editing, custom list/filter/search on UserAdmin |
| Bootstrap 5 UI | Responsive sidebar layout, animated auth cards, dark-text alerts |
| Flash messages | Typed messages (success / error / warning / info) auto-dismiss after 5 s |
| Password UX | Show/hide toggle on every password field; strength meter on register |
| Security | CSRF on every POST, open-redirect guard on login, HSTS/secure cookies in production |

---

## Quick Start

### 1. Clone / unzip and enter the project

```bash
cd authkit
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional for dev)

```bash
cp .env.example .env
# Edit .env with your values
```

For development the defaults work without `.env` — SQLite is used and emails print to the console.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — you will be redirected to the login page.

---

## Running Tests

```bash
python manage.py test accounts
```

The test suite covers registration, login, logout, dashboard, profile updates, password change, password reset, open-redirect protection, and model behaviour (35+ assertions).

---

## Project Structure

```
authkit/
├── authkit/                  # Project configuration
│   ├── settings.py           # All settings, driven by env vars
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                 # Authentication app
│   ├── migrations/
│   ├── admin.py              # Inline profile on UserAdmin
│   ├── apps.py               # Registers signals via ready()
│   ├── forms.py              # Registration, login, profile, password forms
│   ├── models.py             # Profile (OneToOne to User)
│   ├── signals.py            # Auto-create Profile on User creation
│   ├── tests.py              # Full test suite
│   ├── urls.py               # accounts/* URL patterns
│   └── views.py              # All views (register, login, logout, dashboard, profile, password)
├── static/
│   ├── css/custom.css        # Brand utilities, transitions, animations
│   └── js/main.js            # Alert dismiss, password toggle, strength meter
├── templates/
│   ├── base.html             # Navbar + sidebar layout / auth wrapper
│   ├── accounts/
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── password_change.html
│   │   ├── password_reset.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_complete.html
│   │   └── logout_confirm.html
│   └── registration/
│       ├── password_reset_email.html
│       └── password_reset_subject.txt
├── .env.example
├── .gitignore
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## URL Reference

| URL | Name | Auth required |
|---|---|---|
| `/` | — | Redirects to dashboard |
| `/accounts/login/` | `login` | No |
| `/accounts/register/` | `register` | No |
| `/accounts/logout/` | `logout` | Yes |
| `/accounts/dashboard/` | `dashboard` | Yes |
| `/accounts/profile/` | `profile` | Yes |
| `/accounts/password/change/` | `password_change` | Yes |
| `/accounts/password/reset/` | `password_reset` | No |
| `/accounts/password/reset/done/` | `password_reset_done` | No |
| `/accounts/password/reset/<uid>/<token>/` | `password_reset_confirm` | No |
| `/accounts/password/reset/complete/` | `password_reset_complete` | No |
| `/admin/` | — | Staff only |

---

## Configuration

### Email

The default backend prints emails to the console (development). For production, set these env vars (or edit `.env`):

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=AuthKit <noreply@yourdomain.com>
```

### Database

SQLite is used by default. Switch to PostgreSQL:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=authkit
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432
```

Then `pip install psycopg2-binary` and re-run migrations.

---

## Production Checklist

- [ ] Set `SECRET_KEY` to a cryptographically random value (`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Set `DEBUG=False`
- [ ] Set `ALLOWED_HOSTS` to your domain(s)
- [ ] Configure a real email backend
- [ ] Switch to PostgreSQL (or another production database)
- [ ] Run `python manage.py collectstatic`
- [ ] Serve with Gunicorn behind Nginx (or use a platform like Railway / Render)
- [ ] Enable HTTPS — HSTS, secure cookies, and SSL redirect are applied automatically when `DEBUG=False`

---

## Customisation

**Change the accent colour** — edit `--primary` in `templates/base.html`

**Add registration fields** — extend `CustomRegistrationForm` in `accounts/forms.py` and update `register.html`

**Extend the Profile model** — add fields to `accounts/models.py`, then:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## License

MIT — free to use for personal and commercial projects.
