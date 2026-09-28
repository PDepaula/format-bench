"""Renders markdown tables used in REPORT.md into results/analysis/report_tables.md."""
import csv
from collections import defaultdict
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "results/analysis"
FMTS = ["json-compact", "toon", "edn-maps", "edn-table", "edn-table-primer", "csv"]
MODELS = ["haiku", "sonnet", "opus", "pooled"]
md = []


def pct(x):
    return f"{float(x) * 100:.1f}"


S = list(csv.DictReader(open(A / "accuracy_summary.csv")))
for sub, title in [("overall", "All 244 questions (CSV: 109 flat questions)"), ("track:flat", "Flat-only track (109)"), ("track:mixed", "Mixed-structure track (135)"),
                   ("shape:uniform-tables", "Uniform tables (104)"), ("shape:nested-config", "Nested config (29)"), ("shape:mixed", "Mixed shapes (106)"),
                   ("shape:structural-validation", "Structural validation (5)"), ("overall-excl-structural", "All except structural validation (239)")]:
    md.append(f"\n**{title}** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI\n")
    md.append("| model | " + " | ".join(FMTS) + " |")
    md.append("|---" * (len(FMTS) + 1) + "|")
    for m in MODELS:
        cells = []
        for f in FMTS:
            r = [x for x in S if x["model"] == m and x["format"] == f and x["subset"] == sub]
            cells.append(f"{pct(r[0]['accuracy'])} [{pct(r[0]['ci_lo'])}, {pct(r[0]['ci_hi'])}]" if r else "–")
        md.append(f"| {m} | " + " | ".join(cells) + " |")

P = list(csv.DictReader(open(A / "paired.csv")))
for sub in ["overall", "overall-excl-structural", "shape:uniform-tables", "shape:nested-config", "shape:mixed", "track:flat", "track:mixed"]:
    md.append(f"\n**Paired comparisons — {sub}** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)\n")
    md.append("| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |")
    md.append("|---|---|---|---|---|---|---|---|")
    for r in P:
        if r["subset"] != sub or (r["family"] != "primary" and not (sub == "overall" and r["A"] == "toon")):
            continue
        md.append(f"| {r['model']} | {r['A']} vs {r['B']} | {r['n_questions']} | {float(r['diff'])*100:+.1f} | [{float(r['ci_lo'])*100:+.1f}, {float(r['ci_hi'])*100:+.1f}] | {float(r['mcnemar_p']):.3f} | {r.get('holm_p_primary_overall') or ''} | {r['verdict']} |")

for suf, title in [("_lenient", "lenient grader"), ("_no_toolcall_batches", "excluding batches with a fake tool call")]:
    P2 = list(csv.DictReader(open(A / f"paired{suf}.csv")))
    md.append(f"\n**Sensitivity — {title}, overall, pooled**\n")
    md.append("| A vs B | diff | 95% CI | verdict |")
    md.append("|---|---|---|---|")
    for r in P2:
        if r["subset"] == "overall" and r["model"] == "pooled" and r["family"] == "primary":
            md.append(f"| {r['A']} vs {r['B']} | {float(r['diff'])*100:+.1f} | [{float(r['ci_lo'])*100:+.1f}, {float(r['ci_hi'])*100:+.1f}] | {r['verdict']} |")

F = list(csv.DictReader(open(A / "failures.csv")))
md.append("\n**Failure classification (all graded answers)**\n")
md.append("| model | format | correct | comprehension | format (lenient-correct) | format (missing) | call failed |")
md.append("|---|---|---|---|---|---|---|")
for r in F:
    md.append(f"| {r['model']} | {r['format']} | {r['correct']} | {r['comprehension']} | {r['format-lenient']} | {r['format-missing']} | {r['call-failed']} |")

G = list(csv.DictReader(open(ROOT / "results/accuracy/graded.csv")))
calls = {}
for r in G:
    calls[(r["model"], r["batch_id"], r["format"])] = r
beh = defaultdict(lambda: defaultdict(float))
for (m, b, f), r in calls.items():
    k = (m, f)
    beh[k]["n"] += 1
    beh[k]["out"] += int(r["output_tokens"])
    beh[k]["think"] += int(r["thinking_tokens"] or 0)
    beh[k]["extra"] += int(r["extra_lines"]) > 1
    beh[k]["tool"] += r["fake_tool_call"] == "1"
C = {(r["model"], r["format"]): r for r in csv.DictReader(open(A / "per_call_cost.csv"))}
md.append("\n**Reply behaviour and per-call cost** (means per batched call)\n")
md.append("| model | format | calls | input tok | output tok | Opus thinking tok | replies with visible reasoning | fake tool calls | list-price $/call |")
md.append("|---|---|---|---|---|---|---|---|---|")
for (m, f), v in sorted(beh.items(), key=lambda kv: (MODELS.index(kv[0][0]), FMTS.index(kv[0][1]))):
    c = C[(m, f)]
    md.append(f"| {m} | {f} | {int(v['n'])} | {c['mean_input_tokens']} | {c['mean_output_tokens']} | {c['mean_thinking_tokens']} | {100*v['extra']/v['n']:.1f}% | {int(v['tool'])} | {float(c['mean_cost_usd']):.4f} |")

R = list(csv.DictReader(open(ROOT / "results/generation/graded.csv")))


def wil(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z / d * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return c - m, c + m


def cell(k, n):
    lo, hi = wil(k, n)
    return f"{k}/{n} ({100*k/n:.0f}%, [{100*lo:.0f}, {100*hi:.0f}])"


md.append("\n**Generation check** (20 records × 3 samples = 60 per cell; Wilson 95% CI). Parse-valid for EDN requires both edn-data and edn_format to accept.\n")
md.append("| model | format | parse-valid | lossless round-trip | canonical form |")
md.append("|---|---|---|---|---|")
for m in ["haiku", "sonnet", "opus"]:
    for f in ["edn-table", "edn-maps", "toon"]:
        v = [r for r in R if r["model"] == m and r["format"] == f]
        pv = sum(int(r["parse_valid"]) and (f == "toon" or r["parse_valid_edn_format"] == "1") for r in v)
        md.append(f"| {m} | {f} | {cell(pv, len(v))} | {cell(sum(int(r['lossless']) for r in v), len(v))} | {cell(sum(int(r['canonical']) for r in v), len(v))} |")
md.append("\n**Generation lossless rate by record shape** (all models)\n")
md.append("| shape | edn-table | edn-maps | toon |")
md.append("|---|---|---|---|")
for sh in ["flat", "nested", "mixed"]:
    md.append(f"| {sh} | " + " | ".join(cell(sum(int(r['lossless']) for r in R if r['shape'] == sh and r['format'] == f), sum(1 for r in R if r['shape'] == sh and r['format'] == f)) for f in ["edn-table", "edn-maps", "toon"]) + " |")

X = list(csv.DictReader(open(A / "external_check.csv")))
md.append("\n**External check vs upstream (Haiku 4.5)**\n")
md.append("| format | n | upstream single-question | ours, batched (mean 3 seeds) | per-question agreement (majority) |")
md.append("|---|---|---|---|---|")
for r in X:
    md.append(f"| {r['format']} | {r['n_questions']} | {pct(r['upstream_single_question'])} | {pct(r['ours_batched_mean3seeds'])} | {pct(r['per_question_agreement_majority'])} |")

(A / "report_tables.md").write_text("\n".join(md) + "\n")
print(len(md), "lines")
