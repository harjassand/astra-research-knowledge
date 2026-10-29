# Independent checks and interface

## Explicit-cutoff theorem audit

The main worker independently checked the subworker derivation in EXPLICIT_LOCAL_OBSERVABILITY.md and EXPLICIT_BOUND.md:

- The cross-Hamiltonian terms in L*² n_x are x-off-diagonal and only adjacent centers contribute; each has norm <=2g².
- Dissipators outside the closed star commute/cancel on the local off-diagonal observable. The loose closed-star bound <=2 kappa g(D+1) is safe.
- The self-site curvature is 2g²(G-2n_x), with G the neighbors-ready projector (not the all-ready projector).
- Quintic smoothstep has first derivative <=2 and second derivative <=6. Vanishing endpoint derivatives validate twice integrating by parts.
- The interval indexing is consistent: b_{k-1} integrates over I_k; phi_k is supported there and equals one on I_{k+1}, defining b_k.
- The recurrence uses actual b values <=1, so replacing a linear b term by sqrt(b) is valid even when its previous upper bound exceeds one.
- The first-emission conversion uses bounded predictable intensity and does not assume independent events.

## Finite challenge

check_progress.py constructs the exact independent-set matrices, the Heisenberg Lindbladian, and the killed target-event semigroup. The smallest eigenvalue of I-exp(t L_no-x*)I is the exact worst-initial-state event probability. Tested isolated site, edge, triangle, degree-four star, six-site path, and five-cycle at four (g,t) pairs with kappa=1. All 24 curvature-compression checks had residual below 1e-9 and all event effects were positive semidefinite.

At g=kappa=t=1, minimum event probabilities were approximately 0.0747477 (isolated), 0.0361263 (edge), 0.0302850 (triangle), 0.00104909 (four-leaf star), 0.0364162 (path endpoint), and 0.0110085 (five-cycle). These tests support local algebra and expose the slowdown caused by blockers; they do not prove the theorem. Raw results: numerics.json.

## Root weak-drive certificate audit

For epsilon=g/kappa and epsilon²<=1/[100(D+1)], the root's independent argument checks:

p_y<=exp(-kappa t/2)+4epsilon², so after t0=4 log(1/epsilon)/kappa, all p_y<=5epsilon².

For F=<G_x-2n_x-sum_{y~x} b_y* b_x>, Re F>=1-10(D+1)epsilon²>=0.9. With q=-Im<b_x>, q'=-kappa q/2+g Re F and initially q>=-sqrt(5)epsilon, after 2log(10)/kappa one gets q>1.396epsilon, hence q>=epsilon thereafter. After another log(2)/kappa, p_x>=epsilon² thereafter. A final interval 1/kappa gives E N_x>=epsilon² and Pr(N_x>=1)>=epsilon²/2.

Thus T=[4log(1/epsilon)+2log(10)+log(2)+1]/kappa is valid. This is far stronger numerically in its weak-drive regime than the all-coupling cutoff bound.

## What follows and what does not

Applying either single-site minorization after each time block gives P(no event at x in m blocks)<= (1-c)^m, even conditioned on arbitrary history BEFORE those blocks. It is invalid to multiply same-window bounds for different sites merely because each holds for arbitrary initial states: conditioning on another site's FUTURE non-emission changes the dynamics, not just the initial state. A spatial joint-fault law remains open.
