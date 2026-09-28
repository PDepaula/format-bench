# PLAN: EDN vs TOON vs JSON as LLM data formats (pre-registration)

Written and committed **before any benchmark result was produced**. Nothing in
this file was tuned after looking at EDN token counts or model answers. Any
later change is listed under "Deviations" in REPORT.md with its reason.

## 0. Base harness

- Upstream: <https://github.com/toon-format/toon>, commit
  `f151a5d830d001bc244395b891183cba37e0d935` (2026-09-03), vendored unmodified
  in `vendor/toon/` (first commit of this repo). All harness changes are a git
  diff against that commit.
- Reused as-is: the datasets (`benchmarks/src/datasets.ts`, faker seed 12345 /
  67890 / 67891), the 244 generated questions (`src/questions/`), the
  flat-only / mixed-structure track split (`metadata.supportsCSV`), the
  post-encode structural corruption, the per-format primer lines, the prompt
  template (`src/evaluate.ts`) and the deterministic checker
  (`src/normalize.ts#compareAnswers`).
- Question counts (checked before writing this plan): 244 total; flat-only
  track 109 (tabular 41, analytics 30, github 33, 5 structural-validation),
  mixed-structure track 135 (nested 41, event-logs 30, nested-config 29,
  keyed 17, nested-group 18).

## 1. Hypotheses

- **H1** EDN-maps (keyword keys, no colons/commas) uses fewer tokens than
  compact JSON, and the saving is larger on nested data (mixed track) than on
  flat data.
- **H2** EDN-table (`{:cols [...] :rows [[...] ...]}`) matches or beats TOON on
  uniform arrays (tokens and accuracy).
- **H3** A short EDN primer (≤ ~150 tokens) makes up for EDN's thinner training
  data (accuracy), and its per-call token cost pays off at realistic payload
  sizes.
- **H4** Models answer questions about EDN data about as well as about JSON
  and TOON.

## 2. Contenders (format ids)

| id | encoding | primer line (prepended by the harness template) |
| --- | --- | --- |
| `json-compact` | `JSON.stringify(data)` (upstream) | upstream: `JSON (compact): Strict JSON without extra whitespace.` |
| `toon` | upstream TOON encoder, default options | upstream TOON primer (80 o200k tokens) |
| `edn-maps` | direct conversion, keyword keys, vectors for arrays, single line, one space between elements | SHORT primer (below) |
| `edn-table` | as `edn-maps`, but every *tabular-eligible* array becomes `{:cols [...] :rows [...]}`; each row vector after the first starts on a new line | SHORT primer (same as edn-maps) |
| `edn-table-primer` | byte-identical data block to `edn-table` | LONG primer (below) instead of SHORT |
| `csv` | upstream CSV, flat-only track only | upstream CSV primer |

`json-pretty`, `yaml`, `xml` stay in the token tables for reference only; they
are not run for accuracy.

**SHORT primer** (29 o200k tokens):
`EDN: Clojure data notation. Maps {:key value}, vectors [a b c], keyword keys (:name), nil for null.`

**LONG primer** (the H3 treatment; ≤ 150 o200k tokens, exact text frozen here):

```
EDN (Clojure data notation) primer:
- Map: {key value key value ...}. Keys are keywords like :name (field name = keyword without the colon) or, if not keyword-safe, strings.
- Vector: [a b c], elements separated by whitespace; commas are not used.
- Values: "strings", numbers, true, false, nil (null).
- Table: {:cols [:c1 :c2 ...] :rows [[v1 v2 ...] ...]} is an array of records. Each row vector is one record whose Nth value belongs to the Nth column in :cols. Each row starts on a new line; record count = number of rows.
```

Primer tokens are counted in the per-call cost of every format (all formats
carry the upstream primer line), and H3's break-even uses them explicitly.

### Encoding rules (fixed)

- Map keys: emitted as keywords when they match
  `^(?:[A-Za-z*!_?$%&=<>]|[-+.](?![0-9]))[A-Za-z0-9.*+!_?$%&=<>-]*$`, otherwise
  as EDN strings. Values that are strings are always EDN strings (never
  keywords), so decoding keyword→name is unambiguous.
- Strings: `"`-delimited; escape `\\`, `\"`, `\n`, `\r`, `\t`; other control
  characters as `\uXXXX`; all other Unicode emitted raw.
- Numbers: JavaScript `String(n)` (same digits as JSON); non-finite → error.
  `true`/`false`; `null` → `nil`. Date strings stay strings (no `#inst`), as in
  the JSON source.
