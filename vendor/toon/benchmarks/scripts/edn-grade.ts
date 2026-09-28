/**
 * Grades the EDN study's raw accuracy results (PLAN.md §4).
 *
 * - Parses "Q<n>: <answer>" lines from each batched reply.
 * - Primary grade: upstream `compareAnswers`, unchanged.
 * - Secondary grade: pre-registered format-agnostic lenient normaliser, then
 *   `compareAnswers` (used only for failure classification / sensitivity).
 *
 * Output: <repo>/results/accuracy/graded.csv (one row per model × seed × format × question)
 */
import type { AnswerType } from '../src/normalize.ts'
import type { Question } from '../src/types.ts'
import * as fs from 'node:fs'
import * as path from 'node:path'
import { BENCHMARKS_DIR } from '../src/constants.ts'
import { ACCURACY_DATASETS } from '../src/datasets.ts'
import { compareAnswers } from '../src/normalize.ts'
import { generateQuestions } from '../src/questions/index.ts'

const REPO_ROOT = path.join(BENCHMARKS_DIR, '..', '..', '..')
const RAW_DIR = path.join(REPO_ROOT, 'results', 'raw', 'accuracy')

export const SHAPES: Record<string, string> = {
  'tabular': 'uniform-tables',
  'analytics': 'uniform-tables',
  'github': 'uniform-tables',
  'nested-config': 'nested-config',
  'nested': 'mixed',
  'event-logs': 'mixed',
  'keyed': 'mixed',
  'nested-group': 'mixed',
}

const ANSWER_LINE = /^\s*\**Q?(\d+)\**\s*[:.)]\s*(.*)$/

/**
 * Maps question number → answer text. The LAST occurrence wins (deviation D2
 * from PLAN.md's "first match wins": replies that restate questions as
 * "Q1: <question>" headers before a final answer block would otherwise be
 * graded on the header).
 */
export function parseAnswers(text: string): Map<number, string> {
  const answers = new Map<number, string>()
  for (const line of text.split('\n')) {
    const m = line.match(ANSWER_LINE)
    if (!m)
      continue
    const n = Number(m[1])
    answers.set(n, m[2]!.replace(/^\*+\s*|\s*\*+$/g, '').trim())
  }
  return answers
}

/** Pre-registered lenient normaliser (identical for all formats). */
export function lenient(answer: string, type: AnswerType): string {
  let s = answer.trim().replace(/^`+|`+$/g, '').trim()
  if (/^\[[\s\S]*\]$/.test(s) || /^\([\s\S]*\)$/.test(s))
    s = s.slice(1, -1).trim()
  const stripItem = (item: string) => item.trim().replace(/^:/, '').replace(/^["']|["']$/g, '').trim()
  if (type === 'csv-list-ordered' || type === 'csv-list-unordered') {
    if (!s.includes(',') && /\s/.test(s))
      s = s.split(/\s+/).join(',')
    return s.split(',').map(stripItem).join(',')
  }
  return stripItem(s)
}

function csvCell(value: unknown): string {
  const s = String(value ?? '')
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
}

const questions = new Map<string, Question>(generateQuestions().map(q => [q.id, q]))
const datasetTrack = new Map(ACCURACY_DATASETS.map(d => [d.name, d.metadata.supportsCSV ? 'flat' : 'mixed']))

const header = ['model', 'served_model', 'seed', 'batch_id', 'format', 'dataset', 'track', 'shape', 'question_id', 'type', 'answer_type', 'position', 'batch_size', 'expected', 'answer', 'parsed', 'correct', 'correct_lenient', 'error_class', 'verbose']
const rows: string[] = [header.join(',')]
const stats: Record<string, number> = {}

for (const file of fs.readdirSync(RAW_DIR).filter(f => f.endsWith('.jsonl')).sort()) {
  const latest = new Map<string, any>()
  for (const line of fs.readFileSync(path.join(RAW_DIR, file), 'utf8').split('\n').filter(Boolean)) {
    const rec = JSON.parse(line)
    // keep the last ok record per task (a failed attempt is superseded by a later success)
    if (rec.ok || !latest.has(rec.task_id))
      latest.set(rec.task_id, rec)
  }

  for (const rec of latest.values()) {
    const answers = rec.ok ? parseAnswers(rec.text) : new Map<number, string>()
    rec.question_ids.forEach((qid: string, i: number) => {
      const q = questions.get(qid)!
      const type = (q.answerType ?? 'string') as AnswerType
      const parsed = answers.has(i + 1)
      const answer = answers.get(i + 1) ?? ''
      const correct = parsed && compareAnswers(answer, q.groundTruth, type, q.normalizationOptions).match
      const correctLenient = parsed && (correct || compareAnswers(lenient(answer, type), q.groundTruth, type, q.normalizationOptions).match)
      const errorClass = correct ? '' : !rec.ok ? 'call-failed' : !parsed ? 'format-missing' : correctLenient ? 'format-lenient' : 'comprehension'
      const verbose = parsed && answer.length > 60 && q.groundTruth.length < 30
      stats[errorClass || 'correct'] = (stats[errorClass || 'correct'] ?? 0) + 1
      rows.push([
        rec.model,
        (rec.served_models ?? []).join('|'),
        rec.seed,
        rec.batch_id,
        rec.format,
        rec.dataset,
        datasetTrack.get(rec.dataset),
        SHAPES[rec.dataset] ?? 'structural-validation',
        qid,
        q.type,
        type,
        i + 1,
        rec.question_ids.length,
        q.groundTruth,
        answer,
        parsed ? 1 : 0,
        correct ? 1 : 0,
        correctLenient ? 1 : 0,
        errorClass,
        verbose ? 1 : 0,
      ].map(csvCell).join(','))
    })
  }
}

fs.writeFileSync(path.join(REPO_ROOT, 'results', 'accuracy', 'graded.csv'), `${rows.join('\n')}\n`)
console.log(`graded ${rows.length - 1} answers`, stats)
