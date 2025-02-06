#!/bin/bash
cd /home/celian/API
source venv/bin/activate
gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app
