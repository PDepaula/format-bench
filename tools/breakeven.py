"""Primer break-even with interpolated crossing points, per tokenizer
(o200k, Qwen3 from breakeven_counts.csv; Claude Haiku 4.5 / Claude 5 from CLI
usage deltas, n <= 100). Writes results/analysis/breakeven_interp.csv.

cost(format, n) = primer(format) + data(format, n); crossing = smallest real n
(linear interpolation between grid points) where LONG-primer EDN-table is not
more expensive than the comparator."""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
series = defaultdict(lambda: defaultdict(dict))  # (family, tokenizer) -> n -> fmt -> tokens
for r in csv.DictReader(open(ROOT / "results/tokens/breakeven_counts.csv")):
    for tk in ("o200k", "qwen3"):
        series[(r["family"], tk)][int(r["n"])][r["format"]] = int(r[tk])
raw = [json.loads(l) for l in open(ROOT / "results/tokens/claude_raw.jsonl")]
base = {r["model"]: r["input_total"] for r in raw if r["ok"] and r["group"] == "baseline"}
cname = {"haiku": "claude-haiku-4.5", "opus": "claude-5"}
primers = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "results/tokens/primers.csv")):
    primers["o200k"][r["format"]] = int(r["o200k"])
    primers["qwen3"][r["format"]] = int(r["qwen3"])
for r in raw:
    if not r["ok"] or r["model"] not in cname:
        continue
    tk = cname[r["model"]]
    if r["group"] == "primer":
        primers[tk][r["format"]] = r["input_total"] - base[r["model"]]
    elif r["group"].startswith("breakeven:"):
        series[(r["group"].split(":", 1)[1], tk)][int(r["dataset"])][r["format"]] = r["input_total"] - base[r["model"]]


def crossing(ns, f):
    """f(n) = cost(edn-table+P) - cost(comparator); first n where f <= 0, interpolated."""
    prev = None
    for n in ns:
        v = f(n)
        if v <= 0:
            if prev is None:
                return float(n)
            (n0, v0) = prev
            return round(n0 + (n - n0) * v0 / (v0 - v), 1)
        prev = (n, v)
    return "never (<= %d)" % ns[-1]


rows = []
for (fam, tk), s in sorted(series.items()):
    ns = sorted(n for n in s if {"json-compact", "toon", "edn-table"} <= set(s[n]))
    if not ns:
        continue
    P = primers[tk]
    L = P["edn-table-primer"]
    rows.append({
        "family": fam, "tokenizer": tk, "long_primer_tokens": L, "max_n": ns[-1],
        "vs_json_no_primer": crossing(ns, lambda n: L + s[n]["edn-table"] - s[n]["json-compact"]),
        "vs_json_with_primer": crossing(ns, lambda n: L + s[n]["edn-table"] - P["json-compact"] - s[n]["json-compact"]),
        "vs_toon_with_primer": crossing(ns, lambda n: L + s[n]["edn-table"] - P["toon"] - s[n]["toon"]),
        "vs_toon_no_primer": crossing(ns, lambda n: L + s[n]["edn-table"] - s[n]["toon"]),
        "edn_table_minus_toon_per_record_at_max": round((s[ns[-1]]["edn-table"] - s[ns[-1]]["toon"]) / ns[-1], 2),
        "json_minus_edn_table_per_record_at_max": round((s[ns[-1]]["json-compact"] - s[ns[-1]]["edn-table"]) / ns[-1], 2),
    })
with open(ROOT / "results/analysis/breakeven_interp.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
md = ["| family | tokenizer | LONG primer | vs JSON-c (no primer) | vs JSON-c (+primer) | vs TOON (+primer) | vs TOON (no primer) | JSON − EDN-table per record | EDN-table − TOON per record |", "|---" * 9 + "|"]
for r in rows:
    md.append(f"| {r['family']} | {r['tokenizer']} | {r['long_primer_tokens']} | {r['vs_json_no_primer']} | {r['vs_json_with_primer']} | {r['vs_toon_with_primer']} | {r['vs_toon_no_primer']} | {r['json_minus_edn_table_per_record_at_max']:+} | {r['edn_table_minus_toon_per_record_at_max']:+} |")
(ROOT / "results/analysis/breakeven_interp.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
