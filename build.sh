set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating admin user..."
python create_admin.py

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build complete!"