"""Renders markdown tables used in REPORT.md into results/analysis/report_tables.md."""
import csv
from collections import defaultdict
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "results/analysis"
FMTS = ["json-compact", "toon", "edn-maps", "edn-table", "edn-table-primer", "csv"]
MODELS = ["haiku", "sonnet", "opus", "pooled", "pooled-nr"]
FMTS_ALL = FMTS + ["edn-table-lines"]
md = []


def pct(x):
    return f"{float(x) * 100:.1f}"


S = list(csv.DictReader(open(A / "accuracy_summary.csv")))
for sub, title in [("overall", "All 244 questions (CSV: 109 flat questions)"), ("track:flat", "Flat-only track (109)"), ("track:mixed", "Mixed-structure track (135)"),
                   ("shape:uniform-tables", "Uniform tables (104)"), ("shape:nested-config", "Nested config (29)"), ("shape:mixed", "Mixed shapes (106)"),
                   ("shape:structural-validation", "Structural validation (5)"), ("overall-excl-structural", "All except structural validation (239)"),
                   ("informative", "Informative questions only (correctness varies across formats × seeds for that model level)")]:
    fold = sub not in ("overall", "overall-excl-structural")
    if fold:
        md.append(f"\n<details><summary>{title}</summary>\n")
    md.append(f"\n**{title}** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI\n")
    md.append("| model | " + " | ".join(FMTS_ALL) + " |")
    md.append("|---" * (len(FMTS_ALL) + 1) + "|")
    for m in MODELS:
        cells = []
        for f in FMTS_ALL:
            r = [x for x in S if x["model"] == m and x["format"] == f and x["subset"] == sub]
            cells.append(f"{pct(r[0]['accuracy'])} [{pct(r[0]['ci_lo'])}, {pct(r[0]['ci_hi'])}]" if r else "–")
        md.append(f"| {m} | " + " | ".join(cells) + " |")
    if fold:
        md.append("\n</details>")

