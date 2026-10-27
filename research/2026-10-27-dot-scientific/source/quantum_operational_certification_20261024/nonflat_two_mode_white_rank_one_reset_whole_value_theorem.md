# Whole VALUE: arbitrary two-mode logical spectrum with white plus rank-one reset

Status: analytic proof with exact finite sign-propagation certificate; awaiting independent receipt.

## Actual family and exact scope
Let C≥0 be a2×2 logical matrix, ψ any unit vector in the covered reference C³⊗C², and

Y=aI₆+b|ψ><ψ|,   a,b≥0,
X=P_Ω3⊗C+I₃⊗Y.

Then Δ(X)≥0. If C>0, the inequality is strict exactly when Y≠0. The main success is reversible with arbitrary TWO logical eigenweights; its isometric modes share the same qutrit code. This is not a theorem for two arbitrary unrelated Kraus operators. Negative rank-one holes for nonflat C are NOT included.

The physical marginal is(TrC+TrY)I₃, so division by this scalar gives the unnormalized TP Choi operator (trace3), and division by three times it gives the normalized Choi state.

For C>0, diagonalize C by a logical unitary and divide the ENTIRE source by its largest logical eigenvalue. It suffices to take C=diag(1,c),0<c≤1. The flat case c=1 is already received. Singular C has a pure main or zero main and is paid separately by the received arbitrary-reference pure-main theorem; no faithful spectral bound is silently extended through c=0.

## 1. Preserve the actual flag geometry
In the eigenbasis of C write ψ's two physical columns as v₁,v₂∈C³. Put

p=||v₁||², q=1−p=||v₂||²,
δ=pq−|v₁*v₂|²,

so0≤p≤1 and0≤δ≤p(1−p). Complex overlap phases are retained through their exact modulus; no logical pinching is performed. These invariants determine all needed rank-one update determinants, because C is already diagonal and physical unitary covariance is available.

For b>0 define the SAME original source clock

K_b(s)=(I₃⊗C^(1/2))(sI₆+bP_ψ)^-1(I₃⊗C^(1/2)), s>0.

The white reset shift gives exactly

Δ(a,b;C,ψ)=∫_a∞ F₂(K_b(s))ds,
F₂(K)=2logdet[I+(W₃⊗id₂)K]−3logdet(I+K/3)−logdet(I+Tr_codeK). (1)

We receive a single negative-to-positive crossing of this actual integrand for all0<c<1,b>0 and all admissible p,δ.

## 2. Explicit original determinant ratio
Let w=s+b and
q_c=p+(1−p)c, r_c=1−p+pc,
D=(s+1)(s+c), D_i=(3s+1)(3s+c),
A=2wD−b(q_c s+c),
B=4w²D−2bw(q_c s+c)+b²cδ,
J=9s²+(9b+3+3c)s+c+3br_c,
R=w²(s+3)(s+3c)−bw[p(s+3c)+(1−p)c(s+3)]+b²cδ.

The actual ratio is

exp F₂(K_b(s))
 =3^18 s^5 D²A²B² / [64w D_i^6 J³ R].            (2)

Every denominator factor is positive in the stated domain. In particular R/(s²w²) is det(I+Tr_codeK_b), and J is the positive rank-one input determinant head after cancellation of its single s factor.

For independent reconstruction: write x=1/s, β=−b/[s(s+b)] and
h₁(k)=1/(1+kx), h₂(k)=c/(1+kxc),
t_k=p h₁(k)+(1−p)h₂(k), d_k=δ h₁(k)h₂(k).
The output update factor is(1+βt₁/2)(1+βt₁/2+β²d₁/4), the input update is1+βt_(1/3)/3, and the reference update is1+βt₃+β²d₃. Multiplying their baseline determinants gives(2). The exact certificate checks this symbolic identity. A separate actual complex6×6 clock/output and2×2 marginal replay also matches it, without using a scalar surrogate source.

Let N(s)=numerator−denominator in(2). It has degree21, with

c21=49589822592(1+c²)>0,
c0=−64b³c⁷(δ+6)(c+3br_c)³<0.                    (3)

