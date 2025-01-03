# PEV
Poll System Evaluation


## Clone the Repository
Clone and navigate to the project directory:

```bash
https://github.com/Alyzbane/AnalysenKompass.git
cd AnalysenKompass

```

## Setup and Run

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Running the Project

Run these commands manually:
```bash
cd pev
python manage.py migrate
python manage.py runserver
```

## Admin Access

Create a superuser account:
```bash
python manage.py createsuperuser
```

Then access the admin panel at: `http://127.0.0.1:8000/admin`

## Database

SQLite database file is located at `db.sqlite3`. No additional configuration needed - it's created automatically when you run migrations.

## Common URLs

- Homepage: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin`