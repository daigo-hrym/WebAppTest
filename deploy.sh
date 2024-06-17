#!/bin/bash

# Install dependencies
pip install -r requirements.txt 2>&1 | tee /home/LogFiles/pip_install.log

# Start the Gunicorn server
exec sh startup.sh