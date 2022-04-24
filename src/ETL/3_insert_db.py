import sqlite3
import json
import datetime
import aiosql
from pathlib import Path 
from pprint import pprint

pprint(f"=== Running: 3_insert_db.py ===")

# Files
insert_sql = Path("./src/db/insert.sql")
sqlite_path = Path("./src/db/db.sqlite")
data_file = Path("./src/ETL/data/_data.json")

# Load JSON
with data_file.open(mode="r+b") as f:
  data = json.load(f)

# DB Stuff
con = sqlite3.connect(sqlite_path)
queries = aiosql.from_path(insert_sql, "sqlite3")

# Count jobs
count = queries.count_jobs(con)
pprint(f"# Sqlite: Rows in jobs table: {count}")

# Insert Jobs Data
today = datetime.datetime.today().strftime("%Y-%m-%d")
for e in data:
  e["created"] = today
  e["updated"] = today

queries.delete_jobs(con)
pprint(f"# Sqlite: Deleted Entries from jobs table")

queries.bulk_insert_jobs(con, data)
pprint(f"# Sqlite: Inserted Entries in jobs table")

# Count jobs
count = queries.count_jobs(con)
pprint(f"# Sqlite: Rows in jobs table: {count}")

# Save, Close
con.commit()
con.close()