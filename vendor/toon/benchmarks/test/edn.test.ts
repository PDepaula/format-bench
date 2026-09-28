import * as fs from 'node:fs'
import * as path from 'node:path'
import { describe, expect, it } from 'vitest'
import { decode as decodeToon } from '../../packages/toon/src/index.ts'
import { BENCHMARKS_DIR } from '../src/constants.ts'
import { ACCURACY_DATASETS, TOKEN_EFFICIENCY_DATASETS } from '../src/datasets.ts'
import { decodeEdn } from '../src/edn-decode.ts'
import { encodeEdn, encodeEdnMaps, encodeEdnTable, isKeywordSafe, isTabular } from '../src/edn.ts'
import { FORMATS } from '../src/formats.ts'
import { encodeDataset } from '../src/structural-corruption.ts'

const REPO_ROOT = path.join(BENCHMARKS_DIR, '..', '..', '..')
const generation = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'generation', 'records.json'), 'utf8')) as { id: string, data: unknown }[]
const example = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'generation', 'example.json'), 'utf8'))

// Key-order-sensitive deep equality: JSON.stringify follows insertion order.
function expectIdentical(actual: unknown, expected: unknown) {
  expect(JSON.stringify(actual)).toBe(JSON.stringify(expected))
}

const cases: [string, unknown][] = [
  ...ACCURACY_DATASETS.map(d => [`accuracy/${d.name}`, d.data] as [string, unknown]),
  ...TOKEN_EFFICIENCY_DATASETS.map(d => [`tokens/${d.name}`, d.data] as [string, unknown]),
  ...generation.map(r => [`generation/${r.id}`, r.data] as [string, unknown]),
  ['generation/example', example],
]

describe('EDN encoders are lossless (edn-data parser)', () => {
  for (const [name, data] of cases) {
    it(`edn-maps round-trips ${name}`, () => {
      const text = encodeEdnMaps(data)
      expect(text).not.toMatch(/:cols \[/)
      expectIdentical(decodeEdn(text, { expandTables: false }), data)
    })

    it(`edn-table round-trips ${name}`, () => {
      expectIdentical(decodeEdn(encodeEdnTable(data), { expandTables: true }), data)
    })

    it(`layout variants round-trip ${name}`, () => {
      expectIdentical(decodeEdn(encodeEdn(data, { tables: true, rowSeparator: ' ' }), { expandTables: true }), data)
      expectIdentical(decodeEdn(encodeEdn(data, { tables: false, topLevelArraySeparator: '\n' }), { expandTables: false }), data)
    })

    it(`toon round-trips ${name}`, () => {
      expect(decodeToon(FORMATS.toon!.encode(data))).toEqual(data)
    })
  }
})

describe('EDN encoding rules', () => {
  it('uses keywords only for keyword-safe keys', () => {
    expect(isKeywordSafe('orderId')).toBe(true)
    expect(isKeywordSafe('pt-BR')).toBe(true)
    expect(isKeywordSafe('first name')).toBe(false)
    expect(isKeywordSafe('2fa')).toBe(false)
    expect(isKeywordSafe('-1x')).toBe(false)
    expect(isKeywordSafe('a/b')).toBe(false)
    expect(encodeEdnMaps({ 'first name': 'Ann', 'ok': 1 })).toBe('{"first name" "Ann" :ok 1}')
  })

  it('encodes scalars like JSON does', () => {
    expect(encodeEdnMaps({ a: [1, 2.5, -3, null, true, false, 'x"y\n\\', ''] })).toBe('{:a [1 2.5 -3 nil true false "x\\"y\\n\\\\" ""]}')
  })

  it('tabularizes exactly the TOON-primitive-tabular arrays', () => {
    expect(isTabular([{ a: 1, b: 'x' }, { a: 2, b: null }])).toBe(true)
    expect(isTabular([{ a: 1, b: 'x' }, { b: 'y', a: 2 }])).toBe(false)
    expect(isTabular([{ a: 1, b: { c: 1 } }])).toBe(false)
    expect(isTabular([{ a: 1 }, 2])).toBe(false)
    expect(isTabular([])).toBe(false)
    expect(encodeEdnTable({ t: [{ a: 1, b: 'x' }, { a: 2, b: 'y' }] })).toBe('{:t {:cols [:a :b] :rows [[1 "x"]\n[2 "y"]]}}')
  })

  it('refuses source maps that collide with the table form', () => {
    expect(() => encodeEdnTable({ cols: [], rows: [] })).toThrow()
    expect(() => encodeEdnMaps({ x: { rows: 1, cols: 2 } })).toThrow()
  })
})

describe('EDN structural corruption', () => {
  const byName = Object.fromEntries(ACCURACY_DATASETS.map(d => [d.name, d]))
  const control = byName['structural-validation-control']!

  for (const fmt of ['edn-maps', 'edn-table', 'edn-table-primer']) {
    const format = FORMATS[fmt]!
    const expand = fmt !== 'edn-maps'

    it(`${fmt}: control is the plain encoding`, () => {
      expect(encodeDataset(format, control)).toBe(format.encode(control.data))
    })

    it(`${fmt}: truncated drops 3 records`, () => {
      const text = encodeDataset(format, byName['structural-validation-truncated']!)
      expect((decodeEdn(text, { expandTables: expand }) as any).employees).toHaveLength(17)
    })

    it(`${fmt}: extra rows appends 3 records`, () => {
      const text = encodeDataset(format, byName['structural-validation-extra-rows']!)
      expect((decodeEdn(text, { expandTables: expand }) as any).employees).toHaveLength(23)
    })

    it(`${fmt}: width mismatch removes salary from record 10`, () => {
      const text = encodeDataset(format, byName['structural-validation-width-mismatch']!)
      if (expand) {
        expect(() => decodeEdn(text, { expandTables: true })).toThrow(/width/)
        const rows = text.split('\n')
        expect(rows[9]!.slice(1, -1).trim().length).toBeGreaterThan(0)
      }
      else {
        const employees = (decodeEdn(text, { expandTables: false }) as any).employees
        expect(employees[9].salary).toBeUndefined()
        expect(employees[8].salary).toBeDefined()
      }
    })
  }

  it('edn-table-primer sends the byte-identical data block as edn-table', () => {
    for (const d of ACCURACY_DATASETS)
      expect(encodeDataset(FORMATS['edn-table-primer']!, d)).toBe(encodeDataset(FORMATS['edn-table']!, d))
  })
})
