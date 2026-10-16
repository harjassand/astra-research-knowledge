# Candidate: overlap-tolerant joint character moment bound

2026-10-15. Root construction, pending independent review and prior-art comparison. This is a Hamiltonian/interface lemma candidate, not yet an autonomous-memory theorem.

## Hypotheses

A finite collection of independent private frames g_i in finite groups G_i. The full finite-dimensional closed-system (memory plus arbitrary persistent bath plus dilation ancillas) Hamiltonian has the additive form

H_g(t)=H_0(t)+sum_i V_i,g_i(t),

with self-adjoint integrable terms, each V_i depending only on its own frame. H_0 and all frame-independent interventions may be arbitrary; uniform bounds a_i=integral sup_gi ||V_i,gi(t)|| dt are finite. Frame records are inaccessible to subsequent operations. Supports and pulse intervals may overlap for this algebraic claim. A physical QEC application will impose further locality and covariance conditions. The initial input is independent of all frames but may be correlated with the bath/reference.

Let U_g be the full propagator. In Hilbert-space-valued L2 of the independent uniform frame variables, let E_i average frame i and Q_i=I-E_i. Q_i is an orthogonal projection. Characters below use finite abelian groups (as in Pauli-frame conjugation); the projection statement itself needs only independent finite frames.

## Claim

For any subset S, the joint averaged character instrument satisfies

sum_{chi: chi_i nontrivial for every i in S} K_chi^dagger K_chi <= (product_{i in S} a_i^2) I,

where K_chi=E_g conjugate(chi(g)) U_g.

Consequently the probability of all those character labels being nontrivial is bounded by the product for every initial joint state and reference. No bound conditional on earlier nonzero labels is asserted.

## Proposed proof

For selected i in S introduce independent real z_i in [0,1] multiplying V_i,gi. For each fixed frame tuple, the propagator remains unitary for every z. By multivariate fundamental calculus,

Q_S U_(z=1) = Q_S integral_[0,1]^S partial_S U_z dz.

Indeed all other boundary terms have at least one z_i=0. Such a term is independent of g_i because the additive Hamiltonian contains no other g_i-dependent term, and Q_i kills it.

The mixed Duhamel derivative is a sum over all temporal orderings of one insertion of V_i,gi for each i in S, with unitary propagators between insertions. Taking operator norms and integrating, the temporal ordering domains partition the full Cartesian product of insertion times, apart from measure-zero ties. Thus

||partial_S U_z|| <= product_i integral ||V_i,gi(t)|| dt <= product_i a_i.

This assertion includes no factorial loss: the |S|! orderings partition the product integration domain rather than each being bounded by the whole product. For fixed vector psi including any reference, orthogonal projection contraction and Minkowski give

||Q_S U_g psi||_L2(g) <= product_i a_i ||psi||.

Parseval identifies the squared left side with the sum over character Kraus probabilities in the claim. Since this holds for every psi it proves the joint effect inequality.

## Exact scope

- Shared-bath commutators and overlapping pulses are allowed algebraically.
- A Hamiltonian term depending jointly on multiple frames breaks the missing-coupling cancellation unless it is separately charged and analyzed.
- A frame-dependent initial state, exposed frame record, or frame-dependent ideal control not absorbed into the displayed additive model breaks the premise.
- Nontrivial character labels may be revealed only at the end of the full experiment; this lemma does not manufacture a chronological local instrument or a conditional small-error guarantee.
- To use it in the memory argument one must additionally prove that a character tuple controls legal bounded-support Pauli histories and that local-stochastic moment bounds, without iid domination, suffice for the contour escape estimate.
- The bound can be trivial for large action. It is not an empirical noise calibration and does not follow from average gate fidelity.
- This likely combines established fault-path Duhamel estimates with orthogonal randomization; novelty is unclaimed.
