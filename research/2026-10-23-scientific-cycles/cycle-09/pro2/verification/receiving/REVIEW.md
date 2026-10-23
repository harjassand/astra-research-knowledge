# Independent receiving check: block spiders and marked-midpoint witnesses

**Verdict: PASS for both native inputs, all four full-action operations, and
all 66 new marked-midpoint witnesses.**

Reviewer: `/root/cycle8_finite_gate`, Cycle9, 22 October 2026. This check
imports no producer module. It uses exact `Fraction` Gaussian elimination
on independently formed unsigned-incidence normal equations, rather than
the producer's signed projection and subtree substitution. It executes
neither the accepted star-color obstruction suite nor the old 11,142-witness
closure gate.

## 1. Exact sources and what is received

The checker pins the following native sources and complete receiving records:

| File | Bytes | SHA256 |
|---|---:|---|
| `inputs/native_K24_obstruction_16.json` | 1,118 | `6e14c9ccd31a7bcc111a3ab8376c6bc32f40876be3a730d6c451052ae5f4e5a2` |
| `results/native_K24_obstruction_16_receiving.json` | 30,597 | `8bed093c685e37380f794445e1b5f7dc89439148c734b0054cf0f1a67544be0c` |
| `inputs/native_p3_unequal_branch_27.json` | 2,012 | `b426d10920f003f33242fd6187dd3d5074c8dc8b7b553bcf165e037a0ab53896` |
| `results/native_p3_unequal_branch_27_receiving.json` | 61,023 | `238e17ba51b64883e7f6a9d35da2eea21b0c5dea1b8ad2b2014d9b24055c761a` |

Both native inputs contain original vertex/edge data and provenance, without
a block decomposition, root, depth assignment, expression, or coloring.
Those structures are outputs of the native preparation. The checker
verifies each input's exact byte/hash binding in its receiving record.

The p=2 input is also bound edge-for-edge and vertex-for-vertex to graph 2
of the already accepted, hash-pinned `research/root_diagnostic/INPUTS.json`.
Only those saved original bytes are read; the obstruction search is not
executed again. Thus the positive four-action receiver is on the **same
16-vertex support** for which star-four coloring was ruled out.

The p=3 input is independently reconstructed from its stated recipe:
common p=3, k=(4,5,4,5), block parents=(None,0,0,1), and parent middle
slots=(None,0,1,1). This reconstruction uses original IDs, without importing
the input producer. It yields precisely 27 vertices and 54 edges.

## 2. Intrinsic structure checked against all original edges

For each saved block the checker reconstructs every edge of the purported
complete K_(p,k), requires common p>=2 and k>p, and verifies the exact hub
and middle lists. The block edge sets partition the original graph exactly
once. There are no omitted edges or coefficients and no added edge.

Actual vertex memberships are recomputed. Every vertex belongs to one or
two blocks; any shared vertex is a middle in both. Two blocks meet in at
most that one original vertex. The actual block-intersection graph is a
connected tree. Removing each original vertex verifies that its actual cut
vertices are exactly the saved joins.

These complete bipartite blocks are two-connected. Together with the exact
edge partition and verified cut-vertex tree, this shows that they are the
actual maximal two-connected blocks, rather than arbitrary overlapping
pieces. The root is valid, parent/depth arrays are independently recomputed
on the actual tree, and the saved construction order places every parent
before its children.

The checker also constructs and verifies an original-vertex width-p tree
decomposition: one bag containing all p hubs and one middle, internal bag
trees for each block, and connections through the actual shared middles.
Every original edge is covered and running intersection holds for every
vertex. The complete bags and tree edges are retained in `RESULT.json`.

| Native support | p | Blocks | k values | Actual cut vertices | Maximum degree |
|---|---:|---:|---|---|---:|
| Obstruction support | 2 | 3 | 4,4,4 | 2,3 | 4 |
| Unequal branching support | 3 | 4 | 4,5,4,5 | 3,4,10 | 6 |

The global hub/middle partition proves triangle-freeness for both inputs.
The p=3 graph is not claimed to be chordless or degree-four. The checker
retains an explicit chorded six-cycle from its first K_(3,4) block. This is
a genuine generalized-p receiving branch, not another instance inside the
original chordless width-two scope.

