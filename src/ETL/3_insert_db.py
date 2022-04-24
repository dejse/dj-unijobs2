import sqlite3
import json
from datetime import datetime
from pathlib import Path 
from pprint import pprint

pprint(f"=== Running: 3_insert_db.py ===")

# Files
sqlite_path = Path("./src/Backend/db.sqlite3")
data_file = Path("./src/ETL/data/_data.json")

# Load JSON
with data_file.open(mode="r+b") as f:
  data = json.load(f)

# DB Stuff
con = sqlite3.connect(sqlite_path)
c = con.cursor()

# Rebuild uni
c.executescript(
  """
  delete from jobs_uni;
  begin transaction;
  insert into jobs_uni values 
    (null, 'tuw', 'Technische Universität Wien', 'Vienna University of Technology', "Wien", "Vienna"),
    (null, 'uw', 'Universität Wien', 'University of Vienna', "Wien", "Vienna"),
    (null, 'wu', 'Wirtschaftsuniversität Wien', 'Vienna University of Economics and Business', "Wien", "Vienna");
  commit;
  """
)
pprint(f"# Sqlite: Rebuild jobs_uni table")

# Count jobs
count = c.execute("select count(*) from jobs_job;").fetchone()[0]
pprint(f"# Sqlite: Rows in jobs table: {count}")

# Insert Jobs Data
today = datetime.today().strftime("%Y-%m-%d")
for e in data:
  e["created"] = today
  e["updated"] = today

c.execute("delete from jobs_job;")
pprint(f"# Sqlite: Deleted Entries from jobs table")

c.executemany("""
insert into jobs_job(title, href, institute, deadline, lang, uni_id, created_at, updated_at) 
values (:title, :href, :institute, :iso, :language, :uni, :created, :updated);
""", data)
pprint(f"# Sqlite: Inserted Entries in jobs table")

# Count jobs
count = c.execute("select count(*) from jobs_job;").fetchone()[0]
pprint(f"# Sqlite: Rows in jobs table: {count}")

# Save, Close
con.commit()
con.close()