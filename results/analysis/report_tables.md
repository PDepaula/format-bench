
**All 244 questions (CSV: 109 flat questions)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 61.1 [55.2, 66.9] | 64.6 [58.9, 70.2] | 60.8 [54.8, 66.5] | 62.2 [56.6, 67.8] | 61.9 [56.1, 67.6] | 51.4 [42.5, 59.9] |
| sonnet | 64.3 [58.6, 70.0] | 67.3 [61.8, 72.8] | 64.8 [59.0, 70.4] | 64.6 [58.7, 70.4] | 64.8 [58.9, 70.4] | 50.5 [41.3, 59.9] |
| opus | 97.4 [95.4, 99.0] | 98.4 [96.7, 99.6] | 97.5 [95.6, 99.2] | 97.0 [95.0, 98.8] | 97.0 [95.0, 98.8] | 94.5 [90.2, 97.9] |
| pooled | 74.3 [70.3, 78.2] | 76.8 [73.0, 80.5] | 74.4 [70.5, 78.3] | 74.6 [70.6, 78.5] | 74.5 [70.5, 78.5] | 65.4 [59.1, 72.0] |

**Flat-only track (109)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 47.4 [38.5, 56.6] | 51.1 [41.9, 59.9] | 46.8 [37.6, 56.0] | 48.9 [40.1, 58.1] | 49.2 [40.4, 58.4] | 51.4 [42.5, 59.9] |
| sonnet | 48.6 [39.8, 57.8] | 53.5 [44.6, 62.1] | 49.9 [41.3, 58.7] | 48.9 [40.1, 57.5] | 48.9 [39.8, 58.1] | 50.5 [41.6, 59.6] |
| opus | 94.2 [89.6, 97.9] | 96.3 [92.7, 99.1] | 94.5 [89.9, 98.2] | 93.6 [89.3, 97.2] | 94.2 [89.6, 97.9] | 94.5 [90.2, 97.9] |
| pooled | 63.4 [57.0, 69.9] | 67.0 [60.7, 73.1] | 63.7 [57.4, 69.8] | 63.8 [57.5, 70.1] | 64.1 [57.8, 70.3] | 65.4 [58.9, 71.8] |

**Mixed-structure track (135)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 72.1 [64.9, 79.0] | 75.6 [68.4, 82.2] | 72.1 [64.7, 79.3] | 72.8 [65.7, 79.8] | 72.1 [64.9, 78.8] | – |
| sonnet | 77.0 [70.4, 83.2] | 78.5 [71.9, 84.9] | 76.8 [69.9, 83.5] | 77.3 [70.6, 83.7] | 77.5 [70.6, 83.7] | – |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.8 [99.3, 100.0] | 99.3 [98.0, 100.0] | – |
| pooled | 83.0 [78.5, 87.3] | 84.7 [80.2, 88.8] | 83.0 [78.3, 87.4] | 83.3 [78.9, 87.6] | 83.0 [78.3, 87.3] | – |

**Uniform tables (104)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 46.8 [37.5, 56.1] | 48.7 [39.1, 58.0] | 47.1 [37.8, 56.4] | 48.4 [39.4, 57.4] | 48.7 [39.4, 57.7] | 50.0 [41.0, 59.0] |
| sonnet | 48.1 [38.8, 57.4] | 51.3 [42.6, 60.3] | 50.3 [41.7, 59.0] | 48.4 [39.4, 57.7] | 48.4 [39.1, 57.7] | 49.0 [39.7, 58.3] |
| opus | 95.8 [92.0, 98.7] | 96.2 [92.3, 99.0] | 96.2 [92.6, 99.0] | 95.2 [91.3, 98.1] | 95.8 [92.3, 98.7] | 95.2 [91.0, 98.4] |
| pooled | 63.6 [57.3, 69.9] | 65.4 [59.1, 71.5] | 64.5 [58.3, 70.8] | 64.0 [57.4, 70.3] | 64.3 [57.9, 70.6] | 64.7 [58.4, 71.2] |

