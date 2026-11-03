# Graded canonical purification: verified phase convention and strict-range entry

2026-11-03. Complements ROOT_CANONICAL_DOUBLE_PARENT.md. The Gaussian phase convention is checked constructively below. The final bounded-range stability transfer is NOT yet proved by this note.

## 1. Combined-fast-state convention

Order all first-copy physical fermion modes before all second-copy modes. The onsite Gaussian Bell state is

 |B> = product_j (1+a_j^dagger b_j^dagger)|0>/sqrt(2^n)
     = 2^(-n/2) sum_x (-1)^[N(x)(N(x)−1)/2] |x>_a |x>_b.

For an even-parity Gaussian fast state psi (the COMBINED free+decoration state), its canonical graded Choi vector is

 |C(psi)> = psi tensor exp(i pi N_b/2) psi^*.

The identity uses (-1)^[N(N−1)/2]=i^N for even N. The opposite sign in the onsite phase agrees on even N. Crucially, free and decoration subfactors can BOTH change parity while the combined fast state stays even. Purifying each separately and throwing away its parity-dependent phase can insert a rotor-dependent minus sign. Purify the combined covariance, or retain these phases explicitly.

The second physical axial generator must be conjugated by the same onsite phase: Q_A,2=F Q_A,1^* F^dagger with F=exp(i pi N_2/2), plus the free onsite real-structure identification where used. This is NOT −Q_A^*: the scalar self-linking term retains its sign. The free copies retain their same chiral Wilson root; vector charges are exchanged between the ±1 flavors by the onsite real-structure identification. The mixed response A_A(dA_V)^2 is not negated by that V exchange. Decoration's parity identity is preserved and its 2pi bosonic pump has unchanged S. No unearned claim about all possible lattice SPT invariants is needed to verify the explicit doubled symmetry action.

## 2. Explicit Majorana Gaussian rotation

Define the pure fast covariance Gamma_jk=(i/2)<[gamma_j,gamma_k]>, so Gamma is real skew and Gamma²=−I. Let C=direct_sum_j(−X) on the second-copy Majorana coordinates. In transformed second-copy coordinates b'=C^T b, the Bell covariance is

 Gamma_B=[[0,I],[-I,0]],

and the desired covariance is diag(Gamma,−Gamma). Define

 K=[[0,Gamma],[Gamma,0]], K²=−I,
 O=exp(−pi K/4)=(I−K)/sqrt(2).

Then O Gamma_B O^T=diag(Gamma,−Gamma). Transform back by diag(I,C). If A is the resulting real skew logarithm, the physical Gaussian lift is exp[(1/4) gamma_total^T A gamma_total]. It produces the exact canonical Choi phase, not merely the covariance: its overlap with Bell is positive 2^(-n/2), matching normalized (|psi><psi| tensor1)|B>. This positive overlap fixes the ray phase.

`check_graded_purification.py` verifies this in full Fock space for n=2,4, including vacuum, the |11> state representing simultaneous free/decoration parity flips, and generic even Bogoliubov states. Maximum vector error is5.6e-16. Bell overlaps are positive .5 and .25 respectively. `graded_purification_results.json` retains all results. Root independently matched the same convention on15 additional states.

For the actual gapped two-massed-face family, Gamma has spatial/configuration-space quasilocality from the one-body projector resolvent bounds. The finite-time controlled rotation therefore has an acquired quasilocal generator; no many-body ground-state-projector oracle is used. The discontinuous rotor-parameter dependence requires bounded reset kernels, not bare rotor derivatives.

## 3. Product-frame relative bounds after axial averaging

Let U be the acquired controlled purification, H0=sum_i n_i the reference product/Bell parent, and Omega its product vacuum. Its physical prepared ground is exactly axial invariant after the static charge cancellation. Set

 V_t=U^dagger exp(it Q_A) U,
 A_i(t)=V_t n_i V_t^dagger.

