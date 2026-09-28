
#### tokens datasets — o200k

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 14,211 | 9,115 | 14,940 | 9,120 | 8,383 | 22,245 | 17,858 | 26,616 | +5.1% | +0.1% |
| github | flat | 11,640 | 8,937 | 12,332 | 9,465 | 8,711 | 15,337 | 13,337 | 17,294 | +5.9% | +5.9% |
| tabular | flat | 79,057 | 49,978 | 85,056 | 55,075 | 47,153 | 127,061 | 100,054 | 146,605 | +7.6% | +10.2% |
| event-logs | mixed | 128,529 | 154,084 | 134,528 | 134,528 | – | 181,201 | 155,397 | 205,859 | +4.7% | -12.7% |
| keyed | mixed | 15,635 | 10,503 | 15,635 | 15,635 | – | 23,141 | 17,905 | 28,655 | +0.0% | +48.9% |
| nested | mixed | 68,944 | 72,832 | 74,441 | 71,301 | – | 108,611 | 84,701 | 122,119 | +8.0% | -2.1% |
| nested-config | mixed | 552 | 589 | 586 | 578 | – | 905 | 662 | 997 | +6.2% | -1.9% |
| nested-group | mixed | 46,791 | 26,726 | 50,799 | 50,799 | – | 79,779 | 55,475 | 90,306 | +8.6% | +90.1% |
| **total flat** | flat | **104,908** | **68,030** | **112,328** | **73,660** | **64,247** | **164,643** | **131,249** | **190,515** | **+7.1%** | **+8.3%** |
| **total mixed** | mixed | **260,451** | **264,734** | **275,989** | **272,841** | – | **393,637** | **314,140** | **447,936** | **+6.0%** | **+3.1%** |

#### tokens datasets — qwen3

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 18,881 | 13,788 | 19,611 | 13,791 | 13,054 | 26,916 | 22,529 | 31,287 | +3.9% | +0.0% |
| github | flat | 15,004 | 12,502 | 15,697 | 13,028 | 12,274 | 18,702 | 16,713 | 20,436 | +4.6% | +4.2% |
| tabular | flat | 93,095 | 63,797 | 99,095 | 69,114 | 60,970 | 141,100 | 114,122 | 160,021 | +6.4% | +8.3% |
| event-logs | mixed | 154,156 | 181,714 | 162,156 | 162,156 | – | 208,829 | 183,025 | 229,487 | +5.2% | -10.8% |
| keyed | mixed | 18,028 | 13,862 | 18,527 | 18,527 | – | 26,033 | 20,773 | 31,834 | +2.8% | +33.7% |
| nested | mixed | 82,736 | 87,511 | 89,234 | 86,094 | – | 123,404 | 98,878 | 136,016 | +7.9% | -1.6% |
| nested-config | mixed | 597 | 643 | 639 | 631 | – | 960 | 719 | 1,042 | +7.0% | -1.9% |
| nested-group | mixed | 49,065 | 29,773 | 54,066 | 54,066 | – | 83,046 | 58,676 | 92,929 | +10.2% | +81.6% |
| **total flat** | flat | **126,980** | **90,087** | **134,403** | **95,933** | **86,298** | **186,718** | **153,364** | **211,744** | **+5.8%** | **+6.5%** |
| **total mixed** | mixed | **304,582** | **313,503** | **324,622** | **321,474** | – | **442,272** | **362,071** | **491,308** | **+6.6%** | **+2.5%** |

#### tokens datasets — claude-haiku-4.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 14,212 | 8,752 | 16,037 | 9,486 | 8,384 | +12.8% | +8.4% |
| github | flat | 12,707 | 9,439 | 13,758 | 10,296 | 9,287 | +8.3% | +9.1% |
| tabular | flat | 95,109 | 59,087 | 105,068 | 69,089 | 56,672 | +10.5% | +16.9% |
| event-logs | mixed | 135,716 | 162,161 | 143,716 | 143,716 | – | +5.9% | -11.4% |
| keyed | mixed | 17,092 | 11,112 | 17,591 | 17,591 | – | +2.9% | +58.3% |
| nested | mixed | 80,500 | 83,037 | 87,988 | 83,643 | – | +9.3% | +0.7% |
| nested-config | mixed | 668 | 698 | 672 | 664 | – | +0.6% | -4.9% |
| nested-group | mixed | 54,818 | 32,796 | 57,777 | 57,777 | – | +5.4% | +76.2% |
| **total flat** | flat | **122,028** | **77,278** | **134,863** | **88,871** | **74,343** | **+10.5%** | **+15.0%** |
| **total mixed** | mixed | **288,794** | **289,804** | **307,744** | **303,391** | – | **+6.6%** | **+4.7%** |

