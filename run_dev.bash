#!/bin/bash

source venv/bin/activate
export FLASK_APP=main.py
export FLASK_DEBUG=1
flask run --port=8000
