import sqlite3
import json
import datetime
import aiosql
from pathlib import Path 
from pprint import pprint

pprint(f"=== Running: 3_insert_db.py ===")

# Files
file = Path("./src/ETL/data/_data.json")
sqlite_path = Path("./src/db.sqlite")

# Load JSON
with file.open(mode="r+b") as f:
  data = json.load(f)

# DB Stuff
con = sqlite3.connect(sqlite_path)
c = con.cursor()

count = c.execute("select count(*) from jobs_job").fetchone()[0]
pprint(f"# Sqlite: Rows in jobs_job: {count}")


# Insert Unis Data
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
#pprint(c.execute("select * from jobs_uni").fetchall())

# Insert Jobs Data
today = datetime.datetime.today().strftime("%Y-%m-%d")
for e in data:
  e["created_at"] = today
  e["updated_at"] = today

c.execute("delete from jobs_job")
pprint(f"# Sqlite: Deleted Entries from jobs_job table")

c.executemany(
  """
  insert into jobs_job(title, href, institute, deadline, lang, uni_id, created_at, updated_at) 
  values (:jobTitle, :href, :institute, :iso, :language, :uni, :created_at, :updated_at);
  """, data)
pprint(f"# Sqlite: Inserted data into jobs_job")

count = c.execute("select count(*) from jobs_job").fetchone()[0]
pprint(f"# Sqlite: Rows in jobs_job: {count}")

# pprint(c.execute("select * from jobs_job").fetchall()[0])

# Save, Close
con.commit()
con.close()