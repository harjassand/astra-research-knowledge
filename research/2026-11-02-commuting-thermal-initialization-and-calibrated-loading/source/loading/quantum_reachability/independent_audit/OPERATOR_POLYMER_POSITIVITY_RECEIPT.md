# Independent receipt: finite operator gas and inverse-Pauli-noise positivity

1 November2026. **PASS for Part A and for the proposed identification/positivity conclusion in the ACTUAL stabilizer-reference model.** A general-reference energy-change shortcut needs the qualification below. No efficient preparation, reachability, or logical-input protection is certified.

Frozen root `ROOT_OPERATOR_POLYMER_POSITIVITY.md`: SHA256 `9e384f043dd9db6b7be94f5bd319bef239b0cc465fbcf01ff83af98c65f8a9b0`.

## 1. Noncommuting finite matrix-gas induction

Let B=S minus gamma and C=B minus its incompatible neighbors. Deletion–contraction is

 Z(S)=Z(B)+A_gamma Z(C)
     =Z(B)[I+Z(B)^(-1)Z(C)A_gamma].

The last equality uses only compatibility of gamma with every polymer in C, so A_gamma commutes with Z(C). It does NOT require commutation with Z(B).

If B=B0, B1,...,Bk=C is a successive neighbor-deletion sequence, the exact ORDERED identity is

 Z(B)^(-1)Z(C)=product_j [Z(B_j)^(-1)Z(B_(j+1))].

Adjacent inverse factors cancel without commuting anything. Each ratio is covered by induction on a smaller set. Its norm bound, multiplied by ||A_gamma||, is at most mu_gamma/(1+mu_gamma), using the CLOSED neighborhood including gamma itself. Neumann inversion therefore gives the claimed inverse-deletion bound. This proves invertibility simultaneously for all subsets. Zero operators can be removed or handled with positive majorants.

Every compatible product is Hermitian because its factors commute. Scaling all activities by real t in[0,1] preserves Hermiticity and the norm condition. Starting from identity, the real eigenvalues cannot cross zero while invertibility holds. Hence every final gas matrix is strictly positive. No order comparison between noncommuting exponentials is involved.

## 2. Exact centered perturbation expansion

Write T=exp(beta H_ref/2) and U=T exp[-beta(H_ref+V)]T. The centered interaction-picture formula uses

 V_a(t)=exp[(t-beta/2)H_ref] V_a exp[-(t-beta/2)H_ref], 0<=t<=beta.

Because reference terms commute, terms disjoint from the ORIGINAL support of V_a cancel out. Thus each V_a(t) has the stated bounded enlarged support and local norm amplification, with constants independent of total volume. Its time ordering is retained; no replacement by a commuting perturbation occurs.

For a label subset S, let A^V_S be the sum of all words using exactly those labels, each at least once. It also has the exact inclusion-exclusion expression

 A^V_S=sum_(B subset S)(-1)^(|S|-|B|) U_B,
 U_B=T exp[-beta(H_ref+sum_(a in B)V_a)]T.

Every U_B is Hermitian, so each individual A^V_S is Hermitian. This is the required justification; positivity of the total U alone would not imply Hermiticity of an arbitrary component decomposition.

If S decomposes into disconnected enlarged-support components, operators from distinct components commute for all insertion times. The ordered-integral shuffle identity factors A^V_S into the corresponding component activities. Norm bounds at fixed multiplicities sum to

 ||A^V_S|| <= product_(a in S)(exp[x_a]-1),
 x_a=beta sup_t||V_a(t)||.

For a uniform local bound this is a^|S| as claimed. There is no hidden global ||V|| in this estimate.

## 3. Exact inverse-noise formula and local bound

Assume0<=q_i<1/2 and choose Hermitian Pauli representatives. For C_i=(1-q_i)id+q_i Ad(P_i),

 C_i^(-1)=[(1-q_i)/(1-2q_i)] [id-r_i Ad(P_i)],
 r_i=q_i/(1-q_i).

