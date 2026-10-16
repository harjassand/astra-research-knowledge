# Astra: controller bounds with finite-duration and multisector qualifications

16 October 2026. Mathematical research handoff. No new physical device or historical-priority claim.

## Capability

A causal-tester representation converts specified local controller guarantees into joint endpoint-effect bounds despite a shared finite quantum bath. Fixed local schedules can be asynchronous. The two extensions below have DIFFERENT controller contracts and must not be combined by simple substitution.

1. **Finite-duration private random-Z control.** The unknown own-parity-flipping interaction can continue during the controller pulse. If its norm actions before, during, and after the window are a,c,b, and the private phase distribution has coherence multiplier magnitude eta, a local certificate is

   R = sin²(min(arcsin sqrt(F(a,b,eta)) + c, pi/2)).

   Joint endpoint effects are bounded by the product of these R factors. This is an upper certificate, not an exact finite-window optimum. For a specified balanced square pulse of phases +/-theta, eta=cos(theta), and controller Hamiltonian norm limit Omega gives pulse duration tau>=theta/(2 Omega), with hbar=1. A supplied interaction envelope J gives c<=J tau. These do not establish hardware values, wall-energy costs, or an error lower bound.

2. **Partial full-sector refresh.** For one good sector and K finite bad sectors, a specified channel eta Id+(1-eta)sum_j P_j(.)P_j has sharp two-gap endpoint factor

   F_K = p+q-pq + max_(0<=x<=1) [-lambda p q x² + 2 eta sqrt(pq(1-p)(1-q)) x],
   p=sin²(min(a,pi/2)), q=sin²(min(b,pi/2)), lambda=eta+(1-eta)/K.

   An auxiliary label-message construction gives the product of these factors when every fine projector commutes with every coarse good/bad parity, node order is fixed, and node environments are independent and inaccessible. Fine projectors need not commute with one another if their actual order is retained. Uniform sharpness is over sufficiently rich finite models, not every fixed overlapping-projector architecture.

The sector count matters: a=b=pi/6, eta=1/2 gives F_1=36/64 but F_2=37/64. As K grows without bound, the exact factor approaches the inherited retained-pinch mixture bound. A single random-Z phase implements binary dephasing; it does not automatically implement full stabilizer-group pinching. Do not insert F_K into the finite-duration formula without a separate controller reduction.

## Evidence

The enclosed packets contain full analytic arguments, specified equality witnesses where claimed, source dependencies, hashes, and newly written checks. Root review reconstructed the channel identities and bounds; separate internal mathematical reviews challenged the tester interfaces, causal ordering, padding, controller privacy, and action budgets. Fresh extraction and hash checks passed. Direct matrix diagnostics corroborate the proofs; exact rational auxiliary-label identities also passed. These are internal checks, not external peer review or formal verification.

## Closest prior results and attribution

Gutoski–Watrous already supplies positive causal-strategy domination and all-pass product multiplicativity. Fractional-query action-preserving simulation, geometric perturbation bounds, and related shared-bath fault-path methods are established. PRIOR_ART_COMPARISON.md compares six primary sources and identifies the remaining priority question: the particular Hamiltonian-to-private-tester reduction and its exact local optimizations. A bounded search did not settle historical priority.

## Missing operation

A physical application must establish the actual full-joint controller map or Hamiltonian, controller privacy, unavailable discarded environments, the relevant local interaction envelopes, and accessibility of the controlled parity. A reduced coherence-decay measurement is insufficient. In particular, a virtual sign/parity label is not automatically an implementable physical coupling.

The endpoint theorem must also be mapped explicitly to the intended memory's fault-history, syndrome, reservation, and good-CP/support events. That transfer is being investigated separately. It is not supplied by the numerical similarity of probability factors.

## Plausible consequence and decisive tests

Within the stated models, one can remove synchronization as a mathematical requirement and charge finite pulse duration locally while retaining a multiplicative joint certificate. This could simplify controller requirements in a qualified architecture; no practical threshold or resource advantage has yet been established.

Decisive next mathematical test: reconstruct the exact event and operator mapping to the actual memory/support theorem, including staggered entry records and overlapping reservations. Decisive physical test: qualify one compatible controller/interface at the same operating point, with its relevant bath and leakage channels, instead of inferring it from isolated-qubit decay.

## Files

- finite_private_z_refresh_standalone.zip: finite-window theorem and unchanged prerequisites.
- multisector_refresh_proofs_and_checks.zip: exact multisector singleton/product proofs, dependency sources, and replay checks.
- PRIOR_ART_COMPARISON.md: bounded primary-source comparison.
- SHA256SUMS: hashes of these handoff files.

No canonical repository was changed, and no outreach, public release, purchase, or license grant for this new analysis was made.
