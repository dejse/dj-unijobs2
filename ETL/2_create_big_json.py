from pathlib import Path 
from pprint import pprint
import json

pprint(f"=== Running: 2_create_big_json.py ===")

p = Path("./ETL/data").resolve()
file = p / "_data.json"
data = list()

if file.exists():
  pprint(f"Delete: {file.name}")
  file.unlink()

for f in p.iterdir():
  if f.is_file:
    pprint(f"Processing: {f.name}")
    name, language = f.stem.split("-") 
    
    with f.open(mode="r+b") as j:
      JSON = json.loads(j.read())
      
      for d in JSON:
        d["uni"] = name 
        d["language"] = language
      
      data.extend(JSON)

with file.open(mode="w+b") as f:
  data = json.dumps(data, ensure_ascii=False).encode("utf8")
  f.write(data)
  pprint(f"Created: {file.name}")



