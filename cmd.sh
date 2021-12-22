env\Scripts\activate

# ETL
python ETL\1_run_scrappers.py
python ETL\2_create_big_json.py
python ETL\3_insert_db.py

# Backend
cd Backend 
python manage.py runserver
python manage.py makemigrations jobs
python manage.py migrate

pnpx tailwindcss -i Backend/static/css/styles.css -o Backend/static/css/tailwind.css --watch

django-admin makemessages -l en
django-admin compilemessages

python manage.py test --keepdb