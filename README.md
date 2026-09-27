# Django Blog

A small multi-user blog built with Django:
- user registration, login and logout
- profile pages with an avatar upload
- create, read, update and delete posts, where only the author can edit or delete their own posts
- a paginated home feed and per-author pages

## Features

| Area | Details |
|---|---|
| Accounts | Sign-up form with email; login/logout with Django's auth views; a profile is created automatically for each new user (signal) |
| Posts | Class-based views for list, detail, create, update and delete, with `LoginRequiredMixin` and an author-only check (`UserPassesTestMixin`) |
| UI | Bootstrap 4 templates; forms rendered with django-crispy-forms |
| Tests | 6 tests covering public pages, the login requirement, author-only editing, the register flow and the profile signal (`python manage.py test`) |

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser      # optional, for /admin
python manage.py runserver
```

Configuration comes from environment variables:
- `DJANGO_SECRET_KEY`: required in any deployed environment
- `DJANGO_DEBUG`: `1` by default; set to `0` in production
- `DJANGO_ALLOWED_HOSTS`: comma-separated list

## What was fixed in this version

- **Restored the app code.** The repository only had migrations, forms and admin files, so the site couldn't start. The models, views,
  URLs, templates, signal and package `__init__` files were rebuilt to match the existing migrations. `makemigrations --check` confirms
  the models match them exactly.
- **Security.** The secret key was hard-coded and `DEBUG` was always on. Both now come from environment variables. The committed
  SQLite database, which contained user accounts, is no longer tracked. Because the old key is still in git history, treat it as
  compromised and never reuse it.
- **Upgraded to Django 5.2.** Logout is a POST form, as Django 5 requires, and crispy-forms 2 now uses the separate
  `crispy-bootstrap4` template pack.

Tools: Python, Django, SQLite, Bootstrap 4, django-crispy-forms.
