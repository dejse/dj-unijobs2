from pathlib import Path 
from pprint import pprint
import subprocess

p = Path("./ETL/jobs").resolve()
jobs = list(p.iterdir())

pprint(f"=== Running: 1_run_scrappers.py ===")

for f in jobs:
  if f.is_file():
    if f.stem == "test":
      pprint(f"Job: {f.name}")
      subprocess.run(["python", f])
