# REPORT: Is EDN a real contender against TOON and JSON as an LLM data format?

Pre-registration: [`PLAN.md`](PLAN.md) (commit `fa4f204`, pushed before any
encoder output, token count or model answer existed). Deviations: §10 (also
logged live in [`DEVIATIONS.md`](DEVIATIONS.md)). Base harness: upstream
[toon-format/toon](https://github.com/toon-format/toon) at commit
`f151a5d830d001bc244395b891183cba37e0d935`, vendored unmodified in `vendor/toon`
(commit `2788bde`); every change is in [`results/review/harness.diff`](results/review/harness.diff).

## 1. Summary

**EDN is a real contender for comprehension and generation, but it doesn't win on
tokens, which is what TOON is chosen for.** Across 244 questions, 3 Claude
models and 3 seeds, models answer questions about EDN as accurately as about
compact JSON: EDN-maps vs JSON pooled +0.1 pp, 95% CI [−1.1, +1.1], and it is
equivalent within ±5 pp for every model. Small models also *write* EDN more
reliably than TOON: parse-valid 97–100% vs 67–72% for Haiku and Sonnet. But
EDN's syntax costs tokens rather than saving them. On o200k, Qwen3 and
Claude Haiku 4.5, EDN-maps is 6–10% **larger** than compact JSON, because
JSON's `","` and `":"` merge into single tokens and EDN's separators don't.
Only on the Claude 5 tokenizer (Sonnet 5 / Opus 5.5) is EDN-maps smaller, by
1–2%. The tabular EDN form is 6–15% larger than TOON on uniform arrays with
every tokenizer, and TOON stays about 2 pp more accurate (pooled edn-table vs
toon −2.2 pp [−4.0, −0.5], inside the ±5 pp margin). The 144-token primer has
no detectable effect (−0.1 pp [−0.9, +0.8]). EDN without it was already as
well understood as JSON, so the "thinner training data" handicap the primer
was meant to offset did not show up. By data shape:
- **Uniform tables:** use TOON (or CSV for flat data only). EDN-table beats
  JSON by 24–35% of tokens but loses to TOON.
- **Nested config:** all formats are within about 5% of each other on tokens
  and near the accuracy ceiling, so there's no meaningful winner.
- **Mixed data:** EDN-table is 6–13% cheaper than TOON on semi-uniform event
  logs, but far more expensive on data TOON folds into keyed or
  nested-field-group tables (+49–90%).

One more cost: Haiku reacts to EDN with much longer replies (mean 1,622 output
tokens per call on EDN-maps vs 55 on JSON), sometimes including fake tool
calls. That hidden output cost outweighs any input-token difference for that
model.

## 2. Setup actually run

| item | value |
|---|---|
| Datasets / questions | upstream `ACCURACY_DATASETS` (13 datasets, 244 questions; flat-only track 109, mixed 135) and `TOKEN_EFFICIENCY_DATASETS` (8 larger datasets) — ground truths identical to upstream's published run (0 mismatches) |
| Formats | `json-compact`, `toon`, `edn-maps`, `edn-table`, `edn-table-primer` on 244 q; `csv` on the 109 flat q |
| Models (served ids from CLI `modelUsage`) | `claude-haiku-4-5-20251001`, `claude-sonnet-5`, `claude-opus-5-5` |
| Runner | no `ANTHROPIC_API_KEY` in the environment → headless Claude Code subagents: `claude -p --system-prompt "" --tools "" --setting-sources "" --strict-mcp-config --disable-slash-commands --no-session-persistence --effort low`, `MAX_THINKING_TOKENS=0`, `DISABLE_PROMPT_CACHING=1` (`tools/claude_cli.py`) |
| Batching / seeds | ≤10 questions per call from one dataset; 3 seeds, question order and batch composition reshuffled per seed; identical batches for every format and model (paired; asserted by `tools/check_manifest.py`) |
| Calls | 1,593 accuracy calls (0 failures) → 11,961 graded answers; 540 generation calls; 321 token-count calls |
| Grading | upstream `compareAnswers` unchanged (primary); pre-registered lenient normaliser (sensitivity / failure classification) |
| Losslessness | every EDN encoding round-trips through **edn-data** (vitest, 185 tests) and **edn_format** (pytest, 51 tests), key order included; TOON round-trips through upstream `decode` |
| Spend (CLI-reported list price) | accuracy $37.16 (Haiku 4.52, Sonnet 9.58, Opus 23.07), Claude token counting $13.16, generation $2.04, excluded pilots $4.25 → **$56.62** logged, plus < $2 of unlogged manual smoke tests. Budget: $80 (raised from $40 during the run). |

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
- o200k: tiktoken, fed an o200k_base file rebuilt from `gpt-tokenizer`'s ranks.
  tiktoken verified its sha256 `446a9538…`, and the counts are identical to
  `gpt-tokenizer` on all 135 texts.
- Qwen3: HF `tokenizers` with Qwen3 `tokenizer.json`
  (sha256 `aeb13307…`, from npm `@lenml/tokenizer-qwen3@3.7.2`, because
  huggingface.co is blocked here).
- Claude: the **token-counting API was skipped** because there's no API key.
  Counts come from CLI `usage` deltas instead: input(`prefix\n`+data) −
  input(`prefix`), with the baseline constant over 3 repeats, accurate to
  ±1 token.
- Sonnet 5 and Opus 5.5 gave identical counts on all 60 accuracy-dataset
  measurements (one "Claude 5" tokenizer), so Sonnet was not re-measured on the
  large sets.

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

**Whitespace confound check:** EDN-table with all rows on one line, and EDN-maps
with one top-level element per line, gave token counts *identical* to the
layouts used, on every dataset (o200k and Qwen3). Newline vs space costs the
same.

**Why EDN-maps loses to JSON on three of four tokenizers** (o200k splits shown;
Qwen3 splits the same way):

```
{"id":1,"name":"Darla Mertz","department":"Sales","active":true}   20 tokens
  {" id ": 1 ," name ":" D arla  M ertz "," department ":" Sales "," active ": true }
{:id 1 :name "Darla Mertz" :department "Sales" :active true}        21 tokens
  {: id ␠ 1 ␠: name ␠" D arla  M ertz " ␠: department ␠" Sales " ␠: active ␠true }
```

JSON's closing-quote/separator/opening-quote runs (`","`, `":"`) are single
merged tokens. EDN needs `"` plus ` :` or ` "`, and a space before bare
numbers. The keyword colon saves nothing because `{"` and `,"` were already one
token each. The Claude 5 tokenizer evidently merges EDN's separators better:
EDN-maps is 0–8% smaller there.

## 4. Accuracy

The unit is the question: mean correctness over 3 seeds. CIs are percentile
cluster bootstraps over questions (10,000 resamples). "pooled" averages the 3
models per question; it never mixes tokenizers.

<!-- BEGIN:ACCURACY_TABLES -->
**All 244 questions (CSV: 109 flat questions)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 61.1 [55.2, 66.9] | 64.6 [58.9, 70.2] | 60.8 [54.8, 66.5] | 62.2 [56.6, 67.8] | 61.9 [56.1, 67.6] | 51.4 [42.5, 59.9] |
| sonnet | 64.3 [58.6, 70.0] | 67.3 [61.8, 72.8] | 64.8 [59.0, 70.4] | 64.6 [58.7, 70.4] | 64.8 [58.9, 70.4] | 50.5 [41.3, 59.9] |
| opus | 97.4 [95.4, 99.0] | 98.4 [96.7, 99.6] | 97.5 [95.6, 99.2] | 97.0 [95.0, 98.8] | 97.0 [95.0, 98.8] | 94.5 [90.2, 97.9] |
| pooled | 74.3 [70.3, 78.2] | 76.8 [73.0, 80.5] | 74.4 [70.5, 78.3] | 74.6 [70.6, 78.5] | 74.5 [70.5, 78.5] | 65.4 [59.1, 72.0] |

**Flat-only track (109)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 47.4 [38.5, 56.6] | 51.1 [41.9, 59.9] | 46.8 [37.6, 56.0] | 48.9 [40.1, 58.1] | 49.2 [40.4, 58.4] | 51.4 [42.5, 59.9] |
| sonnet | 48.6 [39.8, 57.8] | 53.5 [44.6, 62.1] | 49.9 [41.3, 58.7] | 48.9 [40.1, 57.5] | 48.9 [39.8, 58.1] | 50.5 [41.6, 59.6] |
| opus | 94.2 [89.6, 97.9] | 96.3 [92.7, 99.1] | 94.5 [89.9, 98.2] | 93.6 [89.3, 97.2] | 94.2 [89.6, 97.9] | 94.5 [90.2, 97.9] |
| pooled | 63.4 [57.0, 69.9] | 67.0 [60.7, 73.1] | 63.7 [57.4, 69.8] | 63.8 [57.5, 70.1] | 64.1 [57.8, 70.3] | 65.4 [58.9, 71.8] |

**Mixed-structure track (135)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 72.1 [64.9, 79.0] | 75.6 [68.4, 82.2] | 72.1 [64.7, 79.3] | 72.8 [65.7, 79.8] | 72.1 [64.9, 78.8] | – |
| sonnet | 77.0 [70.4, 83.2] | 78.5 [71.9, 84.9] | 76.8 [69.9, 83.5] | 77.3 [70.6, 83.7] | 77.5 [70.6, 83.7] | – |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.8 [99.3, 100.0] | 99.3 [98.0, 100.0] | – |
| pooled | 83.0 [78.5, 87.3] | 84.7 [80.2, 88.8] | 83.0 [78.3, 87.4] | 83.3 [78.9, 87.6] | 83.0 [78.3, 87.3] | – |

**Uniform tables (104)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 46.8 [37.5, 56.1] | 48.7 [39.1, 58.0] | 47.1 [37.8, 56.4] | 48.4 [39.4, 57.4] | 48.7 [39.4, 57.7] | 50.0 [41.0, 59.0] |
| sonnet | 48.1 [38.8, 57.4] | 51.3 [42.6, 60.3] | 50.3 [41.7, 59.0] | 48.4 [39.4, 57.7] | 48.4 [39.1, 57.7] | 49.0 [39.7, 58.3] |
| opus | 95.8 [92.0, 98.7] | 96.2 [92.3, 99.0] | 96.2 [92.6, 99.0] | 95.2 [91.3, 98.1] | 95.8 [92.3, 98.7] | 95.2 [91.0, 98.4] |
| pooled | 63.6 [57.3, 69.9] | 65.4 [59.1, 71.5] | 64.5 [58.3, 70.8] | 64.0 [57.4, 70.3] | 64.3 [57.9, 70.6] | 64.7 [58.4, 71.2] |

**Nested config (29)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 89.7 [80.5, 96.5] | 92.0 [83.9, 97.7] | 93.1 [83.9, 100.0] | 93.1 [85.1, 98.9] | 92.0 [82.8, 98.9] | – |
| sonnet | 98.9 [96.5, 100.0] | 98.9 [96.5, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.7 [93.1, 100.0] | – |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | – |
| pooled | 96.2 [92.3, 98.9] | 96.9 [93.9, 99.2] | 97.7 [94.6, 100.0] | 97.7 [95.0, 99.6] | 96.5 [92.0, 99.6] | – |

**Mixed shapes (106)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 67.3 [58.5, 75.8] | 71.1 [62.3, 79.6] | 66.3 [57.2, 74.8] | 67.3 [59.1, 75.5] | 66.7 [58.2, 74.8] | – |
| sonnet | 71.1 [63.2, 78.3] | 73.0 [64.8, 80.8] | 70.4 [62.0, 78.3] | 71.1 [62.9, 78.9] | 72.0 [64.1, 79.6] | – |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.7 [99.1, 100.0] | 99.1 [97.5, 100.0] | – |
| pooled | 79.5 [74.1, 84.6] | 81.3 [76.0, 86.4] | 78.9 [73.4, 84.4] | 79.3 [74.0, 84.6] | 79.2 [73.8, 84.5] | – |

**Structural validation (5)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |
| sonnet | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |
| opus | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |
| pooled | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 46.7 [6.7, 86.7] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |

**All except structural validation (239)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 61.1 [55.1, 67.0] | 63.9 [57.9, 69.7] | 61.2 [55.1, 67.2] | 62.2 [56.4, 67.9] | 61.9 [55.9, 67.8] | 50.0 [41.0, 59.0] |
| sonnet | 64.4 [59.0, 70.0] | 66.7 [61.1, 72.2] | 65.3 [59.4, 70.9] | 64.7 [58.9, 70.3] | 64.8 [59.1, 70.7] | 49.0 [39.4, 58.7] |
| opus | 98.2 [96.5, 99.4] | 98.3 [96.7, 99.6] | 98.3 [96.7, 99.6] | 97.8 [96.1, 99.2] | 97.8 [96.1, 99.2] | 95.2 [91.3, 98.4] |
| pooled | 74.6 [70.6, 78.4] | 76.3 [72.4, 80.1] | 74.9 [70.9, 78.7] | 74.9 [71.0, 78.8] | 74.9 [71.0, 78.8] | 64.7 [58.1, 71.2] |

**Paired comparisons — overall** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 244 | -0.3 | [-2.5, +2.1] | 1.000 | 1.0 | equivalent (±5pp) |
| haiku | edn-table vs toon | 244 | -2.5 | [-4.9, -0.1] | 0.092 | 1.0 | B better (within ±5pp) |
| haiku | edn-table-primer vs edn-table | 244 | -0.3 | [-1.8, +1.2] | 0.375 | 1.0 | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 244 | -2.7 | [-5.3, -0.4] | 0.021 | 0.48921 | B better |
| haiku | edn-table-primer vs json-compact | 244 | +0.8 | [-1.1, +2.9] | 1.000 | 1.0 | equivalent (±5pp) |
| haiku | edn-maps vs toon | 244 | -3.8 | [-6.7, -1.2] | 0.002 | 0.04392 | B better |
| haiku | toon vs json-compact | 244 | +3.5 | [+1.1, +6.3] | 0.003 |  | A better |
| sonnet | edn-maps vs json-compact | 244 | +0.4 | [-1.9, +2.6] | 0.424 | 1.0 | equivalent (±5pp) |
| sonnet | edn-table vs toon | 244 | -2.7 | [-5.7, +0.3] | 0.078 | 1.0 | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 244 | +0.1 | [-1.8, +2.1] | 0.227 | 1.0 | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 244 | -2.6 | [-5.3, +0.0] | 0.481 | 1.0 | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 244 | +0.4 | [-1.9, +2.7] | 0.332 | 1.0 | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 244 | -2.6 | [-5.9, +0.5] | 0.442 | 1.0 | no detectable difference |
| sonnet | toon vs json-compact | 244 | +3.0 | [+0.3, +6.0] | 0.078 |  | A better |
| opus | edn-maps vs json-compact | 244 | +0.1 | [-0.4, +0.7] | 1.000 | 1.0 | equivalent (±5pp) |
| opus | edn-table vs toon | 244 | -1.4 | [-2.9, -0.1] | 0.500 | 1.0 | B better (within ±5pp) |
| opus | edn-table-primer vs edn-table | 244 | +0.0 | [-0.7, +0.7] | 1.000 | 1.0 | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 244 | -1.4 | [-3.0, +0.0] | 0.250 | 1.0 | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 244 | -0.4 | [-1.4, +0.5] | 1.000 | 1.0 | equivalent (±5pp) |
| opus | edn-maps vs toon | 244 | -0.8 | [-2.3, +0.4] | 0.500 | 1.0 | equivalent (±5pp) |
| opus | toon vs json-compact | 244 | +1.0 | [-0.0, +2.3] | 0.500 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 244 | +0.1 | [-1.1, +1.1] | 0.791 | 1.0 | equivalent (±5pp) |
| pooled | edn-table vs toon | 244 | -2.2 | [-4.0, -0.5] | 0.027 | 0.5852 | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | 244 | -0.1 | [-0.9, +0.8] | 1.000 | 1.0 | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 244 | -2.2 | [-4.0, -0.6] | 0.052 | 1.0 | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 244 | +0.3 | [-0.8, +1.4] | 0.791 | 1.0 | equivalent (±5pp) |
| pooled | edn-maps vs toon | 244 | -2.4 | [-4.3, -0.7] | 0.064 | 1.0 | B better (within ±5pp) |
| pooled | toon vs json-compact | 244 | +2.5 | [+0.9, +4.4] | 0.017 |  | A better (within ±5pp) |

**Paired comparisons — overall-excl-structural** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 239 | +0.1 | [-1.9, +2.2] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 239 | -1.7 | [-3.9, +0.6] | 0.227 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs edn-table | 239 | -0.3 | [-1.8, +1.3] | 0.375 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 239 | -1.9 | [-4.3, +0.3] | 0.057 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs json-compact | 239 | +0.8 | [-1.1, +2.9] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-maps vs toon | 239 | -2.6 | [-5.2, -0.4] | 0.012 |  | B better |
| sonnet | edn-maps vs json-compact | 239 | +0.8 | [-1.4, +2.9] | 0.267 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 239 | -1.9 | [-4.9, +0.8] | 0.167 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs edn-table | 239 | +0.1 | [-1.8, +2.1] | 0.227 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 239 | -1.8 | [-4.3, +0.6] | 0.804 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 239 | +0.4 | [-1.9, +2.9] | 0.332 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 239 | -1.4 | [-4.3, +1.5] | 0.839 |  | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 239 | +0.1 | [-0.4, +0.8] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 239 | -0.6 | [-1.4, +0.3] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 239 | +0.0 | [-0.7, +0.7] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 239 | -0.6 | [-1.5, +0.3] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 239 | -0.4 | [-1.4, +0.6] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 239 | +0.0 | [-0.7, +0.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 239 | +0.4 | [-0.6, +1.3] | 0.581 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 239 | -1.4 | [-2.8, -0.1] | 0.064 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | 239 | -0.1 | [-0.9, +0.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 239 | -1.4 | [-2.8, -0.2] | 0.115 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 239 | +0.3 | [-0.7, +1.4] | 0.791 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 239 | -1.4 | [-2.8, -0.1] | 0.189 |  | B better (within ±5pp) |

**Paired comparisons — shape:uniform-tables** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 104 | +0.3 | [-3.5, +4.5] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 104 | -0.3 | [-3.2, +2.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs edn-table | 104 | +0.3 | [-1.9, +2.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 104 | -0.0 | [-2.9, +2.9] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs json-compact | 104 | +1.9 | [-1.6, +6.1] | 0.375 |  | no detectable difference |
| haiku | edn-maps vs toon | 104 | -1.6 | [-4.8, +1.3] | 0.500 |  | equivalent (±5pp) |
| sonnet | edn-maps vs json-compact | 104 | +2.2 | [-1.6, +6.1] | 0.508 |  | no detectable difference |
| sonnet | edn-table vs toon | 104 | -2.9 | [-6.7, +1.0] | 0.453 |  | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 104 | -0.0 | [-2.6, +2.9] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 104 | -2.9 | [-6.7, +1.0] | 1.000 |  | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 104 | +0.3 | [-4.2, +4.8] | 0.754 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 104 | -1.0 | [-5.8, +3.9] | 1.000 |  | no detectable difference |
| opus | edn-maps vs json-compact | 104 | +0.3 | [-1.0, +1.9] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 104 | -1.0 | [-2.9, +1.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 104 | +0.6 | [-0.6, +1.9] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 104 | -0.3 | [-1.9, +1.3] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 104 | +0.0 | [-1.6, +1.9] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 104 | +0.0 | [-1.6, +1.6] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 104 | +1.0 | [-0.8, +2.7] | 0.453 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 104 | -1.4 | [-3.2, +0.4] | 0.344 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 104 | +0.3 | [-1.0, +1.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 104 | -1.1 | [-3.1, +0.9] | 0.388 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 104 | +0.8 | [-1.4, +2.9] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 104 | -0.9 | [-3.2, +1.3] | 0.774 |  | equivalent (±5pp) |

**Paired comparisons — shape:nested-config** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 29 | +3.5 | [+0.0, +8.1] | 1.000 |  | no detectable difference |
| haiku | edn-table vs toon | 29 | +1.1 | [-4.6, +8.1] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs edn-table | 29 | -1.1 | [-6.9, +3.5] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs toon | 29 | +0.0 | [-5.8, +6.9] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs json-compact | 29 | +2.3 | [+0.0, +5.8] | 1.000 |  | no detectable difference |
| haiku | edn-maps vs toon | 29 | +1.1 | [-4.6, +8.1] | 1.000 |  | no detectable difference |
| sonnet | edn-maps vs json-compact | 29 | +1.1 | [+0.0, +3.5] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 29 | +1.1 | [+0.0, +3.5] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs edn-table | 29 | -2.3 | [-6.9, +0.0] | 1.000 |  | no detectable difference |
| sonnet | edn-table-primer vs toon | 29 | -1.1 | [-3.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 29 | -1.1 | [-3.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 29 | +1.1 | [+0.0, +3.5] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 29 | +1.5 | [+0.4, +3.1] | 1.000 |  | A better (within ±5pp) |
| pooled | edn-table vs toon | 29 | +0.8 | [-0.8, +2.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 29 | -1.1 | [-3.8, +0.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 29 | -0.4 | [-3.1, +1.9] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 29 | +0.4 | [-0.8, +1.9] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 29 | +0.8 | [-0.8, +2.7] | 1.000 |  | equivalent (±5pp) |

**Paired comparisons — shape:mixed** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 106 | -0.9 | [-3.8, +1.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 106 | -3.8 | [-7.9, -0.0] | 0.016 |  | B better |
| haiku | edn-table-primer vs edn-table | 106 | -0.6 | [-2.8, +1.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 106 | -4.4 | [-8.5, -0.6] | 0.008 |  | B better |
| haiku | edn-table-primer vs json-compact | 106 | -0.6 | [-3.1, +1.9] | 0.500 |  | equivalent (±5pp) |
| haiku | edn-maps vs toon | 106 | -4.7 | [-9.1, -0.9] | 0.016 |  | B better |
| sonnet | edn-maps vs json-compact | 106 | -0.6 | [-3.5, +2.2] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 106 | -1.9 | [-7.2, +3.1] | 0.388 |  | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 106 | +0.9 | [-2.2, +4.4] | 0.219 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 106 | -0.9 | [-5.0, +3.1] | 1.000 |  | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 106 | +0.9 | [-2.2, +4.1] | 0.219 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 106 | -2.5 | [-7.2, +1.9] | 0.754 |  | no detectable difference |
| opus | edn-maps vs json-compact | 106 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 106 | -0.3 | [-0.9, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 106 | -0.6 | [-1.6, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 106 | -0.9 | [-2.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 106 | -0.9 | [-2.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 106 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 106 | -0.5 | [-1.9, +0.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 106 | -2.0 | [-4.6, +0.2] | 0.180 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 106 | -0.1 | [-1.4, +1.1] | 0.688 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 106 | -2.1 | [-4.5, -0.0] | 0.453 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 106 | -0.2 | [-1.4, +0.8] | 0.727 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 106 | -2.4 | [-4.8, -0.4] | 0.180 |  | B better (within ±5pp) |

**Paired comparisons — track:flat** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 109 | -0.6 | [-4.9, +3.7] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 109 | -2.1 | [-5.8, +1.2] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs edn-table | 109 | +0.3 | [-1.8, +2.5] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 109 | -1.8 | [-5.8, +1.5] | 0.688 |  | no detectable difference |
| haiku | edn-table-primer vs json-compact | 109 | +1.8 | [-1.8, +5.8] | 0.375 |  | no detectable difference |
| haiku | edn-maps vs toon | 109 | -4.3 | [-8.9, -0.3] | 0.062 |  | B better |
| sonnet | edn-maps vs json-compact | 109 | +1.2 | [-3.1, +5.2] | 0.754 |  | no detectable difference |
| sonnet | edn-table vs toon | 109 | -4.6 | [-9.2, -0.3] | 0.180 |  | B better |
| sonnet | edn-table-primer vs edn-table | 109 | +0.0 | [-2.5, +2.8] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 109 | -4.6 | [-9.2, -0.3] | 0.549 |  | B better |
| sonnet | edn-table-primer vs json-compact | 109 | +0.3 | [-4.0, +4.6] | 0.754 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 109 | -3.7 | [-9.2, +1.8] | 0.629 |  | no detectable difference |
| opus | edn-maps vs json-compact | 109 | +0.3 | [-0.9, +1.5] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 109 | -2.8 | [-6.1, +0.0] | 0.500 |  | no detectable difference |
| opus | edn-table-primer vs edn-table | 109 | +0.6 | [-0.6, +1.8] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 109 | -2.1 | [-5.5, +0.6] | 0.500 |  | no detectable difference |
| opus | edn-table-primer vs json-compact | 109 | +0.0 | [-1.8, +1.5] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 109 | -1.8 | [-5.2, +0.9] | 0.500 |  | no detectable difference |
| pooled | edn-maps vs json-compact | 109 | +0.3 | [-1.8, +2.2] | 0.727 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 109 | -3.2 | [-6.5, -0.4] | 0.146 |  | B better |
| pooled | edn-table-primer vs edn-table | 109 | +0.3 | [-0.9, +1.5] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 109 | -2.9 | [-6.3, -0.1] | 0.180 |  | B better |
| pooled | edn-table-primer vs json-compact | 109 | +0.7 | [-1.3, +2.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 109 | -3.3 | [-7.0, -0.0] | 0.302 |  | B better |

**Paired comparisons — track:mixed** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 135 | +0.0 | [-2.5, +2.2] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 135 | -2.7 | [-6.2, +0.5] | 0.070 |  | no detectable difference |
| haiku | edn-table-primer vs edn-table | 135 | -0.7 | [-2.7, +1.2] | 0.500 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 135 | -3.5 | [-6.9, -0.2] | 0.021 |  | B better |
| haiku | edn-table-primer vs json-compact | 135 | +0.0 | [-2.0, +2.0] | 0.500 |  | equivalent (±5pp) |
| haiku | edn-maps vs toon | 135 | -3.5 | [-6.9, -0.2] | 0.039 |  | B better |
| sonnet | edn-maps vs json-compact | 135 | -0.2 | [-2.7, +2.0] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 135 | -1.2 | [-5.4, +2.7] | 0.388 |  | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 135 | +0.2 | [-2.5, +3.0] | 0.453 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 135 | -1.0 | [-4.2, +2.2] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 135 | +0.5 | [-2.0, +3.2] | 0.453 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 135 | -1.7 | [-5.4, +1.7] | 0.754 |  | no detectable difference |
| opus | edn-maps vs json-compact | 135 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 135 | -0.2 | [-0.7, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 135 | -0.5 | [-1.2, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 135 | -0.7 | [-2.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 135 | -0.7 | [-2.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 135 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 135 | -0.1 | [-1.1, +1.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 135 | -1.4 | [-3.5, +0.4] | 0.180 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 135 | -0.3 | [-1.4, +0.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 135 | -1.7 | [-3.6, -0.1] | 0.289 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 135 | -0.1 | [-1.0, +0.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 135 | -1.7 | [-3.5, -0.1] | 0.180 |  | B better (within ±5pp) |

**Sensitivity — lenient grader, overall, pooled**

| A vs B | diff | 95% CI | verdict |
|---|---|---|---|
| edn-maps vs json-compact | +0.1 | [-1.0, +1.2] | equivalent (±5pp) |
| edn-table vs toon | -2.1 | [-3.9, -0.4] | B better (within ±5pp) |
| edn-table-primer vs edn-table | -0.2 | [-1.0, +0.6] | equivalent (±5pp) |
| edn-table-primer vs toon | -2.2 | [-4.0, -0.6] | B better (within ±5pp) |
| edn-table-primer vs json-compact | +0.3 | [-0.8, +1.4] | equivalent (±5pp) |
| edn-maps vs toon | -2.4 | [-4.3, -0.6] | B better (within ±5pp) |

**Sensitivity — excluding batches with a fake tool call, overall, pooled**

| A vs B | diff | 95% CI | verdict |
|---|---|---|---|
| edn-maps vs json-compact | +0.1 | [-1.0, +1.1] | equivalent (±5pp) |
| edn-table vs toon | -2.1 | [-3.9, -0.5] | B better (within ±5pp) |
| edn-table-primer vs edn-table | -0.1 | [-1.0, +0.8] | equivalent (±5pp) |
| edn-table-primer vs toon | -2.2 | [-4.0, -0.6] | B better (within ±5pp) |
| edn-table-primer vs json-compact | +0.3 | [-0.9, +1.3] | equivalent (±5pp) |
| edn-maps vs toon | -2.4 | [-4.3, -0.7] | B better (within ±5pp) |
<!-- END:ACCURACY_TABLES -->

<!-- BEGIN:EXTERNAL -->
**External check vs upstream (Haiku 4.5)**

| format | n | upstream single-question | ours, batched (mean 3 seeds) | per-question agreement (majority) |
|---|---|---|---|---|
| json-compact | 244 | 61.9 | 61.1 | 93.4 |
| toon | 244 | 65.6 | 64.6 | 95.1 |
| csv | 109 | 49.5 | 51.4 | 99.1 |
<!-- END:EXTERNAL -->

**Opus caveat:** Opus 5.5 kept using hidden adaptive thinking (665–957 tokens
per call) under every CLI control available (D5). Its near-ceiling accuracy
(97–98%) is therefore *with reasoning*. Opus spent the least thinking on TOON
(665 tokens per call) and the most on CSV (957) and EDN-maps (756).

## 5. Generation check

<!-- BEGIN:GENERATION -->
**Generation check** (20 records × 3 samples = 60 per cell; Wilson 95% CI). Parse-valid for EDN requires both edn-data and edn_format to accept.

| model | format | parse-valid | lossless round-trip | canonical form |
|---|---|---|---|---|
| haiku | edn-table | 58/60 (97%, [89, 99]) | 50/60 (83%, [72, 91]) | 37/60 (62%, [49, 73]) |
| haiku | edn-maps | 58/60 (97%, [89, 99]) | 57/60 (95%, [86, 98]) | 54/60 (90%, [80, 95]) |
| haiku | toon | 40/60 (67%, [54, 77]) | 30/60 (50%, [38, 62]) | 30/60 (50%, [38, 62]) |
| sonnet | edn-table | 60/60 (100%, [94, 100]) | 50/60 (83%, [72, 91]) | 35/60 (58%, [46, 70]) |
| sonnet | edn-maps | 58/60 (97%, [89, 99]) | 57/60 (95%, [86, 98]) | 54/60 (90%, [80, 95]) |
| sonnet | toon | 43/60 (72%, [59, 81]) | 41/60 (68%, [56, 79]) | 41/60 (68%, [56, 79]) |
| opus | edn-table | 60/60 (100%, [94, 100]) | 57/60 (95%, [86, 98]) | 45/60 (75%, [63, 84]) |
| opus | edn-maps | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) |
| opus | toon | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) |

**Generation lossless rate by record shape** (all models)

| shape | edn-table | edn-maps | toon |
|---|---|---|---|
| flat | 60/63 (95%, [87, 98]) | 57/63 (90%, [81, 96]) | 54/63 (86%, [75, 92]) |
| nested | 58/63 (92%, [83, 97]) | 63/63 (100%, [94, 100]) | 49/63 (78%, [66, 86]) |
| mixed | 39/54 (72%, [59, 82]) | 54/54 (100%, [93, 100]) | 28/54 (52%, [39, 65]) |
<!-- END:GENERATION -->

What the failures were:
- **TOON:**
  - unquoted commas inside values (`It's easier to ask forgiveness, than permission`);
  - CSV-style `""` escaping (`"sensor ""B"" recalibrated"`);
  - inline JSON objects inside a primitive array (`mixed[6]: 1,two,true,null,{"three":3},[4,5]`);
  - wrong row or length counts.
- **EDN-table:** non-uniform arrays forced into a table with `nil` for missing
  keys (lossy: `nil` ≠ absent key). This happens on records M1 and M2 (M2 even for
  Opus). Haiku also tabularised an array of arrays (N5), inventing column
  names.
- **EDN-maps:** an invalid keyword `:first\ name` for the key `"first name"`
  (edn-data accepted it, edn_format rejected it; we count it invalid), and the
  lossy rename `:first-name`. `:2fa`, which begins with a digit and so
  strictly isn't a valid keyword, was accepted by both parsers and counted
  lossless but not canonical. That's a lenient call, and it only affects
  N6.

The fairness caveat is that TOON's prompt carried upstream's one-line primer
(80 tokens), while EDN-table carried the 144-token LONG primer. Haiku 4.5's
knowledge cutoff (Feb 2025) predates TOON.

## 6. Primer break-even (H3)

Per-call cost = primer line + data. The LONG primer is 144 o200k / 143 Qwen3 /
159 Haiku / 206 Claude 5 tokens. Uniform-table families, token-benchmark
prefixes of n records:

<!-- BEGIN:BREAKEVEN -->
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
<!-- END:BREAKEVEN -->

- **Against compact JSON with no primer** (conservative), EDN-table + primer is
  cheaper from **n = 20** records (employees, analytics) or **n = 10** (GitHub
  repos) on o200k and Qwen3. It saves 12–22 tokens per record.
- **Against TOON** it never breaks even on uniform tables: EDN-table is
  0–5 tokens per record *more* than TOON before the primer is added.
- **On nested and semi-uniform data** (orders, event logs), EDN-table is
  *larger* than JSON on o200k and Qwen3, so it never breaks even against JSON.
  It does break even against TOON from 10–20 records on event logs, and from
  20–100 records on orders.
- **If the primer is sent once per conversation** (for example in a system
  prompt) and the payload is the accuracy datasets, one call repays it against
  JSON on every uniform table: saving per call is 821–2,175 o200k tokens against
  144 primer tokens. Against TOON it never pays (see
  `results/analysis/breakeven_calls.csv`).
- **Accuracy:** the primer bought no measurable gain (§4), so its cost is pure
  overhead relative to EDN-table with the short primer.

## 7. Verdicts

Each verdict gives the claim, the evidence and what would change it.

**H1: EDN-maps uses fewer tokens than compact JSON, especially on nested data.**
Refuted on o200k, Qwen3 and Claude Haiku 4.5. Supported, but by only 1–2%, on
the Claude 5 tokenizer.
- **Evidence:** token-benchmark totals, EDN-maps vs compact JSON:

  | tokenizer | flat track | mixed track |
  |---|---|---|
  | o200k | +7.1% | +6.0% |
  | Qwen3 | +5.8% | +6.6% |
  | Haiku 4.5 | +10.5% | +6.6% |
  | Claude 5 | −1.3% | −2.2% |

  Deterministic counts, so no interval is needed. Against TOON on nested
  config:

  | tokenizer | EDN-maps | TOON |
  |---|---|---|
  | o200k | 586 | 589 |
  | Qwen3 | 639 | 643 |
  | Haiku 4.5 | 672 | 698 |
  | Claude 5 | 889 | 866 |
- **What would change it:** a different EDN layout can't help, since
  newline and space cost the same. A tokenizer that merges `" :` or `" "` would;
  the Claude 5 tokenizer partly does.

**H2: EDN-table matches or beats TOON on uniform arrays.** Refuted on tokens;
accuracy is equivalent.
- **Evidence, tokens:** on tabular + analytics + GitHub, EDN-table is larger
  than TOON on every tokenizer:

  | tokenizer | EDN-table vs TOON |
  |---|---|
  | o200k | +8.3% |
  | Qwen3 | +6.5% |
  | Haiku 4.5 | +15.0% |
  | Claude 5 | +11.9% |

  The pre-registered "match" band was ±5%. The overhead is almost entirely
  string quoting, since TOON leaves most strings unquoted. On the all-numeric
  analytics set EDN-table ties TOON on o200k and Qwen3 (+0.1% / 0.0%).
- **Evidence, accuracy:** on the 104 uniform-table questions, pooled
  edn-table vs toon is −1.4 pp, CI [−3.2, +0.4]. That CI lies inside ±5 pp, so
  the two are equivalent.
- **What would change it:** an EDN-table variant that leaves strings
  unquoted would no longer be EDN. Adding a `:count` could recover TOON's
  structural-validation advantage, but not its tokens.

**H3: a primer of about 150 tokens makes up for thinner training data and pays
off at realistic payload sizes.** Not supported. The primer doesn't help,
because there was nothing to make up for.
- **Evidence:**
  - edn-table-primer vs edn-table pooled: −0.1 pp [−0.9, +0.8], equivalent,
    for every model.
  - EDN-table *without* the primer is already equivalent to JSON:
    +0.3 pp [−0.8, +1.4].
  - With the primer, EDN-table is still slightly behind TOON: −2.2 pp
    [−4.0, −0.6], significant but inside the ±5 pp margin.
  - The cost side holds only against JSON: break-even at 10–20 uniform
    records, which is ≤50, so "realistic" by the pre-registered rule. It never
    breaks even against TOON.
- **What would change it:** a model with genuinely weak EDN knowledge. We
  tested only Claude models, and even Haiku needed no primer. It would also
  change if the primer were cached once per session, where it becomes
  negligible.

**H4: models understand EDN about as well as JSON and TOON.** Supported
against JSON. Against TOON, EDN is about 2 pp worse, within the margin.
- **Evidence, vs JSON:** EDN-maps vs json-compact is equivalent for every
  model:

  | model | diff | 95% CI |
  |---|---|---|
  | Haiku | −0.3 pp | [−2.5, +2.1] |
  | Sonnet | +0.4 pp | [−1.9, +2.6] |
  | Opus | +0.1 pp | [−0.4, +0.7] |
  | pooled | +0.1 pp | [−1.1, +1.1] |

  EDN-table vs JSON is also equivalent: pooled +0.3 pp [−0.8, +1.4].
- **Evidence, vs TOON:**
  - Pooled: EDN-maps −2.4 pp [−4.3, −0.7] and EDN-table −2.2 pp [−4.0, −0.5],
    both inside the ±5 pp margin.
  - Haiku alone: EDN-maps −3.8 pp [−6.7, −1.2], a real difference whose CI
    crosses −5 pp.
  - Part of TOON's lead is the 5 structural-validation questions, where TOON's
    declared `[N]` is detectable by design and TOON scores 100% vs 47–60%.
    Excluding them, EDN-table vs TOON is −1.4 pp [−2.8, −0.1].
  - None of the TOON-vs-EDN McNemar tests survives Holm correction. The
    smallest adjusted p is 0.044, for Haiku edn-maps vs toon.
- **What would change it:** non-Claude models, or larger or noisier payloads,
  where more models could hit their limits.

**Uniform tables** (tabular, analytics, GitHub): winner on tokens is **CSV** (flat-only) then **TOON**
(EDN-table is +6.5–15% over TOON, and TOON is 29–42% below compact JSON, depending on tokenizer);
accuracy: all formats equivalent (pooled pairwise CIs inside ±5 pp; e.g. edn-table vs toon −1.4 [−3.2, +0.4]).
Confidence: high on tokens (deterministic, all tokenizers agree), low on accuracy differences (none detectable).
Would change if strings were rare (all-numeric analytics: EDN-table ≈ TOON on o200k/Qwen3).

**Nested config** (1 config, 29 questions): no meaningful winner. Tokens are within about 7% for all four
contenders and the order flips by tokenizer: JSON is smallest on o200k and Qwen3, EDN-table on Haiku 4.5, TOON on
Claude 5. Accuracy is at the ceiling (96–98% pooled). EDN-maps vs JSON pooled +1.5 pp [+0.4, +3.1] passes the
bootstrap rule, but the McNemar p is 1.0 with 29 near-ceiling questions, so I treat it as fragile.
Confidence: low. A larger nested-config set would change it.

**Mixed** (orders, event logs, keyed flags, nested-group contacts): depends on the sub-shape.
- **Semi-uniform event logs:** EDN-table is cheapest vs TOON on every tokenizer (−6 to −13%), but
  compact JSON is cheaper still on o200k, Qwen3 and Haiku.
- **Keyed maps and nested-field-group tables:** TOON wins by far (EDN +34–90%), because EDN-table
  has no equivalent of those forms.
- **Accuracy:** pooled edn-table vs toon −2.0 pp [−4.6, +0.2] is inside the margin. Haiku alone
  favours TOON by 3.8 pp [−7.9, −0.0].
- **Winner:** TOON overall on this track (lowest mixed-track total on Claude 5; within 2% of JSON on o200k).
- **Confidence:** medium.

## 8. Grader audit and failure classification

**Hand audit.** I hand-checked 30 uniformly random graded answers per format
(180 in all, seed 777) against the question, ground truth and answer
([`results/audit/audit_sample.csv`](results/audit/audit_sample.csv) and
[`audit_verdicts.csv`](results/audit/audit_verdicts.csv)). There were **0
grader errors** in the sample. All 45 sampled incorrect answers were clean,
wrong values, so they're comprehension errors.

**Systematic scan.** A full scan of all 11,961 answers found one grader error
class. The integer checker *truncates* decimals instead of rounding. Opus
answered q110 ("average stars", truth 184,558.62, expected `184559`) with the
exact `184558.62`, which was graded wrong. That's **3 false negatives in every
format** (Opus, all seeds) and 0 false positives, so it's perfectly
format-neutral and left as is (upstream checker).

<!-- BEGIN:FAILURES -->
**Failure classification (all graded answers)**

| model | format | correct | comprehension | format (lenient-correct) | format (missing) | call failed |
|---|---|---|---|---|---|---|
| haiku | csv | 168 | 159 | 0 | 0 | 0 |
| haiku | edn-maps | 445 | 287 | 0 | 0 | 0 |
| haiku | edn-table | 455 | 276 | 1 | 0 | 0 |
| haiku | edn-table-primer | 453 | 279 | 0 | 0 | 0 |
| haiku | json-compact | 447 | 285 | 0 | 0 | 0 |
| haiku | toon | 473 | 259 | 0 | 0 | 0 |
| opus | csv | 309 | 18 | 0 | 0 | 0 |
| opus | edn-maps | 714 | 18 | 0 | 0 | 0 |
| opus | edn-table | 710 | 22 | 0 | 0 | 0 |
| opus | edn-table-primer | 710 | 22 | 0 | 0 | 0 |
| opus | json-compact | 713 | 19 | 0 | 0 | 0 |
| opus | toon | 720 | 12 | 0 | 0 | 0 |
| sonnet | csv | 165 | 162 | 0 | 0 | 0 |
| sonnet | edn-maps | 474 | 257 | 1 | 0 | 0 |
| sonnet | edn-table | 473 | 257 | 2 | 0 | 0 |
| sonnet | edn-table-primer | 474 | 258 | 0 | 0 | 0 |
| sonnet | json-compact | 471 | 261 | 0 | 0 | 0 |
| sonnet | toon | 493 | 239 | 0 | 0 | 0 |


**Reply behaviour and per-call cost** (means per batched call)

| model | format | calls | input tok | output tok | Opus thinking tok | replies with visible reasoning | fake tool calls | list-price $/call |
|---|---|---|---|---|---|---|---|---|
| haiku | json-compact | 96 | 5778 | 55 | 0 | 0.0% | 0 | 0.0058 |
| haiku | toon | 96 | 5076 | 84 | 0 | 3.1% | 0 | 0.0055 |
| haiku | edn-maps | 96 | 6209 | 1622 | 0 | 10.4% | 10 | 0.0148 |
| haiku | edn-table | 96 | 5278 | 684 | 0 | 7.3% | 4 | 0.0089 |
| haiku | edn-table-primer | 96 | 5405 | 344 | 0 | 4.2% | 2 | 0.0078 |
| haiku | csv | 51 | 4443 | 721 | 0 | 7.8% | 4 | 0.0080 |
| sonnet | json-compact | 96 | 7848 | 104 | 0 | 3.1% | 0 | 0.0202 |
| sonnet | toon | 96 | 6326 | 137 | 0 | 7.3% | 0 | 0.0168 |
| sonnet | edn-maps | 96 | 7776 | 136 | 0 | 4.2% | 0 | 0.0202 |
| sonnet | edn-table | 96 | 6622 | 167 | 0 | 7.3% | 0 | 0.0178 |
| sonnet | edn-table-primer | 96 | 6784 | 98 | 0 | 3.1% | 0 | 0.0175 |
| sonnet | csv | 51 | 5558 | 76 | 0 | 2.0% | 0 | 0.0138 |
| opus | json-compact | 96 | 7785 | 806 | 741 | 0.0% | 0 | 0.0473 |
| opus | toon | 96 | 6263 | 730 | 665 | 0.0% | 0 | 0.0396 |
| opus | edn-maps | 96 | 7713 | 822 | 756 | 0.0% | 0 | 0.0473 |
| opus | edn-table | 96 | 6559 | 768 | 702 | 0.0% | 0 | 0.0416 |
| opus | edn-table-primer | 96 | 6721 | 759 | 693 | 0.0% | 0 | 0.0421 |
| opus | csv | 51 | 5495 | 1012 | 957 | 0.0% | 0 | 0.0422 |
<!-- END:FAILURES -->

- **Format and parse errors** are rare:
  - no missing answer lines at all (the last-match parser recovered every reply);
  - 4 answers were correct only under the lenient grader: `:email` and
    `:rollout` returned *with the keyword colon*, all on EDN formats. That's
    exactly the EDN-specific format failure the plan anticipated, but at
    4/7,092 EDN answers it is negligible;
  - 11 answers in total contained keyword colons.
- **Behavioural confound (Haiku, and slightly Sonnet):** EDN and CSV payloads
  triggered visible reasoning and *fake tool calls*, where the model writes a
  Clojure or Python script and "runs" it in text. Counts: 10 on EDN-maps, 4 on
  EDN-table, 2 on EDN-table-primer, 4 on CSV, 0 on JSON and TOON. Dropping every
  affected batch for all formats (paired) changes no pooled verdict (§4
  sensitivity table).

## 9. Adversarial review and responses

ADVERSARIAL_PLACEHOLDER

## 10. Skipped, sampled or changed relative to PLAN.md

- **D1:** one line added to the shared answer template for every format,
  `- Do not show your work, reasoning or code`. It was decided after a 21-call
  Haiku pilot showed reasoning and fake tool calls in batched replies, and
  before any main run.
- **D2:** the answer parser takes the *last* `Q<n>:` line instead of the
  first, because reasoning replies restated questions as headers.
- **D3:** the Claude token-counting API was **skipped** (no
  `ANTHROPIC_API_KEY`). Claude counts come from CLI usage deltas instead.
- **D4:** the CLI still injects about 780 tokens of environment
  `<system-reminder>`s (paths, date, model id, user e-mail) into every call. It
  is identical across formats but unlike a bare API call.
- **D5:** effort was pinned to `low` for all models, because the parent
  exported `CLAUDE_EFFORT=high`. Opus 5.5's adaptive thinking could not be
  disabled, so Opus results include hidden reasoning (upstream uses none).
  Partial runs made before this fix are in `results/raw/pilot/` and excluded
  ($4.25).
- **Upstream runner not used:** there was no API key, so calls went through
  headless Claude Code subagents as the task allowed. Questions were batched
  (≤10 per call) instead of upstream's one per call; the external check (§4)
  shows batched Haiku matches upstream within about 1 pp.
- **Tokenizer files:** huggingface.co and openaipublic.blob.core.windows.net
  are blocked by the egress policy, so o200k was rebuilt (and hash-verified)
  and Qwen3's `tokenizer.json` came from npm.
- **Generation-check canonical form:** a bug in my own first canonical check
  was fixed before reporting. It rejected keywords in `:cols` and so marked
  every table non-canonical. The lossless and parse-valid metrics were
  unaffected.
- **Generation parse-validity:** reported as "both edn-data and edn_format
  accept". edn-data alone accepted 6 invalid blocks.
- **Nothing was sampled:** all 244 questions, 3 seeds, 3 models and all
  formats ran with 0 failed calls.

## 11. Reproduce

```bash
cd vendor/toon && pnpm install && cd benchmarks
npx vitest run                                  # 189 tests incl. EDN round trips
node scripts/edn-dump-encodings.ts              # build/encodings.json, results/encodings/
cd ../../.. && tools/setup_tokenizers.sh && python3 -m pytest tools/test_edn_roundtrip.py
python3 tools/tokens.py && python3 tools/claude_tokens.py haiku accuracy,tokens   # etc.
(cd vendor/toon/benchmarks && node scripts/edn-make-tasks.ts) && python3 tools/check_manifest.py
python3 tools/run_accuracy.py <haiku|sonnet|opus> 5
(cd vendor/toon/benchmarks && node scripts/edn-grade.ts) && python3 tools/stats.py
(cd vendor/toon/benchmarks && node scripts/edn-gen.ts tasks) && python3 tools/run_accuracy.py <model> 5 generation
(cd vendor/toon/benchmarks && node scripts/edn-gen.ts grade) && python3 tools/gen_edn_crosscheck.py
python3 tools/token_report.py && python3 tools/report_tables.py
```
