#!/bin/bash

# NOTE: This script is not run by default for the template Docker image.
# If you use a custom base image you can add your required system dependencies here.

set -e # Stop script on error
apt-get update && apt-get upgrade -y # Update System

# Install Python 3.11 and pip
apt-get install -y python3.11 python3-venv

# Clean up, remove unnecessary packages and help reduce image size
apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Update pip
pip install --upgrade pip
