from pathlib import Path 
from pprint import pprint
import subprocess

pprint(f"=== Running: 1_run_scrappers.py ===")

# Files
p = Path("./ETL/jobs").resolve()
jobs = list(p.iterdir())

# Run each Job Scrapper
for f in jobs:
  if f.is_file():
    if f.stem == "test":
      pprint(f"Job: {f.name}")
      subprocess.run(["python", f])
