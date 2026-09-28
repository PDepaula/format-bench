"""Token tables (per tokenizer, per track, per dataset) and primer break-even.

Writes results/analysis/tokens_*.csv and results/analysis/tokens.md (tables
pasted into REPORT.md)."""
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "analysis"
OUT.mkdir(parents=True, exist_ok=True)
FORMATS = ["json-compact", "toon", "edn-maps", "edn-table", "csv", "json-pretty", "yaml", "xml"]
CONTENDERS = ["json-compact", "toon", "edn-maps", "edn-table", "csv"]

rows = list(csv.DictReader(open(ROOT / "results/tokens/token_counts.csv")))
primers = {r["format"]: r for r in csv.DictReader(open(ROOT / "results/tokens/primers.csv"))}

# Claude counts from CLI usage deltas
craw = [json.loads(l) for l in open(ROOT / "results/tokens/claude_raw.jsonl")]
claude = defaultdict(dict)  # (model) -> {(group, dataset, format): tokens}
base = {}
for r in craw:
    if r["ok"] and r["group"] == "baseline":
        base.setdefault(r["model"], set()).add(r["input_total"])
for m, b in base.items():
    assert len(b) == 1, f"baseline not constant for {m}: {b}"
base = {m: next(iter(b)) for m, b in base.items()}
for r in craw:
    if r["ok"] and r["group"] != "baseline":
        # PREFIX + "\n" + text  minus  PREFIX  (the "\n" is inside the delta; ±1 token)
        claude[r["model"]][(r["group"], r["dataset"], r["format"])] = r["input_total"] - base[r["model"]]

TOKENIZERS = ["o200k", "qwen3", "claude-haiku-4.5", "claude-sonnet-5", "claude-opus-5.5"]
CMAP = {"claude-haiku-4.5": "haiku", "claude-sonnet-5": "sonnet", "claude-opus-5.5": "opus"}


def count(tk, group, ds, fmt):
    if tk in ("o200k", "qwen3"):
        for r in rows:
            if r["group"] == group and r["dataset"] == ds and r["format"] == fmt:
                return int(r[tk])
        return None
    return claude[CMAP[tk]].get((group, ds, fmt))


def primer_count(tk, fmt):
    if tk in ("o200k", "qwen3"):
        return int(primers[fmt][tk])
    return claude[CMAP[tk]].get(("primer", "-", fmt))


datasets = defaultdict(dict)
for r in rows:
    datasets[r["group"]][r["dataset"]] = r["track"]

md = []
long_rows = []
for group in ("tokens", "accuracy"):
    for tk in TOKENIZERS:
        fmts = FORMATS if tk in ("o200k", "qwen3") else CONTENDERS
        have = [ds for ds in datasets[group] if count(tk, group, ds, "json-compact") is not None]
        if not have:
            continue
        md.append(f"\n#### {group} datasets — {tk}\n")
        md.append("| dataset | track | " + " | ".join(fmts) + " | EDN-maps vs JSON-c | EDN-table vs TOON |")
        md.append("|---" * (len(fmts) + 4) + "|")
        totals = defaultdict(lambda: defaultdict(int))
        for ds in sorted(have, key=lambda d: (datasets[group][d], d)):
            tr = datasets[group][ds]
            vals = {f: count(tk, group, ds, f) for f in fmts}
            for f, v in vals.items():
                if v is not None:
                    totals[tr][f] += v
                    long_rows.append({"group": group, "tokenizer": tk, "dataset": ds, "track": tr, "format": f, "tokens": v})
            em = (vals["edn-maps"] / vals["json-compact"] - 1) * 100
            et = (vals["edn-table"] / vals["toon"] - 1) * 100
            md.append(f"| {ds} | {tr} | " + " | ".join(f"{vals[f]:,}" if vals[f] is not None else "–" for f in fmts) + f" | {em:+.1f}% | {et:+.1f}% |")
        for tr in ("flat", "mixed"):
            t = totals[tr]
            em = (t["edn-maps"] / t["json-compact"] - 1) * 100
            et = (t["edn-table"] / t["toon"] - 1) * 100
            md.append(f"| **total {tr}** | {tr} | " + " | ".join(f"**{t[f]:,}**" if f in t else "–" for f in fmts) + f" | **{em:+.1f}%** | **{et:+.1f}%** |")

