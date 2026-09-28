"""Fairness assertions on results/accuracy/tasks.jsonl (PLAN.md §7):
same questions/batches/order for every format within a seed, every question
answered once per seed per applicable format, and prompts identical apart from
the primer line, format label, fence and data block."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tasks = [json.loads(l) for l in (ROOT / "results/accuracy/tasks.jsonl").open()]
enc = json.loads((ROOT / "build/encodings.json").read_text())
questions = {q["id"]: q for q in json.loads((ROOT / "results/accuracy/questions.json").read_text())}

by_batch = defaultdict(dict)
for t in tasks:
    by_batch[t["batch_id"]][t["format"]] = t

for bid, fmts in by_batch.items():
    qsets = {tuple(t["question_ids"]) for t in fmts.values()}
    assert len(qsets) == 1, bid
    skeletons = set()
    for fmt, t in fmts.items():
        data_fmt = "edn-table" if fmt == "edn-table-primer" else fmt
        data = enc["accuracy"][t["dataset"]][data_fmt]
        p = t["prompt"]
        assert p.count(data) == 1, (bid, fmt)
        p = p.replace(data, "<DATA>")
        primer = enc["primers"][fmt]
        assert p.startswith(primer + "\n\n"), (bid, fmt)
        p = p[len(primer):]
        label = "edn-table" if fmt == "edn-table-primer" else fmt
        fence = {"json-compact": "json", "toon": "toon", "csv": "csv"}.get(fmt, "edn")
        p = p.replace(f"data in {label} format", "data in <LABEL> format", 1).replace(f"```{fence}\n<DATA>", "```<FENCE>\n<DATA>", 1)
        skeletons.add(p)
    assert len(skeletons) == 1, (bid, skeletons)

for seed in (1, 2, 3):
    for fmt in ("json-compact", "toon", "edn-maps", "edn-table", "edn-table-primer", "csv"):
        ids = [q for t in tasks if t["seed"] == seed and t["format"] == fmt for q in t["question_ids"]]
        expected = [q for q in questions if fmt != "csv" or questions[q]["track"] == "flat"]
        assert sorted(ids) == sorted(expected), (seed, fmt)
        assert len(ids) == len(set(ids))
    orders = [[q for t in tasks if t["seed"] == seed and t["format"] == "toon" for q in t["question_ids"]] for seed in (1, 2, 3)]
assert orders[0] != orders[1] != orders[2]
print(f"manifest OK: {len(tasks)} tasks, {len(by_batch)} batches")
