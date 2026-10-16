# Independent audit: overlap-tolerant subset-character effect bound

Date: 2026-10-15.

## Verdict

PASS for the finite-dimensional additive, deletion-stable whole-dilation model stated in SUBSET_CHARACTER_CANDIDATE.md. The constant-one product-of-actions bound is correct; there is no factorial or 2^|S| loss. The result bounds joint character subsets, including arbitrary bath/reference correlations, but neither produces chronological labels nor bounds their probabilities conditional on earlier outcomes. Local support/history transfer and the classical contour consequence are separate tasks.

## 1. Precise statement checked

On a finite-dimensional closed-system Hilbert space, let the complete propagator have Hamiltonian

H_g(t)=H_0(t)+sum_i V_i,g_i(t),

with integrable self-adjoint terms and independent uniform finite frame variables g_i. Only V_i may depend on g_i. Put a_i=integral sup_gi ||V_i,gi(t)|| dt. The initial input must be independent of these frame choices, although it may be arbitrarily correlated across memory, bath, and an untouched reference.

For finite abelian frame groups define K_chi=E_g conjugate(chi(g)) U_g. For every selected subset S,

sum_(chi: chi_i != trivial for all i in S) K_chi† K_chi <= product_(i in S) a_i² I.

Uniform averaging and character normalization are essential as written. The empty subset reduces to Kraus completeness. The orthogonal-projection formulation extends beyond abelian groups, but scalar irreducible characters alone do not provide a complete Fourier basis for a nonabelian group.

## 2. Mixed derivative: why there is no factorial

Fix a frame tuple and multiply each selected V_i by a real parameter z_i in [0,1]. Let U_z(t,s) be the propagator. All these propagators are unitary. The mixed derivative of the final propagator, with each selected parameter differentiated once, is

partial_S U_z(T,0)=(-i)^m sum_(permutations pi of S) integral_(0<t_1<...<t_m<T)
  U_z(T,t_m) V_(pi_m)(t_m) U_z(t_m,t_(m-1)) ... V_(pi_1)(t_1) U_z(t_1,0) dt,

where m=|S|. The formula follows by repeated Duhamel differentiation; every derivative inserts its own V_i once at any chronological position. The existing propagators retain all other couplings, so noncommutativity and shared baths are not discarded.

Taking norms removes only unitary factors. The resulting nonnegative integrals for the m! permutations are exactly the partition of the Cartesian product of the m independently labeled insertion times, excluding measure-zero ties. Therefore

||partial_S U_z(T,0)|| <= product_(i in S) integral ||V_i,gi(t)|| dt <= product_(i in S) a_i.

Bounding each ordered integral separately by the entire Cartesian integral would introduce an unnecessary factorial. The partition identity avoids that mistake. Finite dimension and integrable bounds justify the Duhamel derivatives and the interchanges of finite sums and integrals; no formal unbounded-operator manipulation is needed.

## 3. Deletion stability and the projection step

Let E_i average g_i and Q_i=I-E_i on the vector-valued L2 space of all independent frames. These are commuting orthogonal projections. Multivariate fundamental calculus gives the mixed difference

Delta_S U=integral_[0,1]^S partial_S U_z dz.

Every boundary term in Delta_S except U_(all selected z=1) omits at least one coupling V_i. The whole propagator at that boundary is independent of g_i, because there is no other dependence on that frame anywhere in the Hamiltonian, initial dilation state, or intervention sequence. Q_i therefore kills that boundary term. Consequently

Q_S U_(z=1)=Q_S integral partial_S U_z dz.

For any fixed vector psi, including any untouched reference, projection contraction and Minkowski give

||Q_S(U_g psi)||_L2 <= integral ||partial_S U_z(g) psi||_L2 dz <= product_i a_i ||psi||.

This uses L2 contraction of Q_S. It does not claim pointwise operator-norm contraction, which would be false in general and could introduce spurious powers of two. A frame-independent psi is necessary for the cancellation/projection argument.

## 4. Parseval and full-input CP effects

For finite abelian groups the product characters are a complete orthonormal scalar basis. Q_S keeps exactly those Fourier coefficients whose selected coordinates are all nontrivial. Parseval therefore identifies the square of the previous L2 norm with

