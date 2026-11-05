# Independent audit: periodic versus GNS gap

Date: 2026-11-05. Scope: independent literature screen and proof audit only. No existing proof files were inspected or changed.

## Finding

Under the hypotheses below, the buffer-projection argument gives

\[
\lim_{N\to\infty}\operatorname{gap}(H_N^{\mathrm{per}})
=\operatorname{gap}(H_\omega).
\]

In particular, the argument proves existence of the periodic limit; it does not require existence of that limit as an input. I found no counterexample within this class. The primary sources screened establish the usual one-sided comparison and supply the required MPS estimates, but I did not find an explicit published theorem asserting this exact equality. This is not a novelty or exhaustive-literature claim.

## Hypotheses that must remain explicit

* Finite on-site dimension and finite interaction range r; a translation-invariant positive interaction, written H_N^per = sum_x h_x, with h_x >= 0 and ||h_x|| <= J. A finite collection of interaction shapes can be grouped into h_x.
* One primitive finite-bond-dimension MPS tensor, in a minimal canonical representation with faithful stationary density rho.
* For all sufficiently long open intervals B, ker H_B = G_B = ran Gamma_B. This is the substantive proper-parent assumption, not merely that the MPS is annihilated by every term.
* A uniform positive open-chain gap g on these sufficiently long intervals.
* For sufficiently large rings, the normalized periodic MPS Omega_N is the unique zero-energy ground vector. The infinite MPS omega is the unique ground state, and its GNS kernel is C Omega.

The customary proper primitive MPS parent results provide the final three properties in the intended setting. Positivity/frustration-freeness must not be silently weakened to a telescoping or merely eigenstate-parent construction.

## The two uniform MPS facts

Choose the convention E(X) = sum_i v_i^* X v_i, E(1)=1, E^t(rho)=rho, tr(rho)=1. Primitivity gives ||E^n-E_infinity|| <= c theta^n for some theta<1, with E_infinity(X)=tr(rho X)1. If there are Jordan blocks, enlarge theta above the nontrivial spectral radius; no diagonalizability is required.

### 1. Uniform Schmidt lower bound, hence uniformly bounded local realization

The open MPS map is Gamma_m(B)=sum_i tr(B v_i1...v_im)|i1...im>. Its Gram matrix converges to the strictly positive form tr(rho B^* C). Thus for all m>=m0 there are constants a,b>0 independent of m such that

\[
a\|B\|_{\rm HS}\leq\|\Gamma_m(B)\|\leq b\|B\|_{\rm HS}.
\]

For a ring partition C|B, with both parts at least m0, its unnormalized MPS is (Gamma_C tensor Gamma_B) applied to the fixed virtual maximally entangled vector of rank D^2, up to a fixed transpose/swap convention. Consequently all its D^2 nonzero Schmidt coefficients, after normalization, are bounded below by a model-dependent s_*>0 independent of both lengths. Its Schmidt support on B is exactly G_B.

If phi belongs to H_C tensor G_B, write Omega_N=sum_a s_a u_a tensor w_a and phi=sum_a phi_a tensor w_a. Set O_C u_a=phi_a/s_a and set O_C=0 on the orthogonal complement of span{u_a}. Then

\[
\phi=O_C\Omega_N,\qquad
\|O_C\|\leq\|O_C\|_{\rm HS}
\leq s_*^{-1}\|\phi\|.
\]

This resolves the possible exponential-in-|C| operator-norm objection. The norm is uniform because the Schmidt rank and the positive lower Schmidt bound are both uniform.

### 2. Ring/infinite local-state comparison uniform in the observed length

For an observable A on an m-site contiguous interval of the N-ring,

\[
\omega_N(A)=
\frac{\operatorname{Tr}_{\rm super}(E_A E^{N-m})}
{\operatorname{Tr}_{\rm super}(E^N)},\qquad
\omega(A)=\operatorname{Tr}_{\rm super}(E_A E_\infty).
\]

