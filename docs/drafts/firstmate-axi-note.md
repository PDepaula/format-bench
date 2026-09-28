<!-- DRAFT, not posted. Target: kunchenguid's firstmate / axi community. -->

**What a format benchmark says about TOON as the axi default**

firstmate and the axi tools already lean on TOON: `quota-axi`, `no-mistakes axi status` and
firstmate's own bearings snapshot all hand agents TOON by default, with `--json` as the
fallback. I benchmarked TOON against compact JSON and EDN (3 Claude models × 3 seeds ×
244 questions from TOON's own benchmark, pre-registered, adversarially reviewed), and the
results mostly back that choice, with one caveat worth knowing.

**Supports TOON as the agent-facing read format:**

- On uniform tables TOON is 29–42% smaller than compact JSON, depending on tokenizer, and
  the best EDN layout was still 6.5–15% larger than TOON. Only CSV beat it, and only on
  flat data.
- Comprehension is at least as good as JSON: TOON was about +2.5 pp over compact JSON for
  Haiku+Sonnet, CI [+0.4, +5.3]. Small, but it points the right way.
- On mixed payloads the saving shrinks or vanishes (semi-uniform logs: compact JSON was
  cheaper on 3 of 4 tokenizers), so much of the win depends on the output being list- or
  table-shaped.

**The caveat: agents *writing* TOON.**

- When models had to produce TOON themselves, Haiku round-tripped losslessly only 50% of the
  time (62% with TOON's quoting rules in the prompt) and Sonnet 68% (83% with the rules).
  EDN maps were 95% for both. Opus wrote both TOON and EDN maps perfectly.
- The failures were quoting: unquoted commas inside values, CSV-style `""` escaping, inline
  JSON objects inside primitive arrays.

So: TOON as what tools *emit* to agents looks well-founded. For anything where a
smaller model has to *write* TOON that a script then parses (status lines, structured
replies), put the quoting rules in the prompt and validate by round-tripping, or ask for a
format the model writes more reliably (EDN maps did; JSON was not part of this check).

Caveats: Claude models only, called through headless Claude Code; the benchmark's payloads
are larger and more tabular than typical axi output, so the token numbers may not transfer
directly to small status blocks. Full report and raw data: https://github.com/PDepaula/format-bench
