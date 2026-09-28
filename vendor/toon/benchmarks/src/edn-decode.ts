import { parseEDNString } from 'edn-data'

/**
 * Decodes EDN produced by `edn.ts` (or by a model) back to plain JSON data using
 * the `edn-data` parser.
 *
 * @remarks
 * Strict on types so a round trip cannot pass by accident: map keys must be
 * keywords or strings, keywords are only accepted as map keys (and inside a
 * table's `:cols`), lists/sets/tags are rejected. With `expandTables`, a map
 * whose keys are exactly `:cols` and `:rows` is expanded into an array of
 * records (a row whose width differs from `:cols` is an error).
 */
export function decodeEdn(text: string, { expandTables }: { expandTables: boolean }): unknown {
  const raw = parseEDNString(text, { mapAs: 'doubleArray', keywordAs: 'object', listAs: 'object', setAs: 'object' } as any)
  return convert(raw, expandTables)
}

function isKeyword(value: unknown): value is { key: string } {
  return typeof value === 'object' && value !== null && !Array.isArray(value) && Object.keys(value).length === 1 && typeof (value as any).key === 'string'
}

function isMap(value: unknown): value is { map: [unknown, unknown][] } {
  return typeof value === 'object' && value !== null && !Array.isArray(value) && Array.isArray((value as any).map) && Object.keys(value).length === 1
}

function keyName(key: unknown): string {
  if (isKeyword(key))
    return key.key
  if (typeof key === 'string')
    return key
  throw new Error(`EDN decode: unsupported map key ${JSON.stringify(key)}`)
}

function convert(value: unknown, expandTables: boolean): unknown {
  if (value === null || typeof value === 'string' || typeof value === 'boolean')
    return value
  if (typeof value === 'number')
    return value
  if (typeof value === 'bigint')
    return Number(value)
  if (Array.isArray(value))
    return value.map(v => convert(v, expandTables))
  if (isKeyword(value))
    throw new Error(`EDN decode: keyword :${value.key} used as a value`)
  if (isMap(value)) {
    const entries = value.map
    const names = entries.map(([k]) => keyName(k))
    if (new Set(names).size !== names.length)
      throw new Error('EDN decode: duplicate map key')

    if (expandTables && names.length === 2 && names[0] === 'cols' && names[1] === 'rows' && entries.every(([k]) => isKeyword(k))) {
      const colsRaw = entries[0]![1]
      const rowsRaw = entries[1]![1]
      if (!Array.isArray(colsRaw) || !Array.isArray(rowsRaw))
        throw new Error('EDN decode: malformed table')
      const cols = colsRaw.map(keyName)
      return rowsRaw.map((row) => {
        if (!Array.isArray(row) || row.length !== cols.length)
          throw new Error('EDN decode: table row width differs from :cols')
        const record: Record<string, unknown> = {}
        cols.forEach((c, i) => {
          record[c] = convert(row[i], expandTables)
        })
        return record
      })
    }

    const out: Record<string, unknown> = {}
    entries.forEach(([, v], i) => {
      out[names[i]!] = convert(v, expandTables)
    })
    return out
  }
  throw new Error(`EDN decode: unsupported value ${JSON.stringify(value)}`)
}
