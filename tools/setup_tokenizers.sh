#!/usr/bin/env bash
# Rebuilds the tokenizer files used by tools/tokens.py without huggingface.co or
# openaipublic.blob.core.windows.net (both blocked by this environment's egress policy).
#  - o200k_base: rebuilt from the ranks bundled in the benchmark's gpt-tokenizer
#    dependency; tiktoken verifies the result against its pinned sha256.
#  - Qwen3: tokenizer.json from npm package @lenml/tokenizer-qwen3@3.7.2.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/build/tokenizers"
mkdir -p "$OUT"
cd "$ROOT/vendor/toon/benchmarks"
cat > "$OUT/dump-o200k.mjs" <<'JS'
import ranks from './node_modules/gpt-tokenizer/esm/bpeRanks/o200k_base.js'
import fs from 'node:fs'
const enc = new TextEncoder()
const lines = ranks.map((t, i) => Buffer.from(typeof t === 'string' ? enc.encode(t) : Uint8Array.from(t)).toString('base64') + ' ' + i)
fs.writeFileSync(process.argv[2], lines.join('\n') + '\n')
JS
cp "$OUT/dump-o200k.mjs" ./.dump-o200k.mjs
node ./.dump-o200k.mjs "$OUT/o200k_base.tiktoken"; rm ./.dump-o200k.mjs
sha256sum "$OUT/o200k_base.tiktoken"
cd "$OUT"
npm pack @lenml/tokenizer-qwen3@3.7.2 >/dev/null 2>&1
tar xzf lenml-tokenizer-qwen3-3.7.2.tgz package/models/tokenizer.json
mv package/models/tokenizer.json qwen3-tokenizer.json && rm -rf package lenml-tokenizer-qwen3-3.7.2.tgz
sha256sum qwen3-tokenizer.json
