# Fixed downhill dynamics plus an extensive barrier: a coherent-noise memory criterion

Root author construction, 2026-11-01, pending independent audit and an acquired code/controller instance. This is not yet a quantum-memory construction: the local descent and barrier premises must be proved for an actual code. No Gibbs stationarity or effective-temperature substitution is used. This revision corrects the original dissipator boundary shell after an independent counterexample; ROOT_V1_BOUNDARY_SHELL_UNCORRECTED.md preserves the original author draft.

## Intended capability and model

Seek an autonomous quantum memory at fixed bounded local correction/noise ratios, with a time-independent engineered generator, including unknown coherent perturbations. A bounded-degree interaction graph is allowed at this stage; Euclidean locality, hardware interaction length, and microscopic realization are not silently supplied.

Take a stabilizer code with syndrome s and a nonnegative diagonal potential W(s), W(0)=0. Require W=sum_v w_v(s_local), with bounded local terms and bounded incidence, so every admitted bounded-support Pauli P changes W by at most b, independent of n. Enlarge the admitted move alphabet to include every Pauli appearing in local perturbations and correction operators.

Assume a cutoff B_n=beta n such that the syndrome component S0 reachable from0 by admitted Pauli edges staying below B_n has NO nontrivial logical holonomy: any closed low-potential path acts trivially on the PROTECTED logical subsystem. It may act nontrivially on explicitly retained gauge degrees of freedom. For an ordinary stabilizer code this reduces to stabilizer holonomy; for a subsystem construction it is a gauge-holonomy condition. This is an extensive energy-barrier/decoder-flatness premise. Choose canonical recovery representatives R_s on S0. Then every admitted local Pauli between syndromes of S0 acts as identity on the decoded protected-logical subsystem tensor an operation on syndrome/gauge degrees of freedom. Arbitrary gauge coherences are admitted; no noiseless classical-register assumption is made.

The engineered controller has local syndrome-conditioned Pauli jumps sqrt(r_j(ell)) P_j Pi_ell, where ell is ONLY a bounded-support local syndrome/register pattern and Pi_ell its physical local projector (not a full-system syndrome projector), each enabled jump strictly decreasing W by at least d0>0. Their predicates must be computed from bounded local syndrome neighborhoods. Assume throughout S0 that the total enabled correction rate is at least c*kappa*W(s). This is an EXTENSIVE MOVE-COUNT/DRIFT premise, stronger than merely knowing that some improving move exists. Constants beta,b,c,d0,kappa are independent of n.

This criterion is useful only if an actual local decoder supplies both premises. Small-set expansion valid only up to O(sqrt n), or a polynomial-time global decoder, is not a substitute for them.

## Perturbation admission in a weighted operator norm

Let F=exp(aW), a>0. For any Pauli P with |W(s^P)-W(s)|<=b,

 ||F^(-1/2) i[P,F] F^(-1/2)|| <=2 sinh(ab/2),
 ||F^(1/2) P F^(-1/2)|| <=exp(ab/2).

Thus if a coherent perturbation is V(t)=sum_P P tensor B_P(t), with arbitrary bath operators and sum_P ||B_P(t)||<=h n, then

 -u_H(a)n F <= i[V(t),F] <=u_H(a)n F,
 u_H(a)=2h sinh(ab/2).

F is extended by identity on the bath/reference. Bath Hamiltonians commuting with F make no contribution. No time smoothness, bath bandwidth or Markovian approximation for V is used. A bounded-support local Hamiltonian can be Pauli-expanded with an explicitly paid constant coefficient factor.

For a local Lindblad jump J=sum_P j_P P, write l1(J)=sum_P|j_P|. Set A=F^(1/2)JF^(-1/2) and B=F^(-1/2)[F,J]F^(-1/2). The weighted dissipator equals (A*B+B*A)/2. Hence

 ||F^(-1/2) D[J]^*(F) F^(-1/2)||
 <=(exp(ab)-1) l1(J)^2.

If sum_J l1(J)^2<=gamma n, use u_D(a)=gamma(exp(ab)-1). General local miscalibration of an intended jump can be bounded by expanding the dissipator difference bilinearly; its cross terms and quadratic term must be included, not treated as an independent positive noise jump without justification.

