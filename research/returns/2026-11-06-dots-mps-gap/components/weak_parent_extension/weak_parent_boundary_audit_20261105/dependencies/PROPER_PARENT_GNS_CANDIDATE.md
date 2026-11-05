# Provisional extension: periodic and GNS gaps coincide for proper primitive MPS parents

2026-11-05. Research candidate, not an externally verified theorem or a novelty claim. This document does not modify the previously packaged LTI convergence candidate. Two independent internal audits found no flaw within the stated scope. Their additional positivity checks support the sharper logarithmic-over-linear estimate below. These are internal reviews, not external proof verification.

## 1. Scope and statement

Let a one-dimensional translation-invariant finite-range interaction consist of translates of a nonzero positive operator h, supported on r consecutive sites, with norm M. Assume:

1. A fixed finite-dimensional primitive canonical MPS tensor A has unital transfer E(X)=sum_s A_s X A_s^*, with faithful invariant density sigma for E*.
2. The interaction is frustration free on that MPS. For all sufficiently long open intervals B, ker H_B equals exactly the MPS boundary space S_|B|=ran Gamma_|B|. This is the proper-parent assumption.
3. The open Hamiltonians have a common positive gap g for all sufficiently long intervals; sufficiently large periodic chains have the unique MPS ground state. These are standard proper-parent consequences and are listed explicitly here to avoid weakening the promise silently.

Let Delta_N be the first positive eigenvalue of the N-site periodic Hamiltonian. Let omega be the infinite-chain MPS state and H_omega the nonnegative GNS Hamiltonian implementing the dynamics, with ground vector Omega_omega. Under the assumptions, its ground eigenvalue is simple. Write Delta_GNS=inf(spec H_omega minus {0}).

The proposed conclusion is

    lim_(N->infinity) Delta_N = Delta_GNS,
    Delta_GNS <= Delta_N + O(log N / N).

Constants depend on the fixed model. The proof below establishes existence of the periodic limit independently of the LTI hierarchy. Combined with the existing, separately reviewed nearest-neighbor proper-parent candidate, it would identify that hierarchy's limit with the GNS gap. It proves nothing for general weak parents, merely unique product/injective bulk ground states, higher dimensions, or arbitrary gapped non-frustration-free chains.

This statement is not asserted novel. Standard references already give the easier finite-volume-to-GNS lower-gap implication. Whether this exact equality and elementary quantitative route appear elsewhere remains under examination.

## 2. Two uniform MPS estimates

Use the explicit convention

    Gamma_k |a,b> = sum_(s_1,...,s_k) (A_(s_1)...A_(s_k))_(a,b) |s_1,...,s_k>.

Here G_k=Gamma_k^* Gamma_k tends exponentially to I tensor sigma, not I tensor sigma transpose. Thus, for some 0<theta<1 and C<infinity,

    ||G_k - I tensor sigma|| <= C theta^k.                 (1)

The rate theta is chosen strictly above the modulus of every nontrivial transfer eigenvalue, absorbing any Jordan polynomial. Consequently Gamma_k has a uniformly bounded pseudoinverse once k exceeds a fixed threshold. Moreover, for every k,

    ||Gamma_k||_HS^2 = sum_words ||A_word||_HS^2
                     = tr E^k(I) = D.                    (2)

Let the unnormalized periodic MPS be Omega_N^raw=sum_words tr(A_word)|word>, and let Z_N=||Omega_N^raw||^2. Primitivity implies Z_N=tr(E^N)=1+O(theta^N); hence Z_N stays bounded above and away from zero for large N.

### 2.1 A support-uniform local-state comparison

For a contiguous k-site block C with complementary cyclic buffer of length b=N-k, define F|a,b>=|b,a>. The coefficient matrix of Omega_N^raw across C versus its complement is

    Gamma_k F Gamma_b^T.

Therefore its normalized reduced density matrix is

    rho_(C,N) = Gamma_k F G_b^T F Gamma_k^* / Z_N.          (3)

The infinite MPS marginal is

    rho_(C,infinity) = Gamma_k (sigma^T tensor I) Gamma_k^*. (4)

