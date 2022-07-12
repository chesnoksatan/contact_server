#!/bin/sh

cd /home/pi/contact_manager_server/
export FLASK_APP=main
flask run --host=0.0.0.0
