from pathlib import Path 
from pprint import pprint
import subprocess

p = Path("./ETL/jobs").resolve()
jobs = list(p.iterdir())

for f in jobs:
  if f.is_file():
    if f.stem == "test":
      subprocess.run(["python", f])
