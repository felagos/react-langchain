#!/bin/bash

export PIPENV_VENV_IN_PROJECT=1

# Check if the Pipfile exists
if [ -f "Pipfile" ]; then
  # If it exists, install the packages and create a virtual environment
  pipenv install
else
  # If it doesn't exist, create a new virtual environment
  pipenv shell
fi