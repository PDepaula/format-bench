/**
 * Generation check (PLAN.md §5).
 *
 *   node scripts/edn-gen.ts tasks   → <repo>/results/generation/tasks.jsonl
 *   node scripts/edn-gen.ts grade   → <repo>/results/generation/graded.csv
 *
 * Each model converts 20 JSON records into edn-table, edn-maps and TOON
 * (3 samples each). Grading: parse-valid (edn-data / strict TOON decode),
 * lossless (decoded value deep-equals the source, key order ignored) and, for
 * the table/tabular forms, canonical form (tables exactly where eligible).
 */
import * as fs from 'node:fs'
import * as path from 'node:path'
import process from 'node:process'
import { parseEDNString } from 'edn-data'
import { decode as decodeToon } from '../../packages/toon/src/index.ts'
import { BENCHMARKS_DIR } from '../src/constants.ts'
import { decodeEdn } from '../src/edn-decode.ts'
import { FORMATS } from '../src/formats.ts'
import { TOON_LONG_PRIMER } from '../src/toon-long-primer.ts'

const REPO_ROOT = path.join(BENCHMARKS_DIR, '..', '..', '..')
const GEN_DIR = path.join(REPO_ROOT, 'generation')
const OUT_DIR = path.join(REPO_ROOT, 'results', 'generation')
const RAW_DIRS = [path.join(REPO_ROOT, 'results', 'raw', 'generation'), path.join(REPO_ROOT, 'results', 'raw', 'generation_toonlong')]
const SAMPLES = 3

const TARGETS: Record<string, { name: string, formatId: string, primer?: string }> = {
  'edn-table': { name: 'EDN (table form)', formatId: 'edn-table-primer' }, // LONG primer
  'edn-maps': { name: 'EDN', formatId: 'edn-maps' }, // SHORT primer
  'toon': { name: 'TOON', formatId: 'toon' }, // upstream primer
  // Post-hoc arm (DEVIATIONS D7): TOON with a ~150-token primer stating its quoting rules.
  'toon-long': { name: 'TOON', formatId: 'toon', primer: TOON_LONG_PRIMER },
}
const MAIN_TARGETS = ['edn-table', 'edn-maps', 'toon']

const records = JSON.parse(fs.readFileSync(path.join(GEN_DIR, 'records.json'), 'utf8')) as { id: string, shape: string, data: any }[]
const example = JSON.parse(fs.readFileSync(path.join(GEN_DIR, 'example.json'), 'utf8'))

function buildPrompt(target: string, record: unknown): string {
  const { name, formatId, primer } = TARGETS[target]!
  const format = { ...FORMATS[formatId]!, ...(primer ? { primer } : {}) }
  const fence = format.fence
  return `Convert the JSON data below to ${name}.

${format.primer}

Example. This JSON:
\`\`\`json
${JSON.stringify(example)}
\`\`\`
is written in ${name} as:
\`\`\`${fence}
${format.encode(example)}
\`\`\`

Now convert this JSON:
\`\`\`json
${JSON.stringify(record)}
\`\`\`

Output only the converted data in a single \`\`\`${fence} code block, with nothing before or after it.`
}

/** Last fenced block, or the whole reply if there is none. */
export function extractBlock(text: string): string {
  const blocks = [...text.matchAll(/```[^\n]*\n([\s\S]*?)```/g)]
  return blocks.length ? blocks.at(-1)![1]!.replace(/\n$/, '') : text.trim()
}

function canonicalJson(value: unknown): string {
  if (Array.isArray(value))
    return `[${value.map(canonicalJson).join(',')}]`
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonicalJson((value as any)[k])}`).join(',')}}`
  }
  return JSON.stringify(value)
}

/** Canonical string of a raw edn-data parse tree (keywords kept distinct, map key order ignored). */
function canonicalRaw(value: any): string {
  if (Array.isArray(value))
    return `[${value.map(canonicalRaw).join(' ')}]`
  if (value && typeof value === 'object' && Array.isArray(value.map))
    return `{${value.map.map(([k, v]: [any, any]) => `${canonicalRaw(k)} ${canonicalRaw(v)}`).sort().join(' ')}}`
  if (value && typeof value === 'object' && typeof value.key === 'string' && Object.keys(value).length === 1)
    return `:${value.key}`
  if (value && typeof value === 'object')
    return `#other${JSON.stringify(value)}`
  return JSON.stringify(typeof value === 'bigint' ? Number(value) : value)
}

