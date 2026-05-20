#!/bin/bash
# For Linux/Mac users. Windows users: use setup_windows.bat instead.
set -e

cd "$(dirname "$0")"

export DJANGO_DEBUG=1

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Install dependencies (skip psycopg2-binary locally — SQLite is used instead)
echo "Installing dependencies..."
grep -vE '(psycopg2|^\s*#|^\s*$)' requirements.txt | sed 's/#.*//' > /tmp/requirements_filtered.txt
.venv/bin/pip install -q -r /tmp/requirements_filtered.txt
rm -f /tmp/requirements_filtered.txt

# Run migrations
echo "Running migrations..."
.venv/bin/python manage.py makemigrations travel --noinput 2>/dev/null || true
.venv/bin/python manage.py migrate --noinput

# Import Excel data if DB is empty
RECORD_COUNT=$(.venv/bin/python manage.py shell -c "from travel.models import Travel; print(Travel.objects.count())" 2>/dev/null)
if [ "$RECORD_COUNT" = "0" ] && [ -f "travel.xlsx" ]; then
    echo "Importing data from travel.xlsx..."
    .venv/bin/python manage.py import_excel travel.xlsx
fi

# Collect static files
.venv/bin/python manage.py collectstatic --noinput 2>/dev/null || true

echo ""
echo "========================================="
echo "  Server running at http://localhost:8000"
echo "========================================="
echo ""

.venv/bin/python manage.py runserver 0.0.0.0:8000
