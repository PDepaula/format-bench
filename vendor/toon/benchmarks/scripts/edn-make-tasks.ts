/**
 * Builds the accuracy task manifest for the EDN study (PLAN.md §4):
 * 3 seeds; per seed the 244 questions are shuffled with a seeded PRNG, grouped
 * by dataset in shuffled order and split into ⌈n/10⌉ near-equal batches. Every
 * format gets the same batches (paired design). CSV only on flat datasets.
 *
 * Output: <repo>/results/accuracy/tasks.jsonl and questions.json
 */
import * as fs from 'node:fs'
import * as path from 'node:path'
import process from 'node:process'
import { BENCHMARKS_DIR } from '../src/constants.ts'
import { ACCURACY_DATASETS } from '../src/datasets.ts'
import { buildBatchPrompt } from '../src/evaluate.ts'
import { FORMATS, supportsCSV } from '../src/formats.ts'
import { generateQuestions } from '../src/questions/index.ts'
import { encodeDataset } from '../src/structural-corruption.ts'

const REPO_ROOT = path.join(BENCHMARKS_DIR, '..', '..', '..')
// `node scripts/edn-make-tasks.ts layout` builds the post-hoc layout-confound
// manifest (DEVIATIONS D6): edn-table-lines on the mixed-track batches only.
const LAYOUT = process.argv[2] === 'layout'
const OUT_DIR = path.join(REPO_ROOT, 'results', LAYOUT ? 'accuracy_layout' : 'accuracy')
const SEEDS = [1, 2, 3]
const BATCH_MAX = 10
const STUDY_FORMATS = LAYOUT ? ['edn-table-lines'] : ['json-compact', 'toon', 'edn-maps', 'edn-table', 'edn-table-primer', 'csv']

export function mulberry32(seed: number): () => number {
  let a = seed >>> 0
  return () => {
    a = (a + 0x6D2B79F5) >>> 0
    let t = a
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function shuffle<T>(items: T[], rand: () => number): T[] {
  const a = [...items]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1))
    ;[a[i], a[j]] = [a[j]!, a[i]!]
  }
  return a
}

const questions = generateQuestions()
if (questions.length !== 244)
  throw new Error(`expected 244 questions, got ${questions.length}`)

fs.mkdirSync(OUT_DIR, { recursive: true })
fs.writeFileSync(path.join(OUT_DIR, 'questions.json'), JSON.stringify(questions.map((q) => {
  const ds = ACCURACY_DATASETS.find(d => d.name === q.dataset)!
  return { ...q, track: ds.metadata.supportsCSV ? 'flat' : 'mixed' }
}), null, 1))

const lines: string[] = []
let batchCounter = 0
for (const seed of SEEDS) {
  const shuffled = shuffle(questions, mulberry32(seed * 7919))
  const datasetOrder: string[] = []
  const byDataset = new Map<string, typeof questions>()
  for (const q of shuffled) {
    if (!byDataset.has(q.dataset)) {
      byDataset.set(q.dataset, [])
      datasetOrder.push(q.dataset)
    }
    byDataset.get(q.dataset)!.push(q)
  }

  for (const dsName of datasetOrder) {
    const qs = byDataset.get(dsName)!
    const k = Math.ceil(qs.length / BATCH_MAX)
    const base = Math.floor(qs.length / k)
    const extra = qs.length % k
    let start = 0
    for (let b = 0; b < k; b++) {
      const size = base + (b < extra ? 1 : 0)
      const batch = qs.slice(start, start + size)
      start += size
      const batchId = `s${seed}-b${String(batchCounter++).padStart(3, '0')}`
      const dataset = ACCURACY_DATASETS.find(d => d.name === dsName)!
      for (const fmt of STUDY_FORMATS) {
        if (fmt === 'csv' && !supportsCSV(dataset))
          continue
        if (LAYOUT && supportsCSV(dataset))
          continue
        const format = FORMATS[fmt]!
        const data = encodeDataset(format, dataset)
        lines.push(JSON.stringify({
          task_id: `${batchId}-${fmt}`,
          seed,
          batch_id: batchId,
          dataset: dsName,
          format: fmt,
          question_ids: batch.map(q => q.id),
          prompt: buildBatchPrompt(format, data, batch),
        }))
      }
    }
  }
}

fs.writeFileSync(path.join(OUT_DIR, 'tasks.jsonl'), `${lines.join('\n')}\n`)
console.log(`wrote ${lines.length} tasks`)