Every A_i(t) is positive and annihilates Omega. In the product frame, the actual axial generator is a bounded-interaction quasilocal generator, so for bounded t the quasi-local norm of A_i(t)−n_i is O(|t|). The product-state conditional expectation E_B^Omega onto a ball preserves positivity, norm bounds and annihilation of the local product vacuum. Shell differences therefore annihilate the ball vacuum and obey the elementary relative estimate

 |<psi|O_B|psi>| <= ||O_B|| <psi|(1−P_Omega,B)|psi>
                    <=||O_B|| sum_{x in B}<psi|n_x|psi>.

Summing the exponentially decaying shells gives, for EVERY subset of centers I,

 |sum_{i in I}(A_i(t)−n_i)| <= C1 |t| N,
 sum_{i in I} A_i(t) <= C2 N,
 N=sum_x n_x,

as quadratic-form inequalities, uniformly in volume. Averaging t over a small window around0 inside the axial Haar integral gives

 sum_{i in I} bar A_i >= w N_I−e N,

with w=t0/pi and e=O(C1 t0²). This is a useful local-excitation bound, stronger than only a global spectral gap.

Finite-range product-conditioned truncations a_i,R=E_B_R^Omega(bar A_i) remain positive and exactly product-vacuum-annihilating. Their subset inequalities have e replaced by e+delta_R, where delta_R is the weighted shell tail.

## 4. A precise finite-range relative-form reference

For a FIXED range R, let m=|B_R|, let C bound the subset upper estimate, and c0=2C. Choose classical local terms

 h_i=(c0/m) sum_{x in B_R(i)}n_x,
 H_classical=c0 N.

Write phi_i=a_i,R−h_i. For any subset I, the upper form bound is H_classical/2. For the lower bound, a site outside I is covered by at most m−1 classical blocks centered in I, whereas a site in I receives the positive w N_I contribution. Hence

 sum_I phi_i >= −[1−min(w/c0,1/m)+(e+delta_R)/c0] H_classical.

If e+delta_R<½min(w,c0/m), this gives alpha<1 in the subset relative bound. Such a finite R/window pair exists: choose t0 of order1/m, so e=O(1/m²) and the exponential tail eventually lies below O(1/m).

This matches the STRUCTURE of Yarotsky, arXiv:math-ph/0412040, Theorem2 and its weaker subset assumption(6). The paper explicitly allows infinite-dimensional local Hilbert spaces (lines31 onward of https://arxiv.org/html/math-ph/0412040). It assumes translation-invariant finite-range interactions; a periodic blocked implementation and an even-fermion graded-local adaptation must be checked rather than silently imported. The allowed weak bounded perturbation is beta=delta(kappa,dimension,range)(1−alpha)^[kappa(dimension+1)].

## 5. Critical remaining cutoff/threshold issue

The preceding result is NOT yet the strict-range approximation theorem for the physical canonical parent. A finite-depth approximation U_T to U and physical axial averaging can produce an exactly symmetric bounded-range candidate. But after conjugating it back, comparison to the fixed finite-range reference still includes the irreducible tail bar A−a_R. Merely saying “take R large” is invalid: the allowed beta(R,alpha_R) also depends on R and may shrink faster than the tail. No verified inequality crossing those scales was established here.

A sufficient repair would be a weighted-decay extension of the relative-form stability theorem with fixed constants, or a proof that the quasilocal tail can remain in the purely-relative reference without degrading the bounded-perturbation threshold. Neither may be replaced by generic gap stability for all gapped Hamiltonians. The positive subset coercivity and exact product-frame annihilation above are intended inputs for that missing proof, not its conclusion.

Thus the current completed claims are: the exact graded Gaussian preparation/phase convention; the product-frame subset form bounds; and a finite-range relative-form reference at fixed range. The quasilocal canonical doubled parent has the separately proved common-ground/gap property, but this note does not promote it to the requested bounded-range chiral Hamiltonian.