The omitted prefactor is positive. Pauli conjugation superoperators commute even when their Pauli representatives anticommute. After the relative congruence, Ad(P_i) becomes B_i(.)B_i† with B_i=T P_i T^(-1). Products satisfy the stated telescoping B_F identity up to an irrelevant phase. Thus the finite signed subset expansion for K is exact.

For the actual H_ref=H0 stabilizer memory plus onsite bath, with noise Paulis on memory, P_i H0 P_i commutes with H0. Consequently

 ||B_i||²=||exp[beta(H0-P_i H0 P_i)]||
 <=exp[beta||H0-P_i H0 P_i||].

Only incident flipped checks contribute. Onsite bath terms cancel entirely. The sharper local energy-change bound is therefore valid in the intended model.

**Preserved counterexample to a broader interpretation:** For an arbitrary commuting-term reference (a single Hermitian term already qualifies), B must NOT automatically mean ||H_ref-PH_refP||. Take H=10Z+0.1X, P=Z, beta=1. Then ||H-PHP||=0.2, but ||exp(H/2)P exp(-H/2)||² is about48562.20, exceeding exp(0.2) about1.2214. Analytically, in the eigenbasis of H, its norm squared is at least exp(20)/10001, already larger than exp(0.2).

A universally safe commuting-local-reference bound is B=2 sum_(reference terms touching P)||h||: all other reference terms cancel, and submultiplicativity bounds the remaining local similarity transform. This restores a volume-independent positive parameter region for that broader reference as well, but is not the invalid sharp energy-difference shortcut. The counterexample does not refute the actual stabilizer-reference application.

## 4. Joint component identification

Expand U by selected perturbation labels, then expand the finite inverse-noise subset. For each selected joint set, form connected components in the graph of enlarged perturbation/noise supports. Within a joint component, first split its perturbation-only set into its disjoint V-components and multiply their activities. They commute and are Hermitian. Conjugation by the selected product B_F preserves Hermiticity, and multiplication by the real signed coefficient preserves it too. Noise-only components use the identity as their V-product.

Different joint components have disjoint supports, so their B factors and activities commute and factor. Grouping the joint subsets by these UNIQUE components therefore gives exactly the claimed matrix gas, not a many-to-one cover. The norm estimate is

 ||A_gamma||<=a^(#V labels) product_(i noise labels)[r_i ||B_i||²].

Bounded local incidence/range/dimension makes the joint graph degree uniformly bounded, including bath perturbation labels. With u=max(a,max_i r_i exp(beta B_i)), rooted connected-animal counting makes the closed-neighbor majorant in Part A hold for sufficiently small fixed u. For example use mu_gamma=||A_gamma||exp(|gamma|) and a sufficiently small geometric-series bound on incompatible rooted animals. This controls ALL components, not only scalar or short components, so no code-distance/logical-polymer cutoff is needed for this positivity statement.

Thus K>0 in every finite volume at fixed finite beta and sufficiently small admitted local V/noise strengths, with thresholds independent of memory/bath volume. Congruencing back and restoring the positive prefactor gives C^(-1)(rho_actual)>0. Since the finite inverse channel is trace preserving, its trace is exactly1. No uniform lower spectral gap, efficient matrix representation, or infinite global density matrix is asserted.

## 5. Diagnostics and operational boundary

Saved and ran `test_operator_polymer.py` beside this receipt. A two-qubit noncommuting perturbation example with a nonunitary B_i verifies individual Hermiticity and the full joint expansion against direct inverse noise to norm residual7.6e-16; the test K has minimum eigenvalue about0.92113. All subset inverse-deletion ratios for three incompatible noncommuting Pauli activities pass. These are numerical diagnostics, not replacements for the finite proofs. The general-reference counterexample above is reproduced numerically and has the separate analytic bound stated above.

Positivity supplies only a mathematical preimage. It does not provide its efficient preparation, memory-only access to an inaccessible bath, a conserved-sector reachability argument, or stability of arbitrary reference-entangled logical inputs after noise. Applying inverse noise to the FULL joint Gibbs operator is distinct from loading it under actual physical restrictions. No physical-loading advantage, no novelty claim, and no extension to arbitrary channels or beta->infinity is certified.
