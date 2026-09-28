
**All 244 questions (CSV: 109 flat questions)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 61.1 [55.2, 66.9] | 64.6 [58.9, 70.4] | 60.8 [54.8, 66.8] | 62.2 [56.3, 67.9] | 61.9 [56.1, 67.8] | 51.4 [42.5, 59.9] | 73.1 [66.2, 79.8] |
| sonnet | 64.3 [58.6, 70.1] | 67.3 [61.9, 72.8] | 64.8 [59.0, 70.2] | 64.6 [58.9, 70.4] | 64.8 [59.0, 70.2] | 50.5 [41.3, 59.6] | 76.5 [69.6, 83.0] |
| opus | 97.4 [95.4, 99.0] | 98.4 [96.7, 99.6] | 97.5 [95.5, 99.2] | 97.0 [95.0, 98.8] | 97.0 [95.0, 98.8] | 94.5 [90.2, 97.9] | 100.0 [100.0, 100.0] |
| pooled | 74.3 [70.4, 78.2] | 76.8 [72.9, 80.5] | 74.4 [70.5, 78.2] | 74.6 [70.6, 78.4] | 74.5 [70.6, 78.4] | 65.4 [59.1, 72.0] | 83.2 [78.8, 87.4] |
| pooled-nr | 62.7 [57.1, 68.4] | 66.0 [60.4, 71.4] | 62.8 [57.0, 68.2] | 63.4 [57.9, 68.9] | 63.3 [57.6, 68.8] | 50.9 [42.0, 59.5] | 74.8 [67.9, 81.2] |

<details><summary>Flat-only track (109)</summary>


**Flat-only track (109)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 47.4 [38.5, 56.6] | 51.1 [42.2, 60.2] | 46.8 [37.6, 55.7] | 48.9 [40.1, 57.8] | 49.2 [40.1, 58.1] | 51.4 [42.5, 59.9] | – |
| sonnet | 48.6 [39.5, 57.8] | 53.5 [45.0, 62.4] | 49.9 [41.3, 58.4] | 48.9 [40.1, 57.8] | 48.9 [40.1, 57.8] | 50.5 [41.0, 59.6] | – |
| opus | 94.2 [89.9, 97.9] | 96.3 [93.0, 99.1] | 94.5 [90.2, 98.2] | 93.6 [89.3, 97.2] | 94.2 [89.9, 97.9] | 94.5 [90.2, 97.9] | – |
| pooled | 63.4 [57.0, 69.8] | 67.0 [60.9, 73.1] | 63.7 [57.3, 70.0] | 63.8 [57.5, 70.0] | 64.1 [57.6, 70.3] | 65.4 [59.1, 71.8] | – |
| pooled-nr | 48.0 [39.3, 56.9] | 52.3 [43.6, 60.9] | 48.3 [39.8, 56.9] | 48.9 [40.4, 57.5] | 49.1 [40.4, 58.0] | 50.9 [42.2, 59.9] | – |

</details>

<details><summary>Mixed-structure track (135)</summary>


**Mixed-structure track (135)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 72.1 [64.9, 79.0] | 75.6 [68.4, 82.2] | 72.1 [64.7, 79.3] | 72.8 [65.9, 79.5] | 72.1 [64.9, 79.0] | – | 73.1 [66.2, 79.8] |
| sonnet | 77.0 [70.6, 83.2] | 78.5 [71.9, 84.7] | 76.8 [69.9, 83.5] | 77.3 [70.6, 83.5] | 77.5 [70.9, 84.0] | – | 76.5 [69.4, 83.2] |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.8 [99.3, 100.0] | 99.3 [98.0, 100.0] | – | 100.0 [100.0, 100.0] |
| pooled | 83.0 [78.6, 87.3] | 84.7 [80.2, 88.9] | 83.0 [78.4, 87.3] | 83.3 [78.8, 87.6] | 83.0 [78.3, 87.3] | – | 83.2 [78.6, 87.5] |
| pooled-nr | 74.6 [67.7, 81.0] | 77.0 [70.4, 83.2] | 74.4 [67.5, 81.0] | 75.1 [68.5, 81.5] | 74.8 [68.2, 81.2] | – | 74.8 [68.3, 81.1] |

</details>

<details><summary>Uniform tables (104)</summary>


**Uniform tables (104)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 46.8 [37.5, 56.1] | 48.7 [39.7, 58.0] | 47.1 [37.8, 56.1] | 48.4 [39.4, 57.4] | 48.7 [39.4, 58.0] | 50.0 [41.3, 59.0] | – |
| sonnet | 48.1 [38.8, 57.4] | 51.3 [42.3, 60.3] | 50.3 [41.3, 59.3] | 48.4 [39.4, 57.7] | 48.4 [39.4, 57.7] | 49.0 [39.7, 58.3] | – |
| opus | 95.8 [92.3, 98.7] | 96.2 [92.6, 99.0] | 96.2 [92.6, 99.0] | 95.2 [91.3, 98.4] | 95.8 [92.0, 98.7] | 95.2 [91.3, 98.4] | – |
| pooled | 63.6 [57.2, 69.9] | 65.4 [59.2, 71.5] | 64.5 [58.2, 70.7] | 64.0 [57.7, 70.4] | 64.3 [58.0, 70.7] | 64.7 [58.2, 71.3] | – |
| pooled-nr | 47.4 [38.8, 56.2] | 50.0 [41.3, 59.0] | 48.7 [39.9, 57.2] | 48.4 [39.4, 57.5] | 48.6 [39.6, 57.5] | 49.5 [40.4, 58.5] | – |

</details>

<details><summary>Nested config (29)</summary>


