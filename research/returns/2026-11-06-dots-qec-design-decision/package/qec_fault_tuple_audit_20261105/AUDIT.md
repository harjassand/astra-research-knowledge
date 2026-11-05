# Independent ordered-fault proposal audit

This audit establishes the abstract sampling law, checks the concrete d13/d21
rational tables and frozen sampler, and independently replays the two fixed
statistical runs below. It does not establish novelty, a speed advantage over
optimized external competitors, or a hardware failure probability.

## Coverage and cancellation

Let E be the independent edge-error vector and C(E) an exact minimum-cost
correction with the same interior syndrome. All decoder costs are strictly
positive. For a failure, fix one deterministic simple left-to-right path P in
E xor C(E), with its orientation fixed from left to right. Toggling P in C is a
valid competing correction, so the total cost of faulty edges on P is at least
the total cost of clean edges on P. In particular there is at least one faulty
edge. Define F(E) to be their ordered, oriented list.

For any tuple F of distinct underlying edges, let its score be its total fault
cost minus lower bounds on the initial, intervening, and final clean-gap costs.
The gaps may be shortest-path distances or capped shortest-path distances.
Every canonical tuple has nonnegative score, since each lower bound is at most
the actual corresponding clean segment cost. A gap minimizer is not a selected
or conditioned path: it may overlap other tuple edges or other gaps without
invalidating this lower-bound argument. Interior-only distances are also valid
when canonical internal clean segments cannot visit a boundary.

Suppose a tuple is proposed with mass (product of its edge probabilities)/Z
after score rejection and thinning. Force its edges faulty and independently
sample every other edge. The resulting joint mass of a tuple F and a compatible
error E is P(E)/Z. Accept only when F equals F(E), including orientations and
order. Each failing E then has exactly one accepted representation. Consequently
the acceptance indicator is Bernoulli(P_failure/Z).

No clean-edge survival factor belongs in the tuple weight: no particular clean
gap has been sampled. Multiplying by survival probabilities of one arbitrary
shortest route would generally bias the estimate. No gap-route multiplicity or
choice of a minimizing boundary vertex belongs in the weight either.

## Score folding and stopping

After the most recent fault edge, keep the true accumulated score S and residue
r modulo N. The root coefficient for oriented edge (u,v,e) is
q_e * 2^(c_e - d_L(u)); its initial residue is (c_e - d_L(u)) mod N.
A transition to (x,y,f) has coefficient q_f * 2^(c_f - d(v,x)).
The terminal contribution is

    t(v,r) = 2^(-d_R(v)) * 2^(-((r - d_R(v)) mod N)).

For any finite nonnegative rational supersolution H >= t + T H, use transition
probability T_ij H_j/H_i, terminal probability t_i/H_i, and kill with the remaining
probability. The root normalizer is the sum of root coefficient times H.
Telescope the H factors: a completed tuple has mass

    (product q_e) * 2^(S_final - (S_final mod N)) / Z.

Reject negative final scores and thin the remaining tuples by
2^(-(S_final - (S_final mod N))). This yields the claimed tuple mass exactly.
The final boundary shift must appear in both the terminal table and true score.

Reject a tuple immediately when an underlying edge ID repeats, even in reverse
orientation. This gives a deterministic bound of at most |E| distinct fault
edges before stopping or rejection. Rejecting shared endpoints instead is wrong:
consecutive canonical fault edges can share a vertex.

## Independent finite exhaustive check

`finite_exact_audit.py` imports no builder code. It uses a five-edge weighted
cyclic graph, unequal rational edge probabilities, exact exhaustive minimum-cost
decoding with a fixed tie rule, and a deterministic residual-path selector.

It independently solves the rational folded Markov equations with positive null
slack and propagates the actual conditional transition/termination probabilities.
For N = 1, 2, 4 and either exact gaps or cap 1, it checks:

- Every one of 32 error patterns and all 6,330 distinct-edge oriented tuples.
- Exact root, transition, terminal, null, and repeated-edge probabilities.
- Total proposal mass exactly one, including rejected branches.
- The completed-tuple telescope identity and each canonical score's coverage.
- Z times accepted probability equals 62229/156250000 in every case.
- Incorrect shared-endpoint rejection gives 1744083/12500000000 instead, a
  concrete counterexample to that stronger rejection rule.

Results are in `finite_exact_results.json`. Execution took approximately 3.6 s
in the existing scientific Python environment; this is an audit cost only.

## Remaining practical gates

