"""Runs a task manifest through headless Claude Code subagents.

Usage: python3 tools/run_accuracy.py <haiku|sonnet|opus> [workers] [accuracy|generation]
Appends one JSON line per task to results/raw/accuracy/<model>.jsonl (resumable:
tasks with an ok result are skipped)."""
import json
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import claude_cli  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
model = sys.argv[1]
workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
kind = sys.argv[3] if len(sys.argv) > 3 else "accuracy"
out_path = ROOT / "results" / "raw" / kind / f"{model}.jsonl"
out_path.parent.mkdir(parents=True, exist_ok=True)

tasks = [json.loads(l) for l in (ROOT / "results" / kind / "tasks.jsonl").open()]
done = set()
if out_path.exists():
    for line in out_path.read_text().splitlines():
        r = json.loads(line)
        if r.get("ok"):
            done.add(r["task_id"])
todo = [t for t in tasks if t["task_id"] not in done]
random.Random(f"order-{model}").shuffle(todo)  # execution order only; prompts are fixed
print(f"{model}: {len(todo)} of {len(tasks)} tasks to run", flush=True)

lock = threading.Lock()


def run(t):
    r = claude_cli.call(model, t["prompt"])
    rec = {k: v for k, v in t.items() if k != "prompt"}
    rec.update(model=model, **r)
    return rec


n = 0
cost = 0.0
with ThreadPoolExecutor(max_workers=workers) as ex, out_path.open("a") as f:
    futures = [ex.submit(run, t) for t in todo]
    for fut in as_completed(futures):
        rec = fut.result()
        with lock:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
        n += 1
        cost += rec.get("cost_usd", 0) or 0
        if not rec.get("ok"):
            print("FAILED", rec["task_id"], rec.get("error"), flush=True)
        if n % 25 == 0:
            print(f"{model}: {n}/{len(todo)} cost=${cost:.2f}", flush=True)
print(f"{model}: finished {n} cost=${cost:.2f}", flush=True)
