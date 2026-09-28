/**
 * EDN encoders for the format benchmark.
 *
 * @remarks
 * Two encodings share one serializer:
 *   - `edn-maps`: direct conversion – keyword keys, vectors for arrays, one
 *     space between elements, single line.
 *   - `edn-table`: as `edn-maps`, but every tabular-eligible array (same rule as
 *     TOON's primitive tabular form) becomes `{:cols [...] :rows [...]}`, with
 *     each row after the first on its own line.
 *
 * Both are lossless: see `test/edn.test.ts` (edn-data) and
 * `tools/test_edn_roundtrip.py` (edn_format).
 */

export interface EdnOptions {
  /** Encode tabular-eligible arrays as `{:cols [...] :rows [...]}`. */
  tables: boolean
  /** Separator placed before every table row except the first. */
  rowSeparator?: string
  /** Separator between the elements of the top-level map's array values (layout confound check only). */
  topLevelArraySeparator?: string
}

type Primitive = string | number | boolean | null

// EDN symbol rules restricted to ASCII: may not start with a digit, and a
// leading -, + or . may not be followed by a digit. `:`, `#` and `/` are legal
// constituents in some positions but are excluded to keep decoding trivial.
const KEYWORD_SAFE = /^(?:[A-Z*!_?$%&=<>]|[-+.](?!\d))[\w.*+!?$%&=<>-]*$/i

export function isKeywordSafe(key: string): boolean {
  return KEYWORD_SAFE.test(key)
}

function isPrimitive(value: unknown): value is Primitive {
  return value === null || typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean'
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/**
 * Tabular eligibility: length ≥ 1, every element a plain object with the
 * identical key sequence (≥ 1 key), every value primitive.
 */
export function isTabular(value: unknown[]): value is Record<string, Primitive>[] {
  if (value.length === 0)
    return false

  const first = value[0]
  if (!isPlainObject(first))
    return false

  const keys = Object.keys(first)
  if (keys.length === 0)
    return false

  return value.every((element) => {
    if (!isPlainObject(element))
      return false
    const elementKeys = Object.keys(element)
    if (elementKeys.length !== keys.length || elementKeys.some((k, i) => k !== keys[i]))
      return false
    return elementKeys.every(k => isPrimitive(element[k]))
  })
}

export function encodeString(value: string): string {
  let out = '"'
  for (const char of value) {
    const code = char.codePointAt(0)!
    if (char === '"')
      out += '\\"'
    else if (char === '\\')
      out += '\\\\'
    else if (char === '\n')
      out += '\\n'
    else if (char === '\r')
      out += '\\r'
    else if (char === '\t')
      out += '\\t'
    else if (code < 0x20 || code === 0x7F)
      out += `\\u${code.toString(16).padStart(4, '0')}`
    else
      out += char
  }
  return `${out}"`
}

function encodeNumber(value: number): string {
  if (!Number.isFinite(value))
    throw new Error(`EDN encoder: non-finite number ${value}`)
  // `String` gives the same digits as JSON (e.g. 1e+21, 0.1, -3).
  return String(value)
}

function encodeKey(key: string): string {
  return isKeywordSafe(key) ? `:${key}` : encodeString(key)
}

export function encodePrimitive(value: Primitive): string {
  if (value === null)
    return 'nil'
  if (typeof value === 'string')
    return encodeString(value)
  if (typeof value === 'number')
    return encodeNumber(value)
  return value ? 'true' : 'false'
}

/** Serializes a table node from explicit columns and rows (rows may be ragged – used by structural corruption). */
export function encodeTable(cols: string[], rows: Primitive[][], rowSeparator = '\n'): string {
  const colText = `[${cols.map(encodeKey).join(' ')}]`
  const rowText = rows.map(row => `[${row.map(encodePrimitive).join(' ')}]`).join(rowSeparator)
  return `{:cols ${colText} :rows [${rowText}]}`
}

function encodeValue(value: unknown, options: EdnOptions, depth: number): string {
  if (isPrimitive(value))
    return encodePrimitive(value)

  if (Array.isArray(value)) {
    if (options.tables && isTabular(value)) {
      const cols = Object.keys(value[0]!)
      const rows = value.map(row => cols.map(c => row[c]!))
      return encodeTable(cols, rows, options.rowSeparator ?? '\n')
    }
    const separator = depth === 1 && options.topLevelArraySeparator ? options.topLevelArraySeparator : ' '
    return `[${value.map(v => encodeValue(v, options, depth + 1)).join(separator)}]`
  }

  if (isPlainObject(value)) {
    const keys = Object.keys(value)
    if (keys.length === 2 && keys.includes('cols') && keys.includes('rows'))
      throw new Error('EDN encoder: source map with exactly the keys cols/rows would be ambiguous with the table form')
    const entries = keys.map(k => `${encodeKey(k)} ${encodeValue(value[k], options, depth + 1)}`)
    return `{${entries.join(' ')}}`
  }

  throw new Error(`EDN encoder: unsupported value ${String(value)}`)
}

export function encodeEdn(data: unknown, options: EdnOptions): string {
  return encodeValue(data, options, 0)
}

export const encodeEdnMaps = (data: unknown): string => encodeEdn(data, { tables: false })
export const encodeEdnTable = (data: unknown): string => encodeEdn(data, { tables: true })

/** Short primer shared by `edn-maps` and `edn-table` (the no-primer condition). */
export const EDN_SHORT_PRIMER = 'EDN: Clojure data notation. Maps {:key value}, vectors [a b c], keyword keys (:name), nil for null.'

/** Long primer for `edn-table-primer` (the H3 treatment), frozen in PLAN.md. */
export const EDN_LONG_PRIMER = `EDN (Clojure data notation) primer:
- Map: {key value key value ...}. Keys are keywords like :name (field name = keyword without the colon) or, if not keyword-safe, strings.
- Vector: [a b c], elements separated by whitespace; commas are not used.
- Values: "strings", numbers, true, false, nil (null).
- Table: {:cols [:c1 :c2 ...] :rows [[v1 v2 ...] ...]} is an array of records. Each row vector is one record whose Nth value belongs to the Nth column in :cols. Each row starts on a new line; record count = number of rows.`