**Nested config (29)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 89.7 [80.5, 96.5] | 92.0 [85.1, 97.7] | 93.1 [83.9, 100.0] | 93.1 [83.9, 98.9] | 92.0 [82.8, 98.9] | – | 90.8 [81.6, 97.7] |
| sonnet | 98.9 [96.5, 100.0] | 98.9 [96.5, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.7 [93.1, 100.0] | – | 98.9 [96.5, 100.0] |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | – | 100.0 [100.0, 100.0] |
| pooled | 96.2 [92.3, 98.9] | 96.9 [93.9, 99.2] | 97.7 [94.6, 100.0] | 97.7 [95.0, 99.6] | 96.5 [92.3, 99.6] | – | 96.5 [92.7, 99.2] |
| pooled-nr | 94.2 [88.5, 98.3] | 95.4 [90.8, 98.9] | 96.5 [92.0, 100.0] | 96.5 [92.5, 99.4] | 94.8 [87.9, 99.4] | – | 94.8 [89.1, 98.9] |

</details>

<details><summary>Mixed shapes (106)</summary>


**Mixed shapes (106)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 67.3 [58.5, 75.8] | 71.1 [62.3, 79.2] | 66.3 [57.6, 74.8] | 67.3 [59.1, 75.5] | 66.7 [58.2, 74.8] | – | 68.2 [60.1, 76.4] |
| sonnet | 71.1 [63.2, 78.6] | 73.0 [64.5, 80.8] | 70.4 [62.0, 78.3] | 71.1 [62.9, 78.9] | 72.0 [64.1, 79.6] | – | 70.4 [62.0, 78.3] |
| opus | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.7 [99.1, 100.0] | 99.1 [97.5, 100.0] | – | 100.0 [100.0, 100.0] |
| pooled | 79.5 [74.1, 84.6] | 81.3 [76.0, 86.4] | 78.9 [73.3, 84.2] | 79.3 [74.0, 84.6] | 79.2 [73.7, 84.4] | – | 79.6 [74.2, 84.8] |
| pooled-nr | 69.2 [61.5, 77.0] | 72.0 [63.8, 79.6] | 68.4 [59.9, 76.4] | 69.2 [61.5, 77.0] | 69.3 [61.3, 76.9] | – | 69.3 [61.3, 77.0] |

</details>

<details><summary>Structural validation (5)</summary>


**Structural validation (5)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| sonnet | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| opus | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| pooled | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 46.7 [6.7, 86.7] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |
| pooled-nr | 60.0 [20.0, 100.0] | 100.0 [100.0, 100.0] | 40.0 [0.0, 80.0] | 60.0 [20.0, 100.0] | 60.0 [20.0, 100.0] | 80.0 [40.0, 100.0] | – |

</details>

**All except structural validation (239)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 61.1 [55.4, 67.0] | 63.9 [57.7, 69.7] | 61.2 [55.2, 67.1] | 62.2 [56.4, 68.1] | 61.9 [56.1, 67.8] | 50.0 [41.0, 58.7] | 73.1 [66.2, 79.5] |
| sonnet | 64.4 [58.7, 70.0] | 66.7 [61.0, 72.1] | 65.3 [59.6, 70.9] | 64.7 [58.9, 70.4] | 64.8 [59.0, 70.4] | 49.0 [39.7, 58.3] | 76.5 [69.6, 83.2] |
| opus | 98.2 [96.5, 99.4] | 98.3 [96.7, 99.6] | 98.3 [96.7, 99.6] | 97.8 [96.1, 99.2] | 97.8 [96.0, 99.2] | 95.2 [91.3, 98.4] | 100.0 [100.0, 100.0] |
| pooled | 74.6 [70.5, 78.4] | 76.3 [72.4, 80.0] | 74.9 [70.9, 78.8] | 74.9 [70.9, 78.7] | 74.9 [70.9, 78.8] | 64.7 [58.1, 71.2] | 83.2 [78.8, 87.5] |
| pooled-nr | 62.8 [57.1, 68.3] | 65.3 [59.6, 70.9] | 63.2 [57.5, 68.8] | 63.5 [57.8, 69.1] | 63.4 [57.8, 68.8] | 49.5 [40.2, 58.5] | 74.8 [68.0, 81.2] |

<details><summary>Informative questions only (correctness varies across formats × seeds for that model level)</summary>


**Informative questions only (correctness varies across formats × seeds for that model level)** — accuracy % (mean of 3 seeds), 95% cluster-bootstrap CI

| model | json-compact | toon | edn-maps | edn-table | edn-table-primer | csv | edn-table-lines |
|---|---|---|---|---|---|---|---|
| haiku | 31.2 [22.4, 40.6] | 44.8 [34.4, 55.2] | 30.2 [21.3, 39.6] | 35.4 [27.1, 43.8] | 34.4 [25.5, 43.8] | 41.9 [28.0, 57.0] | 37.4 [26.3, 48.5] |
| sonnet | 36.8 [27.9, 45.6] | 47.5 [38.2, 56.9] | 38.2 [29.4, 47.1] | 37.8 [28.4, 47.1] | 38.2 [28.9, 48.0] | 39.5 [25.4, 54.4] | 41.1 [26.7, 55.6] |
| opus | 79.2 [62.5, 93.8] | 93.8 [87.5, 100.0] | 81.2 [62.5, 95.8] | 72.9 [56.2, 87.5] | 72.9 [54.2, 87.5] | 90.5 [83.3, 97.6] | 100.0 [100.0, 100.0] |
| pooled | 49.8 [45.5, 54.3] | 54.9 [50.1, 59.8] | 50.0 [45.6, 54.4] | 50.4 [45.9, 55.0] | 50.3 [45.9, 55.0] | 49.9 [43.8, 56.5] | 56.4 [50.0, 62.8] |
| pooled-nr | 33.7 [26.5, 41.5] | 42.4 [34.4, 50.7] | 33.9 [26.6, 41.5] | 35.5 [27.9, 43.1] | 35.3 [27.9, 43.1] | 37.7 [25.7, 50.0] | 39.1 [29.0, 49.6] |

</details>

**Paired comparisons — overall-excl-structural** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 239 | +0.1 | [-1.9, +2.2] | [-2.6, +2.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 239 | -1.7 | [-3.9, +0.6] | [-6.3, +1.7] | 0.227 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table-primer vs edn-table | 239 | -0.3 | [-1.8, +1.3] | [-1.9, +1.4] | 0.375 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 239 | -1.9 | [-4.3, +0.3] | [-6.6, +1.5] | 0.057 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table-primer vs json-compact | 239 | +0.8 | [-1.1, +2.9] | [-2.0, +4.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 239 | -2.6 | [-5.2, -0.3] | [-7.5, +0.7] | 0.012 |  | B better | no detectable difference |
| haiku | toon vs json-compact | 239 | +2.8 | [+0.6, +5.3] | [-0.1, +6.8] | 0.012 |  | A better | no detectable difference |
| sonnet | edn-maps vs json-compact | 239 | +0.8 | [-1.3, +2.9] | [-2.1, +3.7] | 0.267 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 239 | -1.9 | [-4.9, +0.8] | [-5.6, +1.4] | 0.167 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 239 | +0.1 | [-1.8, +2.1] | [-2.5, +2.9] | 0.227 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 239 | -1.8 | [-4.3, +0.6] | [-5.1, +0.9] | 0.804 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 239 | +0.4 | [-1.9, +2.9] | [-2.9, +3.4] | 0.332 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 239 | -1.4 | [-4.5, +1.5] | [-4.9, +1.6] | 0.839 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | toon vs json-compact | 239 | +2.2 | [-0.4, +5.0] | [-0.6, +5.4] | 0.167 |  | no detectable difference | no detectable difference |
| opus | edn-maps vs json-compact | 239 | +0.1 | [-0.4, +0.7] | [-0.7, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 239 | -0.6 | [-1.5, +0.3] | [-1.6, +0.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 239 | +0.0 | [-0.7, +0.7] | [-0.8, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 239 | -0.6 | [-1.5, +0.3] | [-1.7, +0.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 239 | -0.4 | [-1.4, +0.6] | [-1.6, +0.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 239 | +0.0 | [-0.7, +0.7] | [-0.8, +0.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 239 | +0.1 | [-0.3, +0.7] | [-0.4, +0.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 239 | +0.4 | [-0.6, +1.3] | [-1.1, +1.7] | 0.581 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 239 | -1.4 | [-2.8, -0.1] | [-3.7, +0.5] | 0.064 |  | B better (within ±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 239 | -0.1 | [-0.9, +0.7] | [-1.0, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 239 | -1.4 | [-2.8, -0.2] | [-3.6, +0.3] | 0.115 |  | B better (within ±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 239 | +0.3 | [-0.8, +1.4] | [-1.2, +1.9] | 0.791 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 239 | -1.4 | [-2.8, +0.0] | [-3.7, +0.4] | 0.189 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | toon vs json-compact | 239 | +1.7 | [+0.4, +3.1] | [+0.3, +3.6] | 0.041 |  | A better (within ±5pp) | A better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | 239 | +0.5 | [-1.0, +1.9] | [-1.7, +2.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 239 | -1.8 | [-3.8, +0.1] | [-5.2, +1.0] | 0.031 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 239 | -0.1 | [-1.3, +1.1] | [-1.5, +1.5] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 239 | -1.9 | [-3.8, -0.1] | [-5.0, +0.6] | 0.125 |  | B better (within ±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 239 | +0.6 | [-0.9, +2.1] | [-1.5, +2.8] | 0.125 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 239 | -2.0 | [-4.2, -0.1] | [-5.6, +0.6] | 0.008 |  | B better (within ±5pp) | no detectable difference |
| pooled-nr | toon vs json-compact | 239 | +2.5 | [+0.6, +4.7] | [+0.4, +5.3] | 0.004 |  | A better (within ±5pp) | A better |

**Paired comparisons — overall** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 244 | -0.3 | [-2.5, +1.9] | [-3.5, +2.4] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 244 | -2.5 | [-4.9, -0.0] | [-7.7, +1.0] | 0.092 | 1.0 | B better (within ±5pp) | no detectable difference |
| haiku | edn-table-primer vs edn-table | 244 | -0.3 | [-1.8, +1.1] | [-1.9, +1.4] | 0.375 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 244 | -2.7 | [-5.3, -0.3] | [-8.0, +0.7] | 0.021 | 0.48921 | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 244 | +0.8 | [-1.1, +2.9] | [-1.9, +4.3] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 244 | -3.8 | [-6.6, -1.2] | [-9.7, -0.3] | 0.002 | 0.04392 | B better | B better |
| haiku | toon vs json-compact | 244 | +3.5 | [+1.1, +6.2] | [+0.5, +8.3] | 0.003 |  | A better | A better |
| sonnet | edn-maps vs json-compact | 244 | +0.4 | [-1.8, +2.6] | [-2.9, +3.5] | 0.424 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 244 | -2.7 | [-5.9, +0.3] | [-7.1, +0.7] | 0.078 | 1.0 | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 244 | +0.1 | [-1.8, +2.2] | [-2.5, +3.1] | 0.227 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 244 | -2.6 | [-5.3, +0.0] | [-6.6, +0.3] | 0.481 | 1.0 | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 244 | +0.4 | [-1.9, +2.9] | [-3.0, +3.3] | 0.332 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 244 | -2.6 | [-5.9, +0.5] | [-7.4, +0.6] | 0.442 | 1.0 | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 244 | +3.0 | [+0.1, +6.0] | [+0.1, +6.9] | 0.078 |  | A better | A better |
| opus | edn-maps vs json-compact | 244 | +0.1 | [-0.4, +0.7] | [-0.7, +0.9] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 244 | -1.4 | [-2.9, -0.1] | [-3.7, -0.1] | 0.500 | 1.0 | B better (within ±5pp) | B better (within ±5pp) |
| opus | edn-table-primer vs edn-table | 244 | +0.0 | [-0.7, +0.7] | [-0.8, +0.9] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 244 | -1.4 | [-3.0, +0.0] | [-3.8, +0.0] | 0.250 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 244 | -0.4 | [-1.4, +0.5] | [-1.6, +0.7] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 244 | -0.8 | [-2.3, +0.4] | [-3.1, +0.3] | 0.500 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 244 | +1.0 | [+0.0, +2.3] | [+0.0, +3.1] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 244 | +0.1 | [-1.0, +1.1] | [-1.7, +1.5] | 0.791 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 244 | -2.2 | [-4.0, -0.5] | [-5.3, -0.1] | 0.027 | 0.5852 | B better (within ±5pp) | B better |
| pooled | edn-table-primer vs edn-table | 244 | -0.1 | [-0.9, +0.8] | [-1.0, +0.9] | 1.000 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 244 | -2.2 | [-4.0, -0.6] | [-5.4, -0.3] | 0.052 | 1.0 | B better (within ±5pp) | B better |
| pooled | edn-table-primer vs json-compact | 244 | +0.3 | [-0.8, +1.3] | [-1.2, +1.9] | 0.791 | 1.0 | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 244 | -2.4 | [-4.4, -0.6] | [-5.9, -0.4] | 0.064 | 1.0 | B better (within ±5pp) | B better |
| pooled | toon vs json-compact | 244 | +2.5 | [+0.9, +4.3] | [+0.8, +5.3] | 0.017 |  | A better (within ±5pp) | A better |
| pooled-nr | edn-maps vs json-compact | 244 | +0.1 | [-1.6, +1.6] | [-2.6, +2.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 244 | -2.6 | [-4.9, -0.5] | [-6.7, +0.3] | 0.008 |  | B better (within ±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 244 | -0.1 | [-1.2, +1.1] | [-1.5, +1.4] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 244 | -2.7 | [-4.9, -0.6] | [-6.6, -0.1] | 0.031 |  | B better (within ±5pp) | B better |
| pooled-nr | edn-table-primer vs json-compact | 244 | +0.6 | [-0.9, +2.1] | [-1.6, +2.8] | 0.125 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 244 | -3.2 | [-5.7, -0.9] | [-7.9, -0.4] | 0.001 |  | B better | B better |
| pooled-nr | toon vs json-compact | 244 | +3.3 | [+1.1, +5.7] | [+0.9, +6.8] | 0.001 |  | A better | A better |

<details><summary>Paired comparisons — informative</summary>


**Paired comparisons — informative** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 64 | -1.0 | [-9.9, +7.8] | [-12.3, +9.3] | 1.000 |  | no detectable difference | no detectable difference |
| haiku | edn-table vs toon | 64 | -9.4 | [-18.8, -0.5] | [-24.4, +3.6] | 0.092 |  | B better | no detectable difference |
| haiku | edn-table-primer vs edn-table | 64 | -1.0 | [-6.8, +4.7] | [-7.7, +4.9] | 0.375 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs toon | 64 | -10.4 | [-19.8, -1.0] | [-25.3, +2.6] | 0.021 |  | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 64 | +3.1 | [-4.2, +10.9] | [-7.0, +15.6] | 1.000 |  | no detectable difference | no detectable difference |
| haiku | edn-maps vs toon | 64 | -14.6 | [-24.5, -4.7] | [-31.7, -1.5] | 0.002 |  | B better | B better |
| haiku | toon vs json-compact | 64 | +13.5 | [+4.2, +23.4] | [+2.6, +27.1] | 0.003 |  | A better | A better |
| sonnet | edn-maps vs json-compact | 68 | +1.5 | [-6.9, +9.3] | [-10.6, +11.6] | 0.424 |  | no detectable difference | no detectable difference |
| sonnet | edn-table vs toon | 68 | -9.8 | [-20.6, +0.5] | [-23.7, +2.2] | 0.078 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 68 | +0.5 | [-6.4, +7.3] | [-10.6, +9.5] | 0.227 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs toon | 68 | -9.3 | [-18.6, -0.0] | [-25.1, +0.7] | 0.481 |  | B better | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 68 | +1.5 | [-6.9, +10.3] | [-11.1, +11.0] | 0.332 |  | no detectable difference | no detectable difference |
| sonnet | edn-maps vs toon | 68 | -9.3 | [-20.6, +2.0] | [-25.8, +1.9] | 0.442 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 68 | +10.8 | [+1.0, +21.6] | [+0.4, +23.2] | 0.078 |  | A better | A better |
| opus | edn-maps vs json-compact | 16 | +2.1 | [-6.2, +10.4] | [-8.9, +12.5] | 1.000 |  | no detectable difference | no detectable difference |
| opus | edn-table vs toon | 16 | -20.8 | [-39.6, -2.1] | [-54.2, -2.8] | 0.500 |  | B better | B better |
| opus | edn-table-primer vs edn-table | 16 | +0.0 | [-10.4, +10.4] | [-14.3, +10.4] | 1.000 |  | no detectable difference | no detectable difference |
| opus | edn-table-primer vs toon | 16 | -20.8 | [-41.7, -2.1] | [-62.5, -2.4] | 0.250 |  | B better | B better |
| opus | edn-table-primer vs json-compact | 16 | -6.2 | [-20.8, +8.3] | [-25.0, +8.3] | 1.000 |  | no detectable difference | no detectable difference |
| opus | edn-maps vs toon | 16 | -12.5 | [-33.3, +4.2] | [-45.8, +5.1] | 0.500 |  | no detectable difference | no detectable difference |
| opus | toon vs json-compact | 16 | +14.6 | [-0.0, +33.3] | [+0.0, +50.0] | 0.500 |  | no detectable difference | no detectable difference |
| pooled | edn-maps vs json-compact | 119 | +0.2 | [-2.1, +2.3] | [-3.4, +3.2] | 0.791 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 119 | -4.5 | [-8.1, -1.2] | [-10.7, -0.3] | 0.027 |  | B better | B better |
| pooled | edn-table-primer vs edn-table | 119 | -0.1 | [-1.8, +1.6] | [-2.4, +1.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 119 | -4.6 | [-8.3, -1.3] | [-11.5, -0.8] | 0.052 |  | B better | B better |
| pooled | edn-table-primer vs json-compact | 119 | +0.6 | [-1.6, +2.7] | [-2.5, +3.9] | 0.791 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 119 | -5.0 | [-8.9, -1.5] | [-12.3, -0.9] | 0.064 |  | B better | B better |
| pooled | toon vs json-compact | 119 | +5.1 | [+1.9, +8.8] | [+1.7, +11.5] | 0.017 |  | A better | A better |
| pooled-nr | edn-maps vs json-compact | 92 | +0.2 | [-4.2, +4.3] | [-6.9, +5.8] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table vs toon | 92 | -6.9 | [-13.0, -1.5] | [-16.4, +0.5] | 0.008 |  | B better | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 92 | -0.2 | [-3.3, +2.9] | [-4.5, +3.4] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 92 | -7.1 | [-13.1, -1.6] | [-17.0, -0.5] | 0.031 |  | B better | B better |
| pooled-nr | edn-table-primer vs json-compact | 92 | +1.6 | [-2.4, +5.6] | [-4.2, +7.5] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-maps vs toon | 92 | -8.5 | [-15.0, -2.5] | [-19.8, -1.2] | 0.001 |  | B better | B better |
| pooled-nr | toon vs json-compact | 92 | +8.7 | [+3.1, +14.7] | [+2.9, +17.4] | 0.001 |  | A better | A better |

</details>

<details><summary>Paired comparisons — shape:uniform-tables</summary>


**Paired comparisons — shape:uniform-tables** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 104 | +0.3 | [-3.5, +4.5] | [-4.7, +5.3] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table vs toon | 104 | -0.3 | [-3.2, +2.2] | [-3.7, +4.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs edn-table | 104 | +0.3 | [-1.9, +2.6] | [-1.9, +3.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 104 | -0.0 | [-2.9, +2.9] | [-3.7, +4.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs json-compact | 104 | +1.9 | [-1.6, +6.1] | [-3.2, +9.3] | 0.375 |  | no detectable difference | no detectable difference |
| haiku | edn-maps vs toon | 104 | -1.6 | [-4.8, +1.3] | [-6.4, +1.9] | 0.500 |  | equivalent (±5pp) | no detectable difference |
| haiku | toon vs json-compact | 104 | +1.9 | [-1.0, +5.5] | [-1.6, +6.3] | 0.250 |  | no detectable difference | no detectable difference |
| sonnet | edn-maps vs json-compact | 104 | +2.2 | [-1.6, +6.1] | [-3.5, +7.2] | 0.508 |  | no detectable difference | no detectable difference |
| sonnet | edn-table vs toon | 104 | -2.9 | [-7.0, +1.0] | [-8.1, +2.6] | 0.453 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 104 | -0.0 | [-2.6, +2.9] | [-4.1, +4.8] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 104 | -2.9 | [-6.7, +1.0] | [-8.4, +1.3] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 104 | +0.3 | [-4.2, +4.8] | [-6.4, +5.6] | 0.754 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-maps vs toon | 104 | -1.0 | [-6.1, +3.9] | [-6.9, +4.1] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 104 | +3.2 | [-1.3, +7.7] | [-1.4, +7.7] | 0.508 |  | no detectable difference | no detectable difference |
| opus | edn-maps vs json-compact | 104 | +0.3 | [-1.0, +1.6] | [-1.5, +2.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 104 | -1.0 | [-2.9, +1.0] | [-3.1, +1.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 104 | +0.6 | [-0.6, +1.9] | [-0.6, +2.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 104 | -0.3 | [-1.9, +1.3] | [-2.2, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 104 | +0.0 | [-1.9, +1.9] | [-2.0, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 104 | +0.0 | [-1.6, +1.6] | [-1.7, +1.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 104 | +0.3 | [-0.6, +1.3] | [-1.0, +1.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 104 | +1.0 | [-0.8, +2.7] | [-1.8, +3.0] | 0.453 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 104 | -1.4 | [-3.2, +0.4] | [-4.0, +1.8] | 0.344 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 104 | +0.3 | [-1.0, +1.6] | [-1.1, +1.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 104 | -1.1 | [-3.1, +0.8] | [-4.2, +1.8] | 0.388 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 104 | +0.8 | [-1.4, +2.9] | [-2.5, +4.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 104 | -0.9 | [-3.1, +1.3] | [-4.2, +1.4] | 0.774 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | toon vs json-compact | 104 | +1.8 | [-0.1, +3.7] | [-0.0, +3.8] | 0.180 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs json-compact | 104 | +1.3 | [-1.3, +3.7] | [-3.2, +4.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 104 | -1.6 | [-4.2, +0.8] | [-5.1, +2.7] | 0.500 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 104 | +0.2 | [-1.6, +2.1] | [-1.9, +2.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 104 | -1.4 | [-4.2, +1.1] | [-5.6, +2.4] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 104 | +1.1 | [-2.1, +4.2] | [-3.6, +5.9] | 0.219 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-maps vs toon | 104 | -1.3 | [-4.5, +1.8] | [-6.1, +2.2] | 0.125 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | toon vs json-compact | 104 | +2.6 | [-0.2, +5.5] | [-0.2, +5.5] | 0.062 |  | no detectable difference | no detectable difference |

</details>

<details><summary>Paired comparisons — shape:nested-config</summary>


**Paired comparisons — shape:nested-config** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 29 | +3.5 | [+0.0, +6.9] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table vs toon | 29 | +1.1 | [-4.6, +8.1] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table-primer vs edn-table | 29 | -1.1 | [-6.9, +3.5] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table-primer vs toon | 29 | +0.0 | [-5.8, +6.9] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-table-primer vs json-compact | 29 | +2.3 | [+0.0, +5.8] | – | 1.000 |  | no detectable difference |  |
| haiku | edn-maps vs toon | 29 | +1.1 | [-4.6, +6.9] | – | 1.000 |  | no detectable difference |  |
| haiku | toon vs json-compact | 29 | +2.3 | [-4.6, +9.2] | – | 1.000 |  | no detectable difference |  |
| sonnet | edn-maps vs json-compact | 29 | +1.1 | [+0.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-table vs toon | 29 | +1.1 | [+0.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-table-primer vs edn-table | 29 | -2.3 | [-6.9, +0.0] | – | 1.000 |  | no detectable difference |  |
| sonnet | edn-table-primer vs toon | 29 | -1.1 | [-3.5, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-table-primer vs json-compact | 29 | -1.1 | [-3.5, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | edn-maps vs toon | 29 | +1.1 | [+0.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| sonnet | toon vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-maps vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table vs toon | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table-primer vs edn-table | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table-primer vs toon | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-table-primer vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | edn-maps vs toon | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| opus | toon vs json-compact | 29 | +0.0 | [+0.0, +0.0] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-maps vs json-compact | 29 | +1.5 | [+0.4, +3.1] | – | 1.000 |  | A better (within ±5pp) |  |
| pooled | edn-table vs toon | 29 | +0.8 | [-0.8, +2.7] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-table-primer vs edn-table | 29 | -1.1 | [-3.8, +0.8] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-table-primer vs toon | 29 | -0.4 | [-3.1, +2.3] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-table-primer vs json-compact | 29 | +0.4 | [-0.8, +1.9] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | edn-maps vs toon | 29 | +0.8 | [-0.8, +2.7] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled | toon vs json-compact | 29 | +0.8 | [-1.9, +3.1] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-maps vs json-compact | 29 | +2.3 | [+0.6, +4.6] | – | 1.000 |  | A better (within ±5pp) |  |
| pooled-nr | edn-table vs toon | 29 | +1.1 | [-1.1, +4.0] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-table-primer vs edn-table | 29 | -1.7 | [-5.2, +1.1] | – | 1.000 |  | no detectable difference |  |
| pooled-nr | edn-table-primer vs toon | 29 | -0.6 | [-4.0, +3.5] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-table-primer vs json-compact | 29 | +0.6 | [-1.1, +2.3] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | edn-maps vs toon | 29 | +1.1 | [-1.1, +4.0] | – | 1.000 |  | equivalent (±5pp) |  |
| pooled-nr | toon vs json-compact | 29 | +1.1 | [-2.3, +4.6] | – | 1.000 |  | equivalent (±5pp) |  |

</details>

<details><summary>Paired comparisons — shape:mixed</summary>


**Paired comparisons — shape:mixed** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 106 | -0.9 | [-3.8, +1.6] | [-4.7, +1.4] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 106 | -3.8 | [-7.9, -0.3] | [-12.5, +1.7] | 0.016 |  | B better | no detectable difference |
| haiku | edn-table-primer vs edn-table | 106 | -0.6 | [-2.8, +1.6] | [-2.8, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 106 | -4.4 | [-8.5, -0.9] | [-12.8, +0.9] | 0.008 |  | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 106 | -0.6 | [-3.1, +1.9] | [-3.7, +1.6] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 106 | -4.7 | [-9.1, -0.9] | [-13.8, +0.9] | 0.016 |  | B better | no detectable difference |
| haiku | toon vs json-compact | 106 | +3.8 | [+0.3, +7.9] | [-0.9, +11.7] | 0.031 |  | A better | no detectable difference |
| haiku | edn-table-lines vs edn-table | 106 | +0.9 | [-1.6, +3.5] | [-1.9, +4.2] | 0.375 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-lines vs toon | 106 | -2.8 | [-7.2, +0.9] | [-10.6, +2.4] | 0.289 |  | no detectable difference | no detectable difference |
| haiku | edn-table-lines vs json-compact | 106 | +0.9 | [-1.9, +4.1] | [-2.0, +4.0] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs json-compact | 106 | -0.6 | [-3.5, +2.2] | [-3.7, +2.4] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 106 | -1.9 | [-7.2, +3.1] | [-8.0, +3.1] | 0.388 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 106 | +0.9 | [-2.2, +4.4] | [-2.9, +4.8] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 106 | -0.9 | [-5.0, +2.8] | [-5.7, +3.1] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 106 | +0.9 | [-2.2, +4.1] | [-2.5, +4.6] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 106 | -2.5 | [-7.2, +1.9] | [-7.5, +1.8] | 0.754 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 106 | +1.9 | [-2.2, +6.6] | [-2.2, +7.0] | 0.344 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs edn-table | 106 | -0.6 | [-3.8, +2.8] | [-3.8, +2.8] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-lines vs toon | 106 | -2.5 | [-6.9, +1.6] | [-7.5, +1.5] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs json-compact | 106 | -0.6 | [-4.1, +2.8] | [-4.5, +3.1] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 106 | -0.3 | [-0.9, +0.0] | [-1.2, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 106 | -0.6 | [-1.6, +0.0] | [-1.7, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 106 | -0.9 | [-2.5, +0.0] | [-2.6, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 106 | -0.9 | [-2.5, +0.0] | [-2.6, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs edn-table | 106 | +0.3 | [+0.0, +0.9] | [+0.0, +1.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs toon | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs json-compact | 106 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 106 | -0.5 | [-1.8, +0.8] | [-2.0, +0.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 106 | -2.0 | [-4.6, +0.3] | [-6.2, +0.7] | 0.180 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table-primer vs edn-table | 106 | -0.1 | [-1.4, +1.1] | [-1.5, +1.2] | 0.688 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 106 | -2.1 | [-4.4, -0.0] | [-5.8, +0.2] | 0.453 |  | B better (within ±5pp) | no detectable difference |
| pooled | edn-table-primer vs json-compact | 106 | -0.2 | [-1.3, +0.9] | [-1.4, +0.9] | 0.727 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 106 | -2.4 | [-4.8, -0.4] | [-6.3, +0.0] | 0.180 |  | B better (within ±5pp) | no detectable difference |
| pooled | toon vs json-compact | 106 | +1.9 | [-0.3, +4.3] | [-0.4, +5.7] | 0.227 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table-lines vs edn-table | 106 | +0.2 | [-1.1, +1.5] | [-1.3, +1.6] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs toon | 106 | -1.8 | [-4.1, +0.2] | [-5.6, +0.6] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table-lines vs json-compact | 106 | +0.1 | [-1.3, +1.6] | [-1.4, +1.6] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs json-compact | 106 | -0.8 | [-2.7, +1.1] | [-3.1, +1.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 106 | -2.8 | [-6.8, +0.6] | [-9.2, +1.3] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 106 | +0.2 | [-1.6, +1.9] | [-1.9, +2.1] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 106 | -2.7 | [-6.1, +0.3] | [-8.5, +0.9] | 0.250 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 106 | +0.2 | [-1.4, +1.7] | [-1.6, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 106 | -3.6 | [-7.1, -0.6] | [-9.4, +0.1] | 0.125 |  | B better | no detectable difference |
| pooled-nr | toon vs json-compact | 106 | +2.8 | [-0.5, +6.6] | [-0.7, +8.5] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs edn-table | 106 | +0.2 | [-1.9, +2.0] | [-2.1, +2.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-lines vs toon | 106 | -2.7 | [-6.3, +0.3] | [-8.3, +0.9] | 0.375 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs json-compact | 106 | +0.2 | [-1.9, +2.2] | [-2.1, +2.4] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |

</details>

<details><summary>Paired comparisons — track:flat</summary>


**Paired comparisons — track:flat** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 109 | -0.6 | [-4.9, +3.7] | [-9.7, +4.3] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| haiku | edn-table vs toon | 109 | -2.1 | [-5.8, +1.2] | [-15.0, +2.2] | 1.000 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs edn-table | 109 | +0.3 | [-1.8, +2.5] | [-2.1, +3.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 109 | -1.8 | [-5.8, +1.5] | [-12.6, +2.9] | 0.688 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs json-compact | 109 | +1.8 | [-1.8, +5.8] | [-3.4, +9.2] | 0.375 |  | no detectable difference | no detectable difference |
| haiku | edn-maps vs toon | 109 | -4.3 | [-8.9, -0.3] | [-25.8, -0.2] | 0.062 |  | B better | B better |
| haiku | toon vs json-compact | 109 | +3.7 | [-0.0, +8.0] | [-0.3, +17.1] | 0.062 |  | no detectable difference | no detectable difference |
| sonnet | edn-maps vs json-compact | 109 | +1.2 | [-3.1, +5.2] | [-9.2, +6.2] | 0.754 |  | no detectable difference | no detectable difference |
| sonnet | edn-table vs toon | 109 | -4.6 | [-9.2, -0.3] | [-17.1, +0.8] | 0.180 |  | B better | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 109 | +0.0 | [-2.8, +2.8] | [-4.0, +4.9] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 109 | -4.6 | [-9.2, -0.3] | [-20.0, +0.0] | 0.549 |  | B better | no detectable difference |
| sonnet | edn-table-primer vs json-compact | 109 | +0.3 | [-4.0, +4.6] | [-6.9, +5.6] | 0.754 |  | equivalent (±5pp) | no detectable difference |
| sonnet | edn-maps vs toon | 109 | -3.7 | [-9.5, +1.8] | [-23.3, +1.7] | 0.629 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 109 | +4.9 | [+0.0, +9.8] | [+0.2, +18.3] | 0.227 |  | no detectable difference | A better |
| opus | edn-maps vs json-compact | 109 | +0.3 | [-0.9, +1.8] | [-1.5, +2.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 109 | -2.8 | [-6.1, +0.0] | [-15.0, +0.0] | 0.500 |  | no detectable difference | no detectable difference |
| opus | edn-table-primer vs edn-table | 109 | +0.6 | [-0.6, +1.8] | [-0.5, +2.4] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 109 | -2.1 | [-5.2, +0.6] | [-12.5, +0.5] | 0.500 |  | no detectable difference | no detectable difference |
| opus | edn-table-primer vs json-compact | 109 | +0.0 | [-1.8, +1.8] | [-2.1, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 109 | -1.8 | [-5.2, +0.9] | [-12.6, +0.7] | 0.500 |  | no detectable difference | no detectable difference |
| opus | toon vs json-compact | 109 | +2.1 | [-0.0, +5.2] | [+0.0, +14.2] | 0.500 |  | no detectable difference | no detectable difference |
| pooled | edn-maps vs json-compact | 109 | +0.3 | [-1.8, +2.1] | [-5.8, +2.5] | 0.727 |  | equivalent (±5pp) | no detectable difference |
| pooled | edn-table vs toon | 109 | -3.2 | [-6.5, -0.4] | [-15.6, +0.3] | 0.146 |  | B better | no detectable difference |
| pooled | edn-table-primer vs edn-table | 109 | +0.3 | [-0.9, +1.6] | [-1.1, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 109 | -2.9 | [-6.2, -0.0] | [-14.8, +0.5] | 0.180 |  | B better | no detectable difference |
| pooled | edn-table-primer vs json-compact | 109 | +0.7 | [-1.3, +2.8] | [-2.8, +4.2] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 109 | -3.3 | [-7.0, +0.0] | [-16.7, -0.1] | 0.302 |  | no detectable difference | B better |
| pooled | toon vs json-compact | 109 | +3.6 | [+0.7, +6.8] | [+0.9, +13.9] | 0.065 |  | A better | A better |
| pooled-nr | edn-maps vs json-compact | 109 | +0.3 | [-2.9, +3.1] | [-9.6, +3.7] | 1.000 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table vs toon | 109 | -3.4 | [-7.2, -0.1] | [-14.9, +0.9] | 0.125 |  | B better | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 109 | +0.1 | [-1.5, +2.0] | [-1.9, +2.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 109 | -3.2 | [-6.9, +0.1] | [-15.6, +0.7] | 0.250 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 109 | +1.1 | [-1.8, +4.1] | [-3.9, +6.1] | 0.219 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-maps vs toon | 109 | -4.0 | [-8.6, -0.0] | [-20.0, +0.1] | 0.016 |  | B better | no detectable difference |
| pooled-nr | toon vs json-compact | 109 | +4.3 | [+0.9, +8.1] | [+1.1, +16.7] | 0.016 |  | A better | A better |

</details>

<details><summary>Paired comparisons — track:mixed</summary>


**Paired comparisons — track:mixed** (diff = A − B in pp; q-CI = pre-registered paired bootstrap over questions; ds-CI = post-review two-stage bootstrap over datasets; McNemar exact on majority-of-seeds; Holm over the pre-registered primary overall family)

| model | A vs B | n | diff | q-CI | ds-CI | McNemar p | Holm p | verdict (q-CI) | verdict (ds-CI) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | edn-maps vs json-compact | 135 | +0.0 | [-2.5, +2.2] | [-3.4, +2.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table vs toon | 135 | -2.7 | [-6.2, +0.2] | [-10.1, +2.1] | 0.070 |  | no detectable difference | no detectable difference |
| haiku | edn-table-primer vs edn-table | 135 | -0.7 | [-2.7, +1.2] | [-2.7, +1.3] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-primer vs toon | 135 | -3.5 | [-6.9, -0.2] | [-10.5, +1.1] | 0.021 |  | B better | no detectable difference |
| haiku | edn-table-primer vs json-compact | 135 | +0.0 | [-2.2, +2.0] | [-2.7, +2.2] | 0.500 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-maps vs toon | 135 | -3.5 | [-7.2, -0.2] | [-11.2, +1.5] | 0.039 |  | B better | no detectable difference |
| haiku | toon vs json-compact | 135 | +3.5 | [+0.2, +6.9] | [-0.7, +9.7] | 0.070 |  | A better | no detectable difference |
| haiku | edn-table-lines vs edn-table | 135 | +0.2 | [-2.0, +2.5] | [-2.7, +3.3] | 0.688 |  | equivalent (±5pp) | equivalent (±5pp) |
| haiku | edn-table-lines vs toon | 135 | -2.5 | [-6.2, +1.0] | [-8.6, +2.1] | 0.344 |  | no detectable difference | no detectable difference |
| haiku | edn-table-lines vs json-compact | 135 | +1.0 | [-1.2, +3.5] | [-1.4, +3.4] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs json-compact | 135 | -0.2 | [-2.7, +2.0] | [-2.9, +2.2] | 0.625 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table vs toon | 135 | -1.2 | [-5.4, +2.7] | [-6.2, +2.7] | 0.388 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-primer vs edn-table | 135 | +0.2 | [-2.5, +3.0] | [-3.1, +3.8] | 0.453 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs toon | 135 | -1.0 | [-4.4, +2.2] | [-4.7, +2.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-primer vs json-compact | 135 | +0.5 | [-2.0, +3.2] | [-2.3, +3.5] | 0.453 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-maps vs toon | 135 | -1.7 | [-5.4, +1.7] | [-6.2, +1.7] | 0.754 |  | no detectable difference | no detectable difference |
| sonnet | toon vs json-compact | 135 | +1.5 | [-2.0, +5.2] | [-1.8, +5.7] | 0.344 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs edn-table | 135 | -0.7 | [-3.2, +2.0] | [-3.3, +2.0] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| sonnet | edn-table-lines vs toon | 135 | -2.0 | [-5.2, +1.2] | [-6.1, +1.1] | 1.000 |  | no detectable difference | no detectable difference |
| sonnet | edn-table-lines vs json-compact | 135 | -0.5 | [-3.2, +2.2] | [-3.5, +2.4] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs json-compact | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table vs toon | 135 | -0.2 | [-0.7, +0.0] | [-1.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs edn-table | 135 | -0.5 | [-1.2, +0.0] | [-1.4, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs toon | 135 | -0.7 | [-2.0, +0.0] | [-2.2, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-primer vs json-compact | 135 | -0.7 | [-2.0, +0.0] | [-2.2, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-maps vs toon | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | toon vs json-compact | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs edn-table | 135 | +0.2 | [+0.0, +0.7] | [+0.0, +1.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs toon | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| opus | edn-table-lines vs json-compact | 135 | +0.0 | [+0.0, +0.0] | [+0.0, +0.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs json-compact | 135 | -0.1 | [-1.2, +1.0] | [-1.6, +1.3] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table vs toon | 135 | -1.4 | [-3.5, +0.4] | [-5.0, +0.8] | 0.180 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs edn-table | 135 | -0.3 | [-1.4, +0.7] | [-1.6, +0.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | 135 | -1.7 | [-3.7, -0.1] | [-4.8, +0.2] | 0.289 |  | B better (within ±5pp) | equivalent (±5pp) |
| pooled | edn-table-primer vs json-compact | 135 | -0.1 | [-1.0, +0.8] | [-1.1, +0.8] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-maps vs toon | 135 | -1.7 | [-3.6, -0.1] | [-5.2, +0.5] | 0.180 |  | B better (within ±5pp) | no detectable difference |
| pooled | toon vs json-compact | 135 | +1.7 | [-0.2, +3.7] | [-0.3, +4.8] | 0.227 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs edn-table | 135 | -0.1 | [-1.1, +1.0] | [-1.4, +1.2] | 0.219 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs toon | 135 | -1.5 | [-3.4, +0.2] | [-4.6, +0.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled | edn-table-lines vs json-compact | 135 | +0.2 | [-0.9, +1.3] | [-1.1, +1.3] | 0.289 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs json-compact | 135 | -0.1 | [-1.7, +1.5] | [-2.3, +1.9] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | 135 | -2.0 | [-4.9, +0.7] | [-7.3, +1.4] | 0.125 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs edn-table | 135 | -0.2 | [-1.8, +1.2] | [-2.1, +1.6] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | 135 | -2.2 | [-4.9, +0.2] | [-6.8, +0.7] | 0.250 |  | equivalent (±5pp) | no detectable difference |
| pooled-nr | edn-table-primer vs json-compact | 135 | +0.2 | [-1.0, +1.5] | [-1.2, +1.5] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | 135 | -2.6 | [-5.4, -0.1] | [-7.9, +0.7] | 0.125 |  | B better | no detectable difference |
| pooled-nr | toon vs json-compact | 135 | +2.5 | [-0.1, +5.4] | [-0.4, +7.1] | 0.125 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs edn-table | 135 | -0.2 | [-2.0, +1.4] | [-2.2, +1.7] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |
| pooled-nr | edn-table-lines vs toon | 135 | -2.2 | [-5.1, +0.2] | [-6.8, +0.7] | 0.375 |  | no detectable difference | no detectable difference |
| pooled-nr | edn-table-lines vs json-compact | 135 | +0.2 | [-1.5, +2.0] | [-1.5, +2.0] | 1.000 |  | equivalent (±5pp) | equivalent (±5pp) |

</details>

**Sensitivity — lenient grader, overall, pooled**

| level | A vs B | diff | 95% CI | verdict |
|---|---|---|---|---|
| pooled | edn-maps vs json-compact | +0.1 | [-1.0, +1.2] | equivalent (±5pp) |
| pooled | edn-table vs toon | -2.1 | [-3.9, -0.4] | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | -0.2 | [-1.0, +0.6] | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | -2.2 | [-4.0, -0.6] | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | +0.3 | [-0.8, +1.3] | equivalent (±5pp) |
| pooled | edn-maps vs toon | -2.4 | [-4.3, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | +0.1 | [-1.5, +1.7] | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | -2.4 | [-4.7, -0.3] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs edn-table | -0.3 | [-1.4, +0.8] | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | -2.7 | [-4.9, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs json-compact | +0.6 | [-0.9, +2.1] | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | -3.1 | [-5.7, -0.8] | B better |

**Sensitivity — excluding batches with a fake tool call, overall, pooled**

| level | A vs B | diff | 95% CI | verdict |
|---|---|---|---|---|
| pooled | edn-maps vs json-compact | +0.1 | [-1.0, +1.1] | equivalent (±5pp) |
| pooled | edn-table vs toon | -2.0 | [-3.9, -0.4] | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | -0.1 | [-1.0, +0.8] | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | -2.2 | [-3.9, -0.5] | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | +0.3 | [-0.9, +1.4] | equivalent (±5pp) |
| pooled | edn-maps vs toon | -2.3 | [-4.2, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | -0.0 | [-1.7, +1.5] | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | -2.5 | [-5.0, -0.3] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs edn-table | -0.2 | [-1.6, +1.2] | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | -2.8 | [-5.2, -0.6] | B better |
| pooled-nr | edn-table-primer vs json-compact | +0.6 | [-1.1, +2.2] | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | -3.4 | [-6.1, -0.9] | B better |

**Sensitivity — excluding the 3 upstream ground-truth bugs (q110, q233, q234), overall, pooled**

| level | A vs B | diff | 95% CI | verdict |
|---|---|---|---|---|
| pooled | edn-maps vs json-compact | +0.1 | [-1.0, +1.1] | equivalent (±5pp) |
| pooled | edn-table vs toon | -2.2 | [-4.1, -0.6] | B better (within ±5pp) |
| pooled | edn-table-primer vs edn-table | -0.1 | [-0.9, +0.7] | equivalent (±5pp) |
| pooled | edn-table-primer vs toon | -2.3 | [-4.1, -0.6] | B better (within ±5pp) |
| pooled | edn-table-primer vs json-compact | +0.3 | [-0.8, +1.3] | equivalent (±5pp) |
| pooled | edn-maps vs toon | -2.4 | [-4.4, -0.7] | B better (within ±5pp) |
| pooled-nr | edn-maps vs json-compact | +0.1 | [-1.6, +1.6] | equivalent (±5pp) |
| pooled-nr | edn-table vs toon | -2.6 | [-5.0, -0.5] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs edn-table | -0.1 | [-1.2, +1.1] | equivalent (±5pp) |
| pooled-nr | edn-table-primer vs toon | -2.7 | [-5.0, -0.6] | B better (within ±5pp) |
| pooled-nr | edn-table-primer vs json-compact | +0.6 | [-0.9, +2.1] | equivalent (±5pp) |
| pooled-nr | edn-maps vs toon | -3.2 | [-5.8, -0.9] | B better |

**Failure classification (all graded answers)**

| model | format | correct | comprehension | format (lenient-correct) | format (missing) | call failed |
|---|---|---|---|---|---|---|
| haiku | csv | 168 | 159 | 0 | 0 | 0 |
| haiku | edn-maps | 445 | 287 | 0 | 0 | 0 |
| haiku | edn-table | 455 | 276 | 1 | 0 | 0 |
| haiku | edn-table-lines | 296 | 109 | 0 | 0 | 0 |
| haiku | edn-table-primer | 453 | 279 | 0 | 0 | 0 |
| haiku | json-compact | 447 | 285 | 0 | 0 | 0 |
| haiku | toon | 473 | 259 | 0 | 0 | 0 |
| opus | csv | 309 | 18 | 0 | 0 | 0 |
| opus | edn-maps | 714 | 18 | 0 | 0 | 0 |
| opus | edn-table | 710 | 22 | 0 | 0 | 0 |
| opus | edn-table-lines | 405 | 0 | 0 | 0 | 0 |
| opus | edn-table-primer | 710 | 22 | 0 | 0 | 0 |
| opus | json-compact | 713 | 19 | 0 | 0 | 0 |
| opus | toon | 720 | 12 | 0 | 0 | 0 |
| sonnet | csv | 165 | 162 | 0 | 0 | 0 |
| sonnet | edn-maps | 474 | 257 | 1 | 0 | 0 |
| sonnet | edn-table | 473 | 257 | 2 | 0 | 0 |
| sonnet | edn-table-lines | 310 | 94 | 1 | 0 | 0 |
| sonnet | edn-table-primer | 474 | 258 | 0 | 0 | 0 |
| sonnet | json-compact | 471 | 261 | 0 | 0 | 0 |
| sonnet | toon | 493 | 239 | 0 | 0 | 0 |

**Reply behaviour and per-call cost** (per batched call; visible output excludes Opus's hidden thinking; fake-tool-call rate with Wilson 95% CI and Fisher exact p vs json-compact of the same model)

| model | format | calls | mean input tok | median visible output | mean visible output | Opus thinking tok | fake tool calls | Fisher p vs JSON | list-price $/call |
|---|---|---|---|---|---|---|---|---|---|
| haiku | json-compact | 96 | 5778 | 59.5 | 55 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0058 |
| haiku | toon | 96 | 5076 | 60.0 | 84 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0055 |
| haiku | edn-maps | 96 | 6209 | 61.5 | 1622 | 0 | 10 (10.4% [5.8, 18.1]) | 0.0015 | 0.0148 |
| haiku | edn-table | 96 | 5278 | 60.5 | 684 | 0 | 4 (4.2% [1.6, 10.2]) | 0.1211 | 0.0089 |
| haiku | edn-table-primer | 96 | 5405 | 60.0 | 344 | 0 | 2 (2.1% [0.6, 7.3]) | 0.4974 | 0.0078 |
| haiku | csv | 51 | 4443 | 55 | 721 | 0 | 4 (7.8% [3.1, 18.5]) | 0.0134 | 0.0080 |
| sonnet | json-compact | 96 | 7848 | 73.0 | 104 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0202 |
| sonnet | toon | 96 | 6326 | 73.5 | 137 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0168 |
| sonnet | edn-maps | 96 | 7776 | 74.0 | 136 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0202 |
| sonnet | edn-table | 96 | 6622 | 74.0 | 167 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0178 |
| sonnet | edn-table-primer | 96 | 6784 | 74.0 | 98 | 0 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0175 |
| sonnet | csv | 51 | 5558 | 64 | 76 | 0 | 0 (0.0% [0.0, 7.0]) | 1.0000 | 0.0138 |
| opus | json-compact | 96 | 7785 | 72.0 | 66 | 741 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0473 |
| opus | toon | 96 | 6263 | 72.0 | 65 | 665 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0396 |
| opus | edn-maps | 96 | 7713 | 72.0 | 66 | 756 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0473 |
| opus | edn-table | 96 | 6559 | 72.0 | 66 | 702 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0416 |
| opus | edn-table-primer | 96 | 6721 | 72.0 | 66 | 693 | 0 (0.0% [0.0, 3.8]) | 1.0000 | 0.0421 |
| opus | csv | 51 | 5495 | 64 | 55 | 957 | 0 (0.0% [0.0, 7.0]) | 1.0000 | 0.0422 |

**Generation check** (20 records × 3 samples = 60 attempts per cell; 95% CI = bootstrap over the 20 records, since samples of one record are near-duplicates). EDN parse-valid requires both edn-data and edn_format to accept. `toon-long` = post-hoc arm with a 156-token quoting-rules primer (D7).

| model | format | parse-valid % [CI] | lossless round-trip % [CI] | canonical form (count) |
|---|---|---|---|---|
| haiku | edn-table | 96.7 [90.0, 100.0] | 83.3 [66.7, 96.7] | 37/60 |
| haiku | edn-maps | 96.7 [90.0, 100.0] | 95.0 [85.0, 100.0] | 54/60 |
| haiku | toon | 66.7 [46.7, 85.0] | 50.0 [30.0, 70.0] | 30/60 |
| haiku | toon-long | 76.7 [61.7, 90.0] | 61.7 [41.7, 81.7] | 37/60 |
| sonnet | edn-table | 100.0 [100.0, 100.0] | 83.3 [66.7, 98.3] | 35/60 |
| sonnet | edn-maps | 96.7 [90.0, 100.0] | 95.0 [85.0, 100.0] | 54/60 |
| sonnet | toon | 71.7 [51.7, 90.0] | 68.3 [48.3, 86.7] | 41/60 |
| sonnet | toon-long | 93.3 [81.7, 100.0] | 83.3 [66.7, 98.3] | 50/60 |
| opus | edn-table | 100.0 [100.0, 100.0] | 95.0 [85.0, 100.0] | 45/60 |
| opus | edn-maps | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 60/60 |
| opus | toon | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 60/60 |
| opus | toon-long | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 60/60 |

**Generation lossless rate by record shape** (all models)

| shape | edn-table | edn-maps | toon | toon-long |
|---|---|---|---|---|
| flat | 60/63 (95%, [87, 98]) | 57/63 (90%, [81, 96]) | 54/63 (86%, [75, 92]) | 57/63 (90%, [81, 96]) |
| nested | 58/63 (92%, [83, 97]) | 63/63 (100%, [94, 100]) | 49/63 (78%, [66, 86]) | 56/63 (89%, [79, 95]) |
| mixed | 39/54 (72%, [59, 82]) | 54/54 (100%, [93, 100]) | 28/54 (52%, [39, 65]) | 34/54 (63%, [50, 75]) |

**External check vs upstream (Haiku 4.5)**

| format | n | upstream single-question | ours, batched (mean 3 seeds) | per-question agreement (majority) |
|---|---|---|---|---|
| json-compact | 244 | 61.9 | 61.1 | 93.4 |
| toon | 244 | 65.6 | 64.6 | 95.1 |
| csv | 109 | 49.5 | 51.4 | 99.1 |
