#!/bin/bash

# Activate Python virtual environment
source venv/bin/activate

# Run server.py
gunicorn -w 4 -b 0.0.0.0 'server:spawn_app()'
