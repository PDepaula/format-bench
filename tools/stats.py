"""Accuracy statistics for the EDN study (PLAN.md §6, plus post-review additions).

Reads results/accuracy/graded.csv and writes (suffix per variant):
  results/analysis/accuracy_summary*.csv   model level × format × subset, cluster-bootstrap CI
  results/analysis/paired*.csv             paired comparisons
  results/analysis/failures*.csv           failure classes per model × format

Model levels: haiku, sonnet, opus, pooled (all three), pooled-nr (Haiku + Sonnet,
the two models that ran without reasoning; added after the adversarial review).

CIs: (1) pre-registered percentile bootstrap over questions; (2) post-review
two-stage bootstrap over datasets then questions within dataset ("ds_ci").
Subset "informative": questions whose correctness varies across the five main
formats × seeds for that model level (post-review, descriptive).
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "analysis"
MODELS = ["haiku", "sonnet", "opus"]
LEVELS = {"haiku": ["haiku"], "sonnet": ["sonnet"], "opus": ["opus"], "pooled": MODELS, "pooled-nr": ["haiku", "sonnet"]}
MAIN = ["json-compact", "toon", "edn-maps", "edn-table", "edn-table-primer"]
FORMATS = MAIN + ["csv", "edn-table-lines"]
PRIMARY = [
    ("edn-maps", "json-compact"),
    ("edn-table", "toon"),
    ("edn-table-primer", "edn-table"),
    ("edn-table-primer", "toon"),
    ("edn-table-primer", "json-compact"),
    ("edn-maps", "toon"),
]
EXTRA = [("toon", "json-compact"), ("edn-table", "json-compact"), ("edn-table", "edn-maps"),
         ("csv", "toon"), ("csv", "edn-table"), ("csv", "json-compact")]
LAYOUT = [("edn-table-lines", "edn-table"), ("edn-table-lines", "toon"), ("edn-table-lines", "json-compact")]
MARGIN = 0.05
B = 10_000


def subsets(q):
    out = ["overall", f"track:{q['track']}", f"shape:{q['shape']}", f"type:{q['type']}"]
    if q["shape"] != "structural-validation":
        out.append("overall-excl-structural")
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
    inside = lo >= -MARGIN and hi <= MARGIN
    if lo > 0:
        return "A better (within ±5pp)" if inside else "A better"
    if hi < 0:
        return "B better (within ±5pp)" if inside else "B better"
    if inside:
        return "equivalent (±5pp)"
    return "no detectable difference"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lenient", action="store_true")
    ap.add_argument("--graded", default=str(ROOT / "results/accuracy/graded.csv"))
    ap.add_argument("--suffix", default="")
    ap.add_argument("--exclude-toolcall-batches", action="store_true",
                    help="sensitivity: drop (model, batch) pairs where any format's reply contained a fake tool call")
    ap.add_argument("--exclude-questions", default="",
                    help="comma-separated question ids to drop (e.g. upstream ground-truth bugs)")
    args = ap.parse_args()
    col = "correct_lenient" if args.lenient else "correct"
    suffix = args.suffix or ("_lenient" if args.lenient else "")
    OUT.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(open(args.graded)))
    if args.exclude_questions:
        drop = set(args.exclude_questions.split(","))
        rows = [r for r in rows if r["question_id"] not in drop]
    if args.exclude_toolcall_batches:
        bad = {(r["model"], r["batch_id"]) for r in rows if r.get("fake_tool_call") == "1"}
        bad_q = {(r["model"], r["seed"], r["question_id"]) for r in rows if (r["model"], r["batch_id"]) in bad}
        rows = [r for r in rows if (r["model"], r["seed"], r["question_id"]) not in bad_q]
        print(f"excluded {len(bad)} (model, batch) pairs")

    qmeta = {}
    score = defaultdict(lambda: defaultdict(dict))  # (model, format) -> qid -> {seed: 0/1}
    fails = defaultdict(lambda: defaultdict(int))
    for r in rows:
        qmeta[r["question_id"]] = r
        score[(r["model"], r["format"])][r["question_id"]][int(r["seed"])] = int(r[col])
        fails[(r["model"], r["format"])][r["error_class"] or "correct"] += 1
    rng = np.random.default_rng(12345)

    def has(level, fmt, q):
        return all(score[(m, fmt)].get(q) for m in LEVELS[level])

    def qscore(level, fmt, qids):
        return np.array([np.mean([v for m in LEVELS[level] for v in score[(m, fmt)][q].values()]) for q in qids])

    def majority(level, fmt, qids):
        return (qscore(level, fmt, qids) > 0.5).astype(int)

    subset_q = defaultdict(list)
    for q, meta in qmeta.items():
        for s in subsets(meta):
            subset_q[s].append(q)
    subset_q = {k: sorted(v) for k, v in subset_q.items()}

    informative = {}
    for level in LEVELS:
        inf = []
        for q in subset_q["overall"]:
            vals = [v for m in LEVELS[level] for f in MAIN for v in score[(m, f)].get(q, {}).values()]
            if vals and min(vals) != max(vals):
                inf.append(q)
        informative[level] = inf

    def boot_q(d):
        idx = rng.integers(0, len(d), size=(B, len(d)))
        return d[idx].mean(axis=1)

    def boot_ds(d, qids):
        """two-stage: resample datasets, then questions within each chosen dataset (vectorised)"""
        groups = defaultdict(list)
        for i, q in enumerate(qids):
            groups[qmeta[q]["dataset"]].append(i)
        g = [np.array(v) for v in groups.values()]
        G = len(g)
        sizes = np.array([len(x) for x in g])
        # sums[j, b, k]: sum of a within-dataset resample of dataset j, for replicate b, slot k
        sums = np.stack([d[x][rng.integers(0, len(x), size=(B, G, len(x)))].sum(axis=2) for x in g])
        chosen = rng.integers(0, G, size=(B, G))
        tot = sums[chosen, np.arange(B)[:, None], np.arange(G)[None, :]].sum(axis=1)
        cnt = sizes[chosen].sum(axis=1)
        return tot / cnt

    # --- accuracy summary
    with open(OUT / f"accuracy_summary{suffix}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "format", "subset", "n_questions", "n_answers", "accuracy", "ci_lo", "ci_hi", "seed1", "seed2", "seed3"])
        for level in LEVELS:
            for fmt in FORMATS:
                for sname, all_q in list(subset_q.items()) + [("informative", informative[level])]:
                    qids = [q for q in all_q if has(level, fmt, q)]
                    if not qids:
                        continue
                    s = qscore(level, fmt, qids)
                    boots = boot_q(s)
                    seeds = []
                    for seed in (1, 2, 3):
                        vals = [score[(m, fmt)][q][seed] for m in LEVELS[level] for q in qids if seed in score[(m, fmt)][q]]
                        seeds.append(round(float(np.mean(vals)), 4) if vals else "")
                    n_ans = sum(len(score[(m, fmt)][q]) for m in LEVELS[level] for q in qids)
                    w.writerow([level, fmt, sname, len(qids), n_ans, round(float(s.mean()), 4),
                                round(float(np.percentile(boots, 2.5)), 4), round(float(np.percentile(boots, 97.5)), 4), *seeds])

    # --- paired comparisons
    out_rows = []
    for level in LEVELS:
        for fam, pairs in (("primary", PRIMARY), ("extra", EXTRA), ("layout", LAYOUT)):
            for a, b in pairs:
                for sname, all_q in list(subset_q.items()) + [("informative", informative[level])]:
                    qids = [q for q in all_q if has(level, a, q) and has(level, b, q)]
                    if not qids:
                        continue
                    sa, sb = qscore(level, a, qids), qscore(level, b, qids)
                    d = sa - sb
                    bq = boot_q(d)
                    lo, hi = float(np.percentile(bq, 2.5)), float(np.percentile(bq, 97.5))
                    ds_lo = ds_hi = ""
                    if sname in ("overall", "overall-excl-structural", "informative") or sname.startswith(("track:", "shape:mixed", "shape:uniform")):
                        bd = boot_ds(d, qids)
                        ds_lo, ds_hi = round(float(np.percentile(bd, 2.5)), 4), round(float(np.percentile(bd, 97.5)), 4)
                    ma, mb = majority(level, a, qids), majority(level, b, qids)
                    n01 = int(((ma == 1) & (mb == 0)).sum())
                    n10 = int(((ma == 0) & (mb == 1)).sum())
                    p = binomtest(n01, n01 + n10, 0.5).pvalue if n01 + n10 else 1.0
                    out_rows.append({
                        "model": level, "A": a, "B": b, "family": fam, "subset": sname, "n_questions": len(qids),
                        "acc_A": round(float(sa.mean()), 4), "acc_B": round(float(sb.mean()), 4),
                        "diff": round(float(d.mean()), 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
                        "ds_ci_lo": ds_lo, "ds_ci_hi": ds_hi,
                        "mcnemar_A_only": n01, "mcnemar_B_only": n10, "mcnemar_p": round(float(p), 5),
                        "verdict": verdict(lo, hi),
                        "verdict_ds": verdict(ds_lo, ds_hi) if ds_lo != "" else "",
                    })
    fam = [r for r in out_rows if r["family"] == "primary" and r["subset"] == "overall" and r["model"] in ("haiku", "sonnet", "opus", "pooled")]
    for r, adj in zip(fam, holm([r["mcnemar_p"] for r in fam])):
        r["holm_p_primary_overall"] = round(adj, 5)
    with open(OUT / f"paired{suffix}.csv", "w", newline="") as f:
        fields = list(dict.fromkeys(list(out_rows[0].keys()) + ["holm_p_primary_overall"]))
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    with open(OUT / f"failures{suffix}.csv", "w", newline="") as f:
        classes = ["correct", "comprehension", "format-lenient", "format-missing", "call-failed"]
        w = csv.writer(f)
        w.writerow(["model", "format", *classes])
        for (m, fmt), c in sorted(fails.items()):
            w.writerow([m, fmt, *[c.get(k, 0) for k in classes]])
    print("wrote", OUT, suffix or "(primary)", "informative:", {k: len(v) for k, v in informative.items()})


if __name__ == "__main__":
    main()
