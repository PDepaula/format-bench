"""Draws the pre-registered grader-audit sample (PLAN.md §7): 30 uniformly
random graded answers per format (seed 777, across models and seeds), plus
context for hand-checking. Writes results/audit/audit_sample.csv.

The hand verdicts live in results/audit/audit_verdicts.csv (written by hand
after reading every sampled row)."""
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "results/accuracy/graded.csv")))
questions = {q["id"]: q for q in json.loads((ROOT / "results/accuracy/questions.json").read_text())}
rng = random.Random(777)
out = []
for fmt in ["json-compact", "toon", "edn-maps", "edn-table", "edn-table-primer", "csv"]:
    pool = [r for r in rows if r["format"] == fmt]
    for r in rng.sample(pool, 30):
        out.append({
            "audit_id": f"{fmt}-{len(out)}",
            "format": fmt, "model": r["model"], "seed": r["seed"], "question_id": r["question_id"],
            "answer_type": r["answer_type"], "question": questions[r["question_id"]]["prompt"],
            "expected": r["expected"], "answer": r["answer"], "graded_correct": r["correct"],
            "error_class": r["error_class"],
        })
(ROOT / "results/audit").mkdir(parents=True, exist_ok=True)
with open(ROOT / "results/audit/audit_sample.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
print(len(out))
