# Independent review: transverse damped-qubit telegraph representation and jump-count bound

31 October 2026. This is a separate mathematical review of the root's stated construction, not an extension of the earlier commuting-noise compiler. No source file or executed circuit was reviewed for this new lemma.

## Verdict

The exact reduced-process representation and the exponential jump-count bound are valid for finitely many bounded Hermitian system operators, including mutually noncommuting ones. The result supplies a positive low-count representation. It does not yet supply an efficient no-jump propagator, holding-time sampler, Kraus implementation, or complete low-cost simulation algorithm.

## Exact model and hierarchy

Let independent stationary symmetric signs xi_i flip at rates lambda_i>0. Put v_i=sqrt(gamma_i lambda_i) and

    H(t)=H0+sum_i v_i xi_i(t) A_i.

Take one ancilla qubit per sign, initialized in its Z-ground state. On system plus ancillas define

    H_ext=H0+sum_i v_i A_i tensor X_i,
    J_i=2 sqrt(lambda_i) sigma_-i.

All identities include identity factors on untouched registers. A system reference and retained controller memory can be included throughout.

For each subset S of the ancilla indices, define the system operator

    x_S=Tr_E[X_S rho_SE],  X_S=product_{i in S} X_i.

Write L0(B)=-i[H0,B] and Li(B)=-i[A_i,B]. Cyclicity of the environment partial trace and X_i squared equal to identity give exactly

    x_S' = L0(x_S) - 2 sum_{i in S} lambda_i x_S
           + sum_i v_i Li(x_{S symmetric-difference {i}}).

Indeed the damping adjoint sends X_i to -2 lambda_i X_i and sends identity to zero. Other ancilla damping terms do not affect X_S. No commutation between A_i and A_j is used.

The classical telegraph signed moments obey precisely this finite closed hierarchy. Both initial hierarchies have x_empty=rho_system and all other x_S=0. Uniqueness of the finite linear ODE proves equality of the system states.

More strongly, every system-only instrument branch applies the same completely positive linear map to every moment in either construction. Induction over interventions proves equality of the system process, including outcome records, retained ancillas, and adaptive selection of system operations. The environment must be retained between interventions. Observing the dilation ancillas or its jump record is not part of this equivalence: those records are not classical telegraph flip records.

The hierarchy is also consistent with positivity: its Fourier transform equals the positive diagonal blocks of rho_SE in the joint X basis. Ground-state initialization supplies the uniform independent classical sign moments, even though the physical ancilla state is not maximally mixed.

## Tilted jump-count inequality

Let N count the actual quantum jumps associated with the J_i in this dilation. For theta>0 put

    kappa=exp(theta)-1,
    delta=2 kappa,
    P_i=|1><1|_i,
    V_i=I+delta P_i,
    V=product_i V_i.

The tilted generator multiplies each positive jump term J_i rho J_i dagger by exp(theta), leaving its anticommutator loss unchanged. Its adjoint acting on V has damping contribution

    -4 lambda_i kappa P_i V_others.

The Hamiltonian contribution for index i is

    i v_i delta A_i [X_i,P_i] V_others.

In the ground/excited block decomposition, their sum before multiplication by V_others is

    [[0, i v_i delta A_i],
     [-i v_i delta A_i, -4 lambda_i kappa I]].

If ||A_i||<=a_i, completing the square gives the operator bound

    block <= [v_i squared delta squared a_i squared /
              (4 lambda_i kappa)] (I-P_i)
          = gamma_i a_i squared kappa (I-P_i)
          <= gamma_i a_i squared kappa V_i.

Multiplication by V_others preserves the inequality because it is positive and acts only on other ancillas. The H0 commutator with V vanishes. Therefore, with Gamma=sum_i gamma_i a_i squared,

    L_theta dagger(V) <= Gamma kappa V.

The tilted evolution is positive. For its unnormalized state, the weighted trace obeys a scalar Gronwall inequality. Initially its V expectation is exactly one because every ancilla is in the ground state. Since V>=I,

    E exp(theta N(T)) <= exp[Gamma T (exp(theta)-1)].

System-only trace-preserving controls leave V invariant under their adjoints, so the same estimate survives interventions. For adaptive instruments, sum the branches with their probabilities; no conditioning on a rare measurement outcome is permitted without charging its probability. The estimate is uniform in the system/reference input state.

Zero-coupling or zero-rate indices can be omitted. If an ancilla is not initially ground, the simple proof instead contains its initial V expectation. The ground initialization is therefore load-bearing for the unit prefactor, although other initial states with vanishing X moments can still represent the same reduced classical process.

## Consequences and limitations

The inequality gives E N(T)<=Gamma T and Poisson-form Chernoff tail bounds, independently of the switching rates. It does not by itself establish stochastic domination by a Poisson random variable, pathwise bounded jump intensity, or a thinning sampler. Actual conditional jump intensity may still be 4 sum_i lambda_i Tr(P_i rho_conditional).

In particular, rare total jumps do not make the no-jump generator cheap: it contains the large damping terms and couplings. An efficient positive no-jump/holding-time/compiler interface remains a separate obligation. No complete noncommuting-noise algorithm or polylogarithmic-rate complexity theorem is accepted by this receipt.

## Primary comparisons

Saira, Bergholm, Ojanen, and Mottonen, “Equivalent qubit dynamics under classical and quantum noise,” Physical Review A 75, 012308 (2007), is a close required comparator:
https://arxiv.org/pdf/quant-ph/0605241

Its Section IV uses longitudinal Z coupling to a defect with both raising and lowering jumps; equal rates reproduce symmetric random telegraph noise. Its other equivalence uses a Born-memory equation. That establishes important prior classical/quantum noise equivalence and control context, but the inspected construction is not the transverse-X, ground-state, one-way-damping representation reviewed here. I did not find the present jump-count MGF in that paper. This limited inspection does not establish novelty.

Tamascelli and coauthors' pseudomode equivalence framework is another relevant primary comparator:
https://arxiv.org/abs/1709.03509

Its stated equivalence is for Gaussian environments with matched means and two-time correlations. Telegraph noise is not Gaussian, so matching two-time correlations alone would not justify the present result. The finite exact moment hierarchy above supplies the needed independent proof.

No priority claim, implementation claim, or operational construction follows from this review.
