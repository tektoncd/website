# A script for local development
# Before you begin
# 1. Set up a Python (3.7+) virtualenv at env/ 
# 2. Set up Firebase CLI (Project ID and credentials)
source env/bin/activate
pip install -r helper/requirements.txt
python helper/helper.py
hugo
firebase deploy