Write u(a)=u_H(a)+u_D(a) for the displayed additive-noise model. These are operator inequalities, not trajectory-count or stationary-state assertions.

## Analysis-only reflected dynamics

Let Q project onto the union of syndrome sectors in S0. Q commutes with F. Define a reflected/censored auxiliary dynamics on QH by replacing each perturbing Hamiltonian with QVQ and each perturbing jump with QJQ. This is an analysis construction; it is not required to be a physically local controller.

Downhill ideal correction jumps cannot leave S0, so their restriction is unchanged on that space. Compression preserves the displayed weighted perturbation bounds because Q commutes with F. All reflected admitted local terms act trivially on the decoded logical subsystem; the reflected dynamics therefore preserves the unknown logical state and its reference correlations exactly.

For any fixed 0<theta<beta, put

 g(a)=c*kappa*theta*(1-exp(-a d0)).

The ideal correction generator obeys on QH

 Lcool^* F <=-g(a)n F+g(a)n exp(a theta n) I.

Indeed for W>=theta n its actual decrement is at least c*kappa*W(1-exp(-a d0))F, while below that region every correction is downhill and contributes nonpositively. If u(a)<g(a), the reflected full generator obeys

 Lref^* F <=-(g(a)-u(a))n F+g(a)n exp(a theta n) I.

For an initial code state, Gronwall gives uniformly at every time

 E_ref F <=[1+g(a)/(g(a)-u(a))] exp(a theta n).

Any admitted move from S0 to its complement must start at W>=B_n-b: otherwise its endpoint would still be a reachable below-cutoff syndrome. Therefore the reflected population in the exit boundary is at most

 p_boundary(t)<=C_a exp[-a((beta-theta)n-b)].

This is a nonstationary energy-flow estimate. The extensive coherent norm O(hn) is matched by the extensive restoring drift O(kappa theta n); no kappa growing with n has been assumed.

## Proposed logical consumer: compare only at the boundary

Embed the reflected state back into the original Hilbert space. A Duhamel comparison between the actual channel and reflected auxiliary channel should be bounded by the generator difference acting on the reflected state. Their coherent difference connects Q to its complement only through the one-step exit boundary. A common thicker two-step shell may be used for all terms. Cauchy--Schwarz/gentle bounds then give a contribution bounded by a constant times

 n h integral_0^T sqrt(p_boundary(t)) dt.

CORRECTION: general local dissipators require the TWO-STEP boundary shell W>=B_n-2b, because the anticommutator contains J*J. The one-step b shell is false: J=X1+X2, W=number of1s, cutoff2, rho=|00><00| produces off-diagonal |11><00| terms despite zero one-step-shell population. With p_boundary,2 at W>=B_n-2b, the proposed corrected bound is ||(D[J]-D[QJQ])(rho_ref)||_1<=4||J||² sqrt(p_boundary,2). The same exponential moment controls this thicker shell, changing only a fixed exp(ab) factor. Keep l1 coefficient constants in the noise budget. Ideal downhill terms agree. This would yield a restricted-code diamond/output error of order

 C n(h+gamma) T exp[-a(beta-theta)n/2],

up to fixed margins and coefficient factors, uniformly over reference entanglement and admitted baths. The reflected channel is decoded identity, so this is the proposed exponentially long coherent-noise memory conclusion.

The exact dissipator comparison, its constants, and the bath-reference extension are under independent audit. Do not cite this last display as an accepted result yet. A bound on instantaneous energy alone is NOT being substituted for a logical decoder: the flat low-potential component and boundary comparison are indispensable.

## Critical construction obligations

1. Produce a concrete code family, LOCAL potential, extensive low-potential move-count bound, and logical barrier for the SAME move alphabet.
2. A local decoder whose potential is a sum of local distances may help, but neither linear-time termination nor existence of one local improving move proves the required rate c*kappa W.
3. Admit actual fixed noisy controller jumps and any auxiliary apparatus. A formal conditional-Pauli jump does not automatically give a microscopic implementation.
4. Charge graph connectivity and physical geometry. Expander-graph locality is not fixed-dimensional geometric locality.
5. Compare known thermal LDPC memories, active fault tolerance and existing Lyapunov/metastability theorems at identical assumptions. No historical novelty or civilisation-level achievement is claimed.
