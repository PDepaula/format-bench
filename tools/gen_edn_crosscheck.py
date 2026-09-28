"""Cross-checks EDN parse validity of generated blocks with the Python edn_format
parser (PLAN.md §5 names both edn-data and edn_format). Adds column
parse_valid_edn_format to results/generation/graded.csv (TOON rows: blank)."""
import csv
import json
from pathlib import Path

import edn_format

ROOT = Path(__file__).resolve().parent.parent
blocks = json.loads((ROOT / "results/generation/extracted_blocks.json").read_text())
path = ROOT / "results/generation/graded.csv"
rows = list(csv.DictReader(path.open()))
for r in rows:
    if r["format"].startswith("toon"):
        r["parse_valid_edn_format"] = ""
        continue
    try:
        edn_format.loads(blocks[f"{r['model']}/{r['task_id']}"])
        r["parse_valid_edn_format"] = "1"
    except Exception:  # noqa: BLE001
        r["parse_valid_edn_format"] = "0"
with path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
dis = [(r["model"], r["task_id"], r["parse_valid"], r["parse_valid_edn_format"]) for r in rows if not r["format"].startswith("toon") and r["parse_valid"] != r["parse_valid_edn_format"]]
print("edn-data vs edn_format disagreements:", dis)