Indeed F(I tensor sigma)^T F=sigma^T tensor I, and the right-hand side has trace one by transfer invariance. Equations (1)-(4), ||Gamma_k||^2<=D, and fixed virtual dimension D^2 show that

    ||rho_(C,N)-rho_(C,infinity)||_1 <= C_0 theta^(N-k),    (5)

with C_0 independent of both k and N. This independence from the growing support is essential. The bound is a finite-dimensional transfer estimate, not a fixed-support weak-limit assertion.

### 2.2 Bounded local preparation of any vector with a ground-space buffer

Partition the N-ring into core C of length L and buffer B of length ell, both above the injectivity threshold. Write P_B for the orthogonal projection onto S_ell. Every vector phi in H_C tensor S_ell can be written as

    phi = (O_C tensor I_B) Omega_N,                       (6)
    ||O_C|| <= K ||phi||,                                (7)

with K depending only on A, not N,L,ell.

One explicit construction avoids a claim about arbitrary physical Schmidt coefficients. Regard phi as a coefficient matrix Y (core rows, buffer columns). Since its buffer support is S_ell, there is X with

    Y = X Gamma_ell^T,
    X = Y (Gamma_ell^+)^T.

Set

    O_C = sqrt(Z_N) X F Gamma_L^+.

Since Gamma_L^+ Gamma_L=I on the virtual space, multiplying the normalized ground coefficient matrix Gamma_L F Gamma_ell^T/sqrt(Z_N) gives Y exactly. Also

    ||O_C|| <= sqrt(Z_N) ||Y||_HS ||Gamma_ell^+|| ||Gamma_L^+||,

which proves (7) using (1). Set O_C to zero outside the MPS core support as this formula does. No exponentially large local-operator norm is hidden in the transfer comparison.

## 3. Project a periodic excitation onto one quiet buffer

Choose a normalized first excited eigenvector psi_N of H_N that is simultaneously an eigenvector of cyclic translation. This is possible even when Delta_N is degenerate. Every translated h term then has expectation Delta_N/N. Set E=Delta_N.

For large N, E<=rM. To see this, choose a nonzero single-site local excitation of the unique ground state and subtract its ground component. Only the r interaction terms touching that site can act on it, so its Rayleigh quotient is at most rM.

Let B be ell consecutive sites, and let P=P_B tensor I_C. The proper-parent hypothesis and the uniform open gap give

    H_B >= g(I-P_B),
    q := ||(I-P)psi_N||^2 <= (ell-r+1) E/(g N).            (8)

Let phi=P psi_N. Then ||phi||^2=1-q and phi is EXACTLY orthogonal to Omega_N because P Omega_N=Omega_N. Thus its local representation (6) obeys

    omega_N(O_C)=0,
    omega_N(O_C^* O_C)=1-q,
    ||O_C||<=K.                                          (9)

The projection need not commute with H_N, but only the interactions crossing the two buffer/core cuts can cause a positive energy cost. Write

    H_N=H_B+H_C+V, chi=(I-P)psi_N,
    b=2(r-1), B_0=bM, ||V||<=B_0,
    e_V=<psi_N,V psi_N>=bE/N.

For sufficiently long disjoint buffer/core intervals there are exactly b crossing translates; using fewer terms only improves the bounds. All components are positive. Internal buffer terms annihilate P, and H_C commutes with P. Consequently

    <phi,H_N phi> <= E+<phi,V phi>-<psi_N,V psi_N>
       <= E+2 sqrt(e_V <chi,V chi>)+<chi,V chi>
       <= E+2 sqrt((bE/N) B_0 q)+B_0 q.                   (10)

The middle line follows by expanding phi=psi_N-chi and applying Cauchy-Schwarz in the positive V form. Define

    R_(N,ell)=2 sqrt((bE/N) B_0 q)+B_0 q
       <= (E/N)[2 sqrt(b B_0 (ell-r+1)/g)
                    +B_0 (ell-r+1)/g].

Thus R_(N,ell)=O(ell/N), uniformly using E<=rM. This sharper estimate uses positivity and the small seam energy e_V, rather than bounding every seam by its operator norm against the whole vector. It does not need the excited-state eigenvalue equation beyond choosing a translation eigenvector with energy E. The older generic seam bound E+B_0 sqrt(q) is valid but unnecessarily loses a square root.

