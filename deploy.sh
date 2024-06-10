#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start the Gunicorn server
exec sh startup.sh
# update 202406101353