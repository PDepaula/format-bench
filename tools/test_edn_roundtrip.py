"""Second, independent losslessness gate: decode every EDN encoding with the
Python `edn_format` parser and compare with the source JSON (key order
included). Run after `node scripts/edn-dump-encodings.ts`.

    python3 -m pytest tools/test_edn_roundtrip.py -q
"""
import json
from pathlib import Path

import edn_format
import pytest
from edn_format import ImmutableDict, ImmutableList, Keyword

ROOT = Path(__file__).resolve().parent.parent
ENC = json.loads((ROOT / "build" / "encodings.json").read_text())


def to_json(value, expand_tables):
    if isinstance(value, Keyword):
        raise AssertionError(f"keyword used as a value: {value}")
    if isinstance(value, (ImmutableList, list, tuple)):
        return [to_json(v, expand_tables) for v in value]
    if isinstance(value, (ImmutableDict, dict)):
        items = list(value.items())
        names = []
        for k, _ in items:
            if isinstance(k, Keyword):
                names.append(k.name)
            elif isinstance(k, str):
                names.append(k)
            else:
                raise AssertionError(f"bad key {k!r}")
        if expand_tables and names == ["cols", "rows"] and all(isinstance(k, Keyword) for k, _ in items):
            cols = [c.name if isinstance(c, Keyword) else c for c in value[Keyword("cols")]]
            rows = value[Keyword("rows")]
            out = []
            for row in rows:
                assert len(row) == len(cols), "ragged table row"
                out.append({c: to_json(v, expand_tables) for c, v in zip(cols, row)})
            return out
        return {n: to_json(v, expand_tables) for n, (_, v) in zip(names, items)}
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return value
    raise AssertionError(f"unsupported {type(value)}: {value!r}")


def canon(x):
    # key order preserved; ints and integral floats compare equal as in JSON
    return json.dumps(x, ensure_ascii=False, sort_keys=False)


CASES = []
for group in ("accuracy", "tokens"):
    for name, fmts in ENC[group].items():
        for fmt in ("edn-maps", "edn-table", "edn-table-oneline", "edn-maps-lines"):
            if fmt in fmts:
                CASES.append((group, name, fmt))


@pytest.mark.parametrize("group,name,fmt", CASES)
def test_roundtrip(group, name, fmt):
    meta = ENC["meta"][f"{group}/{name}"]
    if meta.get("corruption") not in (None, "control"):
        pytest.skip("corrupted variant is intentionally lossy")
    text = ENC[group][name][fmt]
    decoded = to_json(edn_format.loads(text), expand_tables=fmt.startswith("edn-table"))
    source = ENC["sources"][group][name]
    assert canon(decoded) == canon(source)


def test_generation_records_roundtrip():
    import subprocess

    # generation records are covered by the vitest suite; here we re-check the
    # edn_format side using encodings produced by the same encoder.
    out = subprocess.run(
        ["node", "scripts/edn-encode-stdin.ts"],
        cwd=ROOT / "vendor" / "toon" / "benchmarks",
        input=(ROOT / "generation" / "records.json").read_text(),
        capture_output=True, text=True, check=True,
    )
    records = json.loads((ROOT / "generation" / "records.json").read_text())
    enc = json.loads(out.stdout)
    for rec, e in zip(records, enc):
        assert canon(to_json(edn_format.loads(e["edn-maps"]), False)) == canon(rec["data"]), rec["id"]
        assert canon(to_json(edn_format.loads(e["edn-table"]), True)) == canon(rec["data"]), rec["id"]