Canonical normalization writes E_A(X)=V_m^*(A tensor X)V_m with V_m an isometry. Hence ||E_A||<=||A|| in induced operator norm, independently of m. In the fixed D^2-dimensional transfer space, superoperator trace is bounded by a dimension-dependent constant times this norm. Since Tr_super(E^N)=1+O(theta^N), one gets

\[
|\omega_N(A)-\omega(A)|\leq K\theta^{N-m}\|A\|,
\]

uniformly in m and N once the denominator is bounded away from zero. Equivalently, the corresponding reduced density matrices differ in trace norm by at most K theta^(N-m). This stronger, uniform-in-support-size statement is needed; convergence only for each fixed observable would not suffice.

## Reverse comparison: GNS gap <= liminf periodic gap

Let E_N=gap(H_N^per), and choose a normalized first excited vector psi_N that is also a translation eigenvector. This is possible since translation commutes with H_N^per. Let B be a contiguous buffer of length ell, C its complement, P=1_C tensor P_B, Q=1-P, and phi=P psi_N. Translation symmetry yields

\[
q:=\|Q\psi_N\|^2
\leq g^{-1}\langle\psi_N,H_B\psi_N\rangle
\leq\frac{\ell E_N}{gN}.
\]

Moreover phi is exactly orthogonal to Omega_N because P Omega_N=Omega_N.

Write H_N=H_B+H_C+V, where V consists of terms crossing either seam. Its norm is bounded by M=2(r-1)J (or a harmless model-dependent constant for a more general interaction). We have P H_B Q=P H_C Q=0. Using H_N psi_N=E_N psi_N therefore gives

\[
\langle\phi,H_N\phi\rangle
=E_N(1-q)-\langle\phi,VQ\psi_N\rangle
\leq E_N(1-q)+M\sqrt q.
\]

Only the seam norm enters: estimating with ||H_N|| here would lose the argument.

By MPS fact 1, phi=O_C Omega_N with ||O_C||<=s_*^{-1}. By fact 2,

\[
\omega(O_C^*O_C)=1-q+O(\theta^\ell),\qquad
\omega(O_C)=O(\theta^\ell).
\]

For energy, sum only terms whose supports meet C. All other terms annihilate O_C Omega both on the ring and in the infinite system, by positivity and frustration-freeness. The remaining energy observable sum_x O_C^* h_x O_C has norm O(N), and is supported on C together with at most r-1 buffer sites on each end. Thus

\[
\omega\bigl(O_C^*\delta(O_C)\bigr)
\leq E_N(1-q)+M\sqrt q
+K'N\theta^{\ell-2(r-1)}.
\]

Here delta(A)=[H,A] is the energy derivation; insert the conventional factor -i if the generator is instead defined as i[H,A]. Apply the GNS variational inequality to O_C-omega(O_C)1. Subtracting the scalar changes neither the energy nor its local support. This gives

