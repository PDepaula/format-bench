/**
 * Dumps every encoding the EDN study uses, so Python tooling (tokenizers,
 * edn_format round-trip test) sees byte-identical text to what models receive.
 *
 * Output: <repo>/build/encodings.json (large; regenerable) and
 *         <repo>/results/encodings/accuracy/<dataset>.<format>.txt (the exact data blocks sent to models).
 */
import * as fs from 'node:fs'
import * as path from 'node:path'
import { encode as gptEncode } from 'gpt-tokenizer'
import { BENCHMARKS_DIR } from '../src/constants.ts'
import { ACCURACY_DATASETS, TOKEN_EFFICIENCY_DATASETS } from '../src/datasets.ts'
import { encodeEdn } from '../src/edn.ts'
import { FORMATS, supportsCSV } from '../src/formats.ts'
import { encodeDataset } from '../src/structural-corruption.ts'

const REPO_ROOT = path.join(BENCHMARKS_DIR, '..', '..', '..')

// Data blocks: edn-table-primer shares edn-table's block, so it is not dumped separately.
const TOKEN_FORMATS = ['json-pretty', 'json-compact', 'yaml', 'xml', 'toon', 'csv', 'edn-maps', 'edn-table']
const ACCURACY_FORMATS = ['json-compact', 'toon', 'csv', 'edn-maps', 'edn-table']
const BREAKEVEN_SIZES = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]

const layouts = {
  'edn-table-oneline': (data: unknown) => encodeEdn(data, { tables: true, rowSeparator: ' ' }),
  'edn-maps-lines': (data: unknown) => encodeEdn(data, { tables: false, topLevelArraySeparator: '\n' }),
}

const out: Record<string, any> = {
  primers: Object.fromEntries(Object.values(FORMATS).map(f => [f.name, f.primer])),
  accuracy: {},
  tokens: {},
  breakeven: {},
  sources: { accuracy: {}, tokens: {} },
  meta: {},
  gptTokenizer: { accuracy: {}, tokens: {}, primers: {} },
}

for (const [name, primer] of Object.entries(out.primers))
  out.gptTokenizer.primers[name] = gptEncode(primer as string).length

const accDir = path.join(REPO_ROOT, 'results', 'encodings', 'accuracy')
fs.mkdirSync(accDir, { recursive: true })

for (const dataset of ACCURACY_DATASETS) {
  const entry: Record<string, string> = {}
  for (const fmt of ACCURACY_FORMATS) {
    if (fmt === 'csv' && !supportsCSV(dataset))
      continue
    entry[fmt] = encodeDataset(FORMATS[fmt]!, dataset)
    fs.writeFileSync(path.join(accDir, `${dataset.name}.${fmt}.txt`), entry[fmt]!)
  }
  out.accuracy[dataset.name] = entry
  out.sources.accuracy[dataset.name] = dataset.data
  out.meta[`accuracy/${dataset.name}`] = { ...dataset.metadata, corruption: dataset.corruption?.kind ?? null }
  out.gptTokenizer.accuracy[dataset.name] = Object.fromEntries(Object.entries(entry).map(([f, t]) => [f, gptEncode(t).length]))
}

for (const dataset of TOKEN_EFFICIENCY_DATASETS) {
  const entry: Record<string, string> = {}
  for (const fmt of TOKEN_FORMATS) {
    if (fmt === 'csv' && !supportsCSV(dataset))
      continue
    entry[fmt] = FORMATS[fmt]!.encode(dataset.data)
  }
  for (const [name, fn] of Object.entries(layouts))
    entry[name] = fn(dataset.data)
  out.tokens[dataset.name] = entry
  out.sources.tokens[dataset.name] = dataset.data
  out.meta[`tokens/${dataset.name}`] = { ...dataset.metadata, description: dataset.description }
  out.gptTokenizer.tokens[dataset.name] = Object.fromEntries(Object.entries(entry).map(([f, t]) => [f, gptEncode(t).length]))
}

// Break-even series: prefixes of the token-benchmark datasets.
const families: Record<string, { key: string, dataset: string }> = {
  employees: { key: 'employees', dataset: 'tabular' },
  analytics: { key: 'metrics', dataset: 'analytics' },
  github: { key: 'repositories', dataset: 'github' },
  orders: { key: 'orders', dataset: 'nested' },
  'event-logs': { key: 'logs', dataset: 'event-logs' },
}
for (const [family, { key, dataset }] of Object.entries(families)) {
  const source = TOKEN_EFFICIENCY_DATASETS.find(d => d.name === dataset)!
  const rows = source.data[key] as unknown[]
  out.breakeven[family] = {}
  for (const n of BREAKEVEN_SIZES.filter(n => n <= rows.length)) {
    const data = { [key]: rows.slice(0, n) }
    out.breakeven[family][n] = Object.fromEntries(['json-compact', 'toon', 'edn-maps', 'edn-table'].map(f => [f, FORMATS[f]!.encode(data)]))
  }
}

fs.mkdirSync(path.join(REPO_ROOT, 'build'), { recursive: true })
fs.writeFileSync(path.join(REPO_ROOT, 'build', 'encodings.json'), JSON.stringify(out))
console.log('wrote build/encodings.json and results/encodings/accuracy/*')
