# Exact rational entropy-closure control table

Rates, entropies and jump counts are rounded display values; the weighted-L1 bound is rounded upward. The JSON contains exact rational certificate endpoints.

| lambda | Hidden states | Phase rate (approx.) | E (approx.) | E/5 (approx.) | Preparation KL (approx.) | Micro jumps/departure (approx.) | Weighted-L1 upper bound | Entry denominator bits |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 132 | 1.6640625000 | 0.3852639605 | 0.0770527921 | 0.1678094166 | 3.4960937500 | 2.1208920188 | 11 |
| 4 | 650 | 3.6576361452 | 0.6275351882 | 0.1255070376 | 0.2300053581 | 6.4864542178 | 1.1495086511 | 49 |
| 8 | 3,306 | 7.6534711088 | 0.7780062160 | 0.1556012432 | 0.2580289793 | 12.4802066632 | 0.6019698097 | 169 |
| 16 | 16,770 | 15.6524536564 | 0.8698764040 | 0.1739752808 | 0.2715163356 | 24.4786804847 | 0.3060506601 | 513 |
| 32 | 83,810 | 31.6534111777 | 0.9249229587 | 0.1849845917 | 0.2781280832 | 48.4801167665 | 0.1526185361 | 1441 |
| 64 | 411,522 | 63.6552133585 | 0.9572993914 | 0.1914598783 | 0.2813834544 | 96.4828200377 | 0.0752708812 | 3841 |
| 128 | 1,986,690 | 127.6571865792 | 0.9760184034 | 0.1952036807 | 0.2829883637 | 192.4857798688 | 0.0369256608 | 9857 |

This supplied analytic task has direct observable entropy J=1. The family demonstrates the completion and its execution costs; it does not beat direct evaluation of J.
