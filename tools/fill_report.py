"""Substitutes generated tables into REPORT.md placeholders (idempotent: uses
<!-- BEGIN:name --> ... <!-- END:name --> markers after the first fill)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "results/analysis"
tokens = (A / "tokens.md").read_text()
tables = (A / "report_tables.md").read_text()


def section(text, start, end=None):
    i = text.index(start)
    j = text.index(end, i + len(start)) if end else len(text)
    return text[i:j].strip()


blocks = {
    "TOKENS_TABLES": "\n\n".join([
        section(tokens, "#### tokens datasets — o200k", "#### accuracy datasets — o200k"),
        "<details><summary>Accuracy-dataset sizes (the data blocks actually sent; per tokenizer)</summary>\n\n"
        + section(tokens, "#### accuracy datasets — o200k", "#### Primer lines") + "\n\n</details>",
        section(tokens, "#### Primer lines", "#### Primer break-even"),
    ]),
    "ACCURACY_TABLES": section(tables, "**All 244 questions", "**Failure classification"),
    "GENERATION": section(tables, "**Generation check**", "**External check"),
    "BREAKEVEN": section(tokens, "#### Primer break-even"),
    "FAILURES": section(tables, "**Failure classification", "**Generation check**").replace("**Reply behaviour", "\n**Reply behaviour"),
}
report = (ROOT / "REPORT.md").read_text()
for name, body in blocks.items():
    wrapped = f"<!-- BEGIN:{name} -->\n{body}\n<!-- END:{name} -->"
    if f"{name}_PLACEHOLDER" in report:
        report = report.replace(f"{name}_PLACEHOLDER", wrapped)
    else:
        report = re.sub(rf"<!-- BEGIN:{name} -->.*?<!-- END:{name} -->", lambda m: wrapped, report, flags=re.S)
# the external check table belongs in §4 as well
ext = section(tables, "**External check")
if "<!-- BEGIN:EXTERNAL -->" not in report:
    report = report.replace("**Opus caveat:**", f"<!-- BEGIN:EXTERNAL -->\n{ext}\n<!-- END:EXTERNAL -->\n\n**Opus caveat:**", 1)
else:
    report = re.sub(r"<!-- BEGIN:EXTERNAL -->.*?<!-- END:EXTERNAL -->", lambda m: f"<!-- BEGIN:EXTERNAL -->\n{ext}\n<!-- END:EXTERNAL -->", report, flags=re.S)
(ROOT / "REPORT.md").write_text(report)
print("filled; remaining placeholders:", re.findall(r"[A-Z_]+_PLACEHOLDER", report))
