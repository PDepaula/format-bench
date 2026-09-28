"""External check (PLAN.md §4): our batched Haiku accuracy vs upstream's
published single-question Haiku 4.5 results for the formats both ran.
Writes results/analysis/external_check.csv."""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
up = json.load(open(ROOT / "vendor/toon/benchmarks/results/accuracy/models/claude-haiku-4-5-20251001"))
ours = defaultdict(list)
for r in csv.DictReader(open(ROOT / "results/accuracy/graded.csv")):
    if r["model"] == "haiku":
        ours[(r["format"], r["question_id"])].append(int(r["correct"]))
out = []
for fmt in ("json-compact", "toon", "csv"):
    u = {r["questionId"]: int(r["isCorrect"]) for r in up if r["format"] == fmt}
    qids = [q for q in u if (fmt, q) in ours]
    up_acc = sum(u[q] for q in qids) / len(qids)
    our_acc = sum(sum(ours[(fmt, q)]) / len(ours[(fmt, q)]) for q in qids) / len(qids)
    agree = sum((sum(ours[(fmt, q)]) / len(ours[(fmt, q)]) > 0.5) == bool(u[q]) for q in qids) / len(qids)
    out.append({"format": fmt, "n_questions": len(qids), "upstream_single_question": round(up_acc, 4),
                "ours_batched_mean3seeds": round(our_acc, 4), "per_question_agreement_majority": round(agree, 4)})
with open(ROOT / "results/analysis/external_check.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
for r in out:
    print(r)
