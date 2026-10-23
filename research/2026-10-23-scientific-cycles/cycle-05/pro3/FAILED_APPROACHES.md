# Failed or insufficient routes that changed the decision

## Summing separate first-hit norms loses the endpoint

The received strict-c proof bounds each first-hit density and sums its Lp
norm using a geometric contraction. Its constant diverges as c approaches
c_*. Substitution of c=c_* was not valid and was not used. Truncating that
sum at O(loglog n) still introduces a growing factor, so it cannot identify
the critical amplitude. This is a failure of that estimate, not a mixing
counterexample or a failure of the accepted first-order theorem.

The successful replacement stores every bad first hit in one absorbing
boundary vector. The full p-energy can grow by 1+O(theta+Delta+q(E)) per
step; over O(loglog n) steps the product is 1+o(1). There is no divergent
geometric sum. This construction respects the old strict one-step ceiling.

## A pointwise potential alone does not cover arbitrary global transport

The complementary contributor's V=q^(-c eta) supermartingale handles
heterogeneous local steps, backwards moves and cycles when a single dominant
root/core allows other global jumps to be charged by their small q mass.
Arbitrary full-class global transitions need not have a pointwise bounded
transformed row. Extending that potential without accounting for distributed
entry mass would be unjustified. The principal instead uses weighted Jensen
for the global step and counting-measure Jensen for the symmetric local step.
Their different A/E energy coefficients are kept until the mixture is formed.

## Repeated return through a high-target-mass core did not beat the lower

The tested alternative mechanism tried to gain extra amplitude by restarting
transport after visiting the core. In the contributor's one-core class,
TV after a core hit is bounded by 1-pi(core), including every future return.
That is negligible for the old branching family. This closes that proposed
mechanism within its stated class. The new all-class theorem independently
excludes any geometry above the envelope in the declared r0<1 regime.

## Independent entropy allocations would give the wrong sum

An upper of the form a_R+b exp(-c_*u) is not yet the sharp result. Giving a_R
the full K/log n and also taking b=1-exp(-K) spends the same KL budget twice.
The finite inequality k_b+a_R log R<=K+controlled error resolves this.
When k_b has a strict limiting slack, actual killing supports c>c_* and
transport is negligible. When k_b tends to K, the high-weight tail amplitude
vanishes. The maximum follows from those alternatives, not from ignoring
one of two potentially positive terms.

## Absorbing only for counting is essential

Replacing the sampler after its first safe hit by an absorbing chain would
silently discard post-hit returns. Here absorption counts first-hit location
only; nu_j is then propagated by the original C^(n-j). The exact finite
diagnostic checks this full-return identity separately. Initial q(E) is
charged explicitly and q 1_A is a restricted subprobability, not a normalized
conditional start.

## No diagnostic failures in this checkpoint

The frozen Fraction/Decimal diagnostic passed on its first execution. No
test case, tolerance, model hypothesis or mathematical conclusion was adjusted
after seeing the output. Historical tree multiplicity and serialization failures
are preserved in the unchanged source ZIP and were not recreated.

## A remaining boundary is not silently filled

The main critical theorem assumes r0<1. The finite optimal transport spacing
used by the old amplitude lower escapes to infinity as r0 reaches one.
Consequently the old lower cannot be substituted unchanged into r0>=1.
The next seed records a different, unproved candidate for that regime. It is
not an accepted theorem in this archive.