\[
\Delta_\omega\leq
\frac{E_N(1-q)+M\sqrt q+K'N\theta^{\ell-2(r-1)}}
{1-q+O(\theta^\ell)-O(\theta^{2\ell})}.
\]

The E_N are uniformly bounded above: a fixed nontrivial local excitation of omega has nonzero variance and bounded local commutator energy, and the same trial operator works on large rings. Choose ell=ceil(a log N) with a>2/|log theta|. Then q=O(log N/N), the transfer error tends to zero, and

\[
\Delta_\omega\leq E_N+O\!\left(\sqrt{\frac{\log N}{N}}\right).
\]

The error here is one-sided and model dependent. It does not establish a matching two-sided convergence rate.

## Standard forward comparison

For each fixed local A with omega(A)=0 and omega(A^*A)>0, the centered ring trial vector (A-omega_N(A))Omega_N has Rayleigh quotient converging to omega(A^*delta(A))/omega(A^*A). Local vectors are a form core for the GNS Hamiltonian. Taking an infimum over such A gives

\[
\limsup_N E_N\leq\Delta_\omega.
\]

Together with the reverse comparison this proves equality and existence of the limit.

## Primary-source screen and exact anchors

1. S. Bachmann, W. Dybalski, P. Naaijkens, *Lieb–Robinson bounds, Arveson spectrum and Haag–Ruelle scattering theory for gapped quantum spin systems*, Ann. Henri Poincare 17 (2016), 1737–1791. Proposition 5.4, preprint p. 27, is a one-sided finite-volume spectral exclusion result. It does not assert equality of the first gaps. https://arxiv.org/abs/1412.2970 ; https://arxiv.org/pdf/1412.2970

2. B. Nachtergaele, R. Sims, A. Young, *Quasi-Locality Bounds for Quantum Lattice Systems. Part II. Perturbations of Frustration-Free Spin Models with Gapped Ground States*, Ann. Henri Poincare 23 (2022), 393–511. Theorem 7.4 and (7.29) give the GNS lower bound from limsup finite gaps. Appendix B, especially (B.1)–(B.2), (B.14)–(B.15), supplies canonical transfer mixing and uniform MPS-map conditioning. https://arxiv.org/abs/2010.15337 ; https://doi.org/10.1007/s00023-021-01086-5

3. M. Fannes, B. Nachtergaele, R. F. Werner, *Finitely correlated states on quantum spin chains*, Commun. Math. Phys. 144 (1992), 443–490. Original parent-gap and transfer estimates; NSY explicitly attributes its Gram estimate to FNW Lemma 5.2. The primary DOI abstract was checked, while the detailed lemma was checked through its reproduction in NSY. https://doi.org/10.1007/BF02099178

4. C. Fernandez-Gonzalez, N. Schuch, M. M. Wolf, J. I. Cirac, D. Perez-Garcia, *Frustration free gapless Hamiltonians for Matrix Product States*, Commun. Math. Phys. 333 (2015), 299–333, arXiv:1210.6613. Relevant warning, not a counterexample here: its injective-state uncle construction has different finite-dimensional ground spaces and is outside the proper, uniformly open-gapped hypothesis. https://arxiv.org/abs/1210.6613

## Audit verdict

The proposed identification is supported by a short direct proof, rather than by treating an existing one-sided theorem as an equality. The delicate points are exactly the uniform Schmidt lower bound and the state comparison uniform in a growing observed interval; both follow from the primitive finite-dimensional transfer operator. No assumed quasiparticle completeness or absence of nonlocal sectors is needed. The buffer projection itself rules out unseen low-energy periodic sectors.

## Priority distinction: established excitation methods

**Haegeman et al., Phys. Rev. Lett. 111, 080401 (2013), arXiv:1305.2176.** Theorem 1 assumes local Lieb–Robinson dynamics, a uniformly gapped ground state, uniform isolation of the selected nondegenerate momentum-sector energy, and volume-uniform nonzero local spectral weight. Its exponential approximation concerns that selected excitation. Page 4 also explicitly reduces local-operator minimization, by MPS injectivity, to an interval with two additional boundary sites and terms. Thus a local embedding or finite-boundary variational capability is already prior, not a new capability here. Primary: https://arxiv.org/pdf/1305.2176 ; https://doi.org/10.1103/PhysRevLett.111.080401

**Haegeman, Osborne, Verstraete, Phys. Rev. B 88, 075133 (2013).** Section VII A, Eq. (96), optimizes a full K-site replacement tensor and momentum superposition. Table I, p. 075133-28, reports AKLT p=pi upper variational energies: K=1, 10/27; K=2, 0.350634581086138; K=12, 0.350124157337687. These printed numerical values are not certified rounding intervals. Primary: https://doi.org/10.1103/PhysRevB.88.075133 ; https://arxiv.org/abs/1305.1894

Neither stated result directly establishes general periodic/GNS gap equality without the isolation/overlap hypotheses. The buffer argument instead excludes unseen low-energy periodic sectors without those hypotheses. That distinction is not a novelty claim. The reported current AKLT test quotient 0.432 does not improve even the older single-mode value 10/27, much less the optimized block results; it supports a construction check, not practical superiority or a new variational method.
