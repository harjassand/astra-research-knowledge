# Constructing the common law: proof operations, prior art and cost

[Result guide](README.md) · [Complete supplied proof outline](P1_HARD_DISCREPANCY_COVARIANCE_20261106_RETURN.txt) · [Deductions and exact example](corollaries-and-exact-tradeoff.md)

## The additional operation is linear-plus-quadratic response

For rational `c` and positive semidefinite rational `Q`, the source constructs a hard-bounded feasible vertex `v` with

```
c^T(v-x)+(v-x)^T Q(v-x) <= 65 k tr(Q D_x).
```

It uses the original linear optimization oracle, rather than assuming quadratic optimization, a good-vertex optimization oracle or an existing sampler.

Short edges leave enough original-face directions: if `s` coordinates vary, `dim(F)>=s/k`. The original face can be recovered through the symmetric core and the optimization interface without a supplied facet/face oracle. A quadratic compensation budget has sufficiently few positive-curvature directions to coexist with the hard-discrepancy constraints, linear cost and descent. Movement preserves the original face; shrinking faces are counted even when every coordinate remains fractional.

The finite-bit argument includes a positive ridge, certified rational spectral derivatives/directions, strict curvature slack and step-or-original-face-endpoint progress. An exact repair LP inside a small dyadic box preserves original affine/measurement equations while controlling denominator growth. Independent coordinate rounding is not used to break exact equalities.

Terminal fractional coordinates have an exact finite decomposition; a favorable atom gives the response inequality. Convex separation then implies a common mean/covariance law. A quantitative separator-ball/ellipsoid construction collects enough good vertices, closing the gap between existence and finding support. Final extraction keeps rational mean equations exact and uses covariance slack/interiority rather than assuming every boundary SDP has a short rational feasible solution. Exact moment-preserving linear algebra compresses support.

These are the supplied mathematical and oracle-relative algorithmic claims. The actual walk, support collection and rational extraction were not run as a full general pipeline.

## Prior work constrains the novelty

Astra N752 already supplies constructive short-edge hard discrepancy with exact marginals, face access, precision repair and extraction; that first novelty claim was withdrawn. Bansal already combines iterative rounding and concentration under its update/slack hypotheses. Ercan supplies stronger convex-order results with simultaneous-exchange hypotheses not provided by an arbitrary short-edge polytope. Its broader base-polyhedron guarantee does not automatically add arbitrary supplied hard measurements. Weighted matroid methods can be substantially more attractive in applicable parameter regimes.

The proposed contribution is this joint contract and construction under explicit geometry/linear-optimization access. Historical priority for that combination remains unresolved. No generic variance-compensation principle, convex separation or ordinary projection principle is claimed as newly invented.

## Polynomial does not mean usable here

The source's conservative favorable-response iteration bound is of order `2^180 (n+1) T_0^42+n+2`, with `T_0=O(m+n^2)` and large constants, before further collection/extraction work. That is not practical scalability. If the required original-set optimizer is NP-hard, this reduction does not make it cheap. An exponentially long measurement list remains exponential input. All oracle objectives, bit precision, capacity/function values and input acquisition are paid.

The exploration record describes governing Astra material outside the earlier quantum cluster. Public Zenodo metadata also informed the search, but relevant payload requests failed; unavailable proofs/code were excluded from premises and no benchmark was claimed reproduced. Those source ledgers are promised in the held original, not independently reconstructed here.

Reported checks include exact K4 laws, a pairwise-independent law, 60 terminal-covariance fixtures, original-face/slice repairs, 32 compensated-quadratic line cases, 1,000 parameter checks, restricted-resolvent tests and two local spectral-curvature checks. Synthetic local states were not proved reachable by the full walk. Floating checks are not interval certificates. Capital ran no source computation, solver or new audit.
