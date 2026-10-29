# Central attack: compress an imperfect predictive teacher

30 October 2026, Brisbane. Original continuing mission;100/100 NOT_ACHIEVED.
This is an attack and proof state, not a theorem announcement or replacement
of another researcher's canonical problem. Four retained contexts only.

Desired capability: acquire a compact reusable sequential model from partial
observations and an imperfect computational teacher, without requiring a
well-conditioned latent basis. Success would remove a substantive barrier
to reusable scientific world models. It would not alone establish general
scientific intelligence or a physical prediction advantage.

Concrete proposed contract: P is a distribution on a finite alphabet^T with
predictive linear rank<=r at EVERY cut. We can sample full P trajectories.
We can query next-token probabilities/conditional samples of a potentially
arbitrary-rank Q, with an explicit finite-precision cost, and have the
supplied global bound D(P||Q)<=Delta. No conditional P oracle, latent
states, spectral gap or positive hidden-state realization is supplied.
Seek a polynomial-size model, learned and sampled in polynomial time, with
no Q calls after compilation and TV error bounded by epsilon plus an
explicit polynomial/Hölder function of Delta. This contract is NOT proved.

The closest working constructive predecessor was read before committing
depth: Liu--Moitra2411.07536v1, Theorem1.3, Sections3 and6.1--6.2. It learns
any exactly low-rank distribution using conditional queries to THAT target,
through mixture density sketches, robust barycentric spanners and KL
projection. Its finite query simulation controls all conditional rows;
global D(P||Q) does not give that uniform premise. We retain its actual
strong operation and will allow the ordinary method all resulting repairs.
https://arxiv.org/html/2411.07536v1

The new possible operation is localization of global misspecification to a
distribution-weighted predictive state, with stable transition/projection
updates. A small singular value must either be paid as useful information
or discarded with a proved full-sequence error, rather than simply inverted.

Initial failed route: choose every cut's spanner only from fresh random
prefixes, excluding propagated children. This avoids recursively dividing
a conditional-error allowance by the minimum retained token probability.
But coverage of a basis-selected previous prefix can be amplified by its
sample-selection bias: a crude bound costs N_prev*gamma_next/tau. Taking
gamma_next<<1/N_prev can recursively enlarge sample sets with T. This is
a failure of that proof/selection mechanism, not a lower bound for the
desired operation. Including arbitrary children restores the predecessor's
uniform requirement and can reintroduce rare-prefix contamination. The
attack must pay weighted transitions rather than hide either issue.

No model was stolen or external service queried. Only public mathematical
sources, private synthetic computation and existing Astra read-only sources
are used. The global-KL interface is distinguished from the older quantum
CP predictive-operation source N952 and its restricted successors; those
have their own rank/core/reset/conditioning resources.