P = list(csv.DictReader(open(A / "paired.csv")))
for sub in ["overall-excl-structural", "overall", "informative", "shape:uniform-tables", "shape:nested-config", "shape:mixed", "track:flat", "track:mixed"]:
    fold = sub not in ("overall-excl-structural", "overall")
    if fold:
        md.append(f"\n<details><summary>Paired comparisons — {sub}</summary>\n")
    md.append(f"\n**Paired comparisons — {sub}** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)\n")
    md.append("| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in P:
        if r["subset"] != sub:
            continue
        keep = r["family"] == "primary" or (r["A"], r["B"]) == ("toon", "json-compact") or (r["family"] == "layout" and sub in ("track:mixed", "shape:mixed"))
        if not keep:
            continue
        ds = f"[{float(r['ds_ci_lo'])*100:+.1f}, {float(r['ds_ci_hi'])*100:+.1f}]" if r["ds_ci_lo"] else "–"
        md.append(f"| {r['model']} | {r['A']} vs {r['B']} | {r['n_questions']} | {float(r['diff'])*100:+.1f} | [{float(r['ci_lo'])*100:+.1f}, {float(r['ci_hi'])*100:+.1f}] | {ds} | {float(r['mcnemar_p']):.3f} | {r.get('holm_p_primary_overall') or ''} | {r['verdict']} | {r['verdict_ds']} |")
    if fold:
        md.append("\n</details>")

for suf, title in [("_lenient", "lenient grader"), ("_no_toolcall_batches", "excluding batches with a fake tool call"), ("_no_broken_gt", "excluding the 3 upstream ground-truth bugs (q110, q233, q234)")]:
    P2 = list(csv.DictReader(open(A / f"paired{suf}.csv")))
    md.append(f"\n**Sensitivity — {title}, overall, pooled**\n")
    md.append("| level | A vs B | diff | 95% CI | verdict |")
    md.append("|---|---|---|---|---|")
    for r in P2:
        if r["subset"] == "overall" and r["model"] in ("pooled", "pooled-nr") and r["family"] == "primary":
            md.append(f"| {r['model']} | {r['A']} vs {r['B']} | {float(r['diff'])*100:+.1f} | [{float(r['ci_lo'])*100:+.1f}, {float(r['ci_hi'])*100:+.1f}] | {r['verdict']} |")

F = list(csv.DictReader(open(A / "failures.csv")))
md.append("\n**Failure classification (all graded answers)**\n")
md.append("| model | format | correct | comprehension | format (lenient-correct) | format (missing) | call failed |")
md.append("|---|---|---|---|---|---|---|")
for r in F:
    md.append(f"| {r['model']} | {r['format']} | {r['correct']} | {r['comprehension']} | {r['format-lenient']} | {r['format-missing']} | {r['call-failed']} |")

C = {(r["model"], r["format"]): r for r in csv.DictReader(open(A / "per_call_cost.csv"))}
RB = {(r["model"], r["format"]): r for r in csv.DictReader(open(A / "reply_behaviour.csv"))}
md.append("\n**Reply behaviour and per-call cost** (per batched call; visible output excludes Opus's hidden thinking; fake-tool-call rate with Wilson 95% CI and Fisher exact p vs json-compact of the same model)\n")
md.append("| model | format | calls | mean input tok | median visible output | mean visible output | Opus thinking tok | fake tool calls | Fisher p vs JSON | list-price $/call |")
md.append("|---|---|---|---|---|---|---|---|---|---|")
for m in ["haiku", "sonnet", "opus"]:
    for f in FMTS:
        c, b = C[(m, f)], RB[(m, f)]
        md.append(f"| {m} | {f} | {c['calls']} | {c['mean_input_tokens']} | {b['median_visible_output_tokens']} | {b['mean_visible_output_tokens']} | {c['mean_thinking_tokens']} | {b['fake_tool_calls']} ({b['rate_pct']}% [{b['ci_lo_pct']}, {b['ci_hi_pct']}]) | {float(b['fisher_p_vs_json']):.4f} | {float(c['mean_cost_usd']):.4f} |")

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


GC = {(r["model"], r["format"]): r for r in csv.DictReader(open(A / "generation_clustered.csv"))}
md.append("\n**Generation check** (20 records × 3 samples = 60 attempts per cell; 95% CI = bootstrap over the 20 records, since samples of one record are near-duplicates). EDN parse-valid requires both edn-data and edn_format to accept. `toon-long` = post-hoc arm with a 156-token quoting-rules primer (D7).\n")
md.append("| model | format | parse-valid % [CI] | lossless round-trip % [CI] | canonical form (count) |")
md.append("|---|---|---|---|---|")
for m in ["haiku", "sonnet", "opus"]:
    for f in ["edn-table", "edn-maps", "toon", "toon-long"]:
        v = [r for r in R if r["model"] == m and r["format"] == f]
        g = GC[(m, f)]
        md.append(f"| {m} | {f} | {g['parse_valid_pct']} [{g['pv_ci_lo']}, {g['pv_ci_hi']}] | {g['lossless_pct']} [{g['ll_ci_lo']}, {g['ll_ci_hi']}] | {sum(int(r['canonical']) for r in v)}/{len(v)} |")
md.append("\n**Generation lossless rate by record shape** (all models)\n")
md.append("| shape | edn-table | edn-maps | toon | toon-long |")
md.append("|---|---|---|---|---|")
for sh in ["flat", "nested", "mixed"]:
    md.append(f"| {sh} | " + " | ".join(cell(sum(int(r['lossless']) for r in R if r['shape'] == sh and r['format'] == f), sum(1 for r in R if r['shape'] == sh and r['format'] == f)) for f in ["edn-table", "edn-maps", "toon", "toon-long"]) + " |")

X = list(csv.DictReader(open(A / "external_check.csv")))
md.append("\n**External check vs upstream (Haiku 4.5)**\n")
md.append("| format | n | upstream single-question | ours, batched (mean 3 seeds) | per-question agreement (majority) |")
md.append("|---|---|---|---|---|")
for r in X:
    md.append(f"| {r['format']} | {r['n_questions']} | {pct(r['upstream_single_question'])} | {pct(r['ours_batched_mean3seeds'])} | {pct(r['per_question_agreement_majority'])} |")

(A / "report_tables.md").write_text("\n".join(md) + "\n")
print(len(md), "lines")
