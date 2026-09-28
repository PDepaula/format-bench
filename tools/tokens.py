"""Token counts per dataset × format × tokenizer (o200k via tiktoken, Qwen3 via HF tokenizers).

Writes results/tokens/token_counts.csv, primers.csv, breakeven_counts.csv.
Cross-checks tiktoken against the benchmark's gpt-tokenizer counts.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tok import count_o200k, count_qwen3  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENC = json.loads((ROOT / "build" / "encodings.json").read_text())
OUT = ROOT / "results" / "tokens"
OUT.mkdir(parents=True, exist_ok=True)
TOKENIZERS = {"o200k": count_o200k, "qwen3": count_qwen3}

mismatch = 0
rows = []
for group in ("tokens", "accuracy"):
    for ds, fmts in ENC[group].items():
        meta = ENC["meta"][f"{group}/{ds}"]
        track = "flat" if meta["supportsCSV"] else "mixed"
        for fmt, text in fmts.items():
            r = {"group": group, "dataset": ds, "track": track, "format": fmt, "chars": len(text)}
            for tk, fn in TOKENIZERS.items():
                r[tk] = fn(text)
            gt = ENC["gptTokenizer"][group][ds].get(fmt)
            if gt is not None and gt != r["o200k"]:
                mismatch += 1
                print("MISMATCH", group, ds, fmt, gt, r["o200k"])
            rows.append(r)

with open(OUT / "token_counts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

with open(OUT / "primers.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["format", "o200k", "qwen3", "gpt_tokenizer", "text"])
    for fmt, text in ENC["primers"].items():
        w.writerow([fmt, count_o200k(text), count_qwen3(text), ENC["gptTokenizer"]["primers"][fmt], text])

with open(OUT / "breakeven_counts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "n", "format", "o200k", "qwen3"])
    for fam, sizes in ENC["breakeven"].items():
        for n, fmts in sizes.items():
            for fmt, text in fmts.items():
                w.writerow([fam, n, fmt, count_o200k(text), count_qwen3(text)])

print(f"rows={len(rows)} tiktoken-vs-gpt-tokenizer mismatches={mismatch}")
