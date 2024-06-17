#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start the Gunicorn server
exec sh startup.sh