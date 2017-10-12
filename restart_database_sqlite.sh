#!/bin/sh
rm db.sqlite3
rm -rf core/migrations
./manage.py makemigrations core
./manage.py migrate