**Nested config (29)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 89.7 [80.5, 96.5] | 92.0 [83.9, 97.7] | 93.1 [83.9, 100.0] | 93.1 [85.1, 98.9] | 92.0 [82.8, 98.9] | – |
| sonnet | 98.9 [96.5, 100.0] | 98.9 [96.5, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.7 [93.1, 100.0] | – |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | – |
| pooled | 96.2 [92.3, 98.9] | 96.9 [93.9, 99.2] | 97.7 [94.6, 100.0] | 97.7 [95.0, 99.6] | 96.5 [92.0, 99.6] | – |

**Mixed shapes (106)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 67.3 [58.5, 75.8] | 71.1 [62.3, 79.6] | 66.3 [57.2, 74.8] | 67.3 [59.1, 75.5] | 66.7 [58.2, 74.8] | – |
| sonnet | 71.1 [63.2, 78.3] | 73.0 [64.8, 80.8] | 70.4 [62.0, 78.3] | 71.1 [62.9, 78.9] | 72.0 [64.1, 79.6] | – |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.7 [99.1, 100.0] | 99.1 [97.5, 100.0] | – |
| pooled | 79.5 [74.1, 84.6] | 81.3 [76.0, 86.4] | 78.9 [73.4, 84.4] | 79.3 [74.0, 84.6] | 79.2 [73.8, 84.5] | – |

**Structural validation (5)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |
| sonnet | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |
| opus | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |
| pooled | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 46.7 [6.7, 86.7] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] |

**All except structural validation (239)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv |
|---|---|---|---|---|---|---|
| haiku | 61.1 [55.1, 67.0] | 63.9 [57.9, 69.7] | 61.2 [55.1, 67.2] | 62.2 [56.4, 67.9] | 61.9 [55.9, 67.8] | 50.0 [41.0, 59.0] |
| sonnet | 64.4 [59.0, 70.0] | 66.7 [61.1, 72.2] | 65.3 [59.4, 70.9] | 64.7 [58.9, 70.3] | 64.8 [59.1, 70.7] | 49.0 [39.4, 58.7] |
| opus | 98.2 [96.5, 99.4] | 98.3 [96.7, 99.6] | 98.3 [96.7, 99.6] | 97.8 [96.1, 99.2] | 97.8 [96.1, 99.2] | 95.2 [91.3, 98.4] |
| pooled | 74.6 [70.6, 78.4] | 76.3 [72.4, 80.1] | 74.9 [70.9, 78.7] | 74.9 [71.0, 78.8] | 74.9 [71.0, 78.8] | 64.7 [58.1, 71.2] |

**Paired comparisons — overall** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 244 | -0.3 | [-2.5, +2.1] | 1.000 | 1.0 | equivalent (±5pp) |
| haiku | edn-table vs toon | 244 | -2.5 | [-4.9, -0.1] | 0.092 | 1.0 | B better (within ±5pp) |
| haiku | edn-table-primer vs edn-table | 244 | -0.3 | [-1.8, +1.2] | 0.375 | 1.0 | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 244 | -2.7 | [-5.3, -0.4] | 0.021 | 0.48921 | B better |
| haiku | edn-table-primer vs json-compact | 244 | +0.8 | [-1.1, +2.9] | 1.000 | 1.0 | equivalent (±5pp) |
| haiku | edn-maps vs toon | 244 | -3.8 | [-6.7, -1.2] | 0.002 | 0.04392 | B better |
| haiku | toon vs json-compact | 244 | +3.5 | [+1.1, +6.3] | 0.003 |  | A better |
| sonnet | edn-maps vs json-compact | 244 | +0.4 | [-1.9, +2.6] | 0.424 | 1.0 | equivalent (±5pp) |
| sonnet | edn-table vs toon | 244 | -2.7 | [-5.7, +0.3] | 0.078 | 1.0 | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 244 | +0.1 | [-1.8, +2.1] | 0.227 | 1.0 | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 244 | -2.6 | [-5.3, +0.0] | 0.481 | 1.0 | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 244 | +0.4 | [-1.9, +2.7] | 0.332 | 1.0 | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 244 | -2.6 | [-5.9, +0.5] | 0.442 | 1.0 | no detectable difference |
| sonnet | toon vs json-compact | 244 | +3.0 | [+0.3, +6.0] | 0.078 |  | A better |
| opus | edn-maps vs json-compact | 244 | +0.1 | [-0.4, +0.7] | 1.000 | 1.0 | equivalent (±5pp) |
| opus | edn-table vs toon | 244 | -1.4 | [-2.9, -0.1] | 0.500 | 1.0 | B better (within ±5pp) |
| opus | edn-table-primer vs edn-table | 244 | +0.0 | [-0.7, +0.7] | 1.000 | 1.0 | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 244 | -1.4 | [-3.0, +0.0] | 0.250 | 1.0 | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 244 | -0.4 | [-1.4, +0.5] | 1.000 | 1.0 | equivalent (±5pp) |
| opus | edn-maps vs toon | 244 | -0.8 | [-2.3, +0.4] | 0.500 | 1.0 | equivalent (±5pp) |
| opus | toon vs json-compact | 244 | +1.0 | [-0.0, +2.3] | 0.500 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 244 | +0.1 | [-1.1, +1.1] | 0.791 | 1.0 | equivalent (±5pp) |
| pooled | edn-table vs toon | 244 | -2.2 | [-4.0, -0.5] | 0.027 | 0.5852 | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | 244 | -0.1 | [-0.9, +0.8] | 1.000 | 1.0 | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 244 | -2.2 | [-4.0, -0.6] | 0.052 | 1.0 | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 244 | +0.3 | [-0.8, +1.4] | 0.791 | 1.0 | equivalent (±5pp) |
| pooled | edn-maps vs toon | 244 | -2.4 | [-4.3, -0.7] | 0.064 | 1.0 | B better (within ±5pp) |
| pooled | toon vs json-compact | 244 | +2.5 | [+0.9, +4.4] | 0.017 |  | A better (within ±5pp) |