const RAW_OPTS = { mapAs: 'doubleArray', keywordAs: 'object', listAs: 'object', setAs: 'object' } as any

function countToonTabularHeaders(text: string): number {
  return (text.match(/\[\d+\]\{[^}]*\}:/g) ?? []).length
}

function grade(target: string, reply: string, source: unknown) {
  const block = extractBlock(reply)
  let parseValid = false
  let lossless = false
  let canonical = false
  let error = ''
  try {
    if (target === 'toon' || target === 'toon-long') {
      const decoded = decodeToon(block)
      parseValid = true
      lossless = canonicalJson(decoded) === canonicalJson(source)
      canonical = lossless && countToonTabularHeaders(block) === countToonTabularHeaders(FORMATS.toon!.encode(source))
    }
    else {
      parseEDNString(block)
      parseValid = true
      const expand = target === 'edn-table'
      const decoded = decodeEdn(block, { expandTables: expand })
      lossless = canonicalJson(decoded) === canonicalJson(source)
      const reference = FORMATS[target]!.encode(source)
      canonical = lossless && canonicalRaw(parseEDNString(block, RAW_OPTS)) === canonicalRaw(parseEDNString(reference, RAW_OPTS))
    }
  }
  catch (e) {
    error = String((e as Error).message).slice(0, 200)
  }
  return { parseValid, lossless, canonical, error, block }
}

const mode = process.argv[2]

if (mode === 'tasks') {
  // `tasks toon-long` writes the post-hoc arm to results/generation_toonlong/.
  const toonLong = process.argv[3] === 'toon-long'
  const outDir = toonLong ? path.join(REPO_ROOT, 'results', 'generation_toonlong') : OUT_DIR
  fs.mkdirSync(outDir, { recursive: true })
  const lines: string[] = []
  for (const record of records) {
    for (const target of toonLong ? ['toon-long'] : MAIN_TARGETS) {
      for (let s = 1; s <= SAMPLES; s++) {
        lines.push(JSON.stringify({ task_id: `${record.id}-${target}-s${s}`, record: record.id, shape: record.shape, format: target, sample: s, prompt: buildPrompt(target, record.data) }))
      }
    }
  }
  fs.writeFileSync(path.join(outDir, 'tasks.jsonl'), `${lines.join('\n')}\n`)
  console.log(`wrote ${lines.length} generation tasks`)
}
else if (mode === 'grade') {
  const byId = new Map(records.map(r => [r.id, r]))
  const header = ['model', 'task_id', 'record', 'shape', 'format', 'sample', 'ok', 'parse_valid', 'lossless', 'canonical', 'error']
  const rows = [header.join(',')]
  const blocks: Record<string, string> = {}
  const files = RAW_DIRS.filter(d => fs.existsSync(d)).flatMap(d => fs.readdirSync(d).filter(f => f.endsWith('.jsonl')).sort().map(f => path.join(d, f)))
  for (const file of files) {
    const latest = new Map<string, any>()
    for (const line of fs.readFileSync(file, 'utf8').split('\n').filter(Boolean)) {
      const rec = JSON.parse(line)
      if (rec.ok || !latest.has(rec.task_id))
        latest.set(rec.task_id, rec)
    }
    for (const rec of latest.values()) {
      const source = byId.get(rec.record)!.data
      const g = rec.ok ? grade(rec.format, rec.text, source) : { parseValid: false, lossless: false, canonical: false, error: 'call failed', block: '' }
      blocks[`${rec.model}/${rec.task_id}`] = g.block
      rows.push([rec.model, rec.task_id, rec.record, rec.shape, rec.format, rec.sample, rec.ok ? 1 : 0, g.parseValid ? 1 : 0, g.lossless ? 1 : 0, g.canonical ? 1 : 0, JSON.stringify(g.error)].join(','))
    }
  }
  fs.writeFileSync(path.join(OUT_DIR, 'graded.csv'), `${rows.join('\n')}\n`)
  fs.writeFileSync(path.join(OUT_DIR, 'extracted_blocks.json'), JSON.stringify(blocks, null, 1))
  console.log(`graded ${rows.length - 1} generation attempts`)
}
else {
  console.error('usage: edn-gen.ts tasks|grade')
  process.exit(1)
}
