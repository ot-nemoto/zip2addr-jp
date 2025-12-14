#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y sqlite3

python -m pip install --upgrade pip
pip install -e .[test]
