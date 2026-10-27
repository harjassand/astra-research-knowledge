# Whole VALUE: arbitrary three-mode logical spectrum and a maximally entangled reset flag

Status: analytic proof with exact finite coefficient certificate; awaiting independent receipt.

## Actual source and scope
Let C≥0 be any3-by-3 logical matrix and ψ a maximally entangled UNIT vector between the reference code C³ and logical C³. For a,b≥0 put

Y=aI₉+bP_ψ, X=P_Ω3⊗C+I₃⊗Y.

Then Δ(X)≥0. If C>0, equality holds exactly when Y=0. Here Ω3 is unnormalized, whereas ψ is unit. This is a genuinely nonflat rank-three reversible main, not three unrelated Kraus directions. Arbitrary non-maximally-entangled reset flags and negative holes with nonflat C are NOT claimed.

The physical marginal is(TrC+9a+b)I₃. Divide by this scalar for TP Choi trace3, or by three times it for a normalized Choi state.

The paired physical/code unitary covariance and maximal entanglement of ψ let us simultaneously choose ψ=(|00>+|11>+|22>)/√3 and diagonal C. For faithful C, divide the ENTIRE source by λmax(C), and order one maximal eigenvalue first. Write C=diag(1,c,d),0<c,d≤1. No ordering between c and d is needed.

## 1. Actual shared-clock determinant
For b>0 and original reset clock s>0 define

K_b(s)=(I₃⊗C^1/2)(sI₉+bP_ψ)^−1(I₃⊗C^1/2).

The exact white-shift identity is

Δ(X)=∫_a∞F₃(K_b(s))ds,
F₃(K)=2logdet[I+(W₃⊗id₃)K]−3logdet(I+K/3)−logdet(I+Tr_code K).

Let (c₁,c₂,c₃)=(1,c,d), e₁=Σc_i,e₂=Σ_(i<j)c_ic_j,e₃=c₁c₂c₃. Set

O_ij=6(s+b)(s+c_i)(s+c_j)−b[c_i(s+c_j)+c_j(s+c_i)]
 =6s³+6(b+c_i+c_j)s²+[6c_ic_j+5b(c_i+c_j)]s+4bc_ic_j,
J=81s³+(81b+27e₁)s²+(18be₁+9e₂)s+3be₂+3e₃,
R_i=3(s+b)(s+3c_i)−bc_i=3s²+(3b+9c_i)s+8bc_i.

All these heads are strictly positive. The exact ratio is

exp F₃(K_b(s))=
 3^27 s^9 ∏_i(s+c_i)² ∏_(i<j)O_ij²
 / [64 ∏_i(3s+c_i)^6 J³ ∏_i R_i].                    (1)

Derivation: the three diagonal code/logical basis vectors have zero rank-one WH update; each off-diagonal pair (i,j),(j,i) carries a rank-one2-by-2 update. Its determinant head is O_ij/3. The input rank-one head is sJ/3; the reference is diagonal with heads R_i/3. All factors of3 cancel as in(1). A separate exact actual9-by-9 input/output and3-by-3 reference replay is supplied, not merely a scalar surrogate computation.

## 2. All-domain finite sign certificate
Let N(s) be numerator minus denominator in(1). It has degree31, with

[s³¹]N=711559752519106944(1+c²+d²)>0,
N(0)=−884736b³c⁷d⁷(bcd+bc+bd+cd)³<0.

For0<c,d<1 substitute c=z/(1+z),d=w/(1+w), z,w>0, and multiply every coefficient by the SAME positive factor(1+z)^10(1+w)^10. Call the transformed coefficients H_j(b,z,w).

The exact receiving script proves:
* H₀,…,H₁₂ have strictly negative polynomial coefficients.
* H₂₈,…,H₃₁ have strictly positive polynomial coefficients.
* For each j=13,…,26 it receives explicit polynomials A_j,B_j with nonnegative integer coefficients and positive values for b,z,w>0, such that B_j H_(j+1)−A_j H_j has only NONNEGATIVE coefficients.

The14 multiplier pairs use the8 monomials b^i z^k w^l with i,k,l∈{0,1}, in lexicographic order. Their integer weights are stored separately; the receiver uses no numerical optimizer. Some resulting coefficients are zero, which is harmless: if H_j>0 then H_(j+1)>0. Starting from the negative initial block and ending at the positive final block, the coefficient sequence therefore has exactly one sign variation, ignoring zeros. Descartes' rule and the endpoint signs give exactly one positive root of N and exactly one negative-to-positive crossing of the ACTUAL integrand.

If c=1 or d=1, take coefficientwise limits from the open square. A finite real coefficient sequence with at most one sign variation retains that property under limits (ignore zero entries). The displayed constant and leading coefficients remain strictly signed, so the same one-crossing conclusion holds, rather than merely a non-strict entropy limit.

## 3. Whole mass range from the actual source anchor
At a=0 the received `arbitrary_logical_success_reset_flag_value_theorem.md` applies to the SAME C and maximally entangled flag. Its original source has strictly positive deficit for faithful C,b>0. Near s=0, the rational determinant formula makes the kernel at worst logarithmically singular; at infinity the original logdet cancellation is O(s^−2). Thus this is an ordinary convergent improper integral.

Let s_* be the unique crossing. For0≤a≤s_*, removing the negative initial segment strictly increases or retains the positive anchor. For a>s_*, the entire remaining tail is strictly positive. Consequently every a≥0 is paid for b>0.

When b=0, logical diagonalization makes the source the exact direct sum of c_iP_Ω3+aI₉ seeds. Their received whole pure-main VALUE theorem (or the whole two-level theorem) gives positivity, and strict positivity for a>0 and faithful C. When a=b=0 the reversible main has zero deficit.

Finally singular C follows safely by C_ε=C+εI₃ and finite-dimensional entropy continuity. No strict equality classification is inferred through that singular limit.

A larger logical space is covered if the reset flag is maximally entangled onto a THREE-dimensional C-reducing logical subspace: the remaining modes are an actual direct sum of white-reset pure-main seeds. Schmidt rank three without this reducing-subspace condition does not suffice.

## Certificate files
`nonflat_three_mode_maxent_reset_certificate.py/.json/.txt`, `nonflat_three_mode_maxent_reset_chain_weights.json`, and `nonflat_three_mode_maxent_reset_actual_ratio_check.py/.txt`.
