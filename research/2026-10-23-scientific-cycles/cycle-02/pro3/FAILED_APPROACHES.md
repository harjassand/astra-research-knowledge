# Failures and limitations that constrain continuation

Scientific checkpoint: Astra PRO3, 22 October 2026, Australia/Brisbane.

## 1. Closed incoming optional-prefix route

Under the exact public labelled q/Q, candidate-only target oracle, unknown
normalizer, same supplied positive K on the null, bounded-fallback contract,
uniform fixed fractional saving over all null instances is impossible.
Both incoming proofs are accepted. Their actual failed approaches and costs
remain in sources/received_prefix/arm_a and arm_b. No new independent
optional-prefix search was run. This is not a universal adaptive-sampling
impossibility or an obstruction to the explicit changed local kernel here.

## 2. Linear-in-time q-density growth is false

A tempting strengthening of qL<=2q was qL^t<=(t+1)q. It would give a much easier
proof. The independent mechanism challenge found a counterexample and retained
an exact rational version.

Take q=(99/100,1/2000,19/2000), raw weights (1,2200,17), normalize pi proportional
to q times those raw weights, and use the q-reversible R

    [[98849/99000, 13/99000, 23/16500],
     [13/50,       6/25,      1/2],
     [69/475,      1/38,      787/950]].

Correct R by the W-ratio MH acceptance. At t=12, the middle coordinate has
(qL^12)(middle)/q(middle) approximately 13.0622328303, strictly exceeding 13.
The forward KL is approximately 3.1517157347, so K=4 admits it.
The exact rational assertion and input are in the mechanism script/JSON.
An earlier floating-point search located a nearby failure; the replayed
witness itself is exact. The final theorem uses the valid exponential c^s
bound for s of order log log n, not the falsified shortcut.

## 3. Weaker screening does not retain a uniform linear bound

For fixed 0<eta<1, let Q swap two states, q=(1-r,r), pi=(1-p,p), and
p=k/log(1/r) for 0<k<K. For sufficiently small r, all masses are positive,
D(pi||q)<k<K and tends to k, but

    qL_eta(rare)/q(rare) ~ r^(eta-1) -> infinity.

This disproves any uniform finite Lambda for that tempered class. It does
not prove a mixing obstruction. The setwise Holder power bound replaced
linear domination and yielded zero uniform floor for every positive eta.
The eta=0 and eta=1 endpoint formulas are retained in the independent
preparatory note. Do not reuse this witness as a lower-rate theorem.

## 4. The current sharp-interval proof stops at a sufficient threshold

The density power after s steps is eta^s. Making first-hit survival
o(1/log n) asks for s>log log n/kappa, whereas the current truncation/core
argument asks for s<log log n/(-log eta). These are compatible only when
eta>theta_K. No necessity theorem follows. In the remaining interval, the
proved nonsharp rate and zero floor are retained, and the sharp rate is open.

The first draft's display A^2/t=exp(2(log n)^z)/t overlooked A=V+1.
The independent review requested exp(2(log n)^z+o(1))/t. The final source
contains that correction. It changed no argument or conclusion.

## 5. Robustness is not a universal efficiency improvement

The four-state q-uniform example with pi=(3/8,3/8,1/8,1/8) and pair-swap Q
has qL=q and nontrivial local moves, yet one pure-IMH update beats four lazy
hybrid steps at the same expected global-draw count and at lower completely
memoized target-query cost. A second pure comparator matches target-query cost
exactly and still improves TV. The exact branch enumeration is included.

Even delayed acceptance versus ordinary local MH has no free finite-time gain:
the two-state example in the cost note has TV 29/72 versus 7/24 after one
mixture step, while the screen uses fewer target queries. The costs and errors
trade off. Invariance or stationary efficiency ordering is not a TV theorem.

The principal three-state calculation repairs the old trap but pure IMH reaches
all three preset TV levels in fewer steps. At the smallest tolerance the
safeguarded hybrid also uses almost the same expected global count plus a
comparable number of local proposals. All five evaluated uniform hybrid
sufficient certificates are larger than the pure-IMH certificates. None is
discarded or optimized after seeing this unfavorable comparison.

## 6. A richer geometry route already gives stronger ordinary methods

A known compact cover and a certified logweight regularity constant permit
off-proposal bounds and an exact rejection sampler without a known normalizer.
Known adaptive rejection methods are then relevant comparators. This is a
legitimate richer access model, but no concrete scientific input here supplies
a cheap certificate, and a prefix-only gain would not establish utility.
The bounded literature note preserves the deduction; no application campaign
was opened and no physical access was invented.

## 7. Numerical and ideal-real limits

The 80/120-digit agreement checks rounded calculations, not outward intervals.
Exact Fraction tests verify only the specified finite identities, not all
measurable spaces. Matrix powering evaluates distributions at large horizons;
it is not an executed sampler run of that duration. The analytic tempered
extension has no trajectory benchmark. Population K, exact ratios, fixed
reversibility and fixed component selection remain hypotheses. Their empirical
or approximate substitutes have not been proved sufficient.

## 8. Historical operations remain closed

The R3/anMC recipient had known Gaussian regression/covariance and truncated
outer draws; that transfer rejection stands and the sampler is preserved.
B3 retains its pISO enclosed-mass correction, while its full halo inference
failed the frozen adequacy gate. The separate metadata-admission case stays
closed. No favorable extra galaxies, relaxed gate or raw-cube restart occurred.
No protected hidden-entropy, N33, N557, IQM, Morrey or other owner's construction
was duplicated.
