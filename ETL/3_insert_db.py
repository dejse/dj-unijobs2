import sqlite3
import json
from pathlib import Path 
from pprint import pprint

pprint(f"=== Running: 3_insert_db.py ===")

# Files
p = Path("./ETL/data").resolve()
file = p / "_data.json"
sqlite_path = Path("./Backend/db.sqlite3")

# Load JSON
with file.open(mode="r+b") as f:
  data = json.load(f)

# DB Stuff
