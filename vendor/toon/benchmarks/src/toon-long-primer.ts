/**
 * Post-hoc TOON primer for the generation check (DEVIATIONS D7): about the
 * same length as the EDN LONG primer, and it states TOON's quoting and escaping
 * rules (from docs/guide/format-overview.md), which the one-line upstream
 * primer omits.
 */
export const TOON_LONG_PRIMER = `TOON primer:
- Objects: one \`key: value\` per line; nested objects indented 2 spaces under \`key:\`.
- Arrays declare length: \`tags[3]: a,b,c\`. Uniform object arrays are tables: \`items[N]{f1,f2}:\` then one indented comma-separated row per record. Other arrays: \`list[N]:\` then \`- item\` lines.
- Strings are unquoted unless empty, padded with spaces, equal to true/false/null, number-like, starting with - or #, or containing a comma, : " \\ [ ] { } or a control character. Quoted strings use "..." with escapes \\\\ \\" \\n \\r \\t.
- Numbers, true, false, null are bare.`