## 3. Actual designs and whole-component shape

The checker independently reconstructs both designs on original vertex IDs.
For the stable design each block's p hubs use colors 0,...,p-1. An unshared
middle receives p plus its block-depth parity; a shared middle receives p
plus the parity of its shallower incident block. The exact counts are
q=p+2. For the control, all middles receive 2p and alternating block depths
use disjoint p-color hub palettes, giving q=2p+1.

All actual rows are coordinate vectors and have whole-row squared norm one.
The colors are proper and all claimed query columns occur in these inputs.
Every original edge is assigned to its actual unordered color pair.

For every color pair the checker finds the actual connected components
from the original support. Each component is a tree. Each saved center
and arm list is then verified against the complete component: arms have
disjoint vertices, all arm edges exist, their union is the whole component,
and no component is omitted or duplicated. Stable-design arms have length
one or two; control arms all have length one.

| Input / operation | q | Edge components | Largest component | Maximum arm length |
|---|---:|---:|---:|---:|
| n16 stable | 4 | 6 | 7 | 2 |
| n16 star control | 5 | 6 | 5 | 1 |
| n27 stable | 5 | 12 | 7 | 2 |
| n27 star control | 7 | 12 | 6 | 1 |

For example, the checked n16 stable component contains the bichromatic
path `6-2-0-3`. It is a valid bounded-arm tree rather than a star. The
new operation therefore does use the weaker sufficient recovery condition
on the actual graph where star-four coloring is impossible.

This finite shape check supplements the separately reviewed all-depth
block-parity argument. It does not extrapolate a global theorem from the
largest component in the two saved inputs.

## 4. Independent exact full-action inverse

The checker reads the shared original diagonal and all original edge
coefficients as exact rational numbers. Zero coefficients remain explicit
unknown-coordinate entries; none are removed from the support. It forms
every entry of every full original action DX, then adds the actual saved
noise E and checks every observed entry of Y=DX+E.

Own-color cells recover the free diagonal. For each color-pair tree, the
checker constructs its unsigned incidence matrix B from the original edge
endpoints. Its Gram matrix has diagonal 2 and off-diagonal entries equal
to the number of endpoints shared by the two edges. It independently solves

\[
B^\mathsf T B\,d=B^\mathsf T y
\]

by exact rational Gaussian elimination, with positive pivots and exact
substitution of the solution into the original normal system. This is
independent code and a different inversion computation from the producer's
tree-flow decoder.

For noiseless actions, every recovered original coefficient agrees exactly.
For noisy actions, every independently recovered coefficient agrees with
the saved output. The full action of that output matches the saved
projection. Every diagonal normal equation is zero, and for every edge uv,

\[
(Y-\widehat D X)_{u,c(v)}+(Y-\widehat D X)_{v,c(u)}=0.
\]

Thus the output really is the canonical least-squares inverse of all
original observations, including projection of unused observation cells.
No reduced-action oracle or omitted correlation is used.

## 5. Exact errors and matched ordinary controls

Both operations within each input use the **same original D**. The control
noise is checked entrywise to equal the stable operation's noise in its
first p+2 columns, with zero columns appended. The absolute Frobenius noise
norms therefore agree exactly. The control pays all 2p+1 actions.

| Input / q | Noise Frobenius squared | Error Frobenius squared | Error/noise squared ratio |
|---|---|---|---|
| n16 / 4 | `1937/10201` | `404567/1999396` | `404567/379652` |
| n16 / 5 | `1937/10201` | `39981/255025` | `39981/48425` |
| n27 / 5 | `4024/10201` | `36589043/99969800` | `36589043/39435200` |
| n27 / 7 | `4024/10201` | `631276/2295225` | `157819/226350` |

All four projected-action residuals are exactly zero. Their raw observation
residuals are nonzero and agree with the saved values:

| Input / q | Raw `||Y-Dhat X||F^2` |
|---|---|
| n16 / 4 | `8797/142814` |
| n16 / 5 | `5302/51005` |
| n27 / 5 | `226279/1428140` |
| n27 / 7 | `37234/153015` |