## 3. Exact all-domain coefficient receiving
Write N(s)=Σc_j s^j. The coefficient-domain transformation is

c=z/(1+z), z>0,
p=P/(P+Q), P,Q≥0, P+Q>0,
δ=PQ H₁/[(P+Q)²(H₀+H₁)], H₀,H₁≥0, H₀+H₁>0.

This covers every required flag Gram matrix, including p=0,1 and both determinant boundaries. Homogenize each coefficient by the COMMON positive factor

(P+Q)^6(H₀+H₁)²(1+z)^10.

Call the resulting polynomial H_j. Its nonzero coefficients are negative for0≤j≤5 and positive for18≤j≤21. For every j=6,...,16 the supplied exact integer weight vector determines polynomials A_j(b,z),B_j(b,z), each using monomials(1,b,z,bz), with nonnegative coefficients and at least one positive coefficient. Thus both are strictly positive for b,z>0. The receiver proves

B_j H_(j+1)−A_j H_j has ONLY NONNEGATIVE coefficients. (4)

The complete integer vectors are in `nonflat_two_mode_white_rank_one_reset_chain_weights.json`; the eight entries list the four A_j coefficients followed by the four B_j coefficients. Their size is immaterial to the proof: `nonflat_two_mode_white_rank_one_reset_certificate.py` uses only exact integer/rational arithmetic, reconstructs N from(2), expands the stated homogeneous substitution, and verifies every coefficient of all eleven inequalities. The adjacent JSON/text reports receive the positive/zero counts and hashes. No optimizer or floating-point decision appears in the receiving script.

Since both multipliers are positive in the faithful nonflat interior, H_j>0 forces H_(j+1)>0; H_j=0 forces H_(j+1)≥0. Consequently the descending nonzero coefficient sequence has at most one sign variation. Equation(3) ensures it has exactly one. Descartes' rule gives a unique simple positive root s_*, and therefore

F₂(K_b(s))<0 for0<s<s_*,
F₂(K_b(s))>0 for s>s_*.

This is a full-source common-pencil sign theorem. It is not an assumed monotonicity in C, a coherence endpoint argument, or a sampled root count.

## 4. A paid a=0 anchor receives all white shifts
At a=0,b>0, the source is exactly the received arbitrary-logical-success plus rank-one reset-flag family in `arbitrary_logical_success_reset_flag_value_theorem.md`. Its normalized channel has success weight(1+c)/(1+c+b), reset weight b/(1+c+b), and ancillary state C/(1+c). Since C is faithful and ψ lies in the covered reference, the flag overlaps the actual success support, so this anchor has strictly positive deficit.

If0<a≤s_*, equation(1) removes a strictly negative initial segment from the paid anchor. If a≥s_*, it is a strictly positive tail integral. Thus all a≥0,b>0 are strictly paid. The integrand has only integrable logarithmic behavior at zero and O(s^-2) decay at infinity, by the finite-source entropy identity.

For b=0, diagonalize C: the source is the exact orthogonal logical direct sum of two pure maximally entangled mains with qutrit white reset. These are already paid, strictly if a>0. At a=b=0 both pure flags have zero deficit. This establishes the claimed equality statement for C>0.

The c=1 boundary is the received flat logical theorem. For singular C use the already-received pure-main arbitrary-reference theorem, including all outside reset support; additional zero cases are possible, so the faithful equality classification is not asserted there.

## Allowed larger-logical-space corollary and guard
The result extends by actual direct-sum additivity if ψ is supported in a C-REDUCING logical subspace of dimension at most2, with arbitrary additional logical eigenmodes outside it. The outside modes see only the white reset and are individually paid. Merely having Schmidt rank≤2 does NOT imply this reducing-subspace condition when C is nonflat. No compression to a nonreducing logical span is licensed.

Arbitrary nonflat logical rank≥3, negative coherent holes for nonflat C, arbitrary higher-rank reset perturbations, general mixed-main spectra, and unrestricted WH₃ positivity remain open.