with open(OUT / "tokens_long.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(long_rows[0]))
    w.writeheader()
    w.writerows(long_rows)

# primers
md.append("\n#### Primer lines (tokens, prepended to every call)\n")
md.append("| format | " + " | ".join(TOKENIZERS) + " |")
md.append("|---" * (len(TOKENIZERS) + 1) + "|")
for fmt in ["json-compact", "toon", "csv", "edn-maps", "edn-table", "edn-table-primer"]:
    md.append(f"| {fmt} | " + " | ".join(str(primer_count(tk, fmt)) for tk in TOKENIZERS) + " |")

# break-even (o200k, qwen3 only: prefix series were not sent to Claude)
be = defaultdict(lambda: defaultdict(dict))
for r in csv.DictReader(open(ROOT / "results/tokens/breakeven_counts.csv")):
    for tk in ("o200k", "qwen3"):
        be[(r["family"], tk)][int(r["n"])][r["format"]] = int(r[tk])
md.append("\n#### Primer break-even (payload size in records)\n")
md.append("Cost of a call = primer line + data block. `edn-table+P` = LONG primer + EDN-table data. Break-even = smallest n in the grid where edn-table+P ≤ the comparator (\"never\" if not reached by the largest n).\n")
md.append("| family | tokenizer | vs JSON-c (no primer) | vs JSON-c (+its primer) | vs TOON (+its primer) | vs TOON (no primer) | vs EDN-table (short primer) | per-record saving vs JSON-c | per-record Δ vs TOON |")
md.append("|---" * 9 + "|")
be_rows = []
for (fam, tk), series in sorted(be.items()):
    P = int(primers["edn-table-primer"][tk])
    pj, pt, ps = int(primers["json-compact"][tk]), int(primers["toon"][tk]), int(primers["edn-table"][tk])
    ns = sorted(series)

    def first(pred):
        for n in ns:
            if pred(series[n]):
                return n
        return "never"
    cmp = {
        "json_noprimer": first(lambda s: P + s["edn-table"] <= s["json-compact"]),
        "json_primer": first(lambda s: P + s["edn-table"] <= pj + s["json-compact"]),
        "toon_primer": first(lambda s: P + s["edn-table"] <= pt + s["toon"]),
        "toon_noprimer": first(lambda s: P + s["edn-table"] <= s["toon"]),
        "edn_short": first(lambda s: P + s["edn-table"] <= ps + s["edn-table"]),
    }
    nmax = ns[-1]
    per_json = (series[nmax]["json-compact"] - series[nmax]["edn-table"]) / nmax
    per_toon = (series[nmax]["edn-table"] - series[nmax]["toon"]) / nmax
    md.append(f"| {fam} | {tk} | {cmp['json_noprimer']} | {cmp['json_primer']} | {cmp['toon_primer']} | {cmp['toon_noprimer']} | {cmp['edn_short']} | {per_json:+.1f} tok | {per_toon:+.1f} tok |")
    be_rows.append({"family": fam, "tokenizer": tk, "primer_tokens": P, **cmp, "per_record_saving_vs_json": round(per_json, 2), "per_record_extra_vs_toon": round(per_toon, 2)})
    for n in ns:
        s = series[n]
        be_rows[-1][f"n{n}"] = f"{s['json-compact']}/{s['toon']}/{s['edn-table']}"
with open(OUT / "breakeven.csv", "w", newline="") as f:
    keys = list(dict.fromkeys(k for r in be_rows for k in r))
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    w.writerows(be_rows)

(OUT / "tokens.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