Collapsing clean routes does not imply a smaller proposal normalizer. Replacing
actual clean routes by distance lower bounds admits tuples that need not be
realisable as simple residual paths and discards clean-edge probability penalties.
Ordering, orientation, and unrelated fault tuples still cause overlap.

A fixed distance cap can lose geometric suppression as separation grows. Keeping
boundary distances exact avoids one especially damaging relaxation, but the
growth of near-pair storage and gap relaxation must still be measured. A finite
floating spectral-radius estimate is not an exact supersolution certificate.
The final implementation must certify all arithmetic, integer categorical draws,
probability conversion error, boundary filtering, and canonical oriented-tuple
comparison independently before using an exact confidence interval.

## Folded far-kernel aliasing trap

For a scalar distance kernel, writing the capped kernel as a uniform far part
plus a nonnegative near correction is valid. After score folding, that is not
the same positive mixture: a gap of length d shifts the residue by d, whereas
the uniform far part shifts it by D. The correct decomposition is the far term
restricted to the complement of the near set, plus exact near-distance shells.
The builder's inspected floating screen does this subtraction correctly.

A concrete counterexample to using the scalar positive correction in a folded
sampler is N=2, D=1, near distance d=0, and H(0)=1, H(1)=2. At residue 0 the true
near contribution is 1. The incorrectly mixed contribution is
2^(-1) H(1) + (1-2^(-1)) H(0) = 3/2. Thus an implementation must sample the far
target conditional on being outside the near set, or use a different exact
nonnegative construction. It cannot simply reuse scalar near-correction weights.

## Concrete table and sampler checks

The inspected implementation instead samples directly from every target's exact
capped-distance weight. It therefore avoids the folded far-mixture trap.
Frozen sampler SHA256:

    229c5f08443090fb68e8525a1ec31ac7cc4fd16cd740671e34cfb410483074d1

The producer conservatively rounds positive kernel terms upward at 16 fractional
grid bits, then upward again after summation. This cannot underestimate T U.
The final all-row recheck means correctness does not depend on the suggested
repair multiplier being sufficient in advance. The audit does not reuse that
rounding scheme: `check_rows.cpp` rebuilds J and evaluates all rows at their full
common denominator using checked four-limb integer arithmetic.

- d13: 87,808 rows, 88,510,464 gap terms, 75,264 rebuilt J entries.
- d21: 340,736 rows, 1,499,238,400 gap terms, 309,760 rebuilt J entries.
- Largest actual full row and left-hand side in both cases: 185 bits. Largest
  J entry: 117 bits. No terminal rounding was needed in these actual inputs.
- The four-limb arithmetic was separately compared against Python integers on
  12,000 cases, including 1,709 detected overflows.
- Every distance-matrix column was independently verified as an admissible
  potential on every interior edge, with zero at its target. Chaining these
  inequalities along an actual gap proves the necessary lower bound without
  trusting the numerical Dijkstra implementation. Both boundary-distance
  potentials were also checked. There were 13,850,928 internal directed
  inequalities at d13 and 251,457,360 at d21.
- Original graph hash, every published array hash, q rounding, conversion-TV
  sum, allowed root orientations and the exact rational root normalizer match.
- Independent categorical tests checked 286,300 outward prefix enclosures and
  1,573 thresholds, including exact bucket boundaries, all-zero arrays, severe
  dynamic range and arrays of length 65,536.

The floating prefix only proposes a bucket. The code accepts it only if an
upper bound on its preceding prefix is at most the unchanged integer draw and
a lower bound on its ending prefix is strictly larger. Otherwise it computes
the integer prefix. The gamma error proof and explicit outward rounding cover
the stated binary64 operations. Root/terminal sampling, conditional endpoint
and edge selection, distinct underlying-edge checks, exact fair-bit thinning,
independent off-tuple noise and oriented canonical comparison match the law.

Detailed results are in `d13_certificate_results.json`,
`d21_certificate_results.json`, `wide_arithmetic_results.json`, and
`prefix_audit_results.json`. The checks assume the already audited frozen input
graph acquisition and fixed minimum-cost decoder, plus ideal random bits for
the mathematical sampling and coverage statements. Python's deterministic
PRNG does not itself prove those randomness assumptions.

## Exponential inefficiency remains

The builder supplied the following obstruction; this audit independently
verified it. Consider a unit-cost repetition line of 2m edges with fixed
independent error probability 0<p<1/2 and exact gap distances. Every monotone
m-fault subset has score zero, so the exact tuple-cover normalizer is at least
C(2m,m) p^m. A minimum-cost decoder fails only at weight at least m, and the
binomial upper-tail ratio is at most p/(1-p). Consequently

    P_failure / Z <= (1-p)^(m+1) / (1-2p).

