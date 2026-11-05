# Full equilibrium nonuniqueness and a computable pressure with undecidable derivative

Sections 5.1–5.2 of the supplied [complete addendum](package/NOTE.md) give two further corollaries, conditional on the [base construction](../2026-11-05-dots-thermal-fourier/README.md). Their [internal-audit status and exact version](SOURCES.json) are retained; publication introduces no new proof check.

The later [accepting-pin uniqueness package](../2026-11-05-dots-unique-phase/README.md) uses a different single-spin model. Its claimed all-Gibbs uniqueness does not contradict or revise the both-branch full nonuniqueness of the original bilayer family discussed here; this addendum remains conditional on its recorded base version.

## The original family has multiple full states in both branches

Put both exterior Ising layers plus. Conditional bond domination and a Peierls contour estimate give a translation-averaged plus state with common-sign observable `A=(s+r)/2` having mean at least `1-2delta`, where `delta<7.90e-7`. Simultaneous global spin flip gives a distinct negative-mean state. Their equal mixture has zero common mean and nondecaying A correlations, bounded below by `1-8delta`.

This works for **every encoded machine**, including halting ones. Full Gibbs uniqueness and all-observable correlation decay are therefore not extensions of the theorem for the exchange-odd `O=(s-r)/2`. The construction controls relative layer exchange while common global spin order remains possible. Establishing full uniqueness would require a different construction/proof, not reinterpreting this observable.

## Pressure values are computable; the selected field derivative is not decidable

Add a probe field `-hO` and write p_M(h) for pressure. The original integer-energy undecidability instance remains at h=0; arbitrary real probe energies are not being substituted into its stated family. Pressure is even, convex and 1-Lipschitz in h.

For ordinary free **physical** boxes, including only interactions supported entirely inside, the addendum obtains the uniform surface estimate

```text
p_free(M,L,h)-26/L <= p_M(h) <= p_free(M,L,h).
```

Finite sums thus compute pressure values at computable h with an explicit error bound. Brute-force enumeration is not asserted polynomial time. Pressure computability is established background and is credited in the [source notes](package/SOURCES.md).

The variational principle identifies the right/left h derivatives at zero with maximum/minimum O means over translation-invariant Gibbs states. The base theorem gives:

- Halting: both derivatives are zero, so the pressure is differentiable in this field direction at zero.
- Nonhalting: the slopes exceed 1/2 and are below -1/2, respectively, so it is not differentiable there.

Hence deciding this **directional differentiability at a fixed field** throughout the compiled family is undecidable even though pressure values have a computable uniform finite-size approximation. It is not differentiability as a functional of every perturbation, full Gibbs uniqueness, analyticity or a linear-response theorem. Exponential decay for the selected odd observable does not itself supply those stronger conclusions.

The [numerical receipt](package/numerical_checks.json) distinguishes rational contour certificates from floating finite-box sums. Earlier size-driven/phase-diagram results and known pressure computability are credited without claiming general historical firstness. No new Capital scientific execution, physical validation or audit occurred. [Finite-boundary/crossover theorem and limitations](README.md).
