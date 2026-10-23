# Exact full-law Jensen certificate for the actual45 map

22 October 2026. Fixed-map theorem; no universal Morrey conclusion.

Let u be the continuous zero-boundary P1 map on 2P specified by the raw
28-node, 45-triangle certificate
`../../strip_recursion/LEAD_EXACT_TRIANGLE_PACKET.json`. Its normalized
gradient law has 40 coalesced atoms A_i and exact rational weights w_i.
Then, for every finite globally rank-one-convex F on R^(2x2) and every
affine background B,

    sum_i w_i F(B+A_i) >= F(B).

Thus this *whole* actual gradient law cannot give a Morrey counterexample,
including for an integrand other than the displayed translated K test.
The previously negative conditional-strip law is a proper restriction of
this law and is not given a Jensen certificate by this theorem.

## Exact finite data

The corrected V2 allocation has 39 positive root children. Each child is
a finite binary rank-one tree, with three or four leaves from the actual
40-atom support. There are eight three-leaf trees, five four-leaf combs,
and 26 balanced four-leaf trees. Their roots C_j and positive rational
masses alpha_j obey exactly

    det C_j=0,   sum_j alpha_j=1,   sum_j alpha_j C_j=0.

The weighted terminal masses of these trees recover every w_i exactly.
The independent selected-tree replay checks every binary edge and all
40 terminal rows. Two independent original-node-to-tree audits now pass:
`../geometry/actual45_original_source_tree_audit.json` reconstructs the
field using stdlib Fraction without V2/source-law imports, and
`../../adversary/actual45_v2_original_mesh_tree_audit.md` records a separate
BigInt-isolate reconstruction. Both check all 109 strict binary splits.
These arithmetic/proof audits are not external correctness review.

Frozen artifacts and hashes:

- Raw field: `../../strip_recursion/LEAD_EXACT_TRIANGLE_PACKET.json`,
  `ef8f06493cec8554858d472f52f10d25bbee20892bc7b2e27391e9f3e5d054ab`.
- V2 dictionary: `actual45_extended_dictionary_v2.json`,
  `e92a1aa4fb530d57fd61c47f44d7fa299cf9c2c89abeda3b61099d73cb0b1777`.
- Exact allocation: `actual45_extended_allocation_v2.json`,
  `ef8abf78231813f5b0b6790fd01a8e69bcf8c00367638cab3de43afa8caeb6bf`.
- Selected-tree replay: `actual45_selected_tree_replay_v2.json`,
  `bfb8e732b009eec39290495e49e97d1b908a32edd061efef6985c89ec0cb1956`.
- Independent original-source Fraction receipt:
  `../geometry/actual45_original_source_tree_audit.json`,
  `d14f5301f9267a005db4bd4fcf85ff650252a239e8f95739dd6d1e4ddbb7bf82`.

The V2 dictionary has 13,970 exact columns. This number is a search
provenance fact, not part of the theorem: only the 39 displayed exact
trees and their exact mass recovery are needed. The earlier V1 attempt
and the V2 seed-field report failure remain preserved. The failed V2
call reached its optimizer but wrote no allocation result; no result is
inferred from that failed invocation.

## Why a root star proves Jensen

A finite rank-one-convex F is locally Lipschitz, since it is separately
convex in the four matrix entries. Let F_epsilon be its convolution with
a nonnegative compact smooth matrix-space mollifier. It is smooth and
rank-one convex and converges locally uniformly to F.

Since det C_j=0, the whole line t -> B+t C_j has rank-one direction (or
is constant). Convexity on this line gives its tangent inequality

    F_epsilon(B+C_j) >= F_epsilon(B)+DF_epsilon(B):C_j.

The positive weighted sum of these inequalities is at least
F_epsilon(B), because the root mean is zero. Binary rank-one convexity
at every edge of the j-th finite tree bounds its root value by its
weighted terminal values. Sum over the roots, use exact terminal mass
recovery, and take epsilon to zero on the finite set of matrices. This
proves the asserted inequality. Pairwise rank-one connections between
different roots are unnecessary; a binary root assembly is not claimed.

The proof also applies to F(B+L A_i R), for fixed matrix factors L,R,
since rank-one directions remain rank at most one under these changes.
It applies after adding any zero-gradient exterior area, which takes a
positive mixture of this law and delta_0. Consequently the standard
zero extension and rescaling to a box preserve the theorem.

This proof is independent of the separate QC theorem for K. The latter
is needed to label the conditional-strip example a QC conditional Jensen
failure; it is not needed for this full-law R1C certificate.

## Structural question that remains

The first component is the concave pyramid

    u1(x)=2+min{(1,1).x,(2,-4/5).x,(-3,-1/5).x}.

The actual30 example also has one concave component after an output sign
change. Most selected actual45 bottom ports stay in one fixed-first-row
fiber, while several selected trees genuinely use all three first rows.
No theorem here completes arbitrary concave-component P1 maps. The next
obligation is a positive port or surgery identity that works for arbitrary
compatible trace data, rather than another allocation for isolated data.
