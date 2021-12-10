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
c = sqlite3.connect(sqlite_path).cursor()

count = c.execute("select count(*) from jobs_job").fetchone()[0]
pprint(f"# Sqlite: Rows in jobs_job: {count}")

c.execute("delete from jobs_job;")
pprint(f"# Sqlite: Deleted Entries from jobs_job table")


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


# # Insert Jobs Data
# c.executemany(
#     """
#     insert into unijobs_job(id, title, href, institute, deadline, language, uuid, uni_id) 
#     values (null, :jobTitle, :href, :institute, :iso_deadline, :lang, :uuid, :uni);
#     """, data)
# print(f"# Sqlite: Inserted into jobs")