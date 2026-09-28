# Adversarial review (verbatim)

Reviewer: a fresh Opus subagent. It was given only PLAN.md, DEVIATIONS.md,
`results/review/harness.diff` (the diff as of the review) and the raw results.
It was told not to read REPORT.md or results/analysis/. Responses are in
REPORT.md §9.

---

I found 15 issues. None of them overturns the "EDN ≈ JSON" result. Three findings overreach or depart from the pre-registration: "TOON beats EDN" (C4), the H1 verdict wording (C1), and the Haiku verbosity claim (C6). C5 cannot be checked with the inputs I was allowed.

I used only the permitted inputs and re-ran my own analyses from graded.csv, the raw jsonl files, tokens/*, generation/* and the encodings. Scratch files are in /tmp/review/. No repo files were modified.

**Issues**

1. **Major: equivalence comes mostly from questions no format changes (C2, C3, C4).**
   - The number of questions whose correctness varies at all across format × seed: Haiku 64 of 244, Sonnet 68, Opus 16. Opus gets 225 of 244 right in every cell.
   - Haiku and Sonnet sit near the floor on aggregation (28% / 35%) and filtering (17% / 21%). Opus is near the ceiling.
   - Every question that never varies contributes a difference of 0. That narrows the CI and makes ±5pp equivalence almost automatic. For Haiku, ±5pp overall is about ±20pp on the questions that carry signal.
   - Fix: report effects on the informative subset, or fit a model with a random effect per question. Say "equivalent on this benchmark's question mix", not in general.

2. **Major: the "TOON is better" findings are fragile (C4, C2).**
   - The bootstrap resamples questions but ignores that questions come from only 8 non-structural datasets, and effects vary by dataset (event-logs −5.6pp, analytics +1.9pp).
   - Resampling whole datasets, excluding structural questions:

     | comparison | diff | 95% CI |
     |---|---|---|
     | edn-table vs toon | −1.39pp | [−3.03, +0.25] (includes 0) |
     | edn-maps vs toon | −1.35pp | [−3.12, −0.06] |

   - The plan pre-registered McNemar tests with Holm adjustment over the primary family (24 tests). After adjustment only Haiku edn-maps vs toon survives (adjusted p≈0.044).
   - Pooled edn-table vs toon has raw p=0.027, which is about 0.5 after adjustment. Excluding structural questions, raw p=0.064.
   - Verdicts rely on unadjusted CIs across about 6 comparisons × 4 model levels × 15 subsets.

3. **Major: the structural-validation questions (C4).**
   - The truncated and extra-rows questions cannot be answered in JSON or EDN, because neither declares a length. All 3 models × 3 seeds give the same answer every time.
   - Two questions alone move edn-table vs toon from −1.39 to −2.19pp (about 37% of the gap) and TOON vs JSON from +1.72 to +2.50pp.
   - CSV answered "NO" to all 5, including the uncorrupted control, and still scores 4/5. These questions measure a bias toward "NO", not comprehension.
   - Fix: make the headline H4 result the one without structural questions, and report those questions as a separate format-feature test.

4. **Major: layout confound in accuracy (C4, C2).**
   - JSON and EDN are single-line blobs; the event-logs EDN block is one 14,423-character line. TOON puts one record per line.
   - edn-table is byte-identical to edn-maps on event-logs, keyed and nested-group. On those three mixed datasets, "edn-table vs toon" is really single-line EDN vs multi-line TOON.
   - The largest EDN deficit is on event-logs (−5.6pp). The line-broken layout variants were only token-counted, never run for accuracy.
   - Separately, the layout variants have identical token counts to the base encodings on every dataset for both tokenizers. That is plausible for BPE but should be confirmed by diffing the texts.

5. **Major: the H1 verdict departs from the pre-registration (C1).**
   - On the Claude 5 tokenizer, EDN-maps is smaller than JSON on both tracks (token datasets −1.3% flat, −2.2% mixed; accuracy datasets −1.1% / −2.4%). The mixed-track saving is at least the flat one.
   - By the PLAN rule that makes H1 "supported" on that tokenizer, not "marginally true". It is the tokenizer of 2 of the 3 tested models.
   - The other numbers reproduce: o200k +6.0 to +7.1%, Qwen3 +5.2 to +7.0%, Haiku 4.5 +6.6 to +10.9%.
   - The mechanism (`","` / `":"` merging into single tokens) is not shown anywhere in the data: there are no token splits, and it clearly doesn't hold on Claude 5.

6. **Minor: token details for H2 (C2).**
   - "~0% on analytics" is true only on o200k and Qwen3 (+0.1% / 0.0%). On the Claude tokenizers it is +8.4 to +8.8%.
   - The "loses" verdict holds on uniform-table totals: +8.3% / +6.5% / +15.0% / +11.9%.
   - Accuracy is equivalent only pooled. Sonnet alone is −2.9pp [−6.7, +1.0], which is inconclusive. The table form gives no accuracy gain over EDN-maps on uniform tables (−0.5pp).

7. **Major: scope of H3 (C3).**
   - The test compares the long primer with a 29-token short primer, not with no primer. So it cannot answer whether a primer "makes up for training data".
   - The effect is still null on uniform-table questions (+0.3pp [−1.0, +1.6]), so dilution by table-less datasets doesn't explain it.
   - On Claude tokenizers the long primer is 159 tokens (Haiku) and 206 (Claude 5), not ~144.
   - The plan required break-even per tokenizer, but Claude was skipped and this isn't in DEVIATIONS.md. My rough estimate from Claude per-record savings is about 4–12 records, so the conclusion probably holds.
   - "10–20" is an artefact of the grid; the actual crossings are about 6–13 records.
   - Against TOON, EDN-table plus primer does break even on nested families (event-logs about 10 records, orders about 20). "Never cheaper than TOON" holds only for uniform data.

8. **Major: C6 is overclaimed.**
   - The mean of 1,622 output tokens comes from 10 of 96 Haiku EDN-maps calls with fake tool calls (3.5k–29k tokens each). Medians are 62 vs 60 for JSON.
   - CSV, a very familiar format, also had fake tool calls in 4 of 51 calls (Fisher test vs JSON p=0.013). edn-table had 4/96 (p=0.12) and the long-primer variant 2/96. Sonnet and Opus show no effect.
   - The reply I read writes scripts to the CLI's scratchpad path. That points to the Claude Code CLI preamble as the trigger, not unfamiliarity with EDN; it probably would not happen through the raw API.
   - DEVIATIONS D1 says the retest "produced direct answers", but its own file shows s3-b071-edn-table still replied with 32,077 characters.
   - Fix: reword as a rate (about 10% of Haiku calls in a CLI context) with CIs, and report medians.

9. **Major: C5 cannot be checked, and the design can't support it.**
   - The upstream results file is not among the permitted inputs.
   - Even a 1pp match would be weak evidence: upstream is one sample per question, so its standard error is about 3pp at n=244. Only Haiku and only aggregate accuracy were compared, and the template differs (D1 line, CLI preamble).
   - What would matter is whether the TOON−JSON difference is the same with and without batching (ours for Haiku: +3.6pp). Per-question agreement or a small unbatched replication would test that.

10. **Major: Opus is in a different regime (C4 pooled, C1 cost).**
    - Opus thinks despite the settings, and the amount depends on format: mean thinking tokens per call are TOON 665 < edn-table 702 < JSON 741 < edn-maps 756 < CSV 958.
    - Pooling Opus (with reasoning, at the ceiling) with Haiku and Sonnet (no reasoning) pulls pooled differences toward 0.
    - Fix: report pooled results for Haiku and Sonnet only, and count thinking tokens in cost.

11. **Minor: upstream ground-truth bugs (format-neutral).**
    - q233 and q234 expect a field order (…stars, watchers, forks…) that doesn't match the data (…createdAt, updatedAt, pushedAt, stars…). All 54 answers to each are graded wrong; most answers to q234 are "pushedAt", which is correct for the data.
    - q110 expects 184559; the models answer 184558.62, the exact average.
    - A 30-answer-per-format audit could not catch these. Fix: screen for questions wrong in every cell.

12. **Minor: one grader quirk works against EDN.** The prompt says "use the exact string from the data". In EDN that string is `:email`, but the primary grader marks `:email` and `:rollout` wrong. It affects about 4 answers.

13. **Major: the generation check (C7).**
    - **Effective sample size is 20 records, not 60.** The 3 samples per record are near-duplicates: TOON losses sit on 10 records, almost all 3 of 3. Wilson CIs computed on 60 are too narrow by about √3.
    - **Validity checks are not equally strict.** EDN "parse-valid" uses the lenient edn-data parser, which accepted `:"2fa"` and `:first\ name`; edn_format gives 96.7%. TOON uses its strict decoder.
    - **Prompts don't give the same information.** The TOON primer and example show none of TOON's quoting rules. The main TOON failures are exactly unquoted timestamps ("Expected 3 tabular rows, but got 0") and CSV-style `""` escapes. EDN escaping is the same as JSON's.
    - The direction probably holds for lossless output (EDN-table 83% vs TOON 50% / 68%), but the size of the gap depends on the prompt. Fix: record-clustered CIs, a TOON arm with quoting rules, edn_format as the headline parser.

14. **Minor: per-seed columns in stats.py are mislabelled.** It indexes seeds by row order, and execution order was shuffled. 83% of model × format × question lists are not in seed order, so the "seed1/2/3" columns and per-seed Wilson intervals are not per seed.

15. **Minor: pilot and labels.**
    - The pilot ran on main-run batches and informed D1 and D2. The changes were symmetric across formats, but they were decided after seeing data.
    - The labels "edn-maps" and "edn-table" are made-up terms, unlike "json" and "toon".
    - Sonnet used prompt caching despite `DISABLE_PROMPT_CACHING`. This is harmless for the token deltas.

**Which conclusions survive**
- **C1:** the numbers hold. The verdict should be "refuted on o200k, Qwen3 and Haiku 4.5; supported but small (1–2%) on Claude 5", per the pre-registered rule. The mechanism is unverified.
- **C2:** the token result survives, with the analytics caveat. Accuracy equivalence holds only pooled and only weakly (issue 1); Sonnet alone is inconclusive.
- **C3:** survives as "the long primer is no better than the short one". The break-even roughly holds but lacks Claude tokenizers.
- **C4:** "EDN ≈ JSON" is robust in every analysis. "TOON better by ~2pp" is fragile: it doesn't hold up under dataset-level resampling or Holm adjustment, and it is inflated by the structural questions and layout. Call it suggestive at most.
- **C5:** not supported as stated.
- **C6:** reframe as a rare CLI artefact that also hits CSV, not a hidden cost of EDN.
- **C7:** the direction probably holds for Haiku and Sonnet, but the gap is inflated by prompt asymmetry and n=20.
