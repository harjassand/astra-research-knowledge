# Scope decisions and useful failed openings

Research date: 2026-11-05.

The governing result is the connected Gibbs endpoint strong converse in
`../control/endpoint_spectral_trace_theorem.md`, supplemented by the explicit
inverse-polynomial precision corollary in
`../bounded/planar_endpoint_independent_audit.md`. The report is the accessible
consolidation. All earlier accepted results remain unchanged.

## Formal generator uniformization is not a physical simulator

A screened alternative used a finite-dimensional trace-preserving generator
L for which Q J(L) Q is strictly positive, where Q projects orthogonally to
the maximally entangled Choi vector. A Schur-complement estimate then makes
Id+L/gamma completely positive for sufficiently large gamma. Writing this
channel as T gives the algebraic Poisson representation

    exp(t L) = exp(-gamma t) sum_k (gamma t)^k T^k / k!.

The identity component of the Choi matrix and strict conditional positivity
are the relevant finite-channel conditions; an arbitrary Lindblad generator
does not automatically make the simple Euler step completely positive.
For sums of local generators, a Poisson clock can select local maps formally.

That algebra does not yet implement finite-duration local gates, idle noise,
overlapping event schedules, classical clock propagation or raw output
delivery. Allowing events to have zero physical duration would discard the
decisive apparatus problem. No efficient noisy continuous-time simulator or
new physical capability is claimed from this route.

## Fermionic parity did not supply the claimed layer lower bound

The separate note `../bounded/parity_extent_scope_and_bypass.md` preserves the
valid causal-extent statement and its assumptions. Locally physical fermionic
product factors cannot produce arbitrary odd-odd correlations by preselected
classical randomization. But local parity-even Bell measurements, measured
classical outcomes and feedforward can swap a fermionic Bell pair over a
chain. An ancillary fermion can carry the parity record during the endpoint
correction. Thus a nonadaptive quantum lightcone argument cannot be promoted
to the full adaptive apparatus without charging classical propagation and
quantum storage during the wait. This was a real bypass, not a general
fermionic preparation impossibility.

## Depolarizing final-port extension

Let Dep_p have Pauli probabilities (1-p,p/3,p/3,p/3), 0<p<1/2. Put q=p/4.
Convolving an unknown Pauli law r with (1-q,q,0,0) gives pairs (I,X) and
(Y,Z). Inverting the pairs gives

    r_I = [(1-q)(1-p)-q p/3]/(1-2q),
    r_X = [(1-q)p/3-q(1-p)]/(1-2q),
    r_Y = r_Z = p/3.

The X numerator is p/12+p^2/6>0; the I numerator is positive for p<1/2.
They sum to one. Hence Dep_p=Lambda_q composed with R, a physical Pauli
channel. Its entire image lies inside the bit-flip image. This transfers the
strong converse, with q in place of p. It does not prove robustness against
arbitrary correlated, coherent, flagged or target-dependent noise.

## What is and is not completed

The new work completes a foundational endpoint impossibility, including
approximate rather than only exact delivery, connected targets, arbitrary
entangled upstream preparation, physical geometry and a necessary precision
law. It does not supply a preparation algorithm, efficient witness metrology,
target learning, an energy advantage, general Gibbs sampling hardness or a
civilisation-scale practical capability. It is a strict boundary on a broad
universal preparation claim. It leaves encoded output, later correction,
target-preserving final thermalization and weaker observable tasks at their
own contracts. The separately recorded translation-invariant square example
does not inherit the connected root-field amplifier without another proof.
