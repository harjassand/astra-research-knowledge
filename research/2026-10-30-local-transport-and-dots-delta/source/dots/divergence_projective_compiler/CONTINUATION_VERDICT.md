# Continuation result: decoder bridge closed; no symbolic-algorithm advantage

## Useful result

The previously unimplemented inverse-degree bridge is now implemented and
independently reviewed. Raw equations/circuits can acquire the projective chart,
then acquire a strong Jacobian flag or a quasi-translation identity, and construct
a compact **original-state** decoder. A verified subclass has exponential inverse
degree yet globally pole-free, uniformly initial-state-conditioned dynamics on an
explicit ball for all real time. This removes a real capability/conditioning
objection; it does not establish a broad new discovery paradigm.

## What actually passed

- General-n raw coefficient acquisition and strong/quasi decoder:
  22 closure identities, 14 flag checks, 16 expanded inverse component identities,
  plus independent two-sided rational interpreter checks and adverse controls.
- Raw quadratic-budget circuit acquisition in dimensions 2, 4, 8, 16:
  all **34** serialized closure identities independently replayed exactly;
  normalized charts and rotation generators also match exactly.
- n=16 compact raw circuit: 493 source nodes, 17 projective coordinates,
  inverse degree 32,768. The acquired-chart inverse has 226 final live nodes and
  896 allocated nodes. After normalizing the chart, the chain inverse has 62 live
  and 379 allocated nodes. These are different output representations, not
  interchangeable counts.
- Analytic all-real-time bounds: denominator at least 7/8 and inverse absolute
  Jacobian norm below 4/3 on the specified initial ball. This does not bound errors
  in unknown model frequencies.
- Supplemental acquired-artifact evaluation at `t=10^30+1/3`: 80-digit calculation
  agrees with 160-digit calculation to about `4.05e-54`; deliberately insufficient
  20-digit arithmetic incurs error about `1.37e-3`. Precision is charged. Agreement
  is not a rigorous interval-error certificate; the all-time bounds are analytic.

## Comparator kills any claimed algorithmic speed separation

The benchmark raw DAG retains literal chart subgraphs. The equally informed
`same_syntax_comparator.py` uses ordinary pattern/CSE extraction from the identical
input syntax, fits and checks the projective identities, and uses the same
classical flag inverse. It recovers exactly the already independently certified
normalized chart/generator in every saved dimension. n=16 extraction was about
0.00034 s and the whole comparator, including decoder, about 0.92 s in one run;
these are tractability observations, not a controlled general speed ratio.

The n=16 raw field also expands to only 2,361 terms. There is no empirical circuit
versus sparse exponential separation. The earlier proved exponential separation
is only from finite original-state-containing density lifts. No broader classical
algorithm lower bound follows. Strong nilpotence, quasi-translations, polynomial
interpolation, PIT, projective linearization and symbolic Krylov recognition are
classical ingredients; historical novelty of their complete assembly remains
unestablished.

## Clear failure cases and costs

- A locally invertible but noninvertible polynomial map rejects the flag test.
- Pointwise Jacobian nilpotence is not accepted as strong nilpotence; explicit
  same-point-zero/mixed-point-nonzero controls reject that shortcut.
- A nonstrong quasi-translation accepts through its independently valid route.
- A composition of two polynomial shears can be invertible yet fail both selected
  strong/quasi routes. General compact inverse acquisition remains unresolved.
- Exact integer output can have exponential bitlength even with a tiny DAG.
- General raw circuit admission uses randomized PIT; these particular records
  have deterministic replay, not a deterministic general PIT algorithm.
- Source construction, divergence AD, interpolation, rational elimination,
  normalization, decoder build, dead DAG storage, verification and numerical
  precision all count. Recorded partial timings are not a complete speed result.

## Stop condition and genuinely different missing operation

This projective decoder obligation is closed at its stated scope. Adding more
projective dimensions or another easy conjugate is not the next meaningful step.

A decisive blind spot is exact volume-preserving/Hamiltonian dynamics: if
`div f=0`, then `T1=0` and the canonical one-seed route has rank one, however rich
the integrable geometry may be. For example the polynomial quartic oscillator
`q'=p, p'=−q^3` conserves `p^2/2+q^4/4` but this acquisition route returns no full
chart. This is an immediate algebraic obstruction, not a failed numerical budget.

A different operation would be automatic acquisition of invariant fibrations,
commuting flows, or spectral-curve/Lax geometry directly from raw equations,
together with a full-state time decoder—not merely rediscovering a first integral.
That is a research target, not a result delivered here. It should earn continuation
through a nonmanufactured scientific model and comparison to classical symbolic
integrability methods, rather than by another hidden-projective benchmark.

## Artifact map

- Theorems: `STRONG_NILPOTENT_DECODER.md`, `UNIFORMLY_CONDITIONED_FAMILY.md`.
- Implementations/results: `strong_decoder*`, `quadratic_circuit*`,
  `conditioned_flow*`, `same_syntax_comparator*`.
- Independent reviews: `audit/NILPOTENT_BRIDGE_REVIEW.md`,
  `audit/BOUNDED_OSCILLATORY_FAMILY_REVIEW.md`.
- Independent receipts: `audit/strong_decoder_replay.json`,
  `audit/quadratic_circuit_replay.json`, `audit/nilpotent_adversarial_controls.json`.

No upload, publication, external state change, or user-facing research claim was
made during this continuation.