sum_(selected nontrivial chi) ||K_chi psi||².

The vector inequality for every psi proves the claimed operator effect inequality. Completeness follows separately from Parseval and unitarity:

sum_chi K_chi†K_chi=E_g U_g†U_g=I.

Thus these coefficients define a valid joint-character CP instrument for the averaged full experiment. Tensoring any reference identity changes none of the norms or inequalities. Any initial memory-bath entanglement is allowed because the effect bound is on the entire joint input algebra, rather than on one prepared bath state.

For nonabelian groups, one may instead use the complete orthonormal basis of normalized irreducible matrix coefficients, including their dimension factors. The abstract Q_S bound survives, but the scalar-character formula must not simply be reused.

## 5. Dilation, interventions, and record limitations

The claim covers frame-independent CPTP interventions when they are represented inside one common finite-dimensional unitary dilation with frame-independent ancilla preparation. Genuine outcome-controlled operations may be represented by fixed controlled unitaries on retained records. Deleting a coupling must be done in this whole dilation; one must not freeze records to the values they would have had before deletion.

If the actual output traces a dilation ancilla, take any fixed initialization isometry W and output ancilla basis r. The refined actual Kraus operators are L_(chi,r)=<r| K_chi W. Summing r preserves the bound because

sum_r L_(chi,r)†L_(chi,r)=W†K_chi†K_chi W.

Thus the CP-instrument statement survives discarding ancillas. Alternatively, include initially correlated ancillas in the joint input; the full-space effect bound already covers them. Arbitrary physical preparations correlated with the sampled frames are excluded.

Frame-independent instantaneous unitary interventions can be included as fixed propagator breaks, or moved into an interaction picture. Their norms are one and the same proof applies. Arbitrary outcome postselection is different: a selected trace-decreasing branch need not have the uniform conditional bound, and it must not be normalized and substituted for the full unitary dilation. The crossing echo obstruction illustrates precisely why such conditional bounds need not hold.

The Fourier labels may exist only as an end-of-experiment Kraus unravelling. Their existence does not make them causal records available during the experiment. Subsequent access to an explicit frame register can destroy the stated deletion property unless every such dependence is incorporated and charged in the model. Merely calling a controller frame-independent while allowing its input register to contain g_i does not satisfy the initial-state/deletion premise.

## 6. Strength and boundaries

The constant one is sharp in the small-action limit: for commuting independent sign-rotations, a selected character has amplitude product sin(a_i), whose squared ratio to product a_i² tends to one. Thus there is no apparent missing generic combinatorial constant.

No memory-history theorem follows from this norm calculation alone. Joint character blocks can have complicated spacetime support, and end-only labels do not automatically supply legal local chronological faults. The additive representation itself also needs justification for a concrete framed circuit: a term depending jointly on two frame variables, or a frame-dependent ideal control left outside the charged terms, invalidates the deletion argument.

The statement does tolerate overlapping pulses, shared-bath commutators, arbitrary frame-independent Hamiltonian background, and arbitrarily strong unselected couplings. It does not assert iid domination, chronological conditional probabilities, fault tolerance of controls, an infinite-dimensional bath extension, or historical novelty.

## 7. Independent computational checks

1. Inspected and reran ../checks/exact/check_three_pulse_moments.py. Its memory factors are X-mask Paulis, so each Fourier effect is identity on memory tensor the displayed 2x2 bath effect. Exact completeness and all seven subset principal-minor certificates pass. The noncommuting bath factors are retained in chronological order.

2. Added ../checks/numeric/check_subset_character_stress.py, using installed NumPy/SciPy only. Twelve independent tests use three Z3 frames, four overlapping Hamiltonian segments, arbitrary noncommuting 4x4 Hermitian couplings, and a nontrivial frame-independent background. All 84 subset effect inequalities pass; largest measured effect-to-budget ratio is approximately 0.278700619. This numerical test exercises multiple nontrivial characters per coordinate, unlike sign-only examples. It is a stress test rather than the proof.

The analytic argument above is the certification; the computational checks are supplementary.
