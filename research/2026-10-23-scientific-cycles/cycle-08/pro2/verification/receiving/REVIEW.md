# Independent new full-action receiving gate

Cycle8 PRO2, 22 October 2026. Reviewer: `/root/cycle8_finite_gate`.
This is a second, separate obligation from the finite all-depth certificate
gate. It checks two actual new original-support receiving operations. It
does not rerun an old Cycle7 fixture, family discovery or physical benchmark.

## Verdict and source binding

**Both records PASS on the first independent execution.**

| Record | Bytes | SHA256 |
|---|---:|---|
| `A5_three_action_control.json` | 8,482 | `3fb018f3f8d7d0acd9a8a6f4c5df3570cbe024fd54bcce69f50379ec2f196188` |
| `mixed_loaded_16_four_action.json` | 14,889 | `b6396938e76b2b2adb199e103a48bf4087222a78e62e9a45387d790e5acee9df` |

The independent checker `verify_receiving.py` imports no producer module.
It reads and authenticates these exact bytes before performing any check.

For A5 it independently builds the original A_L recipe: doubled two-edge
paths a-b and a-c, and the length-five b-c path, with the actual branch and
internal vertex labels. It independently generates the three-color path
word from the stated base-word/201 rule and matches the entire saved graph
and coloring. The support has 11 vertices and 13 edges and uses all three
claimed directions. This is the stronger control, not evidence for a
four-query gain on A_L.

For the mixed graph it independently expands the saved **original** supplied
expression as an uncolored graph, then separately expands its saved
normalized expression. Both give exactly the saved 16 vertices, 20 edges,
vertex IDs and terminal loads (4,3). Every description node pays its actual
series/parallel/extension degree test. Repeated child references expand as
distinct copies. The checker uses recursive original productions rather
than importing the producer's stack constructor or coloring transitions.
It also matches the saved 19 normalized expanded occurrences.

## Actual support and query checks

For each graph the checker verifies simplicity, the full supplied edge set,
properness, triangle-freeness, maximum degree at most four, distinct
nonadjacent terminals and their exact degrees. It computes every vertex's
actual per-color neighbor multiplicities and matches the saved arrays.
Every edge passes the original multiplicity-based no-bichromatic-P4 test.
Thus the support/flag interface did not replace actual multiplicities in
the receiving operation.

The design is exactly the indicated coordinate seed. Each row has one unit
entry, total row squared norm one, and every claimed color/action is used.
The mixed graph's actual root supports and far-end flags also satisfy its
saved upper-profile target, with degree-four saturation interpreted as an
unspecified color rather than an additional palette value.

The mixed support contains the actual five-cycle

    1 -- 12 -- 2 -- 13 -- 14 -- 1.

This is a useful scope check: a C5 cannot be star-three colored. In a proper
three-coloring each color class has at most two vertices, so one class is a
singleton. Deleting it leaves a four-vertex path in the other two colors,
which violates the star condition. The saved four-coloring therefore has
optimal query count **within star-coordinate designs on this fixture**.
This is not an arbitrary-real three-query lower bound, nor does it exclude
another acyclic three-coordinate recovery design.

## Independent numerical operation

All arithmetic uses exact Python rational numbers. The checker reconstructs
the saved supported symmetric matrix, including every nonzero free diagonal
and edge entry, and the nonzero n-by-q noise array. It independently forms
the entire original action DX and Y=DX+E and compares every saved entry.
No reduced graph, reduced action, known-edge oracle or omitted noise cell
is used.

Recovery is independently implemented through analytic bichromatic-star
least squares, not the producer's tree-substitution routine. For a star
with center observation y0 and k leaf observations y_i, it uses

    d_hat_i = y_i + (y0 - sum_j y_j)/(k+1).

Diagonal values come from own-color action cells. Every edge is recovered
exactly once. This independently recovers the original matrix from the
noiseless action, and every noisy output coefficient matches the saved
output exactly.

The action of that output matches the saved projected action. In addition,
the checker verifies the full normal equations directly: the observation
residual is zero in each diagonal cell, and its two action entries for
each supported edge sum to zero. Since the output action lies in the
supported range, these equations establish the orthogonal projection.
The zero reported projected-action residual is **not** a claim that the
raw noisy observation residual is zero.

| Quantity | A5, three actions | Mixed, four actions |
|---|---|---|
| Noise norm squared | 464/10201 | 890/10201 |
| Matrix Frobenius error squared | 63473/1530150 | 565843/9180900 |
| Output-action minus projected-action norm squared | 0 | 0 |
| Raw observation residual norm squared | 757/102010 | 10711/306030 |
| Exact PSD pivots matched | 11 | 16 |

For an additional exact operator check, form

    C = (3/2) ||E||F^2 I - (Dhat-D)^2.

The checker computes an independent LDL^T recurrence, compares all saved
pivots, and reconstructs every entry of C from the factors. All pivots are
strictly positive on both records. This proves the displayed operator bound
for the actual saved errors without a floating eigensolver.

This finite PSD check is additional receiving verification. The uniform
all-noise operator bound sqrt(3/2), and Frobenius bound sqrt(2), still come
from the retained triangle-free star-recovery proof. A successful numerical
instance alone would not establish those universal bounds.

## Costs and limits

The independent two-record gate body took 0.01593741100805346 seconds wall
and 0.015934076999999998 seconds CPU. Maximum process RSS was 12,320,768
bytes. It includes source reads and hashes, graph reconstruction, complete
original actions, analytic recovery, projection equations, and exact LDL
verification. Startup and final receipt serialization are excluded.

Individual bodies were 0.004462732991669327 seconds for A5 and
0.011363262994564138 seconds for the mixed graph; these are already inside
the total and must not be counted twice. Source reading, reasoning, checker
authoring, review writing and integration totals remain unknown. Producer
construction, failed searches, its own receiving work, and finite-certificate
verification remain separate additional costs.

No application speedup, historical priority, external acceptance or practical
advantage over the full-class five-query control is established by this gate.
The stronger three-query A_L control and all previous constants are retained.

## Reproduction

From the package root:

```
python verification/receiving/verify_receiving.py \
  --output independent_receiving_result.json
```

The checker defaults to the package's `results/` directory and pins both
record identities. `RESULT.json` is the observed machine receipt.
