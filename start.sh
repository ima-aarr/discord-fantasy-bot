#!/bin/bash
set -e

# make sure data dir exists
mkdir -p data

# Upgrade pip then install requirements (Koyeb will cache)
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Start bot
python bot.py
