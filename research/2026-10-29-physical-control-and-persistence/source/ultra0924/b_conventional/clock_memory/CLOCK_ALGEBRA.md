# Which microscopic bath errors actually need to be faults?

29 October 2026. Exact algebraic observation for the CONDITIONAL clock
apparatus, not an admission of general physical data baths. No dynamics run.

In the prefix gauge the actual conditional Hamiltonian and every prescribed
clock-controller/bath coupling have the form

    H_tot(t)=sum_(s admissible) Pi_s tensor H_s(t),       (1)

where Pi_s are the joint nominal source-check projectors and H_s acts only
on clocks and baths. The full nominal bare logical Pauli algebra is the
identity factor in(1). Conditional source-check functions, arbitrary clock
operators and arbitrary bath operators therefore commute with all Pi_s
and with the decoder-corrected logical algebra O_alpha=L_alpha f_alpha(S).

This remains true for finite banks, non-Gaussian bath states, occupation
truncation, arbitrary reused-bath histories, classical bath forces and
coefficient errors WITHIN the prescribed operator span. It is a commutant
statement, not a Gaussian/Markov/low-energy approximation. Arbitrary physical
coupling errors outside that span are not included.

Let G=sum_s Pi_s tensor G_s be the exact joint propagator between noise
events. A source Pauli P has syndrome difference d(P), so

    G^* (P tensor A) G
       =P sum_s Pi_s tensor G_(s+d(P))^* A G_s.         (2)

No source Pauli label has spread. The coefficient is allowed to depend on
ALL source checks and to act on all clocks/baths; it need not stay spatially
local. That distinction cannot be dropped in a receiver admission test.

More generally define a supported-label class consisting of finite sums

    sum_(P in L) P F_P(S;clock,bath),                   (3)

where L is an externally specified set of source Pauli labels. The exact
multiplication rule is

    [P F(S)][Q G(S)]=PQ F(S+d(Q))G(S).                 (4)

Clock/bath coefficients need not commute; their displayed order is retained.
Hence arbitrary histories of(1) interleaved with errors of class(3) keep
only the products of the supplied source Pauli labels. This also follows
Kraus-term by Kraus-term for check-diagonal environment channels; no inverse
of a nonunitary clock channel is needed.

If a supported-label decoder theorem supplies a common Pi_good(S) such that
[P,O_alpha]Pi_good=0 for every admitted label P, it remains true for arbitrary
coefficients F_P in(3): these commute with O_alpha and Pi_good, so

    [P F_P,O_alpha]Pi_good=0.                          (5)

Thus the prescribed clock-only bath/controller dynamics can be GOOD dynamics
rather than bath fault events in a theorem explicitly closed under(3). The
Gaussian memory budget of PROOF.md is not needed merely to prove(2)--(5).
This may remove a false clock-bath-noise prerequisite at the algebraic level.

The boundaries are consequential:

* This does not supply a positive independent support-mark process for the
  OTHER errors. Coherence and arbitrary check-dependent coefficients are
  allowed only if the target theorem actually admits them.
* A generic physical onsite clock bath is NOT automatically the prefix-pulled
  coupling in(1). A physical onsite data bath usually changes syndromes and
  is not good dynamics. The all-physical-seed thermal generator cannot be
  replaced by a clock-only noiseless subsystem and still called the same model.
* The algebra does not establish Gibbs initialization, stationary Peierls
  weights, energy-biased data-error rates, bath renewal, active decoder
  locality/timing or a physical experiment.
* A receiver insisting that F_P depend only on a small local set of checks
  cannot consume(2) for free. The exact expression may have globally
  check-dependent coefficients even though P's label stays fixed.

The source check/logical algebra and prefix table are accepted inputs; they
are not re-proved by a finite fixture. Historical novelty is not claimed.