The stable operation's inequality with squared Frobenius constant
3+sqrt(5) is decided exactly: for rational r=error/noise, either r<=3 or
(r-3)^2<=5 with r>3. No floating square root or solver tolerance is used.
Operator norm is bounded by Frobenius norm. Both controls pass their
squared Frobenius bound 2. In these particular saved records their
Frobenius ratios are already <=3/2, which also certifies the claimed
operator inequality directly. No additional dense PSD calculation is needed.

The universal stable/operator estimates come from the separately reviewed
spider Poincare and star-recovery arguments. Four successful fixed-noise
checks do not prove those all-noise results. Likewise, the observed smaller
control errors do not establish average error or practical runtime
dominance. The control has the stronger uniform conditioning theorem and
uses additional actions; both facts remain visible in the comparison.

## 6. The 66 new marked-midpoint witnesses

The checker reads the exact previously accepted literal certificate from
`sources/cycle8_selected/loaded_star_certificate.json`, 982,625 bytes,
SHA256 `63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525`.
It does not execute its old closure gate or recheck its 11,142 transitions.

The new `results/marked_root_projection.json` is 26,859 bytes, SHA256
`7a0bcde13cead849e1e828bbae564d1f3244f4dc65c9a37b0c173e0fb899fbfc`.
Its 66 rows cover exactly once every inherited family with both actual
port loads at most three. Each row selects an actual target of its named
family, with the exact target index, colors, degrees, supports and flags.

For each target, terminal colors a,b are distinct and the new actual
midpoint color z differs from both. The inherited far-repeat bounds exclude
z at both ports, so adding the actual path a-z-b causes no forbidden old
edge repeat. Its root neighbors remain differently colored. The root's
far-flag upper bound is checked as

\[
\bigl(\{a\}\text{ if }z\in N_L\bigr)
\cup\bigl(\{b\}\text{ if }z\in N_R\bigr).
\]

All exact degree budgets and masks match the saved rows. There are **61
zero-flag upper bounds and five one-flag upper bounds**, with no empty
active-family case.

This new literal check is conditional on the accepted inherited family
guarantees and the marked-midpoint structural representation. It supports
one actual marked degree-two vertex at a time. It neither supplies
simultaneous mark choices nor constitutes an additional native marked-atom
receiving experiment. The known multi-attachment obstruction is unchanged.

## 7. Preserved failure and implementation limits

The first receiver attempt failed during component certification because
the parent-vertex variable `p` overwrote the common hub-side dimension `p`.
The failure was not a successful numerical result and wrote no receiver.
The fixed receiving records checked here are separate from that attempt.

The archived failed source is 8,337 bytes, SHA256
`28795e7c60ee47938c5d38a59f2d790b01d75261b9ce7acfe5d69f50bc8f595f`.
Its receipt `failed/RECEIVER_ATTEMPT_01.json` is 763 bytes, SHA256
`2985de5289b4963d2f4e2a222a9d332c936232d8c6513c4ae92a63ff6a859d2b`.
Both are hash-bound by the checker. The failed run was not instrumented;
its body wall/CPU/RSS costs remain unknown, rather than being set to zero.
The failed source was read and preserved, not executed again.

The independent structural review separately identified a list-membership
cost that would have been quadratic for unbounded block sizes. The actual
source now caches middle sets; that correction and the sorting cost belong
to preparation accounting. The receiving check does not convert these
small input timings into a performance theorem or count a possible faster
algorithm as already implemented.

This review establishes correctness of the actual prepared structures and
outputs, with their exact source binding. It is not historical priority,
outside scientific acceptance, integration, or an application advantage.
The full arbitrary-real four-query problem remains separate.

## 8. Replay and observed check cost

From the owner archive root:

```
python verification/receiving/verify_receiving.py \
  --output verification/receiving/RESULT.replay.json
```

The first execution passed. Total check body wall time was
0.10583182400023361 seconds, CPU time 0.10218705499999998 seconds, and
peak RSS 21,499,904 bytes. The 66-witness projection's source read/parse
and checks are included in that total. These are check costs, not discovery
costs. See `COSTS.md` for scope and unknown totals.
