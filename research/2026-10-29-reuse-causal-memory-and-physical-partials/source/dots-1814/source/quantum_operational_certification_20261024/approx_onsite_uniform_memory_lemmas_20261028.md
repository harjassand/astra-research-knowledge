# Approximate on-site extraction: independently derived uniform-memory lemmas

28 October 2026. **Author-derived mathematical appendix; not an independent receiving receipt.** This file does not modify the exact on-site source. It supplies the structural bounds needed by the separate approximate-on-site construction. All numerical evidence below evaluates declared finite matrices and exact expectation formulas; there are no sampled source calls, acquisition outcomes, or hardware claims.

## 1. Model and notation

Let U:L tensor G -> P be a fixed unitary identification, with q logical qubits and n known physical qubits. Write B_ij=U(sigma_ij tensor I_G)U† for the true logical generators. Assume distinct sites pi(i) and on-site oriented Pauli triples A_ij=V_i sigma_j V_i† exist, with supplied bounds

    ||B_ij-A_ij||op <= tau_ij,             j=X,Z.             (1)

The witnesses pi,V_i are not assumed to be supplied to the learner. Let D_A apply the local V_i†, retain the selected sites in logical order, and trace the rest. No approximate global tensor-factorization claim is necessary. Put t²=sum_i,j tau_ij². Any gauge state may be mixed and entangled with retained memory; the following statements are uniform over it.

## 2. Sharp joint Bell bound from only X,Z

For the global Choi input, purify the arbitrary gauge state and write |Psi>=(I_R tensor U)(|Phi>_RL tensor |g>). The true stabilizers

    T_ij=sigma_ij^T(on R) tensor B_ij, j=X,Z

fix |Psi>. The physically tested on-site stabilizers

    S_ij=sigma_ij^T(on R) tensor A_ij

are commuting Hermitian involutions: X and Z anticommute on each of their two factors, so their tensor products commute; different i use distinct reference/output sites. The product of all 2q positive-stabilizer projectors is precisely the global Bell projector after D_A. For each test,

    <Psi|(I-S_ij)/2|Psi>
      = ||(I-S_ij)|Psi>||²/4
      = ||(T_ij-S_ij)|Psi>||²/4 <= tau_ij²/4.             (2)

The commuting-projector union bound therefore yields

    ell_0(D_A,U;g) <= (1/4) sum_i,j tau_ij² = t²/4.         (3)

This is a full q-Bell-reference statement, not a product-state or independent-gauge assertion. There is no factor q² and no Y-generator premise. If the actual learned proper rotation has columns rhat_ij while r_ij are those of V_i, then

    ell_0(D_hat,U;g)
       <= (1/4)sum_i,j(tau_ij+||rhat_ij-r_ij||₂)².          (4)

All inequalities hold for every gauge/memory state on the same record-defined estimator event.

## 3. Positive signed blocks give relative, not absolute, bias

For any normalized positive gauge state h and any j=X,Z, set

    rho_h=U(I_L/2^q tensor h)U†,
    Delta_j=B_ij rho_h=U(sigma_ij/2^q tensor h)U†.

Here rho_h commutes with B_ij, Delta_j is Hermitian and traceless, and ||Delta_j||1=1. Its reduction to pi(i) is (c_ij dot sigma)/2. Consequently ||c_ij||₂<=1. Moreover,

    r_ij dot c_ij = Tr(A_ij B_ij rho_h)
      = 1 - Tr[(A_ij-B_ij)²rho_h]/2 >= 1-tau_ij²/2.       (5)

The middle equality uses commutation of rho_h with B_ij to equate the two cross terms. It does NOT assume A_ij commutes with rho_h. Thus

    ||c_ij-r_ij||₂ <= tau_ij.                            (6)

If tau_ij<sqrt(2), c_ij is nonzero. Its normalized direction v_ij=c_ij/||c_ij|| satisfies the same bound:

    ||v_ij-r_ij||₂²
      =2(1-(r_ij dot c_ij)/||c_ij||) <= tau_ij².          (7)

In the CP-margin source, the signed gauge block H_ij is positive with trace lambda_ij>=kappa. The actual signed Bloch column is m_ij=lambda_ij c_ij, with h=H_ij/lambda_ij. Therefore its perturbation from the ideal ray scales as lambda_ij tau_ij, not merely tau_ij. Adaptive time averages remain in the same cap: writing lambdabar=mean_t lambda_t, the ratio mbar/lambdabar is a positive lambda-weighted average of the c_t; (5) and ||c||<=1 are preserved.

This observation prevents treating a crude q tau²/kappa² upper bound as an unavoidable robustness floor.

## 4. Conventional normalized-column proper-rotation fit

Suppose an actual empirical two-column mean is mhat_ij=mbar_ij+n_ij. Normalize every nonzero empirical column; if exactly zero, choose a predetermined unit vector. For a=max(positive lower bound on 1-tau_ij²/2), the elementary normalization inequality gives

    ||vhat_ij-vbar_ij||₂ <= 2||n_ij||₂/(kappa a).          (8)

This is valid even at mhat=0 under the declared fallback, since then ||n||=||mbar|| and both unit vectors are at distance at most 2. Consequently

    eta_i := (sum_j||vhat_ij-r_ij||₂²)^(1/2)
       <= (sum_j tau_ij²)^(1/2)
            + 2(sum_j||n_ij||₂²)^(1/2)/(kappa a).         (9)