#### tokens datasets — claude-opus-5.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 18,961 | 8,762 | 18,960 | 9,501 | 8,393 | -0.0% | +8.4% |
| github | flat | 16,743 | 11,285 | 16,603 | 12,155 | 11,125 | -0.8% | +7.7% |
| tabular | flat | 131,583 | 77,603 | 129,541 | 87,570 | 75,187 | -1.6% | +12.8% |
| event-logs | mixed | 189,345 | 200,233 | 187,566 | 187,566 | – | -0.9% | -6.3% |
| keyed | mixed | 24,855 | 12,879 | 22,854 | 22,854 | – | -8.1% | +77.5% |
| nested | mixed | 110,271 | 100,077 | 108,261 | 103,801 | – | -1.8% | +3.7% |
| nested-config | mixed | 911 | 866 | 889 | 881 | – | -2.4% | +1.7% |
| nested-group | mixed | 78,741 | 45,769 | 75,723 | 75,723 | – | -3.8% | +65.4% |
| **total flat** | flat | **167,287** | **97,650** | **165,104** | **109,226** | **94,705** | **-1.3%** | **+11.9%** |
| **total mixed** | mixed | **404,123** | **359,824** | **395,293** | **390,825** | – | **-2.2%** | **+8.6%** |

#### accuracy datasets — o200k

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 2,341 | 1,515 | 2,460 | 1,520 | 1,393 | – | – | – | +5.1% | +0.3% |
| github | flat | 11,640 | 8,937 | 12,332 | 9,465 | 8,711 | – | – | – | +5.9% | +5.9% |
| structural-validation-control | flat | 762 | 486 | 821 | 540 | 458 | – | – | – | +7.7% | +11.1% |
| structural-validation-extra-rows | flat | 883 | 564 | 951 | 625 | 532 | – | – | – | +7.7% | +10.8% |
| structural-validation-missing-fields | flat | 722 | 455 | 777 | 504 | 427 | – | – | – | +7.6% | +10.8% |
| structural-validation-truncated | flat | 650 | 418 | 700 | 464 | 393 | – | – | – | +7.7% | +11.0% |
| structural-validation-width-mismatch | flat | 757 | 483 | 816 | 537 | 455 | – | – | – | +7.8% | +11.2% |
| tabular | flat | 3,909 | 2,457 | 4,208 | 2,727 | 2,321 | – | – | – | +7.6% | +11.0% |
| event-logs | mixed | 4,783 | 5,734 | 5,007 | 5,007 | – | – | – | – | +4.7% | -12.7% |
| keyed | mixed | 1,254 | 851 | 1,254 | 1,254 | – | – | – | – | +0.0% | +47.4% |
| nested | mixed | 6,865 | 7,264 | 7,414 | 7,104 | – | – | – | – | +8.0% | -2.2% |
| nested-config | mixed | 552 | 589 | 586 | 578 | – | – | – | – | +6.2% | -1.9% |
| nested-group | mixed | 2,347 | 1,364 | 2,547 | 2,547 | – | – | – | – | +8.5% | +86.7% |
| **total flat** | flat | **21,664** | **15,315** | **23,065** | **16,382** | **14,690** | – | – | – | **+6.5%** | **+7.0%** |
| **total mixed** | mixed | **15,801** | **15,802** | **16,808** | **16,490** | – | – | – | – | **+6.4%** | **+4.4%** |

