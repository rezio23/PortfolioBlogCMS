# Portfolio Blog CMS

A Django starter project for a personal portfolio and blog CMS backed by MySQL.

## Features

- Split settings for base, development, and production
- Blog, portfolio, contact, core, and accounts apps
- Template, static, media, and docs folders already organized
- MySQL-ready environment configuration

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Update `.env` with your MySQL credentials.
4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

## Settings Module

Development uses `config.settings.development`.

Production uses `config.settings.production`.
