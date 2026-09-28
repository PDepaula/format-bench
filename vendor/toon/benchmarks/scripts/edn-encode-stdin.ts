/** Reads `[{data}, ...]` JSON on stdin and prints the edn-maps / edn-table / toon encodings of each `data`. */
import * as fs from 'node:fs'
import { FORMATS } from '../src/formats.ts'

const records = JSON.parse(fs.readFileSync(0, 'utf8')) as { data: unknown }[]
console.log(JSON.stringify(records.map(r => ({
  'edn-maps': FORMATS['edn-maps']!.encode(r.data),
  'edn-table': FORMATS['edn-table']!.encode(r.data),
  'toon': FORMATS.toon!.encode(r.data),
}))))