The right side decays exponentially in m at fixed p. The tie rule at weight m
can only decrease the failure probability relative to this bound. Nonmonotone
tuples, score folding and supersolution slack cannot improve it. Thus the new
representation does not remove the general exponential bottleneck, even on a
line with unique clean routes and without distance-cap relaxation.

## Fixed production results and conditional target decision

`verify_production.py` verifies all 23 precommit manifest entries and then
replays both fixed-seed runs without modifying production. Every category,
step total, maximum step count, requested random-bit count and categorical
selection count agrees exactly. Each decoder call is instrumented to verify
zero residual syndrome and the original (pre-gauge) L0 parity, independently of
the cut-parity event used by the sampler. Every residual witness also passes
the weighted fault-majority inequality.

- d13: 1,578 accepted in 20,000 trials; 15,033 decoder event checks; individual
  99.9% interval [2.5595549148433986e-8, 3.002621635589656e-8].
- d21: 55 accepted in 10,000 trials; 2,205 decoder event checks; individual
  99.9% interval [1.6876511444865811e-12, 4.18024741599281e-12].

The acceptance endpoints, with denominator 2^24, are respectively
[1220747,1432062] and [56790,140622]. Reverse binomial summation verifies the
four exact Clopper-Pearson inequalities per run, including that adjacent inward
grid points would fail. Exact normalizer multiplication and the full supplied
conversion-TV expansion reproduce the published rational probability endpoints.
No finite-length tail term is omitted. The two new intervals simultaneously
cover with probability at least 99.8% by a union bound, conditional on the stated
ideal-bit sampling assumptions. Additional older intervals change that joint
bookkeeping if they are claimed together.

The d21 lower endpoint is strictly above the independently precommitted target
of failure probability at most 1e-12 per 21-round block. Thus d21 fails that
target in the stated rational projected circuit model and frozen integer-cost
decoder at individual 99.9% confidence. The earlier fixed path-cover interval
straddled the target. This is not a hardware sizing claim or a conclusion about
other noise models or decoders.

Production subprocess wall times were 27.6564 s and 30.1565 s, with peak RSS
138,940 KiB and 226,492 KiB. These times alone do not include acquisition,
floating preprocessing or rational certificate construction; full setup
accounting must accompany any performance comparison. Both fixed runs finished
within their precommitted 20-minute/2-GiB limits. The RSS limit was monitored
periodically, not enforced by a kernel cgroup; whole-process peak RSS was also
collected with wait4. Full replay results are in `production_results.json`.

## Complete operational cost readback

`verify_resources.py` independently reconciles the fresh measurement records,
all copied source hashes, original acquisition records, and production resource
records. Fresh preprocessing reproduces all six arrays byte for byte and the
same exact Z, TV, parameters, and certificate fields.

- d13: acquisition 3.1965 s, fresh preprocessing 19.1401 s, whole production
  process 27.6564 s; separately measured stage sum 49.9929 s.
- d21: acquisition 15.5405 s, fresh preprocessing 187.0633 s, whole production
  process 30.1565 s; separately measured stage sum 232.7603 s.
- Fresh d13 largest single-process peak was 113,604 KiB; its largest sampled
  process-group peak, including concurrent compiler work, was 173,672 KiB.
- Fresh d21 largest single-process peak was 607,712 KiB; sampled group peak
  was 606,628 KiB. Different sampling methods need not have identical maxima.

These are sums from separate measured runs, not uninterrupted acquisition-to-
production benchmarks. Compiler time, process startup, and stage input/output
are included. Research, source/file-copy preparation, hash/equivalence checks,
test development and this independent audit are excluded and identified as such.
Timings are from a shared host, not an optimized external-competitor benchmark.

For comparison, the previous d21 operation's 93.4654 s is also a sum of complete
stage processes: the new result is more costly but resolves the fixed threshold
and has a narrower interval. The previous d13 reported 70.0922 s adds complete
setup to its internal production timer, which excludes interpreter/import
startup. No earlier d13 whole-process resource record was found. Consequently
49.9929 s versus 70.0922 s must not be advertised as a perfectly matched
whole-process speed comparison. Sampling-only comparisons have a consistent
timer scope, but are not complete operational costs.

Full independent readback is in `resource_results.json`.
