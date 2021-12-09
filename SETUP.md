python -m venv venv\
source venv/bin/activate\
pip install -r requirements.txt\
python manage.py makemigrations\
python manage.py migrate\
python manage.py loaddata rest/fixtures/rest_fixtures.json\
python manage.py createsuperuser (optional)\