#### accuracy datasets — qwen3

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | json-pretty | yaml | xml | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analytics | flat | 3,103 | 2,279 | 3,223 | 2,283 | 2,156 | – | – | – | +3.9% | +0.2% |
| github | flat | 15,004 | 12,502 | 15,697 | 13,028 | 12,274 | – | – | – | +4.6% | +4.2% |
| structural-validation-control | flat | 874 | 594 | 934 | 653 | 565 | – | – | – | +6.9% | +9.9% |
| structural-validation-extra-rows | flat | 1,013 | 690 | 1,082 | 756 | 657 | – | – | – | +6.8% | +9.6% |
| structural-validation-missing-fields | flat | 834 | 563 | 890 | 617 | 534 | – | – | – | +6.7% | +9.6% |
| structural-validation-truncated | flat | 744 | 508 | 795 | 559 | 482 | – | – | – | +6.9% | +10.0% |
| structural-validation-width-mismatch | flat | 865 | 587 | 925 | 646 | 558 | – | – | – | +6.9% | +10.1% |
| tabular | flat | 4,499 | 3,039 | 4,799 | 3,318 | 2,901 | – | – | – | +6.7% | +9.2% |
| event-logs | mixed | 5,746 | 6,774 | 6,046 | 6,046 | – | – | – | – | +5.2% | -10.7% |
| keyed | mixed | 1,403 | 1,075 | 1,442 | 1,442 | – | – | – | – | +2.8% | +34.1% |
| nested | mixed | 8,215 | 8,700 | 8,865 | 8,555 | – | – | – | – | +7.9% | -1.7% |
| nested-config | mixed | 597 | 643 | 639 | 631 | – | – | – | – | +7.0% | -1.9% |
| nested-group | mixed | 2,459 | 1,517 | 2,710 | 2,710 | – | – | – | – | +10.2% | +78.6% |
| **total flat** | flat | **26,936** | **20,762** | **28,345** | **21,860** | **20,127** | – | – | – | **+5.2%** | **+5.3%** |
| **total mixed** | mixed | **18,420** | **18,709** | **19,702** | **19,384** | – | – | – | – | **+7.0%** | **+3.6%** |

#### accuracy datasets — claude-haiku-4.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 2,342 | 1,457 | 2,642 | 1,581 | 1,394 | +12.8% | +8.5% |
| github | flat | 12,707 | 9,439 | 13,758 | 10,296 | 9,287 | +8.3% | +9.1% |
| structural-validation-control | flat | 914 | 572 | 1,014 | 675 | 546 | +10.9% | +18.0% |
| structural-validation-extra-rows | flat | 1,056 | 660 | 1,171 | 778 | 630 | +10.9% | +17.9% |
| structural-validation-missing-fields | flat | 869 | 535 | 965 | 634 | 509 | +11.0% | +18.5% |
| structural-validation-truncated | flat | 780 | 492 | 865 | 580 | 469 | +10.9% | +17.9% |
| structural-validation-width-mismatch | flat | 909 | 569 | 1,008 | 672 | 543 | +10.9% | +18.1% |
| tabular | flat | 4,729 | 2,947 | 5,229 | 3,450 | 2,827 | +10.6% | +17.1% |
| event-logs | mixed | 5,042 | 6,026 | 5,342 | 5,342 | – | +6.0% | -11.4% |
| keyed | mixed | 1,371 | 905 | 1,410 | 1,410 | – | +2.8% | +55.8% |
| nested | mixed | 8,032 | 8,291 | 8,780 | 8,350 | – | +9.3% | +0.7% |
| nested-config | mixed | 668 | 698 | 672 | 664 | – | +0.6% | -4.9% |
| nested-group | mixed | 2,751 | 1,666 | 2,898 | 2,898 | – | +5.3% | +73.9% |
| **total flat** | flat | **24,306** | **16,671** | **26,652** | **18,666** | **16,205** | **+9.7%** | **+12.0%** |
| **total mixed** | mixed | **17,864** | **17,586** | **19,102** | **18,664** | – | **+6.9%** | **+6.1%** |

#### accuracy datasets — claude-sonnet-5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 3,126 | 1,467 | 3,125 | 1,596 | 1,403 | -0.0% | +8.8% |
| github | flat | 16,743 | 11,285 | 16,603 | 12,155 | 11,125 | -0.8% | +7.7% |
| structural-validation-control | flat | 1,280 | 759 | 1,259 | 868 | 732 | -1.6% | +14.4% |
| structural-validation-extra-rows | flat | 1,477 | 875 | 1,453 | 999 | 844 | -1.6% | +14.2% |
| structural-validation-missing-fields | flat | 1,211 | 702 | 1,190 | 807 | 675 | -1.7% | +15.0% |
| structural-validation-truncated | flat | 1,096 | 656 | 1,078 | 750 | 632 | -1.6% | +14.3% |
| structural-validation-width-mismatch | flat | 1,273 | 756 | 1,252 | 865 | 729 | -1.6% | +14.4% |
| tabular | flat | 6,541 | 3,860 | 6,440 | 4,369 | 3,739 | -1.5% | +13.2% |
| event-logs | mixed | 7,037 | 7,442 | 6,972 | 6,972 | – | -0.9% | -6.3% |
| keyed | mixed | 1,993 | 1,051 | 1,832 | 1,832 | – | -8.1% | +74.3% |
| nested | mixed | 10,987 | 9,975 | 10,785 | 10,345 | – | -1.8% | +3.7% |
| nested-config | mixed | 911 | 866 | 889 | 881 | – | -2.4% | +1.7% |
| nested-group | mixed | 3,976 | 2,344 | 3,822 | 3,822 | – | -3.9% | +63.1% |
| **total flat** | flat | **32,747** | **20,360** | **32,400** | **22,409** | **19,879** | **-1.1%** | **+10.1%** |
| **total mixed** | mixed | **24,904** | **21,678** | **24,300** | **23,852** | – | **-2.4%** | **+10.0%** |