- Tabular-eligible array (same rule as TOON's primitive tabular form): length
  ≥ 1, every element a plain object, every element has the identical key
  sequence (same keys, same order), every value a primitive
  (string/number/boolean/null). Keyed maps of uniform objects and uniform
  arrays with nested-object cells are **not** tables in EDN-table (they stay
  EDN-maps); TOON's keyed and nested-field-group extensions have no EDN-table
  counterpart.
- A source object whose key set is exactly `{cols, rows}` would be ambiguous;
  the encoder throws (none exist in the datasets).
- Structural-validation corruption for EDN: `edn-maps` gets the same
  parsed-object surgery as upstream `json-compact` (drop records / append
  records / delete the field). `edn-table` and `edn-table-primer` get the same
  treatment as TOON/CSV rows: drop trailing rows / append rows / drop the cell
  from the targeted rows (row narrower than `:cols`). EDN-table carries no
  declared length, so truncation and extra rows are undetectable in it, as in
  JSON.

### Losslessness gate

Every encoder must round-trip every accuracy and token dataset (and the
generation-check records) through a real EDN parser before any model is
called: `edn-data` (npm, vitest) **and** `edn_format` (Python, pytest). The
decoder maps keywords → strings, vectors → arrays, `nil` → null and expands
`{:cols :rows}` tables (EDN-table only). Comparison is deep equality
**including key order**. TOON round-trips through the upstream `decode`. If any
round-trip fails, no accuracy run starts until the encoder is fixed.

## 3. Token counts

- Datasets: upstream `TOKEN_EFFICIENCY_DATASETS` (the larger token-benchmark
  sizes) for the headline tables, and `ACCURACY_DATASETS` (the prompts
  actually sent). Tracks exactly as upstream (flat-only = `supportsCSV`).
- Tokenizers, each reported separately, never averaged:
  1. **o200k_base via `tiktoken`** (Python). huggingface.co and
     openaipublic.blob.core.windows.net are blocked by this environment's
     egress policy, so the `.tiktoken` file is rebuilt from the ranks bundled
     in the upstream benchmark's `gpt-tokenizer` dependency and must match
     tiktoken's pinned sha256 (`446a9538…1a2d`); tiktoken itself verifies it.
     Counts are cross-checked against `gpt-tokenizer` (must be identical).
  2. **Qwen3** via Hugging Face `tokenizers` loading the Qwen3 `tokenizer.json`
     (obtained from npm package `@lenml/tokenizer-qwen3@3.7.2` because HF is
     blocked; sha256 recorded in REPORT.md; vocab 151,643 + Qwen3 added tokens
     incl. `<think>`). No special tokens added.
  3. **Claude**: the token-counting API needs `ANTHROPIC_API_KEY`, which is
     **not set** → the token-counting API is **skipped**. As a substitute
     (clearly labelled), Claude counts are derived from the `usage` block of
     real calls through the Claude Code CLI: tokens(data) =
     input_total(`"DATA:\n" + data`) − input_total(`"DATA:"`) (±1 token
     boundary effect). Measured with Haiku 4.5 and Opus 5.5 on all token
     datasets; Sonnet 5 on the accuracy datasets only, and on the large ones
     only if its counts differ from Opus 5.5 on the accuracy datasets.
- Also reported (tokens only, no accuracy runs) as a whitespace confound check:
  `edn-table` with all rows on one line, and `edn-maps` with one top-level
  array element per line.

## 4. Accuracy

- All 244 questions, no sampling. Formats: `json-compact`, `toon`,
  `edn-maps`, `edn-table`, `edn-table-primer` on all 244; `csv` on the 109
  flat-only questions.
- Models: Claude Haiku (`haiku` → claude-haiku-4-5-20251001), Claude Sonnet
  (`sonnet` → claude-sonnet-5), Claude Opus (`opus` → claude-opus-5-5); the
  served model id is recorded per call from the CLI's `modelUsage`.
- No API key is in the environment, so the upstream runner (`ai` SDK) cannot
  be used. Calls go through **headless Claude Code subagents**
  (`claude -p --model <m>`), configured to approximate upstream's raw API
  call: `--system-prompt ""`, `--tools ""` (no tool use possible),
  `--setting-sources ""`, `--strict-mcp-config`, `--disable-slash-commands`,
  `--no-session-persistence`, `MAX_THINKING_TOKENS=0` (upstream uses
  `reasoning: 'none'`), `DISABLE_PROMPT_CACHING=1`, default temperature. The
  CLI adds a constant ~780–1,000-token preamble identical for every format.
- **Batching**: upstream asks one question per call; we batch (≤ 10 questions
  per call, same dataset only, so each call carries one data block). Prompt =
  upstream template verbatim with the single `Question:` line replaced by a
  numbered list and one extra answer-format line, identical for every format:

  ```
  {primer}

  Given the following data in {label} format:

  ```{fence}
  {data}
  ```

  Questions:
  Q1: ...
  Q2: ...

  Answer format requirements:
  - Answer each question on its own line as "Q<number>: <answer>", in order, with no other text
  - Provide only the value itself, no explanation
  - For numbers: output digits only (no commas, currency symbols, or units)
  - For dates/field names: use the exact string from the data
  - For lists: output comma-separated values with no spaces

  Answers:
  ```

  `{label}` is the format id, except `edn-table-primer` uses `edn-table` so
  the label does not leak the condition. Fences: `json`, `toon`, `csv`, `edn`.
- **Seeds**: 3 seeds (1, 2, 3) per model × format. Per seed the 244 questions
  are shuffled with a seeded PRNG, grouped by dataset in shuffled order, and
  each dataset's list is split into ⌈n/10⌉ near-equal consecutive batches.
  The same batches and order are used for every format and every model within
  a seed (paired design).
- **Parsing**: a line matching `^\s*\**Q?(\d+)\**\s*[:.)]\s*(.*)$` gives the
  answer for question n (first match wins). A missing answer is graded
  incorrect and classified as a *format/parse error*.
- **Grading (primary)**: upstream `compareAnswers` unchanged, per question.
- **Grading (secondary, sensitivity only)**: a pre-registered, format-agnostic
  lenient normaliser applied identically to all formats before
  `compareAnswers`: strip surrounding backticks/brackets `[]`/parentheses,
  strip a leading `:` from each comma-separated item, remove wrapping quotes
  per item, and for `csv-list-*` answers with no comma but spaces, split on
  whitespace. Answers correct only under the lenient grader are classified as
  *format errors*, not comprehension errors.
- Failed CLI calls are retried up to 3 times; persistent failures are
  reported and counted as missing (not silently dropped).
- External check: our batched Haiku accuracy for `json-compact` and `toon` is
  compared with upstream's published single-question Haiku 4.5 results in
  `vendor/toon/benchmarks/results/accuracy/models/`.

## 5. Generation check

- 20 JSON records of varied shape in `generation/records.json` (committed
  with this plan): 7 flat (uniform arrays of primitive objects), 7 nested
  (deep objects, nested arrays, keyed maps), 6 mixed (optional fields, arrays
  of primitives, empty containers, mixed arrays). They include tricky
  scalars shared across formats (quotes, commas, colons, newlines, unicode,
  empty strings, null, negative/float numbers) and two non-keyword-safe keys.
- Target formats: `edn-table`, `edn-maps`, `toon`. Models: haiku, sonnet,
  opus. 3 samples per (model, format, record) → 60 attempts per cell, same CLI
  settings as §4.
- Prompt (identical template; format-specific slots are the format's
  comprehension primer from §2 — LONG for edn-table, SHORT for edn-maps,
  upstream primer for TOON — plus one worked example produced by the
  reference encoder from the same example JSON):

  ```
  Convert the JSON data below to {name}.

  {primer}

  Example. This JSON:
  ```json
  {example_json}
  ```
  is written in {name} as:
  ```{fence}
  {example_encoded}
  ```

  Now convert this JSON:
  ```json
  {record_json}
  ```

  Output only the converted data in a single ```{fence} code block, with nothing before or after it.
  ```
- Metrics per model × format: **parse-valid rate** (the fenced block, or the
  whole reply if unfenced, parses with `edn_format`/`edn-data` for EDN, with
  upstream TOON `decode` (strict) for TOON) and **lossless round-trip rate**
  (decoded value deep-equals the source JSON; key order ignored, numbers
  compared numerically, strings exact; tables expanded for edn-table only).
  Secondary: **canonical-form rate** (parsed structure equals the reference
  encoder's structure, i.e. tables used exactly where eligible). Wilson 95%
  CIs.

## 6. Statistics and decision rules

- Unit: question. Per model × format, accuracy = mean over 3 seeds × questions.
  95% CI by **cluster bootstrap over questions** (10,000 resamples, all seeds
  of a question kept together; seed 12345). Per-seed Wilson intervals are also
  shown for comparability with upstream.
- **Paired comparisons** (per model, and pooled over the 3 models): per
  question q, score_f(q) = mean correctness over seeds (and models when
  pooled); d(q) = score_A(q) − score_B(q); 95% CI of mean d by paired bootstrap
  over questions (10,000 resamples). Also McNemar exact test on
  majority-of-3-seeds correctness, with Holm adjustment within the primary
  family. **A difference is called only if the 95% CI excludes 0**; otherwise
  "no detectable difference".
- **Equivalence margin** for "matches" / "about as well": ±5 percentage
  points. Equivalent = 95% CI of the difference lies entirely inside
  [−5, +5] pp. CI crossing a margin and 0 = inconclusive.
- Primary comparison family (each per model and pooled):
  1. edn-maps vs json-compact
  2. edn-table vs toon
  3. edn-table-primer vs edn-table
  4. edn-table-primer vs toon
  5. edn-table-primer vs json-compact
  6. edn-maps vs toon
- Subsets: overall (244); flat-only track (109); mixed track (135); data
  shapes below. Structural-validation questions (5) are included in overall
  and flat-track numbers, reported separately, and a sensitivity analysis
  drops them (they reward declared lengths by design).
- **Data shapes** (fixed mapping):
  - *Uniform tables*: tabular, analytics, github (104 questions)
  - *Nested config*: nested-config (29)
  - *Mixed*: nested (orders), event-logs, keyed, nested-group (106)
  - *Structural validation*: the 5 validation datasets (5)

### Verdict rules

- **H1** per tokenizer: *supported* if edn-maps < json-compact on both track
  totals **and** the relative saving on the mixed track ≥ that on the flat
  track; *partly supported* if only the first half holds; *refuted* if
  edn-maps ≥ json-compact on either track total. Also reported: edn-maps vs
  TOON on nested-config.
- **H2**: tokens — per tokenizer on the uniform-table datasets (tabular,
  analytics, github; token-benchmark sizes): *beats* if edn-table ≤ 0.95 ×
  TOON, *matches* if within ±5 %, *loses* otherwise. Accuracy — paired
  edn-table vs toon on uniform-table questions: equivalence / difference /
  inconclusive per §6. H2 is *supported* only if tokens match-or-beat on every
  tokenizer and accuracy is equivalent or better (pooled over models).
- **H3**: (a) *primer helps*: edn-table-primer vs edn-table CI > 0 (pooled);
  (b) *makes up for training data*: edn-table-primer equivalent to or better
  than both json-compact and toon (pooled, overall); (c) *pays off*: per
  tokenizer, break-even payload size where
  primer_LONG + data(edn-table) ≤ data(json-compact) [conservative: JSON with
  no primer at all], computed on employees/analytics/github at
  n ∈ {1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000} records; "realistic" =
  break-even at ≤ 50 records. Also reported: break-even vs TOON (with and
  without its primer), and break-even in number of calls when the primer is
  sent once per conversation. H3 is supported if (b) and (c) hold.
- **H4**: per model and pooled, each EDN variant vs json-compact and vs toon:
  *supported* (about as well) if equivalent within ±5 pp; *EDN worse/better*
  if CI excludes 0 in that direction and not equivalent; else inconclusive.
- **Per data shape**: winner on tokens (per tokenizer) and on accuracy
  (pooled, with CI); confidence stated as high (CI excludes 0 for each model),
  medium (pooled only), low (no detectable difference).
- Every verdict is written as: claim; evidence with interval; what would
  change the conclusion.

## 7. Judging rigor

- Fairness checks before trusting numbers: round-trip gate (§2); identical
  question set, template (apart from primer line, label, fence and data
  block), batches and seeds for all formats (asserted by a test on the task
  manifest); token counts via the same text that is sent to models.
- **Grader audit**: 30 uniformly random graded answers per format (fixed
  sampling seed 777, across models and seeds), hand-checked by me (the
  orchestrating agent) against question, ground truth and answer. Grader
  errors reported with direction (which format they favour).
- **Failure classification** for every incorrect answer: format/parse error
  (missing line; correct under lenient grader; explanation text instead of a
  value) vs comprehension error (clean value, wrong). Hand audit also checks
  this classification on the sampled incorrect answers.
- **Confounds tracked**: primer position (same slot for all formats), primer
  length (reported in cost), whitespace/pretty-printing (§3 layout variants),
  tokenizer quirks (per-tokenizer tables, example token splits), batching
  (external check vs upstream), label/fence names.
- **Adversarial review**: after results, a fresh subagent on Opus receives only
  PLAN.md, the harness diff and the raw results and is asked for every reason
  the conclusions could be wrong or unfair. Fixable issues are fixed (with
  re-runs if needed); critique and responses go into REPORT.md.
- Cost: no API key is present, so the $40 API cap does not strictly apply;
  I will still aim to stay near that figure at list prices and report the
  CLI-reported list-price cost (`total_cost_usd`) of every call.

## 8. Deliverables

`PLAN.md` (this file, committed first), harness diff + encoders + tests under
`vendor/toon/benchmarks`, Python tooling under `tools/`, raw per-call and
per-question results under `results/`, and `REPORT.md`.