**Paired comparisons — overall-excl-structural** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 239 | +0.1 | [-1.9, +2.2] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 239 | -1.7 | [-3.9, +0.6] | 0.227 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs edn-table | 239 | -0.3 | [-1.8, +1.3] | 0.375 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 239 | -1.9 | [-4.3, +0.3] | 0.057 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs json-compact | 239 | +0.8 | [-1.1, +2.9] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-maps vs toon | 239 | -2.6 | [-5.2, -0.4] | 0.012 |  | B better |
| sonnet | edn-maps vs json-compact | 239 | +0.8 | [-1.4, +2.9] | 0.267 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 239 | -1.9 | [-4.9, +0.8] | 0.167 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs edn-table | 239 | +0.1 | [-1.8, +2.1] | 0.227 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 239 | -1.8 | [-4.3, +0.6] | 0.804 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 239 | +0.4 | [-1.9, +2.9] | 0.332 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 239 | -1.4 | [-4.3, +1.5] | 0.839 |  | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 239 | +0.1 | [-0.4, +0.8] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 239 | -0.6 | [-1.4, +0.3] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 239 | +0.0 | [-0.7, +0.7] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 239 | -0.6 | [-1.5, +0.3] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 239 | -0.4 | [-1.4, +0.6] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 239 | +0.0 | [-0.7, +0.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 239 | +0.4 | [-0.6, +1.3] | 0.581 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 239 | -1.4 | [-2.8, -0.1] | 0.064 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | 239 | -0.1 | [-0.9, +0.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 239 | -1.4 | [-2.8, -0.2] | 0.115 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 239 | +0.3 | [-0.7, +1.4] | 0.791 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 239 | -1.4 | [-2.8, -0.1] | 0.189 |  | B better (within ±5pp) |

**Paired comparisons — shape:uniform-tables** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 104 | +0.3 | [-3.5, +4.5] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 104 | -0.3 | [-3.2, +2.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs edn-table | 104 | +0.3 | [-1.9, +2.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 104 | -0.0 | [-2.9, +2.9] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs json-compact | 104 | +1.9 | [-1.6, +6.1] | 0.375 |  | no detectable difference |
| haiku | edn-maps vs toon | 104 | -1.6 | [-4.8, +1.3] | 0.500 |  | equivalent (±5pp) |
| sonnet | edn-maps vs json-compact | 104 | +2.2 | [-1.6, +6.1] | 0.508 |  | no detectable difference |
| sonnet | edn-table vs toon | 104 | -2.9 | [-6.7, +1.0] | 0.453 |  | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 104 | -0.0 | [-2.6, +2.9] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 104 | -2.9 | [-6.7, +1.0] | 1.000 |  | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 104 | +0.3 | [-4.2, +4.8] | 0.754 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 104 | -1.0 | [-5.8, +3.9] | 1.000 |  | no detectable difference |
| opus | edn-maps vs json-compact | 104 | +0.3 | [-1.0, +1.9] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 104 | -1.0 | [-2.9, +1.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 104 | +0.6 | [-0.6, +1.9] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 104 | -0.3 | [-1.9, +1.3] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 104 | +0.0 | [-1.6, +1.9] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 104 | +0.0 | [-1.6, +1.6] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 104 | +1.0 | [-0.8, +2.7] | 0.453 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 104 | -1.4 | [-3.2, +0.4] | 0.344 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 104 | +0.3 | [-1.0, +1.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 104 | -1.1 | [-3.1, +0.9] | 0.388 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 104 | +0.8 | [-1.4, +2.9] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 104 | -0.9 | [-3.2, +1.3] | 0.774 |  | equivalent (±5pp) |

**Paired comparisons — shape:nested-config** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 29 | +3.5 | [+0.0, +8.1] | 1.000 |  | no detectable difference |
| haiku | edn-table vs toon | 29 | +1.1 | [-4.6, +8.1] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs edn-table | 29 | -1.1 | [-6.9, +3.5] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs toon | 29 | +0.0 | [-5.8, +6.9] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs json-compact | 29 | +2.3 | [+0.0, +5.8] | 1.000 |  | no detectable difference |
| haiku | edn-maps vs toon | 29 | +1.1 | [-4.6, +8.1] | 1.000 |  | no detectable difference |
| sonnet | edn-maps vs json-compact | 29 | +1.1 | [+0.0, +3.5] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 29 | +1.1 | [+0.0, +3.5] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs edn-table | 29 | -2.3 | [-6.9, +0.0] | 1.000 |  | no detectable difference |
| sonnet | edn-table-primer vs toon | 29 | -1.1 | [-3.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 29 | -1.1 | [-3.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 29 | +1.1 | [+0.0, +3.5] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 29 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 29 | +1.5 | [+0.4, +3.1] | 1.000 |  | A better (within ±5pp) |
| pooled | edn-table vs toon | 29 | +0.8 | [-0.8, +2.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 29 | -1.1 | [-3.8, +0.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 29 | -0.4 | [-3.1, +1.9] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 29 | +0.4 | [-0.8, +1.9] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 29 | +0.8 | [-0.8, +2.7] | 1.000 |  | equivalent (±5pp) |

**Paired comparisons — shape:mixed** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 106 | -0.9 | [-3.8, +1.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 106 | -3.8 | [-7.9, -0.0] | 0.016 |  | B better |
| haiku | edn-table-primer vs edn-table | 106 | -0.6 | [-2.8, +1.6] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 106 | -4.4 | [-8.5, -0.6] | 0.008 |  | B better |
| haiku | edn-table-primer vs json-compact | 106 | -0.6 | [-3.1, +1.9] | 0.500 |  | equivalent (±5pp) |
| haiku | edn-maps vs toon | 106 | -4.7 | [-9.1, -0.9] | 0.016 |  | B better |
| sonnet | edn-maps vs json-compact | 106 | -0.6 | [-3.5, +2.2] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 106 | -1.9 | [-7.2, +3.1] | 0.388 |  | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 106 | +0.9 | [-2.2, +4.4] | 0.219 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 106 | -0.9 | [-5.0, +3.1] | 1.000 |  | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 106 | +0.9 | [-2.2, +4.1] | 0.219 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 106 | -2.5 | [-7.2, +1.9] | 0.754 |  | no detectable difference |
| opus | edn-maps vs json-compact | 106 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 106 | -0.3 | [-0.9, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 106 | -0.6 | [-1.6, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 106 | -0.9 | [-2.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 106 | -0.9 | [-2.5, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 106 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 106 | -0.5 | [-1.9, +0.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 106 | -2.0 | [-4.6, +0.2] | 0.180 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 106 | -0.1 | [-1.4, +1.1] | 0.688 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 106 | -2.1 | [-4.5, -0.0] | 0.453 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 106 | -0.2 | [-1.4, +0.8] | 0.727 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 106 | -2.4 | [-4.8, -0.4] | 0.180 |  | B better (within ±5pp) |

**Paired comparisons — track:flat** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 109 | -0.6 | [-4.9, +3.7] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 109 | -2.1 | [-5.8, +1.2] | 1.000 |  | no detectable difference |
| haiku | edn-table-primer vs edn-table | 109 | +0.3 | [-1.8, +2.5] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 109 | -1.8 | [-5.8, +1.5] | 0.688 |  | no detectable difference |
| haiku | edn-table-primer vs json-compact | 109 | +1.8 | [-1.8, +5.8] | 0.375 |  | no detectable difference |
| haiku | edn-maps vs toon | 109 | -4.3 | [-8.9, -0.3] | 0.062 |  | B better |
| sonnet | edn-maps vs json-compact | 109 | +1.2 | [-3.1, +5.2] | 0.754 |  | no detectable difference |
| sonnet | edn-table vs toon | 109 | -4.6 | [-9.2, -0.3] | 0.180 |  | B better |
| sonnet | edn-table-primer vs edn-table | 109 | +0.0 | [-2.5, +2.8] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 109 | -4.6 | [-9.2, -0.3] | 0.549 |  | B better |
| sonnet | edn-table-primer vs json-compact | 109 | +0.3 | [-4.0, +4.6] | 0.754 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 109 | -3.7 | [-9.2, +1.8] | 0.629 |  | no detectable difference |
| opus | edn-maps vs json-compact | 109 | +0.3 | [-0.9, +1.5] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 109 | -2.8 | [-6.1, +0.0] | 0.500 |  | no detectable difference |
| opus | edn-table-primer vs edn-table | 109 | +0.6 | [-0.6, +1.8] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 109 | -2.1 | [-5.5, +0.6] | 0.500 |  | no detectable difference |
| opus | edn-table-primer vs json-compact | 109 | +0.0 | [-1.8, +1.5] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 109 | -1.8 | [-5.2, +0.9] | 0.500 |  | no detectable difference |
| pooled | edn-maps vs json-compact | 109 | +0.3 | [-1.8, +2.2] | 0.727 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 109 | -3.2 | [-6.5, -0.4] | 0.146 |  | B better |
| pooled | edn-table-primer vs edn-table | 109 | +0.3 | [-0.9, +1.5] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 109 | -2.9 | [-6.3, -0.1] | 0.180 |  | B better |
| pooled | edn-table-primer vs json-compact | 109 | +0.7 | [-1.3, +2.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 109 | -3.3 | [-7.0, -0.0] | 0.302 |  | B better |

**Paired comparisons — track:mixed** (diff = A − B in pp; 95% paired bootstrap CI; McNemar exact on majority-of-seeds; Holm over the primary overall family)

| model | A vs B | n | diff | 95% CI | McNemar p | Holm p | verdict |
|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 135 | +0.0 | [-2.5, +2.2] | 1.000 |  | equivalent (±5pp) |
| haiku | edn-table vs toon | 135 | -2.7 | [-6.2, +0.5] | 0.070 |  | no detectable difference |
| haiku | edn-table-primer vs edn-table | 135 | -0.7 | [-2.7, +1.2] | 0.500 |  | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 135 | -3.5 | [-6.9, -0.2] | 0.021 |  | B better |
| haiku | edn-table-primer vs json-compact | 135 | +0.0 | [-2.0, +2.0] | 0.500 |  | equivalent (±5pp) |
| haiku | edn-maps vs toon | 135 | -3.5 | [-6.9, -0.2] | 0.039 |  | B better |
| sonnet | edn-maps vs json-compact | 135 | -0.2 | [-2.7, +2.0] | 0.625 |  | equivalent (±5pp) |
| sonnet | edn-table vs toon | 135 | -1.2 | [-5.4, +2.7] | 0.388 |  | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 135 | +0.2 | [-2.5, +3.0] | 0.453 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 135 | -1.0 | [-4.2, +2.2] | 1.000 |  | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 135 | +0.5 | [-2.0, +3.2] | 0.453 |  | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 135 | -1.7 | [-5.4, +1.7] | 0.754 |  | no detectable difference |
| opus | edn-maps vs json-compact | 135 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table vs toon | 135 | -0.2 | [-0.7, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 135 | -0.5 | [-1.2, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 135 | -0.7 | [-2.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 135 | -0.7 | [-2.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| opus | edn-maps vs toon | 135 | +0.0 | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 135 | -0.1 | [-1.1, +1.0] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table vs toon | 135 | -1.4 | [-3.5, +0.4] | 0.180 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 135 | -0.3 | [-1.4, +0.7] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 135 | -1.7 | [-3.6, -0.1] | 0.289 |  | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | 135 | -0.1 | [-1.0, +0.8] | 1.000 |  | equivalent (±5pp) |
| pooled | edn-maps vs toon | 135 | -1.7 | [-3.5, -0.1] | 0.180 |  | B better (within ±5pp) |

**Sensitivity — lenient grader, overall, pooled**

| A vs B | diff | 95% CI | verdict |
|---|---|---|---|
| edn-maps vs json-compact | +0.1 | [-1.0, +1.2] | equivalent (±5pp) |
| edn-table vs toon | -2.1 | [-3.9, -0.4] | B better (within ±5pp) |
| edn-table-primer vs edn-table | -0.2 | [-1.0, +0.6] | equivalent (±5pp) |
| edn-table-primer vs toon | -2.2 | [-4.0, -0.6] | B better (within ±5pp) |
| edn-table-primer vs json-compact | +0.3 | [-0.8, +1.4] | equivalent (±5pp) |
| edn-maps vs toon | -2.4 | [-4.3, -0.6] | B better (within ±5pp) |

**Sensitivity — excluding batches with a fake tool call, overall, pooled**

| A vs B | diff | 95% CI | verdict |
|---|---|---|---|
| edn-maps vs json-compact | +0.1 | [-1.0, +1.1] | equivalent (±5pp) |
| edn-table vs toon | -2.1 | [-3.9, -0.5] | B better (within ±5pp) |
| edn-table-primer vs edn-table | -0.1 | [-1.0, +0.8] | equivalent (±5pp) |
| edn-table-primer vs toon | -2.2 | [-4.0, -0.6] | B better (within ±5pp) |
| edn-table-primer vs json-compact | +0.3 | [-0.9, +1.3] | equivalent (±5pp) |
| edn-maps vs toon | -2.4 | [-4.3, -0.7] | B better (within ±5pp) |

**Failure classification (all graded answers)**

| model | format | correct | comprehension | format (lenient-correct) | format (missing) | call failed |
|---|---|---|---|---|---|---|
| haiku | csv | 168 | 159 | 0 | 0 | 0 |
| haiku | edn-maps | 445 | 287 | 0 | 0 | 0 |
| haiku | edn-table | 455 | 276 | 1 | 0 | 0 |
| haiku | edn-table-primer | 453 | 279 | 0 | 0 | 0 |
| haiku | json-compact | 447 | 285 | 0 | 0 | 0 |
| haiku | toon | 473 | 259 | 0 | 0 | 0 |
| opus | csv | 309 | 18 | 0 | 0 | 0 |
| opus | edn-maps | 714 | 18 | 0 | 0 | 0 |
| opus | edn-table | 710 | 22 | 0 | 0 | 0 |
| opus | edn-table-primer | 710 | 22 | 0 | 0 | 0 |
| opus | json-compact | 713 | 19 | 0 | 0 | 0 |
| opus | toon | 720 | 12 | 0 | 0 | 0 |
| sonnet | csv | 165 | 162 | 0 | 0 | 0 |
| sonnet | edn-maps | 474 | 257 | 1 | 0 | 0 |
| sonnet | edn-table | 473 | 257 | 2 | 0 | 0 |
| sonnet | edn-table-primer | 474 | 258 | 0 | 0 | 0 |
| sonnet | json-compact | 471 | 261 | 0 | 0 | 0 |
| sonnet | toon | 493 | 239 | 0 | 0 | 0 |

**Reply behaviour and per-call cost** (means per batched call)

| model | format | calls | input tok | output tok | Opus thinking tok | replies with visible reasoning | fake tool calls | list-price $/call |
|---|---|---|---|---|---|---|---|---|
| haiku | json-compact | 96 | 5778 | 55 | 0 | 0.0% | 0 | 0.0058 |
| haiku | toon | 96 | 5076 | 84 | 0 | 3.1% | 0 | 0.0055 |
| haiku | edn-maps | 96 | 6209 | 1622 | 0 | 10.4% | 10 | 0.0148 |
| haiku | edn-table | 96 | 5278 | 684 | 0 | 7.3% | 4 | 0.0089 |
| haiku | edn-table-primer | 96 | 5405 | 344 | 0 | 4.2% | 2 | 0.0078 |
| haiku | csv | 51 | 4443 | 721 | 0 | 7.8% | 4 | 0.0080 |
| sonnet | json-compact | 96 | 7848 | 104 | 0 | 3.1% | 0 | 0.0202 |
| sonnet | toon | 96 | 6326 | 137 | 0 | 7.3% | 0 | 0.0168 |
| sonnet | edn-maps | 96 | 7776 | 136 | 0 | 4.2% | 0 | 0.0202 |
| sonnet | edn-table | 96 | 6622 | 167 | 0 | 7.3% | 0 | 0.0178 |
| sonnet | edn-table-primer | 96 | 6784 | 98 | 0 | 3.1% | 0 | 0.0175 |
| sonnet | csv | 51 | 5558 | 76 | 0 | 2.0% | 0 | 0.0138 |
| opus | json-compact | 96 | 7785 | 806 | 741 | 0.0% | 0 | 0.0473 |
| opus | toon | 96 | 6263 | 730 | 665 | 0.0% | 0 | 0.0396 |
| opus | edn-maps | 96 | 7713 | 822 | 756 | 0.0% | 0 | 0.0473 |
| opus | edn-table | 96 | 6559 | 768 | 702 | 0.0% | 0 | 0.0416 |
| opus | edn-table-primer | 96 | 6721 | 759 | 693 | 0.0% | 0 | 0.0421 |
| opus | csv | 51 | 5495 | 1012 | 957 | 0.0% | 0 | 0.0422 |

**Generation check** (20 records × 3 samples = 60 per cell; Wilson 95% CI). Parse-valid for EDN requires both edn-data and edn_format to accept.

| model | format | parse-valid | lossless round-trip | canonical form |
|---|---|---|---|---|
| haiku | edn-table | 58/60 (97%, [89, 99]) | 50/60 (83%, [72, 91]) | 37/60 (62%, [49, 73]) |
| haiku | edn-maps | 58/60 (97%, [89, 99]) | 57/60 (95%, [86, 98]) | 54/60 (90%, [80, 95]) |
| haiku | toon | 40/60 (67%, [54, 77]) | 30/60 (50%, [38, 62]) | 30/60 (50%, [38, 62]) |
| sonnet | edn-table | 60/60 (100%, [94, 100]) | 50/60 (83%, [72, 91]) | 35/60 (58%, [46, 70]) |
| sonnet | edn-maps | 58/60 (97%, [89, 99]) | 57/60 (95%, [86, 98]) | 54/60 (90%, [80, 95]) |
| sonnet | toon | 43/60 (72%, [59, 81]) | 41/60 (68%, [56, 79]) | 41/60 (68%, [56, 79]) |
| opus | edn-table | 60/60 (100%, [94, 100]) | 57/60 (95%, [86, 98]) | 45/60 (75%, [63, 84]) |
| opus | edn-maps | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) |
| opus | toon | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) | 60/60 (100%, [94, 100]) |

**Generation lossless rate by record shape** (all models)

| shape | edn-table | edn-maps | toon |
|---|---|---|---|
| flat | 60/63 (95%, [87, 98]) | 57/63 (90%, [81, 96]) | 54/63 (86%, [75, 92]) |
| nested | 58/63 (92%, [83, 97]) | 63/63 (100%, [94, 100]) | 49/63 (78%, [66, 86]) |
| mixed | 39/54 (72%, [59, 82]) | 54/54 (100%, [93, 100]) | 28/54 (52%, [39, 65]) |

**External check vs upstream (Haiku 4.5)**

| format | n | upstream single-question | ours, batched (mean 3 seeds) | per-question agreement (majority) |
|---|---|---|---|---|
| json-compact | 244 | 61.9 | 61.1 | 93.4 |
| toon | 244 | 65.6 | 64.6 | 95.1 |
| csv | 109 | 49.5 | 51.4 | 99.1 |
