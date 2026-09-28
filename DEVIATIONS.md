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
answers (`results/raw/pilot/haiku-pilot-template-v2-retest.txt`). The pilot
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