Fit a PROPER rotation Rhat_i to the two unit columns, with objective gap delta_i. Since both columns of any proper rotation are unit, maximizing the two-column inner product is exactly minimizing their squared Euclidean residual. The objective guarantee yields

    sum_j||rhat_ij-vhat_ij||₂²
       <= sum_j||r_ij-vhat_ij||₂² + 2delta_i.

A triangle inequality in R^6 gives

    s_i := (sum_j||rhat_ij-r_ij||₂²)^(1/2)
       <= 2eta_i + sqrt(2delta_i).                       (10)

This uses only the X,Z errors required by (4), rather than inflating to all three fitted columns. Globally define n²=sum_i,j||n_ij||₂² and Delta=sum_i delta_i. Equations (4),(9),(10) yield

    sqrt(ell_0)
       <= (3/2)t + 2n/(kappa a) + sqrt(Delta/2).          (11)

At vanishing statistical/fit error the certified structural loss is at most (9/4)t², or (9/2)q tau² for a common two-axis tau. The meaningful robustness order is q tau², independent of kappa; kappa still controls ordinary acquisition precision and sample size. The same conventional finite quaternion fit as the exact on-site source is available, but empirical normalization must be finitely approximated and its explicit column error added to (9). No irrational normalization is granted as a free physical control.

## 5. Transfer to the strongest current-memory full-CPTP oracle

For any fixed decoder D and U, there is a Bell-block POVM {T_alpha} on G, with positive T_alpha and sum_alpha T_alpha=I_G. For product local unitary extraction it can be written explicitly: after arranging selected sites first, put W=(tensor_i Vhat_i† tensor I)U, K_alpha=2^(-q)Tr_L[W(P_alpha tensor I)], and T_alpha=K_alpha†K_alpha. The Pauli coefficient identity gives sum T_alpha=I_G.

The virtual identity loss is Tr[(I-T_I)h]. Since (3) or (11) holds for EVERY gauge state h, it implies the Loewner inequality I-T_I<=b I_G with the corresponding bound b (or min{1,b}). For the actual later source state let G_alpha be its positive emitted gauge blocks. Then

    ell(D E)-ell(D_* E)
      =sum_(alpha!=I)Tr[(G_I-G_alpha)T_alpha]
      <=Tr[G_I(I-T_I)] <= b Tr(G_I) <= b.               (12)

Under G_I-G_alpha>=0 for all alpha, exact algebra extraction D_* is optimal among ALL full-CPTP q-logical receivers. The upper bound uses G_alpha>=0; dominance is the separate assumption needed to identify the informed optimum. If the G_alpha are obtained from CP maps acting on arbitrary retained memory, (12) holds at each actual conditional source state. No changed-past-policy oracle is introduced.

## 6. Genuine future-memory obstruction: Theta(q tau²)

There are q logical qubits and q physical gauge qubits. Fix 0<theta<=pi/2 and unknown signs s_i in {+1,-1}. Define independent controlled weak rotations

    U_s = tensor_i [ I_L tensor |0><0|_G
                     + Rz(s_i theta)_L tensor |1><1|_G ]. (13)

During every training call the source emits gauge |0...0>; at the future service it emits |1...1>. There is no logical Pauli noise: G_I is the only nonzero block, so kappa=1 and the informed full-CPTP oracle has zero loss. All training data, even those of an arbitrarily powerful learner, are identical across the 2^q choices of s. Relative to the on-site identity basis, B_iZ=Z_i exactly and

    ||B_iX-X_i||op=2 sin(theta/2)=tau.                   (14)

At the future gauge, averaging uniformly over the unobserved signs gives a tensor product Z-dephasing channel with p=sin²(theta/2)=tau²/4. Its identity Pauli probability is (1-p)^q and is the largest Pauli probability. No CPTP receiver can exceed that entanglement fidelity: the Bell-block POVM here is a probability vector, so its weighted success is at most the largest Pauli weight. Hence for EVERY training-based frozen receiver there is a source completion s whose expected future Bell loss is at least

    1-(1-tau²/4)^q.                                    (15)

This is Theta(q tau²) when q tau² is small. The lower bound is not restricted to product receivers, to proper rotations, or to ordinary calibration. It is a hidden-completion/future-memory information obstruction. With no permitted persistence assumption on the gauge state, adding calibration calls cannot eliminate it. The witness A=I is valid even though it need not be the closest possible on-site witness.

## 7. Local weak-crosstalk interface

Suppose U=W U_0 and U_0 has the exact on-site algebra A_ij. Let W solve dW/ds=-iH(s)W, W(0)=I. The safe Duhamel identity differentiates W† A W, not a fixed-operator approximation to the forward-evolved generator:

    d(W† A W)/ds=iW†[H(s),A]W.

Thus

    ||W A_ij W†-A_ij||op
       <= integral ||[H(s),A_ij]||op ds
       <= 2 integral sum_(e contains pi(i)) ||H_e(s)||op ds, (16)

when H(s)=sum_e H_e(s) and terms not meeting pi(i) act trivially on that site. This allows bounded incident integrated coupling, not a global ||H|| bound proportional to q. Substitution in (3) or (11) gives a quadratic local-coupling floor summed over sites. A fixed W/U is still required through service; uncontrolled time drift of the algebra is not certified by (16).

## Evidence

`approx_onsite_uniform_memory_lemmas_check_20261028.py` and its JSON output evaluate noncommuting coupled-unitary fixtures, arbitrary positive gauge states, exact expectation Bloch columns, proper normalized fits, full gauge-uniform Bell operators, Bell-block POVMs, and the controlled-rotation lower construction. Floating evaluation is a deterministic regression check, not a substitute for the analytical proofs above. Original exact-on-site files are untouched.
