# Deviations log (running; merged into REPORT.md at the end)

Each entry is timestamped and committed when it is made.

## D1 (2026-09-28, before any main accuracy run) — one extra answer-format line for all formats

A 21-call Haiku pilot with the pre-registered batch template
(`results/raw/pilot/haiku-pilot-template-v1.jsonl`) showed that, unlike
upstream's single-question calls, batched calls sometimes make the model show
its work: 5/21 replies contained long step-by-step reasoning, and 2 of those
contained fake tool calls (Python/Clojure scripts in `<function_calls>` text),
because the Claude Code CLI injects ~780 tokens of environment
`<system-reminder>`s (scratchpad path, proxy notes, date, model id) into the
user turn even with `--system-prompt ""`. That reasoning is incompatible with
upstream's `reasoning: 'none'` design and adds noise.
Change: one line added to the shared template, for every format:
`- Do not show your work, reasoning or code`.
A retest of the pilot's reasoning batches with this line produced direct
answers in 10 of 12 replies (`results/raw/pilot/haiku-pilot-template-v2-retest.txt`;
correction added after review: the same batch, s3-b071-edn-table, stayed very
long in both retests). The pilot
calls are excluded from all analyses. No format-specific wording changed; the
manifest fairness check still passes.

## D2 (2026-09-28, before any main accuracy run) — last "Q<n>:" line wins

PLAN.md said "first match wins". Pilot replies that did reason restated each
question as a `**Q1: <question>**` header and then ended with a clean answer
block; first-match parsing would grade the header. The parser now takes the
last matching line per question number. Same rule for all formats.

## D3 — Claude token counts via CLI usage, not the token-counting API

Pre-announced in PLAN.md §3 (no ANTHROPIC_API_KEY). Listed here for completeness.

## D4 — the Claude CLI's injected preamble

PLAN.md §4 expected a "constant ~780–1,000-token preamble". Inspection showed
its content: environment `<system-reminder>` blocks (working directory,
scratchpad path, proxy note, model id and knowledge cutoff, date, user e-mail,
git attribution text). It is identical for every format and cannot be removed
without an API key (`--bare` requires `ANTHROPIC_API_KEY`).

## D5 (2026-09-28, before the main accuracy runs) — effort pinned to low; Opus 5.5 thinks anyway

The parent session exports `CLAUDE_EFFORT=high`, which the subagents
inherited. Haiku 4.5 and Sonnet 5 produced 0 thinking tokens with
`MAX_THINKING_TOKENS=0`, but Opus 5.5 used adaptive extended thinking
(~400–1,300 thinking tokens per batch) under every CLI control tried:
`MAX_THINKING_TOKENS=0`, `--settings '{"alwaysThinkingEnabled":false}'`,
`CLAUDE_CODE_DISABLE_THINKING=1`, `--effort low` (lowest, still ~750).
Change: `--effort low` and `CLAUDE_EFFORT=low` for every model. Consequence:
Opus results are *with hidden reasoning* and are not comparable to upstream's
`reasoning: 'none'` numbers; within-Opus format comparisons stay paired and
fair (same settings for all formats). Opus thinking tokens are reported per
format as a secondary "reading effort" measure. The partial runs made before
this change (`results/raw/pilot/*-pilot-effort-high.jsonl`) are excluded.

## Post-review changes (after the adversarial review; exploratory, not pre-registered)

The adversarial review (REPORT.md §9) ran after all pre-registered results
existed. Everything below was added in response to it. It supplements the
pre-registered analyses and replaces none of them.

### D6 — layout-confound accuracy run (`edn-table-lines`)
The review noted that on the mixed datasets EDN is one long line while TOON puts one
record per line. New format `edn-table-lines`: identical content to `edn-table`,
with one top-level record or map entry per line. It uses the same short primer, the
same `edn-table` prompt label, and the same batches and seeds. It ran on the 45
mixed-track batches per model (the flat datasets are byte-identical to
`edn-table`), for all 3 models. Manifest: `results/accuracy_layout/`. Cost
$2.89.

### D7 — generation check: TOON arm with a quoting-rules primer (`toon-long`)
The review noted that the TOON prompt (upstream one-line primer) omits TOON's quoting
rules, while EDN-table got the 144-token LONG primer. The new arm is TOON with a
156-token primer stating the quoting and escaping rules from upstream's
`docs/guide/format-overview.md` (`src/toon-long-primer.ts`). It uses the same records,
example and template, 3 samples per record, for all 3 models. Cost $0.74.

### D8 — statistics additions
- **Seed columns:** the per-seed columns used row order, not the seed field
  (a bug). They are now keyed by seed. Point estimates and CIs were unaffected,
  since they average over seeds.
- **`pooled-nr` level:** Haiku + Sonnet only, the two models that ran without
  reasoning.
- **Dataset-level CIs:** a two-stage bootstrap (datasets, then questions) is
  reported next to the pre-registered question bootstrap.
- **`informative` subset:** questions whose correctness varies across the five
  main formats × seeds.
- **Ground-truth sensitivity:** a run excluding the three upstream
  ground-truth bugs (q110, q233, q234).
- **Generation CIs:** clustered by record (bootstrap over the 20 records).
- **Headline H4:** now uses questions excluding structural validation (as the
  review asked). The all-question numbers stay in the tables.

### D9 — Claude tokenizers in the break-even analysis
PLAN §6 asked for break-even per tokenizer. The first report covered o200k and
Qwen3 only. The break-even series (n ≤ 100) were then measured with Haiku 4.5
and Opus 5.5 CLI usage deltas ($1.98), and crossings are now interpolated
(`tools/breakeven.py`).
