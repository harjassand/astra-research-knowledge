# Canonical local noise orientation rather than an unidentifiable original mixer

28 October 2026. Root candidate algebraic extension. This is not yet a received acquisition theorem. It supplies the target and identifiability contract for the developing three-contrast whitening construction. No earlier governing source is changed.

## 1. Physical family and the right target

Suppose the stationary reduced physical channel on n actual input qubits is

    N = Ad_V composed (tensor_i E_i),

where E_i are unknown qubit CPTP channels, and V is an unknown fixed unitary whose conjugated single-qubit Pauli algebras have bounded output support. The source's complete memory realization may be larger; the reduced identity must hold at every conditional history used by calibration, not merely at one initial memory state.

Use Bloch column vectors, E_i: r -> T_i r + t_i. Assume T_i invertible and det(T_i)>0. Right polar decomposition gives

    S_i = (T_i^T T_i)^(1/2)>0,
    O_i = T_i S_i^(-1) in SO(3).

Choose a qubit unitary U_i implementing O_i. Its irrelevant global sign does not affect any channel. Define E_i' = Ad_(U_i dagger) composed E_i, a genuine CPTP channel with Bloch data (S_i, O_i^T t_i), and

    V_eff = V (tensor_i U_i).

Then EXACTLY N = Ad_(V_eff) composed (tensor_i E_i'). No environmental reconstruction or nonphysical inverse of E_i was taken. Local Pauli supports are unchanged as algebras: each new generator is a real linear combination of the old three generators on the same support. The operational inverse target is V_eff dagger, leaving the product dissipative channels E_i'. It is not noiseless recovery or the original V dagger.

Original V is not identifiable from the reduced source without an extra convention. For arbitrary local unitaries W_i, replacing V by V(tensor W_i) and E_i by Ad_(W_i dagger) E_i leaves N unchanged. Even complete calibration of N cannot resolve this gauge. The positive Bloch polar convention fixes this ambiguity when det(T_i)>0 and T_i is nonsingular. A claim to recover the original V under this unrestricted channel family would therefore be false.

## 2. Three ordinary contrasts expose the canonical algebra

Prepare physical input i along each signed Pauli axis j, with other inputs averaged to I/2. Write rho_k=E_k'(I/2), and let

    B_(i,a)=V_eff sigma_(i,a) V_eff dagger,
    R_i=V_eff [(I_i/2) tensor_(k!=i) rho_k] V_eff dagger.

The ACTUAL signed reduced-output contrast is

    Delta_(i,j)=sum_a S_i[a,j] B_(i,a) R_i.

R_i is positive and commutes with the whole own-qubit algebra. It need not commute with other input-qubit algebras, and the unsigned output need not be maximally mixed. On a known output envelope J containing the whole own-qubit support, partial trace preserves the same identity with R_i,J and B_(i,a),J.

Let C_j denote these local contrasts and define the real Gram matrix G_jk=Tr(C_j C_k). Own-algebra commutation implies

    Tr(B_a B_b R_J^2)=delta_ab Tr(R_J^2).

For a!=b, B_a B_b is proportional to the third Pauli; conjugation by a different own Pauli changes its sign and leaves R_J^2 invariant. Therefore, with g=Tr(R_J^2)>0,

    G = g S_i^2,
    F_j = sum_k C_k [G^(-1/2)]_kj = B_(i,j),J R_J / sqrt(g).

If R_J is strictly positive, functional calculus gives sign(F_j)=B_(i,j),J. Whitening does NOT itself output a reflection unless R_J is scalar. The final sign step is load-bearing. This supplies a concrete exact algebraic route from ordinary local response operators to a physical canonical inverse.

Finite acquisition still requires actual interval-certified support, a certified positive Gram gap, a certified sign gap, perturbation/finite precision bounds and the physical extraction circuit. These obligations belong to the separate developing whitening source and are not assumed solved here. Direct dense channel tomography is the equally informed ordinary comparator.

## 3. Boundaries and costs that cannot be erased

An invertible CPTP qubit channel has full-rank E_i(I/2). If that output were rank one, positivity would force both output states for every opposite input pair into the same one-dimensional support, making the channel constant and T_i singular. This proves strict positivity for a fixed finite instance, but supplies no useful numerical floor and no uniform polynomial sample guarantee by itself.

For bounded output envelope J, locality can restrict spectator dependence to its backward input cone, as in the separate aligned amplitude-damping source. A local lower eigenvalue premise and a lower singular value of S_i would then determine completion cost. No product over all n spectator eigenvalues should be inserted without checking this local reduction. Quantitative finite guards remain unresolved in this note.

If det(T_i)<0, O_i is an improper rotation and cannot be absorbed into a physical qubit unitary. This note does not silently implement a transpose or claim the same positive convention. Singular T_i loses at least one contrast direction; Gram whitening cannot restore erased information. These are representation boundaries, not generic impossibility theorems for every quantum task.

If conditional memory selects different channels, sums of contrasts need not retain a single common R_i and S_i. The fixed-product premise above is substantive. A one-time fit does not license it at every future memory state. An actual complete-norm approximation to V_eff dagger, once independently acquired, can be composed with arbitrary future source maps relative to that same fixed inverse; it does not certify that future native noise remains product or correctable.

No historical novelty, practical advantage, hardware performance, threshold or broad unknown-noise recovery solution is claimed. The new point under investigation is a canonical physical target and an exact common-factor cancellation mechanism that could expand acquisition beyond aligned amplitude damping.
