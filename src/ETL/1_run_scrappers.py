from pathlib import Path 
from pprint import pprint
import subprocess

pprint(f"=== Running: 1_run_scrappers.py ===")

# Files
p = Path("./src/ETL/jobs").resolve()
jobs = list(p.iterdir())


# Run each Job Scrapper
for f in jobs:
  if f.is_file():
    if f.stem != "helpers":
      pprint(f"Job: {f.name}")
      cmd = f"env\\Scripts\\activate && python {f}"
      subprocess.call(cmd, shell=True)
      #subprocess.run(["python", f])
