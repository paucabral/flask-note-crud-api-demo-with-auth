#!/usr/bin/env bash
# exit on error
set -o errexit

pip3 install -r requirements.txt

flask db init
flask db migrate
flask db upgrade