# REPORT: Is EDN a real contender against TOON and JSON as an LLM data format?

Pre-registration: [`PLAN.md`](PLAN.md) (commit `fa4f204`, pushed before any
encoder output, token count or model answer existed). Deviations: §10 (also
logged live in [`DEVIATIONS.md`](DEVIATIONS.md)). Base harness: upstream
[toon-format/toon](https://github.com/toon-format/toon) at commit
`f151a5d830d001bc244395b891183cba37e0d935`, vendored unmodified in `vendor/toon`
(commit `2788bde`); every change is in [`results/review/harness.diff`](results/review/harness.diff).

## 1. Summary

**EDN is a real contender as a *readable* format, and models understand it as well as
JSON. It is not a contender as a *token-saving* format, which is the job TOON is chosen
for.**

**Comprehension.** Across all 244 upstream questions, 3 Claude models and 3 seeds,
EDN-maps and compact JSON are equivalent.
- The ±5 pp margin holds for every model under the question bootstrap, the
  dataset-level bootstrap, the lenient grader, and with the fake-tool-call
  batches or the broken ground truths removed.
- Pooled over the three models: +0.1 pp, 95% CI [−1.1, +1.1].
- EDN-table is also equivalent to JSON.

**Versus TOON.** Both EDN forms trail TOON by about 2 pp on non-structural
questions, the same size as TOON's lead over JSON.
- Haiku+Sonnet, EDN-table vs TOON: −1.8 pp [−3.8, +0.1].
- That lead is not robust under dataset-level resampling or Holm correction.
  Call it suggestive.
- Putting EDN records on separate lines, as TOON does, did not close the gap:
  −0.2 pp vs single-line EDN.

**Tokens.** EDN's syntax usually costs tokens instead of saving them.
- **EDN-maps vs compact JSON:** 6–10% *larger* on o200k, Qwen3 and
  Claude Haiku 4.5, and 1–2% smaller on the Claude 5 tokenizer
  (Sonnet 5 / Opus 5.5).
- **EDN-table vs TOON on uniform arrays:** 6.5–15% larger on every tokenizer.
  EDN-table does beat compact JSON by 24–35%.
- **The 144-token primer:** does nothing measurable (−0.1 pp [−0.9, +0.8]).
  EDN without it was already understood as well as JSON.

**Generation.** Small models *write* EDN more reliably than TOON. Haiku's lossless
output is 95% for EDN-maps vs 50% for TOON, and still 62% for TOON after TOON's
quoting rules were added to its primer. For Sonnet the gap to EDN-table closes once
TOON gets those rules (83% vs 83%). Opus writes every format correctly.

**By data shape:**
- **Uniform tables:** TOON (or CSV if the data is flat).
- **Deeply nested config:** no winner. Everything is within about 7% on tokens,
  and accuracy is at the ceiling.
- **Mixed data:** it depends.
  - Semi-uniform logs: EDN-table beats TOON by 6–13% on tokens, but compact JSON
    is cheaper still on 3 of 4 tokenizers.
  - Data that TOON folds into keyed or nested-field-group tables: TOON is 34–90%
    cheaper.

## 2. Setup actually run

| item | value |
|---|---|
| Datasets / questions | upstream `ACCURACY_DATASETS` (13 datasets, 244 questions; flat-only track 109, mixed 135) and `TOKEN_EFFICIENCY_DATASETS` (8 larger datasets). Ground truths match upstream's published run exactly. |
| Formats | `json-compact`, `toon`, `edn-maps`, `edn-table`, `edn-table-primer` on 244 q; `csv` on the 109 flat q; post-hoc `edn-table-lines` on the 135 mixed q (D6) |
| Models (served ids from CLI `modelUsage`) | `claude-haiku-4-5-20251001`, `claude-sonnet-5`, `claude-opus-5-5` |
| Runner | no `ANTHROPIC_API_KEY` in the environment → headless Claude Code subagents: `claude -p --system-prompt "" --tools "" --setting-sources "" --strict-mcp-config --disable-slash-commands --no-session-persistence --effort low`, `MAX_THINKING_TOKENS=0`, `DISABLE_PROMPT_CACHING=1` (`tools/claude_cli.py`) |
| Batching / seeds | ≤10 questions per call from one dataset; 3 seeds, question order and batch composition reshuffled per seed; identical batches for every format and model (paired; asserted by `tools/check_manifest.py`) |
| Calls | 1,593 + 135 accuracy calls (0 failures) → 13,176 graded answers; 720 generation calls; 496 token-count calls |
| Grading | upstream `compareAnswers` unchanged (primary); pre-registered lenient normaliser (sensitivity / failure classification) |
| Losslessness | every EDN encoding round-trips through **edn-data** (vitest) and **edn_format** (pytest), with key order included. TOON round-trips through upstream `decode`. |
| Spend (CLI-reported list price) | Logged: **$62.23** (see breakdown below), plus < $2 of unlogged manual smoke tests. Budget: $80 (raised from $40 during the run). |

Spend breakdown (logged):

| item | cost |
|---|---|
| Pre-registered accuracy runs | $37.16 (Haiku 4.52, Sonnet 9.58, Opus 23.07) |
| Claude token counting | $15.14 |
| Generation | $2.78 |
| Layout re-run | $2.89 |
| Excluded pilots | $4.25 |

Encoding example (the same employee in each format):

```
json-compact  {"employees":[{"id":1,"name":"Darla Mertz MD","email":"vida80@yahoo.com","department":"Engineering","salary":146288,"yearsExperience":24,"active":true},…
toon          employees[100]{id,name,email,department,salary,yearsExperience,active}:
                1,Darla Mertz MD,vida80@yahoo.com,Engineering,146288,24,true
edn-maps      {:employees [{:id 1 :name "Darla Mertz MD" :email "vida80@yahoo.com" :department "Engineering" :salary 146288 :yearsExperience 24 :active true} …
edn-table     {:employees {:cols [:id :name :email :department :salary :yearsExperience :active] :rows [[1 "Darla Mertz MD" "vida80@yahoo.com" "Engineering" 146288 24 true]
              [2 "Mr. Erick Renner DDS" …]
```

## 3. Token counts

Each tokenizer is reported separately and never averaged. Data blocks only;
primer lines are listed separately below.
- **o200k:** tiktoken, fed an o200k_base file rebuilt from `gpt-tokenizer`'s
  ranks. tiktoken verified its sha256 `446a9538…`, and the counts are identical
  to `gpt-tokenizer` on all 135 texts.
- **Qwen3:** HF `tokenizers` with Qwen3 `tokenizer.json` (sha256
  `aeb13307…`, from npm `@lenml/tokenizer-qwen3@3.7.2`, because huggingface.co
  is blocked here).
- **Claude:** the **token-counting API was skipped** because there's no API
  key. Counts come from CLI `usage` deltas instead: input(`prefix\n`+data) −
  input(`prefix`), with the baseline constant over 3 repeats, accurate to ±1
  token.
- **Sonnet 5 = Opus 5.5:** identical counts on all 60 accuracy-dataset
  measurements (one "Claude 5" tokenizer).

<!-- BEGIN:TOKENS_TABLES -->
#### tokens datasets — o200k

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 14,211 | 9,115 | 14,940 | 9,120 | 8,383 | 22,245 | 17,858 | 26,616 | +5.1% | +0.1% |
| github | flat | 11,640 | 8,937 | 12,332 | 9,465 | 8,711 | 15,337 | 13,337 | 17,294 | +5.9% | +5.9% |
| tabular | flat | 79,057 | 49,978 | 85,056 | 55,075 | 47,153 | 127,061 | 100,054 | 146,605 | +7.6% | +10.2% |
| event-logs | mixed | 128,529 | 154,084 | 134,528 | 134,528 | – | 181,201 | 155,397 | 205,859 | +4.7% | -12.7% |
| keyed | mixed | 15,635 | 10,503 | 15,635 | 15,635 | – | 23,141 | 17,905 | 28,655 | +0.0% | +48.9% |
| nested | mixed | 68,944 | 72,832 | 74,441 | 71,301 | – | 108,611 | 84,701 | 122,119 | +8.0% | -2.1% |
| nested-config | mixed | 552 | 589 | 586 | 578 | – | 905 | 662 | 997 | +6.2% | -1.9% |
| nested-group | mixed | 46,791 | 26,726 | 50,799 | 50,799 | – | 79,779 | 55,475 | 90,306 | +8.6% | +90.1% |
| **total flat** | flat | **104,908** | **68,030** | **112,328** | **73,660** | **64,247** | **164,643** | **131,249** | **190,515** | **+7.1%** | **+8.3%** |
| **total mixed** | mixed | **260,451** | **264,734** | **275,989** | **272,841** | – | **393,637** | **314,140** | **447,936** | **+6.0%** | **+3.1%** |

#### tokens datasets — qwen3

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 18,881 | 13,788 | 19,611 | 13,791 | 13,054 | 26,916 | 22,529 | 31,287 | +3.9% | +0.0% |
| github | flat | 15,004 | 12,502 | 15,697 | 13,028 | 12,274 | 18,702 | 16,713 | 20,436 | +4.6% | +4.2% |
| tabular | flat | 93,095 | 63,797 | 99,095 | 69,114 | 60,970 | 141,100 | 114,122 | 160,021 | +6.4% | +8.3% |
| event-logs | mixed | 154,156 | 181,714 | 162,156 | 162,156 | – | 208,829 | 183,025 | 229,487 | +5.2% | -10.8% |
| keyed | mixed | 18,028 | 13,862 | 18,527 | 18,527 | – | 26,033 | 20,773 | 31,834 | +2.8% | +33.7% |
| nested | mixed | 82,736 | 87,511 | 89,234 | 86,094 | – | 123,404 | 98,878 | 136,016 | +7.9% | -1.6% |
| nested-config | mixed | 597 | 643 | 639 | 631 | – | 960 | 719 | 1,042 | +7.0% | -1.9% |
| nested-group | mixed | 49,065 | 29,773 | 54,066 | 54,066 | – | 83,046 | 58,676 | 92,929 | +10.2% | +81.6% |
| **total flat** | flat | **126,980** | **90,087** | **134,403** | **95,933** | **86,298** | **186,718** | **153,364** | **211,744** | **+5.8%** | **+6.5%** |
| **total mixed** | mixed | **304,582** | **313,503** | **324,622** | **321,474** | – | **442,272** | **362,071** | **491,308** | **+6.6%** | **+2.5%** |

#### tokens datasets — claude-haiku-4.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 14,212 | 8,752 | 16,037 | 9,486 | 8,384 | +12.8% | +8.4% |
| github | flat | 12,707 | 9,439 | 13,758 | 10,296 | 9,287 | +8.3% | +9.1% |
| tabular | flat | 95,109 | 59,087 | 105,068 | 69,089 | 56,672 | +10.5% | +16.9% |
| event-logs | mixed | 135,716 | 162,161 | 143,716 | 143,716 | – | +5.9% | -11.4% |
| keyed | mixed | 17,092 | 11,112 | 17,591 | 17,591 | – | +2.9% | +58.3% |
| nested | mixed | 80,500 | 83,037 | 87,988 | 83,643 | – | +9.3% | +0.7% |
| nested-config | mixed | 668 | 698 | 672 | 664 | – | +0.6% | -4.9% |
| nested-group | mixed | 54,818 | 32,796 | 57,777 | 57,777 | – | +5.4% | +76.2% |
| **total flat** | flat | **122,028** | **77,278** | **134,863** | **88,871** | **74,343** | **+10.5%** | **+15.0%** |
| **total mixed** | mixed | **288,794** | **289,804** | **307,744** | **303,391** | – | **+6.6%** | **+4.7%** |

#### tokens datasets — claude-opus-5.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 18,961 | 8,762 | 18,960 | 9,501 | 8,393 | -0.0% | +8.4% |
| github | flat | 16,743 | 11,285 | 16,603 | 12,155 | 11,125 | -0.8% | +7.7% |
| tabular | flat | 131,583 | 77,603 | 129,541 | 87,570 | 75,187 | -1.6% | +12.8% |
| event-logs | mixed | 189,345 | 200,233 | 187,566 | 187,566 | – | -0.9% | -6.3% |
| keyed | mixed | 24,855 | 12,879 | 22,854 | 22,854 | – | -8.1% | +77.5% |
| nested | mixed | 110,271 | 100,077 | 108,261 | 103,801 | – | -1.8% | +3.7% |
| nested-config | mixed | 911 | 866 | 889 | 881 | – | -2.4% | +1.7% |
| nested-group | mixed | 78,741 | 45,769 | 75,723 | 75,723 | – | -3.8% | +65.4% |
| **total flat** | flat | **167,287** | **97,650** | **165,104** | **109,226** | **94,705** | **-1.3%** | **+11.9%** |
| **total mixed** | mixed | **404,123** | **359,824** | **395,293** | **390,825** | – | **-2.2%** | **+8.6%** |

<details><summary>Accuracy-dataset sizes (the data blocks actually sent; per tokenizer)</summary>

#### accuracy datasets — o200k

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 2,341 | 1,515 | 2,460 | 1,520 | 1,393 | – | – | – | +5.1% | +0.3% |
| github | flat | 11,640 | 8,937 | 12,332 | 9,465 | 8,711 | – | – | – | +5.9% | +5.9% |
| structural-validation-control | flat | 762 | 486 | 821 | 540 | 458 | – | – | – | +7.7% | +11.1% |
| structural-validation-extra-rows | flat | 883 | 564 | 951 | 625 | 532 | – | – | – | +7.7% | +10.8% |
| structural-validation-missing-fields | flat | 722 | 455 | 777 | 504 | 427 | – | – | – | +7.6% | +10.8% |
| structural-validation-truncated | flat | 650 | 418 | 700 | 464 | 393 | – | – | – | +7.7% | +11.0% |
| structural-validation-width-mismatch | flat | 757 | 483 | 816 | 537 | 455 | – | – | – | +7.8% | +11.2% |
| tabular | flat | 3,909 | 2,457 | 4,208 | 2,727 | 2,321 | – | – | – | +7.6% | +11.0% |
| event-logs | mixed | 4,783 | 5,734 | 5,007 | 5,007 | – | – | – | – | +4.7% | -12.7% |
| keyed | mixed | 1,254 | 851 | 1,254 | 1,254 | – | – | – | – | +0.0% | +47.4% |
| nested | mixed | 6,865 | 7,264 | 7,414 | 7,104 | – | – | – | – | +8.0% | -2.2% |
| nested-config | mixed | 552 | 589 | 586 | 578 | – | – | – | – | +6.2% | -1.9% |
| nested-group | mixed | 2,347 | 1,364 | 2,547 | 2,547 | – | – | – | – | +8.5% | +86.7% |
| **total flat** | flat | **21,664** | **15,315** | **23,065** | **16,382** | **14,690** | – | – | – | **+6.5%** | **+7.0%** |
| **total mixed** | mixed | **15,801** | **15,802** | **16,808** | **16,490** | – | – | – | – | **+6.4%** | **+4.4%** |

#### accuracy datasets — qwen3

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 3,103 | 2,279 | 3,223 | 2,283 | 2,156 | – | – | – | +3.9% | +0.2% |
| github | flat | 15,004 | 12,502 | 15,697 | 13,028 | 12,274 | – | – | – | +4.6% | +4.2% |
| structural-validation-control | flat | 874 | 594 | 934 | 653 | 565 | – | – | – | +6.9% | +9.9% |
| structural-validation-extra-rows | flat | 1,013 | 690 | 1,082 | 756 | 657 | – | – | – | +6.8% | +9.6% |
| structural-validation-missing-fields | flat | 834 | 563 | 890 | 617 | 534 | – | – | – | +6.7% | +9.6% |
| structural-validation-truncated | flat | 744 | 508 | 795 | 559 | 482 | – | – | – | +6.9% | +10.0% |
| structural-validation-width-mismatch | flat | 865 | 587 | 925 | 646 | 558 | – | – | – | +6.9% | +10.1% |
| tabular | flat | 4,499 | 3,039 | 4,799 | 3,318 | 2,901 | – | – | – | +6.7% | +9.2% |
| event-logs | mixed | 5,746 | 6,774 | 6,046 | 6,046 | – | – | – | – | +5.2% | -10.7% |
| keyed | mixed | 1,403 | 1,075 | 1,442 | 1,442 | – | – | – | – | +2.8% | +34.1% |
| nested | mixed | 8,215 | 8,700 | 8,865 | 8,555 | – | – | – | – | +7.9% | -1.7% |
| nested-config | mixed | 597 | 643 | 639 | 631 | – | – | – | – | +7.0% | -1.9% |
| nested-group | mixed | 2,459 | 1,517 | 2,710 | 2,710 | – | – | – | – | +10.2% | +78.6% |
| **total flat** | flat | **26,936** | **20,762** | **28,345** | **21,860** | **20,127** | – | – | – | **+5.2%** | **+5.3%** |
| **total mixed** | mixed | **18,420** | **18,709** | **19,702** | **19,384** | – | – | – | – | **+7.0%** | **+3.6%** |

#### accuracy datasets — claude-haiku-4.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 2,342 | 1,457 | 2,642 | 1,581 | 1,394 | +12.8% | +8.5% |
| github | flat | 12,707 | 9,439 | 13,758 | 10,296 | 9,287 | +8.3% | +9.1% |
| structural-validation-control | flat | 914 | 572 | 1,014 | 675 | 546 | +10.9% | +18.0% |
| structural-validation-extra-rows | flat | 1,056 | 660 | 1,171 | 778 | 630 | +10.9% | +17.9% |
| structural-validation-missing-fields | flat | 869 | 535 | 965 | 634 | 509 | +11.0% | +18.5% |
| structural-validation-truncated | flat | 780 | 492 | 865 | 580 | 469 | +10.9% | +17.9% |
| structural-validation-width-mismatch | flat | 909 | 569 | 1,008 | 672 | 543 | +10.9% | +18.1% |
| tabular | flat | 4,729 | 2,947 | 5,229 | 3,450 | 2,827 | +10.6% | +17.1% |
| event-logs | mixed | 5,042 | 6,026 | 5,342 | 5,342 | – | +6.0% | -11.4% |
| keyed | mixed | 1,371 | 905 | 1,410 | 1,410 | – | +2.8% | +55.8% |
| nested | mixed | 8,032 | 8,291 | 8,780 | 8,350 | – | +9.3% | +0.7% |
| nested-config | mixed | 668 | 698 | 672 | 664 | – | +0.6% | -4.9% |
| nested-group | mixed | 2,751 | 1,666 | 2,898 | 2,898 | – | +5.3% | +73.9% |
| **total flat** | flat | **24,306** | **16,671** | **26,652** | **18,666** | **16,205** | **+9.7%** | **+12.0%** |
| **total mixed** | mixed | **17,864** | **17,586** | **19,102** | **18,664** | – | **+6.9%** | **+6.1%** |

#### accuracy datasets — claude-sonnet-5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 3,126 | 1,467 | 3,125 | 1,596 | 1,403 | -0.0% | +8.8% |
| github | flat | 16,743 | 11,285 | 16,603 | 12,155 | 11,125 | -0.8% | +7.7% |
| structural-validation-control | flat | 1,280 | 759 | 1,259 | 868 | 732 | -1.6% | +14.4% |
| structural-validation-extra-rows | flat | 1,477 | 875 | 1,453 | 999 | 844 | -1.6% | +14.2% |
| structural-validation-missing-fields | flat | 1,211 | 702 | 1,190 | 807 | 675 | -1.7% | +15.0% |
| structural-validation-truncated | flat | 1,096 | 656 | 1,078 | 750 | 632 | -1.6% | +14.3% |
| structural-validation-width-mismatch | flat | 1,273 | 756 | 1,252 | 865 | 729 | -1.6% | +14.4% |
| tabular | flat | 6,541 | 3,860 | 6,440 | 4,369 | 3,739 | -1.5% | +13.2% |
| event-logs | mixed | 7,037 | 7,442 | 6,972 | 6,972 | – | -0.9% | -6.3% |
| keyed | mixed | 1,993 | 1,051 | 1,832 | 1,832 | – | -8.1% | +74.3% |
| nested | mixed | 10,987 | 9,975 | 10,785 | 10,345 | – | -1.8% | +3.7% |
| nested-config | mixed | 911 | 866 | 889 | 881 | – | -2.4% | +1.7% |
| nested-group | mixed | 3,976 | 2,344 | 3,822 | 3,822 | – | -3.9% | +63.1% |
| **total flat** | flat | **32,747** | **20,360** | **32,400** | **22,409** | **19,879** | **-1.1%** | **+10.1%** |
| **total mixed** | mixed | **24,904** | **21,678** | **24,300** | **23,852** | – | **-2.4%** | **+10.0%** |

#### accuracy datasets — claude-opus-5.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 3,126 | 1,467 | 3,125 | 1,596 | 1,403 | -0.0% | +8.8% |
| github | flat | 16,743 | 11,285 | 16,603 | 12,155 | 11,125 | -0.8% | +7.7% |
| structural-validation-control | flat | 1,280 | 759 | 1,259 | 868 | 732 | -1.6% | +14.4% |
| structural-validation-extra-rows | flat | 1,477 | 875 | 1,453 | 999 | 844 | -1.6% | +14.2% |
| structural-validation-missing-fields | flat | 1,211 | 702 | 1,190 | 807 | 675 | -1.7% | +15.0% |
| structural-validation-truncated | flat | 1,096 | 656 | 1,078 | 750 | 632 | -1.6% | +14.3% |
| structural-validation-width-mismatch | flat | 1,273 | 756 | 1,252 | 865 | 729 | -1.6% | +14.4% |
| tabular | flat | 6,541 | 3,860 | 6,440 | 4,369 | 3,739 | -1.5% | +13.2% |
| event-logs | mixed | 7,037 | 7,442 | 6,972 | 6,972 | – | -0.9% | -6.3% |
| keyed | mixed | 1,993 | 1,051 | 1,832 | 1,832 | – | -8.1% | +74.3% |
| nested | mixed | 10,987 | 9,975 | 10,785 | 10,345 | – | -1.8% | +3.7% |
| nested-config | mixed | 911 | 866 | 889 | 881 | – | -2.4% | +1.7% |
| nested-group | mixed | 3,976 | 2,344 | 3,822 | 3,822 | – | -3.9% | +63.1% |
| **total flat** | flat | **32,747** | **20,360** | **32,400** | **22,409** | **19,879** | **-1.1%** | **+10.1%** |
| **total mixed** | mixed | **24,904** | **21,678** | **24,300** | **23,852** | – | **-2.4%** | **+10.0%** |

</details>

#### Primer lines (tokens, prepended to every call)

| format | o200k | qwen3 | claude-haiku-4.5 | claude-sonnet-5 | claude-opus-5.5 |
|---|---|---|---|---|---|
| json-compact | 10 | 10 | 13 | 22 | 22 |
| toon | 80 | 81 | 96 | 124 | 124 |
| csv | 15 | 15 | 17 | 23 | 23 |
| edn-maps | 29 | 28 | 32 | 44 | 44 |
| edn-table | 29 | 28 | 32 | 44 | 44 |
| edn-table-primer | 144 | 143 | 159 | 206 | 206 |
<!-- END:TOKENS_TABLES -->

**Whitespace confound check.**
- The two layout variants, EDN-table with all rows on one line and EDN-maps
  with one top-level element per line, gave token counts *identical* to the
  layouts used, on every dataset (o200k and Qwen3).
- The texts really differ: for example, event logs are 1 line vs 75 lines.
  Newline and space are each one token here.

**Why EDN-maps loses to JSON on three of four tokenizers** (o200k splits; Qwen3
splits identically, shown by `tools/tok.py`):

```
{"id":1,"name":"Darla Mertz","department":"Sales","active":true}   20 tokens
  {" id ": 1 ," name ":" D arla  M ertz "," department ":" Sales "," active ": true }
{:id 1 :name "Darla Mertz" :department "Sales" :active true}        21 tokens
  {: id ␠ 1 ␠: name ␠" D arla  M ertz " ␠: department ␠" Sales " ␠: active ␠true }
```

- **JSON:** runs of closing quote, separator and opening quote (`","`,
  `":"`) are single merged tokens.
- **EDN:** needs `"` plus ` :` or ` "`, and a space before bare numbers.
  Dropping the quotes around keys saves nothing, because `{"` and `,"` were
  already one token each.
- **Claude 5 tokenizer:** the merge pattern must differ, since EDN-maps is
  0–8% smaller there. Its splits are not observable through the CLI, so this
  part is inferred, not shown.

## 4. Accuracy

- **Unit:** the question, scored as mean correctness over 3 seeds (and over
  models for pooled levels).
- **Levels:** "pooled" = all three models; "pooled-nr" = Haiku + Sonnet, the
  models that ran without reasoning. Opus 5.5's hidden thinking could not be
  switched off (D5), which puts it in a different regime near the ceiling.
- **Columns:** `csv` covers the 109 flat questions only and `edn-table-lines`
  the 135 mixed questions only. Compare them via the paired tables, not across
  columns.
- **CIs:**
  - "q-CI" is the pre-registered percentile bootstrap over questions
    (10,000 resamples).
  - "ds-CI" is a post-review two-stage bootstrap over datasets and then
    questions. It is more honest, because effects vary by dataset.

<!-- BEGIN:ACCURACY_TABLES -->
**All 244 questions (CSV: 109 flat questions)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 61.1 [55.2, 66.9] | 64.6 [58.9, 70.4] | 60.8 [54.8, 66.8] | 62.2 [56.3, 67.9] | 61.9 [56.1, 67.8] | 51.4 [42.5, 59.9] | 73.1 [66.2, 79.8] |
| sonnet | 64.3 [58.6, 70.1] | 67.3 [61.9, 72.8] | 64.8 [59.0, 70.2] | 64.6 [58.9, 70.4] | 64.8 [59.0, 70.2] | 50.5 [41.3, 59.6] | 76.5 [69.6, 83.0] |
| opus | 97.4 [95.4, 99.0] | 98.4 [96.7, 99.6] | 97.5 [95.5, 99.2] | 97.0 [95.0, 98.8] | 97.0 [95.0, 98.8] | 94.5 [90.2, 97.9] | 100.0 [100.0, 100.0] |
| pooled | 74.3 [70.4, 78.2] | 76.8 [72.9, 80.5] | 74.4 [70.5, 78.2] | 74.6 [70.6, 78.4] | 74.5 [70.6, 78.4] | 65.4 [59.1, 72.0] | 83.2 [78.8, 87.4] |
| pooled-nr | 62.7 [57.1, 68.4] | 66.0 [60.4, 71.4] | 62.8 [57.0, 68.2] | 63.4 [57.9, 68.9] | 63.3 [57.6, 68.8] | 50.9 [42.0, 59.5] | 74.8 [67.9, 81.2] |

<details><summary>Flat-only track (109)</summary>


**Flat-only track (109)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 47.4 [38.5, 56.6] | 51.1 [42.2, 60.2] | 46.8 [37.6, 55.7] | 48.9 [40.1, 57.8] | 49.2 [40.1, 58.1] | 51.4 [42.5, 59.9] | – |
| sonnet | 48.6 [39.5, 57.8] | 53.5 [45.0, 62.4] | 49.9 [41.3, 58.4] | 48.9 [40.1, 57.8] | 48.9 [40.1, 57.8] | 50.5 [41.0, 59.6] | – |
| opus | 94.2 [89.9, 97.9] | 96.3 [93.0, 99.1] | 94.5 [90.2, 98.2] | 93.6 [89.3, 97.2] | 94.2 [89.9, 97.9] | 94.5 [90.2, 97.9] | – |
| pooled | 63.4 [57.0, 69.8] | 67.0 [60.9, 73.1] | 63.7 [57.3, 70.0] | 63.8 [57.5, 70.0] | 64.1 [57.6, 70.3] | 65.4 [59.1, 71.8] | – |
| pooled-nr | 48.0 [39.3, 56.9] | 52.3 [43.6, 60.9] | 48.3 [39.8, 56.9] | 48.9 [40.4, 57.5] | 49.1 [40.4, 58.0] | 50.9 [42.2, 59.9] | – |

</details>

<details><summary>Mixed-structure track (135)</summary>


**Mixed-structure track (135)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 72.1 [64.9, 79.0] | 75.6 [68.4, 82.2] | 72.1 [64.7, 79.3] | 72.8 [65.9, 79.5] | 72.1 [64.9, 79.0] | – | 73.1 [66.2, 79.8] |
| sonnet | 77.0 [70.6, 83.2] | 78.5 [71.9, 84.7] | 76.8 [69.9, 83.5] | 77.3 [70.6, 83.5] | 77.5 [70.9, 84.0] | – | 76.5 [69.4, 83.2] |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.8 [99.3, 100.0] | 99.3 [98.0, 100.0] | – | 100.0 [100.0, 100.0] |
| pooled | 83.0 [78.6, 87.3] | 84.7 [80.2, 88.9] | 83.0 [78.4, 87.3] | 83.3 [78.8, 87.6] | 83.0 [78.3, 87.3] | – | 83.2 [78.6, 87.5] |
| pooled-nr | 74.6 [67.7, 81.0] | 77.0 [70.4, 83.2] | 74.4 [67.5, 81.0] | 75.1 [68.5, 81.5] | 74.8 [68.2, 81.2] | – | 74.8 [68.3, 81.1] |

</details>

<details><summary>Uniform tables (104)</summary>


**Uniform tables (104)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 46.8 [37.5, 56.1] | 48.7 [39.7, 58.0] | 47.1 [37.8, 56.1] | 48.4 [39.4, 57.4] | 48.7 [39.4, 58.0] | 50.0 [41.3, 59.0] | – |
| sonnet | 48.1 [38.8, 57.4] | 51.3 [42.3, 60.3] | 50.3 [41.3, 59.3] | 48.4 [39.4, 57.7] | 48.4 [39.4, 57.7] | 49.0 [39.7, 58.3] | – |
| opus | 95.8 [92.3, 98.7] | 96.2 [92.6, 99.0] | 96.2 [92.6, 99.0] | 95.2 [91.3, 98.4] | 95.8 [92.0, 98.7] | 95.2 [91.3, 98.4] | – |
| pooled | 63.6 [57.2, 69.9] | 65.4 [59.2, 71.5] | 64.5 [58.2, 70.7] | 64.0 [57.7, 70.4] | 64.3 [58.0, 70.7] | 64.7 [58.2, 71.3] | – |
| pooled-nr | 47.4 [38.8, 56.2] | 50.0 [41.3, 59.0] | 48.7 [39.9, 57.2] | 48.4 [39.4, 57.5] | 48.6 [39.6, 57.5] | 49.5 [40.4, 58.5] | – |

</details>

<details><summary>Nested config (29)</summary>


**Nested config (29)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 89.7 [80.5, 96.5] | 92.0 [85.1, 97.7] | 93.1 [83.9, 100.0] | 93.1 [83.9, 98.9] | 92.0 [82.8, 98.9] | – | 90.8 [81.6, 97.7] |
| sonnet | 98.9 [96.5, 100.0] | 98.9 [96.5, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.7 [93.1, 100.0] | – | 98.9 [96.5, 100.0] |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | – | 100.0 [100.0, 100.0] |
| pooled | 96.2 [92.3, 98.9] | 96.9 [93.9, 99.2] | 97.7 [94.6, 100.0] | 97.7 [95.0, 99.6] | 96.5 [92.3, 99.6] | – | 96.5 [92.7, 99.2] |
| pooled-nr | 94.2 [88.5, 98.3] | 95.4 [90.8, 98.9] | 96.5 [92.0, 100.0] | 96.5 [92.5, 99.4] | 94.8 [87.9, 99.4] | – | 94.8 [89.1, 98.9] |

</details>

<details><summary>Mixed shapes (106)</summary>


**Mixed shapes (106)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 67.3 [58.5, 75.8] | 71.1 [62.3, 79.2] | 66.3 [57.6, 74.8] | 67.3 [59.1, 75.5] | 66.7 [58.2, 74.8] | – | 68.2 [60.1, 76.4] |
| sonnet | 71.1 [63.2, 78.6] | 73.0 [64.5, 80.8] | 70.4 [62.0, 78.3] | 71.1 [62.9, 78.9] | 72.0 [64.1, 79.6] | – | 70.4 [62.0, 78.3] |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.7 [99.1, 100.0] | 99.1 [97.5, 100.0] | – | 100.0 [100.0, 100.0] |
| pooled | 79.5 [74.1, 84.6] | 81.3 [76.0, 86.4] | 78.9 [73.3, 84.2] | 79.3 [74.0, 84.6] | 79.2 [73.7, 84.4] | – | 79.6 [74.2, 84.8] |
| pooled-nr | 69.2 [61.5, 77.0] | 72.0 [63.8, 79.6] | 68.4 [59.9, 76.4] | 69.2 [61.5, 77.0] | 69.3 [61.3, 76.9] | – | 69.3 [61.3, 77.0] |

</details>

<details><summary>Structural validation (5)</summary>


**Structural validation (5)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| sonnet | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| opus | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| pooled | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 46.7 [6.7, 86.7] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| pooled-nr | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |

</details>

**All except structural validation (239)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 61.1 [55.4, 67.0] | 63.9 [57.7, 69.7] | 61.2 [55.2, 67.1] | 62.2 [56.4, 68.1] | 61.9 [56.1, 67.8] | 50.0 [41.0, 58.7] | 73.1 [66.2, 79.5] |
| sonnet | 64.4 [58.7, 70.0] | 66.7 [61.0, 72.1] | 65.3 [59.6, 70.9] | 64.7 [58.9, 70.4] | 64.8 [59.0, 70.4] | 49.0 [39.7, 58.3] | 76.5 [69.6, 83.2] |
| opus | 98.2 [96.5, 99.4] | 98.3 [96.7, 99.6] | 98.3 [96.7, 99.6] | 97.8 [96.1, 99.2] | 97.8 [96.0, 99.2] | 95.2 [91.3, 98.4] | 100.0 [100.0, 100.0] |
| pooled | 74.6 [70.5, 78.4] | 76.3 [72.4, 80.0] | 74.9 [70.9, 78.8] | 74.9 [70.9, 78.7] | 74.9 [70.9, 78.8] | 64.7 [58.1, 71.2] | 83.2 [78.8, 87.5] |
| pooled-nr | 62.8 [57.1, 68.3] | 65.3 [59.6, 70.9] | 63.2 [57.5, 68.8] | 63.5 [57.8, 69.1] | 63.4 [57.8, 68.8] | 49.5 [40.2, 58.5] | 74.8 [68.0, 81.2] |

<details><summary>Informative questions only (correctness varies across formats × seeds for that model level)</summary>


**Informative questions only (correctness varies across formats × seeds for that model level)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 31.2 [22.4, 40.6] | 44.8 [34.4, 55.2] | 30.2 [21.3, 39.6] | 35.4 [27.1, 43.8] | 34.4 [25.5, 43.8] | 41.9 [28.0, 57.0] | 37.4 [26.3, 48.5] |
| sonnet | 36.8 [27.9, 45.6] | 47.5 [38.2, 56.9] | 38.2 [29.4, 47.1] | 37.8 [28.4, 47.1] | 38.2 [28.9, 48.0] | 39.5 [25.4, 54.4] | 41.1 [26.7, 55.6] |
| opus | 79.2 [62.5, 93.8] | 93.8 [87.5, 100.0] | 81.2 [62.5, 95.8] | 72.9 [56.2, 87.5] | 72.9 [54.2, 87.5] | 90.5 [83.3, 97.6] | 100.0 [100.0, 100.0] |
| pooled | 49.8 [45.5, 54.3] | 54.9 [50.1, 59.8] | 50.0 [45.6, 54.4] | 50.4 [45.9, 55.0] | 50.3 [45.9, 55.0] | 49.9 [43.8, 56.5] | 56.4 [50.0, 62.8] |
| pooled-nr | 33.7 [26.5, 41.5] | 42.4 [34.4, 50.7] | 33.9 [26.6, 41.5] | 35.5 [27.9, 43.1] | 35.3 [27.9, 43.1] | 37.7 [25.7, 50.0] | 39.1 [29.0, 49.6] |

</details>

**Paired comparisons — overall-excl-structural** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 239 | +0.1 | [-1.9, +2.2] | [-2.6, +2.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 239 | -1.7 | [-3.9, +0.6] | [-6.3, +1.7] | 0.227 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table-primer vs edn-table | 239 | -0.3 | [-1.8, +1.3] | [-1.9, +1.4] | 0.375 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 239 | -1.9 | [-4.3, +0.3] | [-6.6, +1.5] | 0.057 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table-primer vs json-compact | 239 | +0.8 | [-1.1, +2.9] | [-2.0, +4.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 239 | -2.6 | [-5.2, -0.3] | [-7.5, +0.7] | 0.012 |  | B better | no detectable difference |
| haiku | toon vs json-compact | 239 | +2.8 | [+0.6, +5.3] | [-0.1, +6.8] | 0.012 |  | A better | no detectable difference |
| sonnet | edn-maps vs json-compact | 239 | +0.8 | [-1.3, +2.9] | [-2.1, +3.7] | 0.267 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 239 | -1.9 | [-4.9, +0.8] | [-5.6, +1.4] | 0.167 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 239 | +0.1 | [-1.8, +2.1] | [-2.5, +2.9] | 0.227 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 239 | -1.8 | [-4.3, +0.6] | [-5.1, +0.9] | 0.804 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 239 | +0.4 | [-1.9, +2.9] | [-2.9, +3.4] | 0.332 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 239 | -1.4 | [-4.5, +1.5] | [-4.9, +1.6] | 0.839 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | toon vs json-compact | 239 | +2.2 | [-0.4, +5.0] | [-0.6, +5.4] | 0.167 |  | no detectable difference | no detectable difference |
| opus | edn-maps vs json-compact | 239 | +0.1 | [-0.4, +0.7] | [-0.7, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 239 | -0.6 | [-1.5, +0.3] | [-1.6, +0.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 239 | +0.0 | [-0.7, +0.7] | [-0.8, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 239 | -0.6 | [-1.5, +0.3] | [-1.7, +0.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 239 | -0.4 | [-1.4, +0.6] | [-1.6, +0.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 239 | +0.0 | [-0.7, +0.7] | [-0.8, +0.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 239 | +0.1 | [-0.3, +0.7] | [-0.4, +0.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 239 | +0.4 | [-0.6, +1.3] | [-1.1, +1.7] | 0.581 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 239 | -1.4 | [-2.8, -0.1] | [-3.7, +0.5] | 0.064 |  | B better (within ±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 239 | -0.1 | [-0.9, +0.7] | [-1.0, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 239 | -1.4 | [-2.8, -0.2] | [-3.6, +0.3] | 0.115 |  | B better (within ±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 239 | +0.3 | [-0.8, +1.4] | [-1.2, +1.9] | 0.791 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 239 | -1.4 | [-2.8, +0.0] | [-3.7, +0.4] | 0.189 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | toon vs json-compact | 239 | +1.7 | [+0.4, +3.1] | [+0.3, +3.6] | 0.041 |  | A better (within ±5pp) | A better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | 239 | +0.5 | [-1.0, +1.9] | [-1.7, +2.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 239 | -1.8 | [-3.8, +0.1] | [-5.2, +1.0] | 0.031 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 239 | -0.1 | [-1.3, +1.1] | [-1.5, +1.5] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 239 | -1.9 | [-3.8, -0.1] | [-5.0, +0.6] | 0.125 |  | B better (within ±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 239 | +0.6 | [-0.9, +2.1] | [-1.5, +2.8] | 0.125 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 239 | -2.0 | [-4.2, -0.1] | [-5.6, +0.6] | 0.008 |  | B better (within ±5pp) | no detectable difference |
| pooled-nr | toon vs json-compact | 239 | +2.5 | [+0.6, +4.7] | [+0.4, +5.3] | 0.004 |  | A better (within ±5pp) | A better |

**Paired comparisons — overall** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 244 | -0.3 | [-2.5, +1.9] | [-3.5, +2.4] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 244 | -2.5 | [-4.9, -0.0] | [-7.7, +1.0] | 0.092 | 1.0 | B better (within ±5pp) | no detectable difference |
| haiku | edn-table-primer vs edn-table | 244 | -0.3 | [-1.8, +1.1] | [-1.9, +1.4] | 0.375 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 244 | -2.7 | [-5.3, -0.3] | [-8.0, +0.7] | 0.021 | 0.48921 | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 244 | +0.8 | [-1.1, +2.9] | [-1.9, +4.3] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 244 | -3.8 | [-6.6, -1.2] | [-9.7, -0.3] | 0.002 | 0.04392 | B better | B better |
| haiku | toon vs json-compact | 244 | +3.5 | [+1.1, +6.2] | [+0.5, +8.3] | 0.003 |  | A better | A better |
| sonnet | edn-maps vs json-compact | 244 | +0.4 | [-1.8, +2.6] | [-2.9, +3.5] | 0.424 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 244 | -2.7 | [-5.9, +0.3] | [-7.1, +0.7] | 0.078 | 1.0 | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 244 | +0.1 | [-1.8, +2.2] | [-2.5, +3.1] | 0.227 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 244 | -2.6 | [-5.3, +0.0] | [-6.6, +0.3] | 0.481 | 1.0 | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 244 | +0.4 | [-1.9, +2.9] | [-3.0, +3.3] | 0.332 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 244 | -2.6 | [-5.9, +0.5] | [-7.4, +0.6] | 0.442 | 1.0 | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 244 | +3.0 | [+0.1, +6.0] | [+0.1, +6.9] | 0.078 |  | A better | A better |
| opus | edn-maps vs json-compact | 244 | +0.1 | [-0.4, +0.7] | [-0.7, +0.9] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 244 | -1.4 | [-2.9, -0.1] | [-3.7, -0.1] | 0.500 | 1.0 | B better (within ±5pp) | B better (within ±5pp) |
| opus | edn-table-primer vs edn-table | 244 | +0.0 | [-0.7, +0.7] | [-0.8, +0.9] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 244 | -1.4 | [-3.0, +0.0] | [-3.8, +0.0] | 0.250 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 244 | -0.4 | [-1.4, +0.5] | [-1.6, +0.7] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 244 | -0.8 | [-2.3, +0.4] | [-3.1, +0.3] | 0.500 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 244 | +1.0 | [+0.0, +2.3] | [+0.0, +3.1] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 244 | +0.1 | [-1.0, +1.1] | [-1.7, +1.5] | 0.791 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 244 | -2.2 | [-4.0, -0.5] | [-5.3, -0.1] | 0.027 | 0.5852 | B better (within ±5pp) | B better |
| pooled | edn-table-primer vs edn-table | 244 | -0.1 | [-0.9, +0.8] | [-1.0, +0.9] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 244 | -2.2 | [-4.0, -0.6] | [-5.4, -0.3] | 0.052 | 1.0 | B better (within ±5pp) | B better |
| pooled | edn-table-primer vs json-compact | 244 | +0.3 | [-0.8, +1.3] | [-1.2, +1.9] | 0.791 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 244 | -2.4 | [-4.4, -0.6] | [-5.9, -0.4] | 0.064 | 1.0 | B better (within ±5pp) | B better |
| pooled | toon vs json-compact | 244 | +2.5 | [+0.9, +4.3] | [+0.8, +5.3] | 0.017 |  | A better (within ±5pp) | A better |
| pooled-nr | edn-maps vs json-compact | 244 | +0.1 | [-1.6, +1.6] | [-2.6, +2.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 244 | -2.6 | [-4.9, -0.5] | [-6.7, +0.3] | 0.008 |  | B better (within ±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 244 | -0.1 | [-1.2, +1.1] | [-1.5, +1.4] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 244 | -2.7 | [-4.9, -0.6] | [-6.6, -0.1] | 0.031 |  | B better (within ±5pp) | B better |
| pooled-nr | edn-table-primer vs json-compact | 244 | +0.6 | [-0.9, +2.1] | [-1.6, +2.8] | 0.125 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 244 | -3.2 | [-5.7, -0.9] | [-7.9, -0.4] | 0.001 |  | B better | B better |
| pooled-nr | toon vs json-compact | 244 | +3.3 | [+1.1, +5.7] | [+0.9, +6.8] | 0.001 |  | A better | A better |

<details><summary>Paired comparisons — informative</summary>


**Paired comparisons — informative** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 64 | -1.0 | [-9.9, +7.8] | [-12.3, +9.3] | 1.000 |  | no detectable difference | no detectable difference |
| haiku | edn-table vs toon | 64 | -9.4 | [-18.8, -0.5] | [-24.4, +3.6] | 0.092 |  | B better | no detectable difference |
| haiku | edn-table-primer vs edn-table | 64 | -1.0 | [-6.8, +4.7] | [-7.7, +4.9] | 0.375 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs toon | 64 | -10.4 | [-19.8, -1.0] | [-25.3, +2.6] | 0.021 |  | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 64 | +3.1 | [-4.2, +10.9] | [-7.0, +15.6] | 1.000 |  | no detectable difference | no detectable difference |
| haiku | edn-maps vs toon | 64 | -14.6 | [-24.5, -4.7] | [-31.7, -1.5] | 0.002 |  | B better | B better |
| haiku | toon vs json-compact | 64 | +13.5 | [+4.2, +23.4] | [+2.6, +27.1] | 0.003 |  | A better | A better |
| sonnet | edn-maps vs json-compact | 68 | +1.5 | [-6.9, +9.3] | [-10.6, +11.6] | 0.424 |  | no detectable difference | no detectable difference |
| sonnet | edn-table vs toon | 68 | -9.8 | [-20.6, +0.5] | [-23.7, +2.2] | 0.078 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 68 | +0.5 | [-6.4, +7.3] | [-10.6, +9.5] | 0.227 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs toon | 68 | -9.3 | [-18.6, -0.0] | [-25.1, +0.7] | 0.481 |  | B better | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 68 | +1.5 | [-6.9, +10.3] | [-11.1, +11.0] | 0.332 |  | no detectable difference | no detectable difference |
| sonnet | edn-maps vs toon | 68 | -9.3 | [-20.6, +2.0] | [-25.8, +1.9] | 0.442 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 68 | +10.8 | [+1.0, +21.6] | [+0.4, +23.2] | 0.078 |  | A better | A better |
| opus | edn-maps vs json-compact | 16 | +2.1 | [-6.2, +10.4] | [-8.9, +12.5] | 1.000 |  | no detectable difference | no detectable difference |
| opus | edn-table vs toon | 16 | -20.8 | [-39.6, -2.1] | [-54.2, -2.8] | 0.500 |  | B better | B better |
| opus | edn-table-primer vs edn-table | 16 | +0.0 | [-10.4, +10.4] | [-14.3, +10.4] | 1.000 |  | no detectable difference | no detectable difference |
| opus | edn-table-primer vs toon | 16 | -20.8 | [-41.7, -2.1] | [-62.5, -2.4] | 0.250 |  | B better | B better |
| opus | edn-table-primer vs json-compact | 16 | -6.2 | [-20.8, +8.3] | [-25.0, +8.3] | 1.000 |  | no detectable difference | no detectable difference |
| opus | edn-maps vs toon | 16 | -12.5 | [-33.3, +4.2] | [-45.8, +5.1] | 0.500 |  | no detectable difference | no detectable difference |
| opus | toon vs json-compact | 16 | +14.6 | [-0.0, +33.3] | [+0.0, +50.0] | 0.500 |  | no detectable difference | no detectable difference |
| pooled | edn-maps vs json-compact | 119 | +0.2 | [-2.1, +2.3] | [-3.4, +3.2] | 0.791 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 119 | -4.5 | [-8.1, -1.2] | [-10.7, -0.3] | 0.027 |  | B better | B better |
| pooled | edn-table-primer vs edn-table | 119 | -0.1 | [-1.8, +1.6] | [-2.4, +1.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 119 | -4.6 | [-8.3, -1.3] | [-11.5, -0.8] | 0.052 |  | B better | B better |
| pooled | edn-table-primer vs json-compact | 119 | +0.6 | [-1.6, +2.7] | [-2.5, +3.9] | 0.791 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 119 | -5.0 | [-8.9, -1.5] | [-12.3, -0.9] | 0.064 |  | B better | B better |
| pooled | toon vs json-compact | 119 | +5.1 | [+1.9, +8.8] | [+1.7, +11.5] | 0.017 |  | A better | A better |
| pooled-nr | edn-maps vs json-compact | 92 | +0.2 | [-4.2, +4.3] | [-6.9, +5.8] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table vs toon | 92 | -6.9 | [-13.0, -1.5] | [-16.4, +0.5] | 0.008 |  | B better | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 92 | -0.2 | [-3.3, +2.9] | [-4.5, +3.4] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 92 | -7.1 | [-13.1, -1.6] | [-17.0, -0.5] | 0.031 |  | B better | B better |
| pooled-nr | edn-table-primer vs json-compact | 92 | +1.6 | [-2.4, +5.6] | [-4.2, +7.5] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-maps vs toon | 92 | -8.5 | [-15.0, -2.5] | [-19.8, -1.2] | 0.001 |  | B better | B better |
| pooled-nr | toon vs json-compact | 92 | +8.7 | [+3.1, +14.7] | [+2.9, +17.4] | 0.001 |  | A better | A better |

</details>

<details><summary>Paired comparisons — shape:uniform-tables</summary>


**Paired comparisons — shape:uniform-tables** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 104 | +0.3 | [-3.5, +4.5] | [-4.7, +5.3] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table vs toon | 104 | -0.3 | [-3.2, +2.2] | [-3.7, +4.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs edn-table | 104 | +0.3 | [-1.9, +2.6] | [-1.9, +3.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 104 | -0.0 | [-2.9, +2.9] | [-3.7, +4.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs json-compact | 104 | +1.9 | [-1.6, +6.1] | [-3.2, +9.3] | 0.375 |  | no detectable difference | no detectable difference |
| haiku | edn-maps vs toon | 104 | -1.6 | [-4.8, +1.3] | [-6.4, +1.9] | 0.500 |  | equivalent (±5pp) | no detectable difference |
| haiku | toon vs json-compact | 104 | +1.9 | [-1.0, +5.5] | [-1.6, +6.3] | 0.250 |  | no detectable difference | no detectable difference |
| sonnet | edn-maps vs json-compact | 104 | +2.2 | [-1.6, +6.1] | [-3.5, +7.2] | 0.508 |  | no detectable difference | no detectable difference |
| sonnet | edn-table vs toon | 104 | -2.9 | [-7.0, +1.0] | [-8.1, +2.6] | 0.453 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 104 | -0.0 | [-2.6, +2.9] | [-4.1, +4.8] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 104 | -2.9 | [-6.7, +1.0] | [-8.4, +1.3] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 104 | +0.3 | [-4.2, +4.8] | [-6.4, +5.6] | 0.754 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-maps vs toon | 104 | -1.0 | [-6.1, +3.9] | [-6.9, +4.1] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 104 | +3.2 | [-1.3, +7.7] | [-1.4, +7.7] | 0.508 |  | no detectable difference | no detectable difference |
| opus | edn-maps vs json-compact | 104 | +0.3 | [-1.0, +1.6] | [-1.5, +2.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 104 | -1.0 | [-2.9, +1.0] | [-3.1, +1.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 104 | +0.6 | [-0.6, +1.9] | [-0.6, +2.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 104 | -0.3 | [-1.9, +1.3] | [-2.2, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 104 | +0.0 | [-1.9, +1.9] | [-2.0, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 104 | +0.0 | [-1.6, +1.6] | [-1.7, +1.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 104 | +0.3 | [-0.6, +1.3] | [-1.0, +1.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 104 | +1.0 | [-0.8, +2.7] | [-1.8, +3.0] | 0.453 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 104 | -1.4 | [-3.2, +0.4] | [-4.0, +1.8] | 0.344 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 104 | +0.3 | [-1.0, +1.6] | [-1.1, +1.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 104 | -1.1 | [-3.1, +0.8] | [-4.2, +1.8] | 0.388 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 104 | +0.8 | [-1.4, +2.9] | [-2.5, +4.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 104 | -0.9 | [-3.1, +1.3] | [-4.2, +1.4] | 0.774 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | toon vs json-compact | 104 | +1.8 | [-0.1, +3.7] | [-0.0, +3.8] | 0.180 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs json-compact | 104 | +1.3 | [-1.3, +3.7] | [-3.2, +4.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 104 | -1.6 | [-4.2, +0.8] | [-5.1, +2.7] | 0.500 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 104 | +0.2 | [-1.6, +2.1] | [-1.9, +2.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 104 | -1.4 | [-4.2, +1.1] | [-5.6, +2.4] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 104 | +1.1 | [-2.1, +4.2] | [-3.6, +5.9] | 0.219 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-maps vs toon | 104 | -1.3 | [-4.5, +1.8] | [-6.1, +2.2] | 0.125 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | toon vs json-compact | 104 | +2.6 | [-0.2, +5.5] | [-0.2, +5.5] | 0.062 |  | no detectable difference | no detectable difference |

</details>

<details><summary>Paired comparisons — shape:nested-config</summary>


**Paired comparisons — shape:nested-config** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 29 | +3.5 | [+0.0, +6.9] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table vs toon | 29 | +1.1 | [-4.6, +8.1] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table-primer vs edn-table | 29 | -1.1 | [-6.9, +3.5] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table-primer vs toon | 29 | +0.0 | [-5.8, +6.9] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table-primer vs json-compact | 29 | +2.3 | [+0.0, +5.8] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-maps vs toon | 29 | +1.1 | [-4.6, +6.9] | – | 1.000 |  | no detectable difference |  |
| haiku | toon vs json-compact | 29 | +2.3 | [-4.6, +9.2] | – | 1.000 |  | no detectable difference |  |
| sonnet | edn-maps vs json-compact | 29 | +1.1 | [+0.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-table vs toon | 29 | +1.1 | [+0.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-table-primer vs edn-table | 29 | -2.3 | [-6.9, +0.0] | – | 1.000 |  | no detectable difference |  |
| sonnet | edn-table-primer vs toon | 29 | -1.1 | [-3.5, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-table-primer vs json-compact | 29 | -1.1 | [-3.5, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-maps vs toon | 29 | +1.1 | [+0.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | toon vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-maps vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table vs toon | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table-primer vs edn-table | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table-primer vs toon | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table-primer vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-maps vs toon | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | toon vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-maps vs json-compact | 29 | +1.5 | [+0.4, +3.1] | – | 1.000 |  | A better (within ±5pp) |  |
| pooled | edn-table vs toon | 29 | +0.8 | [-0.8, +2.7] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-table-primer vs edn-table | 29 | -1.1 | [-3.8, +0.8] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-table-primer vs toon | 29 | -0.4 | [-3.1, +2.3] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-table-primer vs json-compact | 29 | +0.4 | [-0.8, +1.9] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-maps vs toon | 29 | +0.8 | [-0.8, +2.7] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | toon vs json-compact | 29 | +0.8 | [-1.9, +3.1] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-maps vs json-compact | 29 | +2.3 | [+0.6, +4.6] | – | 1.000 |  | A better (within ±5pp) |  |
| pooled-nr | edn-table vs toon | 29 | +1.1 | [-1.1, +4.0] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-table-primer vs edn-table | 29 | -1.7 | [-5.2, +1.1] | – | 1.000 |  | no detectable difference |  |
| pooled-nr | edn-table-primer vs toon | 29 | -0.6 | [-4.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-table-primer vs json-compact | 29 | +0.6 | [-1.1, +2.3] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-maps vs toon | 29 | +1.1 | [-1.1, +4.0] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | toon vs json-compact | 29 | +1.1 | [-2.3, +4.6] | – | 1.000 |  | equivalent (±5pp) |  |

</details>

<details><summary>Paired comparisons — shape:mixed</summary>


**Paired comparisons — shape:mixed** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 106 | -0.9 | [-3.8, +1.6] | [-4.7, +1.4] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 106 | -3.8 | [-7.9, -0.3] | [-12.5, +1.7] | 0.016 |  | B better | no detectable difference |
| haiku | edn-table-primer vs edn-table | 106 | -0.6 | [-2.8, +1.6] | [-2.8, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 106 | -4.4 | [-8.5, -0.9] | [-12.8, +0.9] | 0.008 |  | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 106 | -0.6 | [-3.1, +1.9] | [-3.7, +1.6] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 106 | -4.7 | [-9.1, -0.9] | [-13.8, +0.9] | 0.016 |  | B better | no detectable difference |
| haiku | toon vs json-compact | 106 | +3.8 | [+0.3, +7.9] | [-0.9, +11.7] | 0.031 |  | A better | no detectable difference |
| haiku | edn-table-lines vs edn-table | 106 | +0.9 | [-1.6, +3.5] | [-1.9, +4.2] | 0.375 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-lines vs toon | 106 | -2.8 | [-7.2, +0.9] | [-10.6, +2.4] | 0.289 |  | no detectable difference | no detectable difference |
| haiku | edn-table-lines vs json-compact | 106 | +0.9 | [-1.9, +4.1] | [-2.0, +4.0] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs json-compact | 106 | -0.6 | [-3.5, +2.2] | [-3.7, +2.4] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 106 | -1.9 | [-7.2, +3.1] | [-8.0, +3.1] | 0.388 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 106 | +0.9 | [-2.2, +4.4] | [-2.9, +4.8] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 106 | -0.9 | [-5.0, +2.8] | [-5.7, +3.1] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 106 | +0.9 | [-2.2, +4.1] | [-2.5, +4.6] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 106 | -2.5 | [-7.2, +1.9] | [-7.5, +1.8] | 0.754 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 106 | +1.9 | [-2.2, +6.6] | [-2.2, +7.0] | 0.344 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs edn-table | 106 | -0.6 | [-3.8, +2.8] | [-3.8, +2.8] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-lines vs toon | 106 | -2.5 | [-6.9, +1.6] | [-7.5, +1.5] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs json-compact | 106 | -0.6 | [-4.1, +2.8] | [-4.5, +3.1] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 106 | -0.3 | [-0.9, +0.0] | [-1.2, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 106 | -0.6 | [-1.6, +0.0] | [-1.7, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 106 | -0.9 | [-2.5, +0.0] | [-2.6, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 106 | -0.9 | [-2.5, +0.0] | [-2.6, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs edn-table | 106 | +0.3 | [+0.0, +0.9] | [+0.0, +1.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs toon | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs json-compact | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 106 | -0.5 | [-1.8, +0.8] | [-2.0, +0.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 106 | -2.0 | [-4.6, +0.3] | [-6.2, +0.7] | 0.180 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table-primer vs edn-table | 106 | -0.1 | [-1.4, +1.1] | [-1.5, +1.2] | 0.688 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 106 | -2.1 | [-4.4, -0.0] | [-5.8, +0.2] | 0.453 |  | B better (within ±5pp) | no detectable difference |
| pooled | edn-table-primer vs json-compact | 106 | -0.2 | [-1.3, +0.9] | [-1.4, +0.9] | 0.727 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 106 | -2.4 | [-4.8, -0.4] | [-6.3, +0.0] | 0.180 |  | B better (within ±5pp) | no detectable difference |
| pooled | toon vs json-compact | 106 | +1.9 | [-0.3, +4.3] | [-0.4, +5.7] | 0.227 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table-lines vs edn-table | 106 | +0.2 | [-1.1, +1.5] | [-1.3, +1.6] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs toon | 106 | -1.8 | [-4.1, +0.2] | [-5.6, +0.6] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table-lines vs json-compact | 106 | +0.1 | [-1.3, +1.6] | [-1.4, +1.6] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs json-compact | 106 | -0.8 | [-2.7, +1.1] | [-3.1, +1.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 106 | -2.8 | [-6.8, +0.6] | [-9.2, +1.3] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 106 | +0.2 | [-1.6, +1.9] | [-1.9, +2.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 106 | -2.7 | [-6.1, +0.3] | [-8.5, +0.9] | 0.250 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 106 | +0.2 | [-1.4, +1.7] | [-1.6, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 106 | -3.6 | [-7.1, -0.6] | [-9.4, +0.1] | 0.125 |  | B better | no detectable difference |
| pooled-nr | toon vs json-compact | 106 | +2.8 | [-0.5, +6.6] | [-0.7, +8.5] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs edn-table | 106 | +0.2 | [-1.9, +2.0] | [-2.1, +2.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-lines vs toon | 106 | -2.7 | [-6.3, +0.3] | [-8.3, +0.9] | 0.375 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs json-compact | 106 | +0.2 | [-1.9, +2.2] | [-2.1, +2.4] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |

</details>

<details><summary>Paired comparisons — track:flat</summary>


**Paired comparisons — track:flat** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 109 | -0.6 | [-4.9, +3.7] | [-9.7, +4.3] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table vs toon | 109 | -2.1 | [-5.8, +1.2] | [-15.0, +2.2] | 1.000 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs edn-table | 109 | +0.3 | [-1.8, +2.5] | [-2.1, +3.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 109 | -1.8 | [-5.8, +1.5] | [-12.6, +2.9] | 0.688 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs json-compact | 109 | +1.8 | [-1.8, +5.8] | [-3.4, +9.2] | 0.375 |  | no detectable difference | no detectable difference |
| haiku | edn-maps vs toon | 109 | -4.3 | [-8.9, -0.3] | [-25.8, -0.2] | 0.062 |  | B better | B better |
| haiku | toon vs json-compact | 109 | +3.7 | [-0.0, +8.0] | [-0.3, +17.1] | 0.062 |  | no detectable difference | no detectable difference |
| sonnet | edn-maps vs json-compact | 109 | +1.2 | [-3.1, +5.2] | [-9.2, +6.2] | 0.754 |  | no detectable difference | no detectable difference |
| sonnet | edn-table vs toon | 109 | -4.6 | [-9.2, -0.3] | [-17.1, +0.8] | 0.180 |  | B better | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 109 | +0.0 | [-2.8, +2.8] | [-4.0, +4.9] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 109 | -4.6 | [-9.2, -0.3] | [-20.0, +0.0] | 0.549 |  | B better | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 109 | +0.3 | [-4.0, +4.6] | [-6.9, +5.6] | 0.754 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-maps vs toon | 109 | -3.7 | [-9.5, +1.8] | [-23.3, +1.7] | 0.629 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 109 | +4.9 | [+0.0, +9.8] | [+0.2, +18.3] | 0.227 |  | no detectable difference | A better |
| opus | edn-maps vs json-compact | 109 | +0.3 | [-0.9, +1.8] | [-1.5, +2.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 109 | -2.8 | [-6.1, +0.0] | [-15.0, +0.0] | 0.500 |  | no detectable difference | no detectable difference |
| opus | edn-table-primer vs edn-table | 109 | +0.6 | [-0.6, +1.8] | [-0.5, +2.4] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 109 | -2.1 | [-5.2, +0.6] | [-12.5, +0.5] | 0.500 |  | no detectable difference | no detectable difference |
| opus | edn-table-primer vs json-compact | 109 | +0.0 | [-1.8, +1.8] | [-2.1, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 109 | -1.8 | [-5.2, +0.9] | [-12.6, +0.7] | 0.500 |  | no detectable difference | no detectable difference |
| opus | toon vs json-compact | 109 | +2.1 | [-0.0, +5.2] | [+0.0, +14.2] | 0.500 |  | no detectable difference | no detectable difference |
| pooled | edn-maps vs json-compact | 109 | +0.3 | [-1.8, +2.1] | [-5.8, +2.5] | 0.727 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table vs toon | 109 | -3.2 | [-6.5, -0.4] | [-15.6, +0.3] | 0.146 |  | B better | no detectable difference |
| pooled | edn-table-primer vs edn-table | 109 | +0.3 | [-0.9, +1.6] | [-1.1, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 109 | -2.9 | [-6.2, -0.0] | [-14.8, +0.5] | 0.180 |  | B better | no detectable difference |
| pooled | edn-table-primer vs json-compact | 109 | +0.7 | [-1.3, +2.8] | [-2.8, +4.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 109 | -3.3 | [-7.0, +0.0] | [-16.7, -0.1] | 0.302 |  | no detectable difference | B better |
| pooled | toon vs json-compact | 109 | +3.6 | [+0.7, +6.8] | [+0.9, +13.9] | 0.065 |  | A better | A better |
| pooled-nr | edn-maps vs json-compact | 109 | +0.3 | [-2.9, +3.1] | [-9.6, +3.7] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table vs toon | 109 | -3.4 | [-7.2, -0.1] | [-14.9, +0.9] | 0.125 |  | B better | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 109 | +0.1 | [-1.5, +2.0] | [-1.9, +2.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 109 | -3.2 | [-6.9, +0.1] | [-15.6, +0.7] | 0.250 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 109 | +1.1 | [-1.8, +4.1] | [-3.9, +6.1] | 0.219 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-maps vs toon | 109 | -4.0 | [-8.6, -0.0] | [-20.0, +0.1] | 0.016 |  | B better | no detectable difference |
| pooled-nr | toon vs json-compact | 109 | +4.3 | [+0.9, +8.1] | [+1.1, +16.7] | 0.016 |  | A better | A better |

</details>

<details><summary>Paired comparisons — track:mixed</summary>


**Paired comparisons — track:mixed** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 135 | +0.0 | [-2.5, +2.2] | [-3.4, +2.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 135 | -2.7 | [-6.2, +0.2] | [-10.1, +2.1] | 0.070 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs edn-table | 135 | -0.7 | [-2.7, +1.2] | [-2.7, +1.3] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 135 | -3.5 | [-6.9, -0.2] | [-10.5, +1.1] | 0.021 |  | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 135 | +0.0 | [-2.2, +2.0] | [-2.7, +2.2] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 135 | -3.5 | [-7.2, -0.2] | [-11.2, +1.5] | 0.039 |  | B better | no detectable difference |
| haiku | toon vs json-compact | 135 | +3.5 | [+0.2, +6.9] | [-0.7, +9.7] | 0.070 |  | A better | no detectable difference |
| haiku | edn-table-lines vs edn-table | 135 | +0.2 | [-2.0, +2.5] | [-2.7, +3.3] | 0.688 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-lines vs toon | 135 | -2.5 | [-6.2, +1.0] | [-8.6, +2.1] | 0.344 |  | no detectable difference | no detectable difference |
| haiku | edn-table-lines vs json-compact | 135 | +1.0 | [-1.2, +3.5] | [-1.4, +3.4] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs json-compact | 135 | -0.2 | [-2.7, +2.0] | [-2.9, +2.2] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 135 | -1.2 | [-5.4, +2.7] | [-6.2, +2.7] | 0.388 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 135 | +0.2 | [-2.5, +3.0] | [-3.1, +3.8] | 0.453 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 135 | -1.0 | [-4.4, +2.2] | [-4.7, +2.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 135 | +0.5 | [-2.0, +3.2] | [-2.3, +3.5] | 0.453 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 135 | -1.7 | [-5.4, +1.7] | [-6.2, +1.7] | 0.754 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 135 | +1.5 | [-2.0, +5.2] | [-1.8, +5.7] | 0.344 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs edn-table | 135 | -0.7 | [-3.2, +2.0] | [-3.3, +2.0] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-lines vs toon | 135 | -2.0 | [-5.2, +1.2] | [-6.1, +1.1] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs json-compact | 135 | -0.5 | [-3.2, +2.2] | [-3.5, +2.4] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 135 | -0.2 | [-0.7, +0.0] | [-1.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 135 | -0.5 | [-1.2, +0.0] | [-1.4, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 135 | -0.7 | [-2.0, +0.0] | [-2.2, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 135 | -0.7 | [-2.0, +0.0] | [-2.2, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs edn-table | 135 | +0.2 | [+0.0, +0.7] | [+0.0, +1.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs toon | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs json-compact | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 135 | -0.1 | [-1.2, +1.0] | [-1.6, +1.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 135 | -1.4 | [-3.5, +0.4] | [-5.0, +0.8] | 0.180 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 135 | -0.3 | [-1.4, +0.7] | [-1.6, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 135 | -1.7 | [-3.7, -0.1] | [-4.8, +0.2] | 0.289 |  | B better (within ±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 135 | -0.1 | [-1.0, +0.8] | [-1.1, +0.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 135 | -1.7 | [-3.6, -0.1] | [-5.2, +0.5] | 0.180 |  | B better (within ±5pp) | no detectable difference |
| pooled | toon vs json-compact | 135 | +1.7 | [-0.2, +3.7] | [-0.3, +4.8] | 0.227 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs edn-table | 135 | -0.1 | [-1.1, +1.0] | [-1.4, +1.2] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs toon | 135 | -1.5 | [-3.4, +0.2] | [-4.6, +0.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs json-compact | 135 | +0.2 | [-0.9, +1.3] | [-1.1, +1.3] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs json-compact | 135 | -0.1 | [-1.7, +1.5] | [-2.3, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 135 | -2.0 | [-4.9, +0.7] | [-7.3, +1.4] | 0.125 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 135 | -0.2 | [-1.8, +1.2] | [-2.1, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 135 | -2.2 | [-4.9, +0.2] | [-6.8, +0.7] | 0.250 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 135 | +0.2 | [-1.0, +1.5] | [-1.2, +1.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 135 | -2.6 | [-5.4, -0.1] | [-7.9, +0.7] | 0.125 |  | B better | no detectable difference |
| pooled-nr | toon vs json-compact | 135 | +2.5 | [-0.1, +5.4] | [-0.4, +7.1] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs edn-table | 135 | -0.2 | [-2.0, +1.4] | [-2.2, +1.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-lines vs toon | 135 | -2.2 | [-5.1, +0.2] | [-6.8, +0.7] | 0.375 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs json-compact | 135 | +0.2 | [-1.5, +2.0] | [-1.5, +2.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |

</details>

**Sensitivity — lenient grader, overall, pooled**

| level | A vs B | diff | 95% CI | verdict |
|---|---|---|---|---|
| pooled | edn-maps vs json-compact | +0.1 | [-1.0, +1.2] | equivalent (±5pp) |
| pooled | edn-table vs toon | -2.1 | [-3.9, -0.4] | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | -0.2 | [-1.0, +0.6] | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | -2.2 | [-4.0, -0.6] | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | +0.3 | [-0.8, +1.3] | equivalent (±5pp) |
| pooled | edn-maps vs toon | -2.4 | [-4.3, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | +0.1 | [-1.5, +1.7] | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | -2.4 | [-4.7, -0.3] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs edn-table | -0.3 | [-1.4, +0.8] | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | -2.7 | [-4.9, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs json-compact | +0.6 | [-0.9, +2.1] | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | -3.1 | [-5.7, -0.8] | B better |

**Sensitivity — excluding batches with a fake tool call, overall, pooled**

| level | A vs B | diff | 95% CI | verdict |
|---|---|---|---|---|
| pooled | edn-maps vs json-compact | +0.1 | [-1.0, +1.1] | equivalent (±5pp) |
| pooled | edn-table vs toon | -2.0 | [-3.9, -0.4] | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | -0.1 | [-1.0, +0.8] | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | -2.2 | [-3.9, -0.5] | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | +0.3 | [-0.9, +1.4] | equivalent (±5pp) |
| pooled | edn-maps vs toon | -2.3 | [-4.2, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | -0.0 | [-1.7, +1.5] | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | -2.5 | [-5.0, -0.3] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs edn-table | -0.2 | [-1.6, +1.2] | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | -2.8 | [-5.2, -0.6] | B better |
| pooled-nr | edn-table-primer vs json-compact | +0.6 | [-1.1, +2.2] | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | -3.4 | [-6.1, -0.9] | B better |

**Sensitivity — excluding the 3 upstream ground-truth bugs (q110, q233, q234), overall, pooled**

| level | A vs B | diff | 95% CI | verdict |
|---|---|---|---|---|
| pooled | edn-maps vs json-compact | +0.1 | [-1.0, +1.1] | equivalent (±5pp) |
| pooled | edn-table vs toon | -2.2 | [-4.1, -0.6] | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | -0.1 | [-0.9, +0.7] | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | -2.3 | [-4.1, -0.6] | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | +0.3 | [-0.8, +1.3] | equivalent (±5pp) |
| pooled | edn-maps vs toon | -2.4 | [-4.4, -0.7] | B better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | +0.1 | [-1.6, +1.6] | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | -2.6 | [-5.0, -0.5] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs edn-table | -0.1 | [-1.2, +1.1] | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | -2.7 | [-5.0, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs json-compact | +0.6 | [-0.9, +2.1] | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | -3.2 | [-5.8, -0.9] | B better |
<!-- END:ACCURACY_TABLES -->

**External check vs upstream (Haiku 4.5).**
- Batched vs single-question accuracy: JSON 61.1% vs 61.9%, TOON 64.6% vs
  65.6%, CSV 51.4% vs 49.5%, with 93–99% per-question agreement.
- The effect of interest reproduces: TOON − JSON is +3.5 pp here
  (CI [+1.1, +6.3]) vs +3.7 pp upstream.
- Upstream is one sample per question, so its own SE is about 3 pp. This check
  shows batching didn't visibly distort Haiku's JSON-vs-TOON behaviour. It does
  not prove batching is harmless for every format or model.

<!-- BEGIN:EXTERNAL -->
**External check vs upstream (Haiku 4.5)**

| format | n | upstream single-question | ours, batched (mean 3 seeds) | per-question agreement (majority) |
|---|---|---|---|---|
| json-compact | 244 | 61.9 | 61.1 | 93.4 |
| toon | 244 | 65.6 | 64.6 | 95.1 |
| csv | 109 | 49.5 | 51.4 | 99.1 |
<!-- END:EXTERNAL -->

**Opus.**
- Its accuracy is 97–98% *with hidden reasoning*.
- Thinking tokens per call differ by format: TOON 665 < edn-table 702 <
  JSON 741 < edn-maps 756 < CSV 957. That makes TOON the cheapest format for
  Opus to reason over.

## 5. Generation check

<!-- BEGIN:GENERATION -->
**Generation check** (20 records × 3 samples = 60 attempts per cell; 95% CI = bootstrap over the 20 records, since samples of one record are near-duplicates). EDN parse-valid requires both edn-data and edn_format to accept. `toon-long` = post-hoc arm with a 156-token quoting-rules primer (D7).

| model | format | parse-valid % [CI] | lossless round-trip % [CI] | canonical form (count) |
|---|---|---|---|---|
| haiku | edn-table | 96.7 [90.0, 100.0] | 83.3 [66.7, 96.7] | 37/60 |
| haiku | edn-maps | 96.7 [90.0, 100.0] | 95.0 [85.0, 100.0] | 54/60 |
| haiku | toon | 66.7 [46.7, 85.0] | 50.0 [30.0, 70.0] | 30/60 |
| haiku | toon-long | 76.7 [61.7, 90.0] | 61.7 [41.7, 81.7] | 37/60 |
| sonnet | edn-table | 100.0 [100.0, 100.0] | 83.3 [66.7, 98.3] | 35/60 |
| sonnet | edn-maps | 96.7 [90.0, 100.0] | 95.0 [85.0, 100.0] | 54/60 |
| sonnet | toon | 71.7 [51.7, 90.0] | 68.3 [48.3, 86.7] | 41/60 |
| sonnet | toon-long | 93.3 [81.7, 100.0] | 83.3 [66.7, 98.3] | 50/60 |
| opus | edn-table | 100.0 [100.0, 100.0] | 95.0 [85.0, 100.0] | 45/60 |
| opus | edn-maps | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 60/60 |
| opus | toon | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 60/60 |
| opus | toon-long | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 60/60 |

**Generation lossless rate by record shape** (all models)

| shape | edn-table | edn-maps | toon | toon-long |
|---|---|---|---|---|
| flat | 60/63 (95%, [87, 98]) | 57/63 (90%, [81, 96]) | 54/63 (86%, [75, 92]) | 57/63 (90%, [81, 96]) |
| nested | 58/63 (92%, [83, 97]) | 63/63 (100%, [94, 100]) | 49/63 (78%, [66, 86]) | 56/63 (89%, [79, 95]) |
| mixed | 39/54 (72%, [59, 82]) | 54/54 (100%, [93, 100]) | 28/54 (52%, [39, 65]) | 34/54 (63%, [50, 75]) |
<!-- END:GENERATION -->

**What the failures were:**
- **TOON:**
  - unquoted commas inside values;
  - CSV-style `""` escaping;
  - inline JSON objects inside primitive arrays (`mixed[6]: 1,two,true,null,{"three":3},[4,5]`);
  - unquoted values TOON must quote.
  The quoting-rules primer (`toon-long`) reduced these a lot for Sonnet, less so
  for Haiku.
- **EDN-table:**
  - non-uniform arrays forced into a table, with `nil` for missing keys
    (records M1 and M2; M2 even for Opus), which is lossy;
  - Haiku tabularising an array of arrays (N5) with invented column names.
- **EDN-maps:**
  - an invalid keyword `:first\ name` for the key `"first name"` (edn-data
    accepted it, edn_format rejected it; we count it invalid);
  - the lossy rename `:first-name`.
  - `:2fa` (strictly not a valid keyword) was accepted by both parsers and
    counted lossless but not canonical. That's a lenient call, and only record
    N6 is affected.

**Fairness notes:**
- The original TOON arm used upstream's one-line primer (80 tokens). EDN-table
  had the 144-token LONG primer. The post-hoc `toon-long` arm (156 tokens)
  levels this.
- Haiku 4.5's knowledge cutoff (Feb 2025) predates TOON.
- Effective n is 20 records per cell, so CIs are wide.

## 6. Primer break-even (H3)

Per-call cost = primer line + data. Interpolated crossing points, in records,
over the prefix series of each token-benchmark dataset. For the Claude
tokenizers the series was measured up to n = 100 (D9).

<!-- BEGIN:BREAKEVEN -->
| family | tokenizer | LONG primer | vs JSON-c (no primer) | vs JSON-c (+primer) | vs TOON (+primer) | vs TOON (no primer) | JSON − EDN-table per record | EDN-table − TOON per record |
|---|---|---|---|---|---|---|---|---|
| analytics | claude-5 | 206 | 9.1 | 8.2 | never (<= 100) | never (<= 100) | +25.7 | +2.09 |
| analytics | claude-haiku-4.5 | 159 | 13.7 | 12.7 | never (<= 100) | never (<= 100) | +12.81 | +2.04 |
| analytics | o200k | 144 | 11.6 | 10.9 | never (<= 200) | never (<= 200) | +13.9 | +0.03 |
| analytics | qwen3 | 143 | 11.6 | 10.9 | never (<= 200) | never (<= 200) | +13.9 | +0.01 |
| employees | claude-5 | 206 | 10.6 | 9.6 | never (<= 100) | never (<= 100) | +21.74 | +5.07 |
| employees | claude-haiku-4.5 | 159 | 13.8 | 12.8 | never (<= 100) | never (<= 100) | +12.81 | +5.03 |
| employees | o200k | 144 | 13.5 | 12.7 | never (<= 2000) | never (<= 2000) | +11.99 | +2.55 |
| employees | qwen3 | 143 | 13.5 | 12.7 | never (<= 2000) | never (<= 2000) | +11.99 | +2.66 |
| event-logs | claude-5 | 206 | never (<= 100) | never (<= 100) | 13.4 | 33.4 | +0.95 | -6.4 |
| event-logs | claude-haiku-4.5 | 159 | never (<= 100) | never (<= 100) | 7.1 | 17.8 | -4.01 | -9.34 |
| event-logs | o200k | 144 | never (<= 2000) | never (<= 2000) | 6.8 | 15.1 | -3.0 | -9.78 |
| event-logs | qwen3 | 143 | never (<= 2000) | never (<= 2000) | 6.5 | 14.9 | -4.0 | -9.78 |
| github | claude-5 | 206 | 5.6 | 5.1 | never (<= 100) | never (<= 100) | +45.88 | +8.7 |
| github | claude-haiku-4.5 | 159 | 8.0 | 7.5 | never (<= 100) | never (<= 100) | +24.11 | +8.57 |
| github | o200k | 144 | 8.0 | 7.5 | never (<= 100) | never (<= 100) | +21.75 | +5.28 |
| github | qwen3 | 143 | 8.7 | 8.2 | never (<= 100) | never (<= 100) | +19.76 | +5.26 |
| orders | claude-5 | 206 | 17.4 | 15.9 | never (<= 100) | never (<= 100) | +12.96 | +7.37 |
| orders | claude-haiku-4.5 | 159 | never (<= 100) | never (<= 100) | never (<= 100) | never (<= 100) | -6.34 | +1.2 |
| orders | o200k | 144 | never (<= 500) | never (<= 500) | 19.0 | 47.5 | -4.71 | -3.06 |
| orders | qwen3 | 143 | never (<= 500) | never (<= 500) | 18.8 | 51.5 | -6.72 | -2.83 |

<details><summary>Grid-point version (o200k / Qwen3, n up to 2000; first grid n at or past the crossing)</summary>

#### Primer break-even (payload size in records)

Cost of a call = primer line + data block. `edn-table+P` = LONG primer + EDN-table data. Break-even = smallest n in the grid where edn-table+P ≤ the comparator ("never" if not reached by the largest n).

| family | tokenizer | vs JSON-c (no primer) | vs JSON-c (+its primer) | vs TOON (+its primer) | vs TOON (no primer) | vs EDN-table (short primer) | per-record saving vs JSON-c | per-record Δ vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | o200k | 20 | 20 | never | never | never | +13.9 tok | +0.0 tok |
| analytics | qwen3 | 20 | 20 | never | never | never | +13.9 tok | +0.0 tok |
| employees | o200k | 20 | 20 | never | never | never | +12.0 tok | +2.5 tok |
| employees | qwen3 | 20 | 20 | never | never | never | +12.0 tok | +2.7 tok |
| event-logs | o200k | never | never | 10 | 20 | never | -3.0 tok | -9.8 tok |
| event-logs | qwen3 | never | never | 10 | 20 | never | -4.0 tok | -9.8 tok |
| github | o200k | 10 | 10 | never | never | never | +21.8 tok | +5.3 tok |
| github | qwen3 | 10 | 10 | never | never | never | +19.8 tok | +5.3 tok |
| orders | o200k | never | never | 20 | 50 | never | -4.7 tok | -3.1 tok |
| orders | qwen3 | never | never | 20 | 100 | never | -6.7 tok | -2.8 tok |

</details>
<!-- END:BREAKEVEN -->

- **Uniform tables vs compact JSON with no primer** (conservative): the LONG
  primer is repaid from **about 6–14 records** on every tokenizer (GitHub 5.6–8.7;
  analytics 9.1–13.7; employees 10.6–13.8).
- **Uniform tables vs TOON:** never repaid. EDN-table costs 0–9 tokens more
  per record *before* the primer.
- **Semi-uniform event logs:** EDN-table + primer undercuts TOON (+ its primer)
  from 6.5–13.4 records. It never undercuts compact JSON within the measured
  range. On Claude 5, JSON is only 0.95 tokens per record more, too little to
  repay the primer by n = 100.
- **If the primer is sent once per conversation:** one uniform-table call of
  the accuracy datasets' size repays it against JSON (saving 761–4,588 tokens
  per call vs 144–206 primer tokens; `breakeven_calls.csv`). Against TOON it is
  never repaid on uniform data.
- **Accuracy:** the primer bought nothing (§4). Relative to the 29-token short
  primer it is pure overhead.
- **Scope:** we compared LONG vs SHORT primer, not LONG vs *no* primer. Every
  format in this harness carries a primer line.

## 7. Verdicts

Each verdict gives the claim, the evidence and what would change it.

**H1: EDN-maps uses fewer tokens than compact JSON, especially on nested data.**
The verdict differs by tokenizer, per the pre-registered rule (fewer tokens on
both tracks, and a mixed-track saving at least as large as the flat-track one):
- **Refuted** on o200k, Qwen3 and Claude Haiku 4.5.
- **Supported, but tiny,** on the Claude 5 tokenizer (Sonnet 5 / Opus 5.5).

- **Evidence:** EDN-maps vs compact JSON, token-benchmark totals.
  Deterministic counts, so no interval is needed.

  | tokenizer | flat track | mixed track |
  |---|---|---|
  | o200k | +7.1% | +6.0% |
  | Qwen3 | +5.8% | +6.6% |
  | Haiku 4.5 | +10.5% | +6.6% |
  | Claude 5 | −1.3% | −2.2% |

  EDN-maps vs TOON on nested config:

  | tokenizer | EDN-maps | TOON |
  |---|---|---|
  | o200k | 586 | 589 |
  | Qwen3 | 639 | 643 |
  | Haiku 4.5 | 672 | 698 |
  | Claude 5 | 889 | 866 |
- **Confidence:** high; counts are deterministic.
- **What would change it:** only the tokenizer. Layout doesn't matter, since
  newline and space cost the same.

**H2: EDN-table matches or beats TOON on uniform arrays.** Refuted on tokens;
accuracy shows no detectable difference.
- **Evidence, tokens:** on tabular + analytics + GitHub, EDN-table is larger than
  TOON on every tokenizer:

  | tokenizer | EDN-table vs TOON |
  |---|---|
  | o200k | +8.3% |
  | Qwen3 | +6.5% |
  | Haiku 4.5 | +15.0% |
  | Claude 5 | +11.9% |

  The pre-registered "match" band was ±5%. Almost all of the overhead is string
  quoting. On the all-numeric analytics set EDN-table ties TOON only on o200k
  and Qwen3 (+0.1% / 0.0%); on the Claude tokenizers it is +8.4% / +8.8%.
- **Evidence, accuracy:** on the 104 uniform-table questions, pooled
  edn-table vs toon is −1.4 pp, q-CI [−3.2, +0.4]. That's equivalent under the
  pre-registered rule. But Sonnet alone is −2.9 pp [−6.7, +1.0], which is
  inconclusive.
- **Confidence:** high on tokens, low on accuracy.
- **What would change it:** unquoted strings, which would no longer be EDN.

**H3: a primer of about 150 tokens makes up for thinner training data and pays
off at realistic sizes.** Not supported: the primer has no effect, and there was
no handicap to make up for.
- **Evidence:**
  - edn-table-primer vs edn-table: −0.1 pp, q-CI [−0.9, +0.8] and ds-CI
    [−1.0, +0.9], equivalent for every model.
  - The null effect also holds on uniform-table questions (+0.3 pp) and on the
    informative subset.
  - EDN-table without the long primer is already equivalent to JSON.
  - The cost side "pays off" only against JSON: 6–14 records, ≤50, so
    realistic by the pre-registered rule. Never against TOON on uniform data.
- **Confidence:** high that the long primer doesn't beat the short one.
  Unknown whether *no* primer would be worse, because that wasn't tested.
- **What would change it:** a model with weak EDN knowledge. Only Claude was
  tested, and even Haiku needed nothing beyond one line.

**H4: models understand EDN about as well as JSON and TOON.**
- **vs JSON:** supported, with high confidence.
- **vs TOON:** EDN is about 2 pp lower, which is suggestive but not robust.
- **Evidence, vs JSON** (the headline uses all non-structural questions, D8):
  EDN-maps vs json-compact is equivalent within ±5 pp for every model and both
  pooled levels, under both CI methods:

  | level | diff | q-CI | ds-CI |
  |---|---|---|---|
  | Haiku | +0.1 pp | [−1.9, +2.2] | [−2.6, +2.8] |
  | Sonnet | +0.8 pp | [−1.3, +2.9] | [−2.1, +3.7] |
  | Opus | +0.1 pp | [−0.4, +0.7] | [−0.7, +0.9] |
  | pooled-nr | +0.5 pp | [−1.0, +1.9] | [−1.7, +2.5] |

  The same holds with the lenient grader, without the tool-call batches,
  without the broken ground truths, and on all 244 questions. On the
  informative subset (the 92 questions that vary for Haiku+Sonnet) it is
  +0.2 pp [−4.2, +4.3].
- **Evidence, vs TOON** (non-structural questions):
  - pooled-nr edn-table vs toon: −1.8 pp, q-CI [−3.8, +0.1], ds-CI [−5.2, +1.0];
  - pooled-nr edn-maps vs toon: −2.0 pp, q-CI [−4.2, −0.1], ds-CI [−5.6, +0.6];
  - no TOON-vs-EDN McNemar test survives Holm, except Haiku edn-maps vs toon on
    all 244 questions (adjusted p = 0.044);
  - with all 244 questions, TOON's lead grows (edn-table vs toon −2.2 pp
    pooled), because 2 of the 5 structural-validation questions (truncation,
    extra rows) are answerable only with a declared length. CSV answers "NO" to
    all 5, including the control, and still scores 4/5.
  - On the informative subset, TOON's lead over EDN (−6.9 to −8.5 pp) is about
    the same as its lead over JSON (+8.7 pp). **EDN sits where JSON sits.**
- **What would change it:** non-Claude models; larger or noisier payloads; a
  model-based analysis with random effects per question. The equivalence
  statements are "on this benchmark's question mix", and Opus contributes
  almost no signal (16 informative questions).

**Uniform tables** (tabular, analytics, GitHub):
- **Tokens:** CSV (flat only) wins, then TOON. EDN-table is +6.5–15% over TOON,
  and TOON is 29–42% below compact JSON, depending on tokenizer.
- **Accuracy:** no detectable difference between formats (pooled edn-table vs
  toon −1.4 [−3.2, +0.4]).
- **Confidence:** high on tokens, low on accuracy differences.
- **What would change it:** mostly numeric tables with few strings, where
  EDN-table ≈ TOON on o200k and Qwen3.

**Nested config** (1 config, 29 questions): no meaningful winner.
- **Tokens:** within about 7% for all four contenders, and the order flips by
  tokenizer: JSON is smallest on o200k and Qwen3, EDN-table on Haiku 4.5, TOON
  on Claude 5.
- **Accuracy:** at the ceiling, 96–98% pooled.
- **EDN-maps vs JSON:** pooled +1.5 pp [+0.4, +3.1] passes the bootstrap rule,
  but the McNemar p is 1.0 with 29 near-ceiling questions, so I treat it as
  fragile.
- **Confidence:** low. A larger nested-config set would change it.

**Mixed** (orders, event logs, keyed flags, nested-group contacts): it depends
on the sub-shape.
- **Semi-uniform event logs:** EDN-table beats TOON by 6–13% on tokens, but
  compact JSON is cheaper than both on o200k, Qwen3 and Haiku.
- **Keyed and nested-group data:** TOON wins by 34–90%, because EDN-table has no
  equivalent of those forms.
- **Accuracy:** pooled-nr edn-table vs toon on the mixed track is −2.0 pp,
  q-CI [−4.9, +0.7], ds-CI [−7.3, +1.4], so no detectable difference. The
  line-broken EDN variant doesn't change that: `edn-table-lines` vs `edn-table`
  −0.2 pp [−2.0, +1.4], vs TOON −2.2 pp [−5.1, +0.2].
- **Winner:** TOON overall on this track (lowest mixed-track total on Claude 5,
  within 2% of JSON on o200k).
- **Confidence:** medium on tokens, low on accuracy.

## 8. Grader audit and failure classification

**Hand audit.** I hand-checked 30 uniformly random graded answers per format
(180 in all, seed 777) against the question, ground truth and answer
([`audit_sample.csv`](results/audit/audit_sample.csv),
[`audit_verdicts.csv`](results/audit/audit_verdicts.csv)).
- **0 grader errors** in the sample.
- All 45 sampled incorrect answers were clean, wrong values, so they're
  comprehension errors.

**Full-data scans, after the audit and the review.** These found upstream grader
and ground-truth errors that a 30-per-format sample couldn't catch. **All of them
are format-neutral.**
- **q110 (integer truncation):** the checker truncates decimals. Opus's exact
  answer 184558.62 is graded wrong against `184559`: 3 false negatives in every
  format.
- **q233 / q234 (wrong ground truth):** upstream hard-codes the GitHub field
  order `…,stars,watchers,forks,…`, but the data (and every format's encoding)
  has `…,createdAt,updatedAt,pushedAt,stars,…`. All answers to both questions
  are graded wrong, in every cell; most q234 answers ("pushedAt") are correct
  for the data.
- **Effect:** excluding q110, q233 and q234 changes no verdict (§4 sensitivity
  table).
- **One EDN-specific grader behaviour:** the prompt says "use the exact string
  from the data", and in EDN that string is `:email`. The primary grader marks
  4–5 such answers wrong, all on EDN formats. The lenient grader accepts them,
  and no verdict changes.

<!-- BEGIN:FAILURES -->
**Failure classification (all graded answers)**

| model | format | correct | comprehension | format (lenient-correct) | format (missing) | call failed |
|---|---|---|---|---|---|---|
| haiku | csv | 168 | 159 | 0 | 0 | 0 |
| haiku | edn-maps | 445 | 287 | 0 | 0 | 0 |
| haiku | edn-table | 455 | 276 | 1 | 0 | 0 |
| haiku | edn-table-lines | 296 | 109 | 0 | 0 | 0 |
| haiku | edn-table-primer | 453 | 279 | 0 | 0 | 0 |
| haiku | json-compact | 447 | 285 | 0 | 0 | 0 |
| haiku | toon | 473 | 259 | 0 | 0 | 0 |
| opus | csv | 309 | 18 | 0 | 0 | 0 |
| opus | edn-maps | 714 | 18 | 0 | 0 | 0 |
| opus | edn-table | 710 | 22 | 0 | 0 | 0 |
| opus | edn-table-lines | 405 | 0 | 0 | 0 | 0 |
| opus | edn-table-primer | 710 | 22 | 0 | 0 | 0 |
| opus | json-compact | 713 | 19 | 0 | 0 | 0 |
| opus | toon | 720 | 12 | 0 | 0 | 0 |
| sonnet | csv | 165 | 162 | 0 | 0 | 0 |
| sonnet | edn-maps | 474 | 257 | 1 | 0 | 0 |
| sonnet | edn-table | 473 | 257 | 2 | 0 | 0 |
| sonnet | edn-table-lines | 310 | 94 | 1 | 0 | 0 |
| sonnet | edn-table-primer | 474 | 258 | 0 | 0 | 0 |
| sonnet | json-compact | 471 | 261 | 0 | 0 | 0 |
| sonnet | toon | 493 | 239 | 0 | 0 | 0 |


**Reply behaviour and per-call cost** (per batched call; visible output excludes Opus's hidden thinking; fake-tool-call rate with Wilson 95% CI and Fisher exact p vs json-compact of the same model)

| model | format | calls | mean input tok | median visible output | mean visible output | Opus thinking tok | fake tool calls | Fisher p vs JSON | list-price $/call |
|---|---|---|---|---|---|---|---|---|---|
| haiku | json-compact | 96 | 5778 | 59.5 | 55 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0058 |
| haiku | toon | 96 | 5076 | 60.0 | 84 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0055 |
| haiku | edn-maps | 96 | 6209 | 61.5 | 1622 | 0 | 10 (10.4% [5.8, 18.1]) | 0.0015 | 0.0148 |
| haiku | edn-table | 96 | 5278 | 60.5 | 684 | 0 | 4 (4.2% [1.6, 10.2]) | 0.1211 | 0.0089 |
| haiku | edn-table-primer | 96 | 5405 | 60.0 | 344 | 0 | 2 (2.1% [0.6, 7.3]) | 0.4974 | 0.0078 |
| haiku | csv | 51 | 4443 | 55 | 721 | 0 | 4 (7.8% [3.1, 18.5]) | 0.0134 | 0.0080 |
| sonnet | json-compact | 96 | 7848 | 73.0 | 104 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0202 |
| sonnet | toon | 96 | 6326 | 73.5 | 137 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0168 |
| sonnet | edn-maps | 96 | 7776 | 74.0 | 136 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0202 |
| sonnet | edn-table | 96 | 6622 | 74.0 | 167 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0178 |
| sonnet | edn-table-primer | 96 | 6784 | 74.0 | 98 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0175 |
| sonnet | csv | 51 | 5558 | 64 | 76 | 0 | 0 (0.0% [0.0, 7.0]) | 1.0000 | 0.0138 |
| opus | json-compact | 96 | 7785 | 72.0 | 66 | 741 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0473 |
| opus | toon | 96 | 6263 | 72.0 | 65 | 665 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0396 |
| opus | edn-maps | 96 | 7713 | 72.0 | 66 | 756 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0473 |
| opus | edn-table | 96 | 6559 | 72.0 | 66 | 702 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0416 |
| opus | edn-table-primer | 96 | 6721 | 72.0 | 66 | 693 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0421 |
| opus | csv | 51 | 5495 | 64 | 55 | 957 | 0 (0.0% [0.0, 7.0]) | 1.0000 | 0.0422 |
<!-- END:FAILURES -->

**Failure classes.**
- Every failure is a clean wrong value (comprehension), except the 4–5
  keyword-colon answers above.
- There were no missing answer lines.

**Fake tool calls, a CLI artefact.**
- **What happens:** Haiku sometimes writes a pretend script (Clojure or Python,
  targeting the CLI's scratchpad path) and "runs" it in text.
- **Where:**

  | format | calls with a fake tool call | Fisher p vs JSON |
  |---|---|---|
  | EDN-maps | 10.4% [5.8, 18.1] | 0.0015 |
  | CSV | 7.8% | 0.013 |
  | EDN-table | 4.2% | 0.12 |
  | EDN-table-primer | 2.1% | — |
  | JSON | 0% | — |
  | TOON | 0% | — |

  Sonnet and Opus: 0 for every format.
- **Median reply length is unchanged** (Haiku 59.5–61.5 visible tokens for
  every format), so the mean of 1,622 on EDN-maps is a tail effect.
- **Interpretation:** a less familiar payload in an agent-flavoured context (the
  CLI's injected environment reminders, D4) triggers it. It is probably not what
  a bare API call would do.
- **Effect on verdicts:** dropping every affected batch for all formats changes
  no pooled verdict.

## 9. Adversarial review and responses

After the first full set of results, a fresh Opus subagent received only
PLAN.md, DEVIATIONS.md, the harness diff and the raw results (not this report
or my analysis files). It was asked to find every reason the conclusions could
be wrong or unfair. Its 15 points and my responses:

1. **Equivalence is inflated by questions nobody gets wrong (or right)**
   (major).
   - **Agreed.** Only 64 (Haiku), 68 (Sonnet) and 16 (Opus) questions vary at
     all.
   - **Added:** an "informative" subset, reported next to every comparison.
     EDN-maps ≈ JSON survives there (+0.2 pp [−4.2, +4.3] for Haiku+Sonnet).
   - **Reworded:** equivalence claims now say "on this benchmark's question
     mix".
2. **TOON-beats-EDN is fragile** (major; resample datasets, apply Holm).
   - **Agreed and fixed.** A two-stage dataset bootstrap is now reported for
     every comparison.
   - Holm is shown. Only Haiku edn-maps vs toon survives it.
   - The TOON-over-EDN claim is downgraded to "suggestive, about 2 pp, the
     same size as TOON over JSON".
3. **Structural-validation questions drive part of the TOON gap** (major).
   - **Agreed.** The H4 headline now uses non-structural questions (239). The
     structural 5 are reported separately as a format-feature test.
   - Noted that CSV's all-"NO" answers score 4/5.
4. **Layout confound** (major: single-line EDN vs one-record-per-line TOON).
   - **Tested, not just argued.** I ran a line-broken EDN-table variant on all
     mixed batches with all 3 models (D6).
   - Result: −0.2 pp vs single-line EDN-table [−2.0, +1.4] for Haiku+Sonnet,
     so layout doesn't explain the gap.
   - Also confirmed the whitespace-variant texts differ (1 vs 75 lines on event
     logs) while their token counts match.
5. **H1 verdict wording departs from the pre-registered rule** (major).
   - **Agreed.** H1 is now "supported on Claude 5 (tiny), refuted on the other
     three".
   - The token-split mechanism is shown in §3; the reviewer didn't have it. It
     is stated as unobservable for Claude 5.
6. **H2 details** (analytics tie only on o200k and Qwen3; Sonnet alone
   inconclusive). **Agreed and reworded.**
7. **H3 scope** (LONG vs SHORT, not vs none; Claude break-even missing; grid
   artefact; nested break-even vs TOON exists).
   - **Agreed on all four.**
   - Claude break-even was measured (D9), and crossings are now interpolated:
     6–14 records vs JSON.
   - The nested-data break-even vs TOON is reported.
   - The scope limitation is stated.
8. **C6 overclaimed** (major; the mean is a tail, CSV is also affected, and
   the likely cause is the CLI).
   - **Agreed.** It is now reported as rates with CIs, Fisher tests and
     medians, and attributed to the CLI context.
   - DEVIATIONS D1's retest file does show one reply still at 32k characters.
     D1's claim that the retest "produced direct answers" was too strong.
     Corrected here: in the 12 retest replies, 10 were direct, 2 had a one-line preamble, and the same batch (s3-b071-edn-table) stayed very long both times.
9. **External check can't support "batching didn't distort"** (major).
   - **Partly agreed.** The upstream file is in the repo (the reviewer wasn't
     given it). Per-question agreement is 93–99%, and the TOON−JSON gap
     reproduces (+3.5 vs +3.7 pp).
   - Toned down to "no visible distortion for Haiku JSON/TOON". An unbatched
     replication across formats was not run.
10. **Opus is a different regime** (major).
    - **Agreed.** A Haiku+Sonnet pooled level (`pooled-nr`) is added and used
      for headline H4 statements.
    - Opus thinking tokens per format are reported, and counted in cost.
11. **Upstream ground-truth bugs, q233/q234** (minor).
    - **Confirmed and reported** (§8). They are wrong in every cell, so
      format-neutral.
    - A sensitivity run without them changes nothing.
12. **Grader marks `:email` wrong despite "exact string from the data"**
    (minor). **Agreed.** It affects 4–5 answers, all EDN. No verdict changes
    under the lenient grader.
13. **Generation fairness** (major: n = 20, lenient EDN parser, TOON prompt
    lacks quoting rules).
    - All three are addressed:
      - CIs are now clustered by record;
      - EDN parse-valid requires edn_format too (this was already the case in
        the first report's table);
      - a post-hoc `toon-long` arm with a 156-token quoting-rules primer was
        run (D7).
    - The TOON gap shrinks: Sonnet lossless 68% → 83%, equal to EDN-table.
      Haiku 50% → 62%, still below EDN-table at 83% and EDN-maps at 95%.
14. **Per-seed columns mislabelled** (minor). **Bug confirmed and fixed** (D8).
    Only the per-seed columns were affected; means and CIs were not.
15. **Pilot informed D1/D2; labels are made-up words; Sonnet cached despite
    the flag** (minor). **Acknowledged.**
    - D1 and D2 were symmetric across formats and decided before any format
      comparison was seen.
    - The labels `edn-maps` / `edn-table` parallel upstream's `json-compact`.
    - Caching doesn't affect usage-delta token counts (verified: baselines were
      constant).

**Conclusions the review changed:**
- H1 wording (now per tokenizer).
- H4 headline (non-structural questions; TOON's lead downgraded to
  suggestive).
- The Haiku verbosity claim (now a CLI-context tail effect, not "a hidden cost
  of EDN").
- The generation gap (it narrows when TOON gets comparable instructions).

**Conclusions that stood:** EDN ≈ JSON on comprehension, and EDN loses to TOON
on tokens.

## 10. Skipped, sampled or changed relative to PLAN.md

**Before the main runs** (D1–D5):
- **D1:** one line added to the shared template for every format:
  `- Do not show your work, reasoning or code`. It followed a 21-call Haiku
  pilot that showed reasoning and fake tool calls.
- **D2:** the answer parser takes the *last* `Q<n>:` line.
- **D3:** the Claude token-counting API was **skipped** (no `ANTHROPIC_API_KEY`).
  Claude counts come from CLI usage deltas instead.
- **D4:** the CLI injects about 780 tokens of environment `<system-reminder>`s
  into every call. It is identical across formats but unlike a bare API call.
- **D5:** effort was pinned to `low`. Opus 5.5's adaptive thinking could not
  be disabled, so Opus results include hidden reasoning. The partial runs made
  before this are excluded ($4.25).

**After the adversarial review** (post hoc, exploratory; D6–D9):
- **D6:** `edn-table-lines` layout run.
- **D7:** `toon-long` generation arm.
- **D8:** statistics additions: the Haiku+Sonnet pooled level, dataset
  bootstrap, informative subset, ground-truth sensitivity, seed-column fix,
  record-clustered generation CIs, and a non-structural H4 headline.
- **D9:** Claude break-even measured, with interpolated crossings.

**Other differences from the plan:**
- **Upstream runner not used:** there was no API key, so calls went through
  headless Claude Code subagents, as the task allowed.
- **Batching:** questions were batched (≤10 per call) instead of upstream's one
  per call.
- **Tokenizer files:** huggingface.co and openaipublic.blob.core.windows.net
  are blocked by the egress policy. o200k was rebuilt and hash-verified;
  Qwen3's `tokenizer.json` came from npm.
- **Canonical-form bug:** my own first generation canonical-form check was
  buggy (it marked all tables non-canonical). It was fixed before the first
  report; lossless and parse-valid were unaffected.
- **Nothing was sampled:** all 244 questions, 3 seeds, 3 models and all formats
  ran, with 0 failed calls. Sonnet was not measured on the large token datasets
  because its tokenizer matched Opus's, per PLAN §3.

## 11. Reproduce

```bash
cd vendor/toon && pnpm install && cd benchmarks
npx vitest run                                  # EDN round trips (edn-data), corruption, fairness
node scripts/edn-dump-encodings.ts              # build/encodings.json, results/encodings/
cd ../../.. && tools/setup_tokenizers.sh && python3 -m pytest tools/test_edn_roundtrip.py   # edn_format
python3 tools/tokens.py && python3 tools/claude_tokens.py <haiku|opus|sonnet> accuracy,tokens,breakeven
(cd vendor/toon/benchmarks && node scripts/edn-make-tasks.ts && node scripts/edn-make-tasks.ts layout) && python3 tools/check_manifest.py
python3 tools/run_accuracy.py <model> 5 [accuracy|accuracy_layout]
(cd vendor/toon/benchmarks && node scripts/edn-grade.ts)
python3 tools/stats.py [--lenient | --exclude-toolcall-batches --suffix _no_toolcall_batches | --exclude-questions q110,q233,q234 --suffix _no_broken_gt]
(cd vendor/toon/benchmarks && node scripts/edn-gen.ts tasks && node scripts/edn-gen.ts tasks toon-long)
python3 tools/run_accuracy.py <model> 5 [generation|generation_toonlong]
(cd vendor/toon/benchmarks && node scripts/edn-gen.ts grade) && python3 tools/gen_edn_crosscheck.py
python3 tools/external_check.py && python3 tools/token_report.py && python3 tools/breakeven.py
python3 tools/report_tables.py && python3 tools/fill_report.py
```
