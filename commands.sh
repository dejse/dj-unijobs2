. env/Scripts/activate
pip freeze > requirements.txt

# ETL
python src/ETL/1_run_scrappers.py
python src/ETL/2_create_big_json.py
python src/ETL/3_insert_db.py

# Django
cd src/Backend 
python manage.py runserver
python manage.py makemigrations jobs
python manage.py migrate

pnpx tailwindcss -i src/Backend/static/css/styles.css -o src/Backend/static/css/tailwind.css --watch

django-admin makemessages -l en
django-admin compilemessages

python manage.py test --keepdb