## 4. Transfer that excitation to the infinite-chain GNS representation

Consider O=O_C on the infinite chain. Its variance obeys (5),(7),(9):

    omega(O^*O) >= 1-q-C_0 K^2 theta^ell,
    |omega(O)| <= C_0 K theta^ell,
    V := omega(O^*O)-|omega(O)|^2
       >= 1-q-C_0 K^2 theta^ell-C_0^2 K^2 theta^(2ell).    (11)

Let J_C be the set of interaction translates meeting C and put

    F_O = sum_(i in J_C) O^* h_i O.

Frustration freeness implies

    omega(F_O) = <pi(O)Omega_omega,H_omega pi(O)Omega_omega>,
    omega_N(F_O) = <phi,H_N phi>.                         (12)

F_O is positive, has norm at most M(L+r-1)K^2, and is supported on C enlarged by r-1 sites at each end. The remaining buffer has length ell-2(r-1), so for ell>2(r-1), (5) and (10) give

    omega(F_O) <= E+R_(N,ell)
                  + C_0 M(L+r-1)K^2 theta^(ell-2(r-1)).  (13)

Center O by subtracting omega(O)I. The energy numerator is unchanged, and its squared GNS norm is V. Once V>0, the GNS Rayleigh principle therefore gives

    Delta_GNS <= [E+R_(N,ell)
                  + C_0 M(L+r-1)K^2 theta^(ell-2(r-1))]
                 /[1-q-C_0 K^2 theta^ell
                       -C_0^2 K^2 theta^(2ell)].          (14)

Taking ell=ceil(c log N), with c>2/|log theta| and above all fixed thresholds, gives q=O(log N/N), transfer error O(N theta^ell)=O(1/N), and

    Delta_GNS <= Delta_N+O(log N/N).                (15)

The argument for r=1 is also harmless: B_0=0, and all interactions are onsite.

## 5. The other inequality and existence of the limit

For any fixed local O with positive omega-variance, use (O-omega_N(O))Omega_N as a periodic variational excitation. Transfer convergence gives

    limsup_N Delta_N
      <= omega(O^* [H,O]) /
         [omega(O^*O)-|omega(O)|^2].                      (16)

For bounded finite-range interactions, local vectors pi(O)Omega_omega are a form core of the GNS Hamiltonian. One direct justification is that H_omega^k pi(O)Omega_omega=pi(delta^k(O))Omega_omega. At each commutator the support grows by at most 2(r-1), and the norm is bounded by 2M times the number of overlapping translates. Iterating bounds ||delta^k(O)|| by a fixed exponential in k times k! and a fixed polynomial in k. Thus every local vector is analytic for H_omega for a positive time radius. The invariant dense local domain is an essential-self-adjointness core by the analytic-vector theorem, hence also a form core. Thus the infimum of these local Rayleigh quotients is Delta_GNS. This is the standard GNS variational characterization; it is not a new assumption that all excitations are exactly local. Taking the infimum in (16), and combining with (15), gives

    limsup_N Delta_N <= Delta_GNS <= liminf_N Delta_N.

The periodic limit exists and equals Delta_GNS.

Simplicity of the GNS ground eigenvalue can also be obtained without an additional assumption: the standard uniform proper-parent periodic gap delta>0 and convergence of ground-state local expectations imply the local Poincare inequality omega(O^*[H,O])>=delta Var_omega(O). Extension from the local form core gives H_omega>=delta(I-|Omega_omega><Omega_omega|). The proof does not identify a possibly degenerate GNS gap by an incorrect variance denominator.

## 6. Consequences and limitations

