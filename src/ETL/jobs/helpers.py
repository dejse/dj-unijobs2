import json 
from pathlib import Path

def save_file(data, filename = ""):
  data_path = Path("./src/ETL/data").resolve()
  file = data_path / filename 
  JSON = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
  with file.open(mode="w+b") as f: 
    f.write(JSON)