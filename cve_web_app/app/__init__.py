from flask import Flask
from tinydb import TinyDB, Query
import os

app = Flask(__name__)

# Ensure correct path for cves_db.json
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cves_db.json')
print(f"Database path: {db_path}")
db = TinyDB(db_path)

from app import routes
