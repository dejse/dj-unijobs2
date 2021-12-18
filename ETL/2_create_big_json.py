from pathlib import Path 
from pprint import pprint
from datetime import datetime
import json

pprint(f"=== Running: 2_create_big_json.py ===")

# Files
p = Path("./ETL/data").resolve()
file = p / "_data.json"
data = list()

if file.exists():
  pprint(f"Delete: {file.name}")
  file.unlink()

# Run through each [uni].json
# Create Big JSON File
for f in p.iterdir():
  if f.is_file:
    pprint(f"Processing: {f.name}")
    name, language = f.stem.split("-") 
    
    with f.open(mode="r+b") as j:
      JSON = json.loads(j.read())
      
      for d in JSON:
        d["uni"] = name 
        d["language"] = language
        d["iso"] = datetime.strptime(d["deadline"], "%d.%m.%Y").strftime("%Y-%m-%d")

      data.extend(JSON)

# Write JSON File
with file.open(mode="w+b") as f:
  data = json.dumps(data, ensure_ascii=False, indent=4).encode("utf8")
  f.write(data)
  pprint(f"Created: {file.name}")



