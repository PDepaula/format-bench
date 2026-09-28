"""Claude token counts derived from CLI usage (the token-counting API needs
ANTHROPIC_API_KEY, which is not set, so it was skipped).

tokens(text) = input_total(PREFIX + "\n" + text) - input_total(PREFIX)
Usage: python3 tools/claude_tokens.py <model> <groups: accuracy,tokens>
Appends to results/tokens/claude_raw.jsonl (resumable).
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import claude_cli  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENC = json.loads((ROOT / "build" / "encodings.json").read_text())
RAW = ROOT / "results" / "tokens" / "claude_raw.jsonl"
PREFIX = "Reply with only OK.\nDATA:"
CONTENDERS = ["json-compact", "toon", "csv", "edn-maps", "edn-table"]

model = sys.argv[1]
groups = sys.argv[2].split(",")

done = set()
if RAW.exists():
    for line in RAW.read_text().splitlines():
        r = json.loads(line)
        if r.get("ok"):
            done.add((r["model"], r["group"], r["dataset"], r["format"], r.get("rep", 0)))

jobs = []
for rep in range(3):
    jobs.append(("baseline", "-", "-", rep, PREFIX))
for fmt, text in ENC["primers"].items():
    jobs.append(("primer", "-", fmt, 0, PREFIX + "\n" + text))
for g in groups:
    for ds, fmts in ENC[g].items():
        for fmt in CONTENDERS:
            if fmt in fmts:
                jobs.append((g, ds, fmt, 0, PREFIX + "\n" + fmts[fmt]))
jobs = [j for j in jobs if (model, j[0], j[1], j[2], j[3]) not in done]
print(f"{model}: {len(jobs)} calls")


def run(job):
    g, ds, fmt, rep, prompt = job
    r = claude_cli.call(model, prompt)
    r.update(model=model, group=g, dataset=ds, format=fmt, rep=rep, prompt_chars=len(prompt))
    r.pop("text", None) if r.get("ok") and len(r.get("text", "")) < 20 else None
    return r


with ThreadPoolExecutor(max_workers=6) as ex, RAW.open("a") as f:
    for r in ex.map(run, jobs):
        f.write(json.dumps(r) + "\n")
        f.flush()
        if not r.get("ok"):
            print("FAILED", r)
print("done")
