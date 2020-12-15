#!/bin/bash

rm -rf queuedapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations queuedapi
python manage.py migrate queuedapi
python manage.py loaddata users.json
python manage.py loaddata tokens.json
python manage.py loaddata queueusers.json
python manage.py loaddata trips.json
python manage.py loaddata itineraries.json
python manage.py loaddata rideitineraries.json
python manage.py loaddata ridereviews.json
python manage.py loaddata ridefavorites.json