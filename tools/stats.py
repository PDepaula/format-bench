"""Accuracy statistics for the EDN study (PLAN.md §6).

Reads results/accuracy/graded.csv and writes:
  results/analysis/accuracy_summary.csv   model × format × subset, cluster-bootstrap CI
  results/analysis/paired.csv             pre-registered paired comparisons
  results/analysis/failures.csv           failure classes per model × format
Grade column: `correct` (primary, upstream checker) or `correct_lenient` via --lenient.
"""
import argparse
import csv
import itertools
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "analysis"
MODELS = ["haiku", "sonnet", "opus"]
FORMATS = ["json-compact", "toon", "edn-maps", "edn-table", "edn-table-primer", "csv"]
PRIMARY = [
    ("edn-maps", "json-compact"),
    ("edn-table", "toon"),
    ("edn-table-primer", "edn-table"),
    ("edn-table-primer", "toon"),
    ("edn-table-primer", "json-compact"),
    ("edn-maps", "toon"),
]
EXTRA = [("toon", "json-compact"), ("edn-table", "json-compact"), ("edn-table", "edn-maps"), ("csv", "toon"), ("csv", "edn-table"), ("csv", "json-compact")]
MARGIN = 0.05
B = 10_000


def subsets(q):
    out = ["overall", f"track:{q['track']}", f"shape:{q['shape']}"]
    if q["shape"] != "structural-validation":
        out.append("overall-excl-structural")
    out.append(f"type:{q['type']}")
    return out


def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adj = [0.0] * len(pvals)
    running = 0.0
    m = len(pvals)
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
    return adj


def verdict(lo, hi):
    if lo > 0:
        return "A better"
    if hi < 0:
        return "B better"
    if lo >= -MARGIN and hi <= MARGIN:
        return "equivalent (±5pp)"
    return "no detectable difference"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lenient", action="store_true")
    ap.add_argument("--graded", default=str(ROOT / "results/accuracy/graded.csv"))
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()
    col = "correct_lenient" if args.lenient else "correct"
    suffix = args.suffix or ("_lenient" if args.lenient else "")
    OUT.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(open(args.graded)))
    qmeta = {}
    # score[(model, format)][qid] -> list of 0/1 over seeds
    score = defaultdict(lambda: defaultdict(list))
    fails = defaultdict(lambda: defaultdict(int))
    for r in rows:
        qmeta[r["question_id"]] = r
        score[(r["model"], r["format"])][r["question_id"]].append(int(r[col]))
        fails[(r["model"], r["format"])][r["error_class"] or "correct"] += 1
    models = [m for m in MODELS if any(k[0] == m for k in score)]
    rng = np.random.default_rng(12345)

    def qscore(model, fmt, qids):
        """per-question mean over seeds (and models if model == 'pooled')"""
        ms = models if model == "pooled" else [model]
        out = []
        for q in qids:
            vals = [v for m in ms for v in score[(m, fmt)].get(q, [])]
            out.append(np.mean(vals) if vals else np.nan)
        return np.array(out)

    def majority(model, fmt, qids):
        ms = models if model == "pooled" else [model]
        out = []
        for q in qids:
            vals = [v for m in ms for v in score[(m, fmt)].get(q, [])]
            out.append(1 if vals and np.mean(vals) > 0.5 else 0)
        return np.array(out)

    subset_q = defaultdict(list)
    for q, meta in qmeta.items():
        for s in subsets(meta):
            subset_q[s].append(q)
    subset_q = {k: sorted(v) for k, v in subset_q.items()}

    # --- accuracy summary
    with open(OUT / f"accuracy_summary{suffix}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "format", "subset", "n_questions", "n_answers", "accuracy", "ci_lo", "ci_hi", "seed1", "seed2", "seed3"])
        for model in models + ["pooled"]:
            for fmt in FORMATS:
                for sname, qids in subset_q.items():
                    qids = [q for q in qids if score[(models[0], fmt)].get(q)] if fmt == "csv" else qids
                    if not qids:
                        continue
                    s = qscore(model, fmt, qids)
                    if np.isnan(s).any():
                        continue
                    idx = rng.integers(0, len(s), size=(B, len(s)))
                    boots = s[idx].mean(axis=1)
                    ms = models if model == "pooled" else [model]
                    seeds = []
                    for si in range(3):
                        vals = [score[(m, fmt)][q][si] for m in ms for q in qids if len(score[(m, fmt)][q]) > si]
                        seeds.append(round(float(np.mean(vals)), 4) if vals else "")
                    n_ans = sum(len(score[(m, fmt)][q]) for m in ms for q in qids)
                    w.writerow([model, fmt, sname, len(qids), n_ans, round(float(s.mean()), 4),
                                round(float(np.percentile(boots, 2.5)), 4), round(float(np.percentile(boots, 97.5)), 4), *seeds])

    # --- paired comparisons
    out_rows = []
    for model in models + ["pooled"]:
        for a, b in PRIMARY + EXTRA:
            for sname, qids in subset_q.items():
                if "csv" in (a, b):
                    qids = [q for q in qids if qmeta[q]["track"] == "flat"]
                if not qids:
                    continue
                sa, sb = qscore(model, a, qids), qscore(model, b, qids)
                if np.isnan(sa).any() or np.isnan(sb).any():
                    continue
                d = sa - sb
                idx = rng.integers(0, len(d), size=(B, len(d)))
                boots = d[idx].mean(axis=1)
                lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
                ma, mb = majority(model, a, qids), majority(model, b, qids)
                n01 = int(((ma == 1) & (mb == 0)).sum())
                n10 = int(((ma == 0) & (mb == 1)).sum())
                p = binomtest(n01, n01 + n10, 0.5).pvalue if n01 + n10 else 1.0
                out_rows.append({
                    "model": model, "A": a, "B": b, "family": "primary" if (a, b) in PRIMARY else "extra",
                    "subset": sname, "n_questions": len(qids),
                    "acc_A": round(float(sa.mean()), 4), "acc_B": round(float(sb.mean()), 4),
                    "diff": round(float(d.mean()), 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
                    "mcnemar_A_only": n01, "mcnemar_B_only": n10, "mcnemar_p": round(float(p), 5),
                    "verdict": verdict(lo, hi),
                })
    fam = [r for r in out_rows if r["family"] == "primary" and r["subset"] == "overall"]
    for r, adj in zip(fam, holm([r["mcnemar_p"] for r in fam])):
        r["holm_p_primary_overall"] = round(adj, 5)
    with open(OUT / f"paired{suffix}.csv", "w", newline="") as f:
        fields = list(out_rows[0].keys()) + ["holm_p_primary_overall"]
        w = csv.DictWriter(f, fieldnames=list(dict.fromkeys(fields)))
        w.writeheader()
        w.writerows(out_rows)

    with open(OUT / f"failures{suffix}.csv", "w", newline="") as f:
        classes = ["correct", "comprehension", "format-lenient", "format-missing", "call-failed"]
        w = csv.writer(f)
        w.writerow(["model", "format", *classes])
        for (m, fmt), c in sorted(fails.items()):
            w.writerow([m, fmt, *[c.get(k, 0) for k in classes]])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
