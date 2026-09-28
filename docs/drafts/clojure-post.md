<!-- DRAFT, not posted. Target: r/Clojure or ClojureVerse. Replace <repo-url> before posting. -->

**Title:** Is EDN viable as an LLM data format? I benchmarked it against JSON and TOON

I've wondered whether it's worth passing EDN straight to LLMs (tool-call arguments, context
payloads, structured output) instead of converting to JSON at the boundary. So I ran EDN
through TOON's own retrieval benchmark: 244 questions, 13 datasets, 3 Claude models
(Haiku 4.5, Sonnet 5, Opus 5.5), 3 seeds, plus token counts on four tokenizers and a check
of how well models *write* EDN. The plan was pre-registered before any results existed, and
an adversarial review was run on the results.

What I found:

- **Comprehension: EDN ties JSON.** Models answer questions about EDN maps as accurately
  as about compact JSON: +0.5 pp for Haiku+Sonnet pooled, 95% CI [−1.7, +2.5], and inside a
  ±5 pp equivalence margin for every model. A 150-token "how to read EDN" primer made no
  difference, because nothing needed fixing.
- **Tokens: EDN is not a saver.** EDN maps are 6–10% *larger* than compact JSON on
  OpenAI's o200k, Qwen3 and Claude Haiku 4.5 tokenizers, and only 1–2% smaller on the
  Claude 5 tokenizer. Dropping the quotes around keys saves nothing, because BPE already
  merges `","` and `":"` into single tokens, while EDN needs `" :` and spaces before numbers.
  A columnar EDN layout (`{:cols [...] :rows [[...]]}`) is 24–35% smaller than JSON on
  uniform tables, but still 6.5–15% larger than TOON.
- **Generation: models write EDN reliably.** Asked to encode records, Haiku produced
  lossless EDN maps 95% of the time vs 50% for TOON (62% with TOON's quoting rules spelled
  out). Sonnet: 95% vs 68% (83%). Opus wrote both perfectly. The EDN failures were telling
  though: an invalid keyword like `:first\ name` for a key with a space, and silently
  renaming `"first name"` to `:first-name`. Keys that aren't valid keywords are the real
  hazard.

So for Clojure-side tooling: EDN is a perfectly reasonable wire format to an LLM if you
care about readability and round-tripping without a JSON layer. Just don't pick it to save
tokens, and use string keys (or validate keywords) when keys come from outside.

Caveats: Claude models only, called through headless Claude Code rather than the raw API,
and the generation check is 20 records per cell, so its intervals are wide. Everything is
in the repo, including the raw replies, the deviations log and the review:
<repo-url>