- If the earlier proper-parent LTI convergence proof is accepted, its nearest-neighbor hierarchy converges to the physical GNS gap, not merely a separately defined periodic limit.
- Known convergent local GNS variational upper bounds can then be paired with the lower hierarchy to give arbitrarily tight two-sided bounds on this promised class. For exactly specified rational/algebraic interaction and tensor data, finite real-algebraic SDP feasibility and MPS contraction make this an eventual-termination algorithm at any requested rational tolerance. No decision algorithm for whether the proper-parent promise holds is claimed. This is a conditional computability consequence, not a polynomial-time algorithm, numerical implementation of exact certification, or new variational principle.
- Actual certification for numerical input still requires validated interval/algebraic arithmetic and feasible lower certificates. Floating-point eigenvalues or approximate SDPs do not alone constitute certified bounds.
- The proof uses exact eventual open ground-space equality twice: the buffer projection must both have small failure probability and force the finite-rank MPS buffer support. A unique infinite injective MPS ground state alone does not supply either implication.
- No strong practical improvement follows from the O(log N/N) rate; model-dependent constants and exponential Hilbert-space costs can be large.
- Existing MPS excitation methods can yield much sharper practical upper estimates. No benchmark superiority is claimed.

## 7. Citations and priority clarification (append-only packaging update)

This section adds source attribution and access limitations to the previously reviewed mathematical text; Sections 1-6 above are unchanged. The additional [literature-priority audit](LITERATURE_PRIORITY_AUDIT.md) is a targeted source review, not a third proof verification.

- The standard direction in Section 5, limsup Delta_N <= Delta_GNS, is explicitly supported by Nachtergaele, Sims and Young, *Quasi-Locality Bounds for Quantum Lattice Systems. Part II*, Theorem 7.4, equations (7.26)-(7.29), with the local-vector core discussed in Section 7.2. Primary version inspected by the priority auditor: [arXiv:2010.15337v3](https://arxiv.org/html/2010.15337v3); published DOI [10.1007/s00023-021-01086-5](https://doi.org/10.1007/s00023-021-01086-5). For the present rank-one periodic ground projection, the theorem's local-indistinguishability condition reduces to convergence of ground-state local expectations. Its conclusion is one-sided; it does not establish the reverse estimate or exact periodic-gap convergence.
- Bachmann, Dybalski and Naaijkens, [arXiv:1412.2970v2](https://arxiv.org/html/1412.2970v2), Proposition 5.4, gives finite-volume-to-GNS spectral exclusion. It likewise does not recover arbitrary finite-periodic excitations in the selected GNS sector.
- The MPS estimates of Section 2 have standard antecedents in Nachtergaele-Sims-Young Appendix B, especially equations (B.14)-(B.15), which attribute their Gram estimate to Fannes-Nachtergaele-Werner Lemma 5.2. **Access caveat:** the original FNW 1992 full article was not successfully inspected in the priority pass: Springer supplied a preview, and Project Euclid presented a security check. Its abstract and bibliography were accessible, and the Gram estimate was checked through its later reproduction. No claim is made that FNW contains no equivalent periodic/GNS result. Original DOI: [10.1007/BF02099178](https://doi.org/10.1007/BF02099178).
- Standard positive-gap results include Nachtergaele, [cond-mat/9410110](https://arxiv.org/html/cond-mat/9410110), Proposition 12 and equation (6.10), and Szehr-Wolf, [arXiv:1402.4175v2](https://arxiv.org/html/1402.4175v2), Theorem 2 and Corollary 3. The inspected statements prove uniform positivity or stability, not the exact equality proposed here.
- Local embedding and optimized excitation upper methods are already established: Haegeman et al., [arXiv:1305.2176v2](https://arxiv.org/html/1305.2176v2), Theorem 1 and its MPS discussion; Haegeman-Osborne-Verstraete, [arXiv:1305.1894](https://arxiv.org/abs/1305.1894), Section VII A and Table I. Their stronger practical AKLT estimates are acknowledged in the README and first audit. The selected-excitation localization theorem uses uniform momentum-sector isolation and local spectral weight, neither assumed in the present proof.
- Rozman, Molnar and Schuch, [arXiv:2607.19078v1](https://arxiv.org/html/2607.19078v1), Section 3.2, Theorem 6 and Section 4.4, supports the proper-parent distinction and uniform gaps. Its displayed asymptotic lower-bound convergence is to limsup open-chain gaps, which is not the exact periodic/GNS gap in general.

Defensible priority statement: We give a direct candidate proof under the stated assumptions. The easy direction is standard and explicitly cited. No matching full equality theorem was located in the targeted review, but priority for the reverse inequality and quantitative bound remains unresolved, particularly given the incomplete access to the original FNW article.