#### accuracy datasets — claude-opus-5.5

| dataset | track | json-compact | toon | edn-maps | edn-table | csv | EDN-maps vs JSON-c | EDN-table vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | flat | 3,126 | 1,467 | 3,125 | 1,596 | 1,403 | -0.0% | +8.8% |
| github | flat | 16,743 | 11,285 | 16,603 | 12,155 | 11,125 | -0.8% | +7.7% |
| structural-validation-control | flat | 1,280 | 759 | 1,259 | 868 | 732 | -1.6% | +14.4% |
| structural-validation-extra-rows | flat | 1,477 | 875 | 1,453 | 999 | 844 | -1.6% | +14.2% |
| structural-validation-missing-fields | flat | 1,211 | 702 | 1,190 | 807 | 675 | -1.7% | +15.0% |
| structural-validation-truncated | flat | 1,096 | 656 | 1,078 | 750 | 632 | -1.6% | +14.3% |
| structural-validation-width-mismatch | flat | 1,273 | 756 | 1,252 | 865 | 729 | -1.6% | +14.4% |
| tabular | flat | 6,541 | 3,860 | 6,440 | 4,369 | 3,739 | -1.5% | +13.2% |
| event-logs | mixed | 7,037 | 7,442 | 6,972 | 6,972 | – | -0.9% | -6.3% |
| keyed | mixed | 1,993 | 1,051 | 1,832 | 1,832 | – | -8.1% | +74.3% |
| nested | mixed | 10,987 | 9,975 | 10,785 | 10,345 | – | -1.8% | +3.7% |
| nested-config | mixed | 911 | 866 | 889 | 881 | – | -2.4% | +1.7% |
| nested-group | mixed | 3,976 | 2,344 | 3,822 | 3,822 | – | -3.9% | +63.1% |
| **total flat** | flat | **32,747** | **20,360** | **32,400** | **22,409** | **19,879** | **-1.1%** | **+10.1%** |
| **total mixed** | mixed | **24,904** | **21,678** | **24,300** | **23,852** | – | **-2.4%** | **+10.0%** |

#### Primer lines (tokens, prepended to every call)

| format | o200k | qwen3 | claude-haiku-4.5 | claude-sonnet-5 | claude-opus-5.5 |
|---|---|---|---|---|---|
| json-compact | 10 | 10 | 13 | 22 | 22 |
| toon | 80 | 81 | 96 | 124 | 124 |
| csv | 15 | 15 | 17 | 23 | 23 |
| edn-maps | 29 | 28 | 32 | 44 | 44 |
| edn-table | 29 | 28 | 32 | 44 | 44 |
| edn-table-primer | 144 | 143 | 159 | 206 | 206 |

#### Primer break-even (payload size in records)

Cost of a call = primer line + data block. `edn-table+P` = LONG primer + EDN-table data. Break-even = smallest n in the grid where edn-table+P ≤ the comparator ("never" if not reached by the largest n).

| family | tokenizer | vs JSON-c (no primer) | vs JSON-c (+its primer) | vs TOON (+its primer) | vs TOON (no primer) | vs EDN-table (short primer) | per-record saving vs JSON-c | per-record Δ vs TOON |
|---|---|---|---|---|---|---|---|---|
| analytics | o200k | 20 | 20 | never | never | never | +13.9 tok | +0.0 tok |
| analytics | qwen3 | 20 | 20 | never | never | never | +13.9 tok | +0.0 tok |
| employees | o200k | 20 | 20 | never | never | never | +12.0 tok | +2.5 tok |
| employees | qwen3 | 20 | 20 | never | never | never | +12.0 tok | +2.7 tok |
| event-logs | o200k | never | never | 10 | 20 | never | -3.0 tok | -9.8 tok |
| event-logs | qwen3 | never | never | 10 | 20 | never | -4.0 tok | -9.8 tok |
| github | o200k | 10 | 10 | never | never | never | +21.8 tok | +5.3 tok |
| github | qwen3 | 10 | 10 | never | never | never | +19.8 tok | +5.3 tok |
| orders | o200k | never | never | 20 | 50 | never | -4.7 tok | -3.1 tok |
| orders | qwen3 | never | never | 20 | 100 | never | -6.7 tok | -2.8 tok |
