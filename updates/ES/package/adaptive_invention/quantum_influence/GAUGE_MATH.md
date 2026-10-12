# Constructive mutation: acquire a density-phase gauge from the Hamiltonian

Date: 2026-10-13. This is a restricted exact operation, not a solution for all interacting Hamiltonians. It does not take a conjugating circuit, a compressed state, a low-rank influence tensor or quantum measurements as input. Its recognizer acquires the conjugacy from constant-size local Hamiltonian entries.

Gauge-solvable correlated hopping is established: [Schulz–Shastry (1997)](https://arxiv.org/abs/cond-mat/9707135) removes position-dependent gauge interactions by a unitary transformation, and [Osterloh–Amico–Eckern (2000)](https://arxiv.org/abs/cond-mat/0003099) characterizes generalized correlated gauge hopping. The family and the general transformation principle below are therefore not claimed as new. The retained contribution is a complete explicit recognition-to-product-boundary-to-local-readout derivation, including zeros, phase aliases, rejection and error accounting.

## 1. Recognizable input class

Use an open N-site qubit chain. Let \(n_j=(I-Z_j)/2\), \(T_j=\sigma_j^+\sigma_{j+1}^-\), with \(\sigma^+=(X+iY)/2\). A right-moving occupation changes \(|10\rangle\) to \(|01\rangle\) through T_j. Input local terms specify

\[
H=\sum_j\bigl[\tau_j(Z_{j-1},Z_{j+2})T_j+
\overline{\tau_j}(Z_{j-1},Z_{j+2})T_j^\dagger\bigr]
+\sum_j\mu_j n_j, \tag{C1}
\]

where absent boundary variables are ignored, each \(\mu_j\) is real, and each hopping table \(\tau_j(z_L,z_R)\) has only four entries. One can read these tables from constant-size local matrices or a constant-size Pauli expansion. The scope requires that no other local matrix entries/terms are present. Matching the hopping entries while silently ignoring additional terms would be invalid.

The class is accepted exactly when there exist unit complex numbers \(u_l\) and complex hoppings \(a_j\), including zeros, for which

\[
\tau_j(z_L,z_R)=a_j u_{j-1}^{z_L}u_{j+1}^{-z_R},
\qquad u_0=u_N=1. \tag{C2}
\]

Indices here are one-based for spins and bonds; the outside u values denote absent gauge bonds. Equivalently, write \(u_l=e^{2i\theta_l}\) and

\[
W=\exp\left(i\sum_{l=1}^{N-1}\theta_l Z_lZ_{l+1}\right),
\qquad H=W H_0W^\dagger,
\]

\[
H_0=\sum_j(a_jT_j+\bar a_jT_j^\dagger)+\sum_j\mu_jn_j. \tag{C3}
\]

Indeed, the central \(Z_jZ_{j+1}\) commutes with T_j. Its two external neighbors contribute phases \(e^{2i\theta_{j-1}Z_{j-1}}\) and \(e^{-2i\theta_{j+1}Z_{j+2}}\). This proves (C2)-(C3). Generic angles produce density-dependent hopping with three- and four-site spin terms and nonquadratic terms in the ordinary fermionic variables. The class is nevertheless unitarily equivalent to a quadratic chain, which is a substantive restriction.

## 2. Acquisition, zero bonds and aliases

For a nonzero table, first require all four entries to have equal nonzero magnitude. Ratios yield

\[
u_{j-1}^2=\frac{\tau_j(+,+)}{\tau_j(-,+)},
\qquad
u_{j+1}^2=\frac{\tau_j(+,-)}{\tau_j(+,+)}. \tag{C4}
\]

Collect all proposals for each \(u_l^2\) from neighboring nonzero hoppings. Require unit modulus and consistency. Choose either square root for each constrained \(u_l\). For a gauge bond with no proposal, set \(u_l=1\). Recover

\[
a_j=\tau_j(+,+)u_{j+1}/u_{j-1}, \tag{C5}
\]

and verify all four entries of every table using (C2). This last check catches local phase products that the two sampled ratios alone miss. The recognition uses O(N) arithmetic on local data.

The cases do not require a nonzero-bond or small-angle promise:

- A table with all entries zero means \(a_j=0\). It imposes no gauge constraints. A table with some zero and some nonzero entries is rejected as a pure-phase hopping table.
- An unconstrained \(u_l\) occurs when both neighboring hoppings that could reveal it vanish, or when the chain is too short. The corresponding gauge gate commutes with the surviving \(H_0\); choosing it to be one gives a valid reconstructed Hamiltonian. No missing phase needs to be inferred.
- At the left/right edge the absent phase must be one. Artificial dependence on a nonexistent outside spin is rejected. N=1 has only the diagonal potential. For N=2 the sole ZZ gauge gate commutes with the only hopping and is unidentifiable; choose it to be one.
- The ratio fixes \(u_l\) only up to sign, or \(\theta_l\) modulo pi/2. A sign change is absorbed into the neighboring recovered complex hoppings. Its extra gate is proportional to \(Z_lZ_{l+1}\), hence is a product of onsite Z operators. Reconstruction and boundary contraction use the same chosen root, so the physical answer is invariant. Allowing signed/complex quadratic hoppings removes a spurious branch-consistency problem. The algorithm never assumes the recovered angle equals an originally used angle.

For exact arithmetic, all checks are equalities between the local input coefficients and algebraic square roots of their ratios. No logarithm or angle reconstruction is needed. The code uses floating arithmetic with an explicit residual, so its numerical checks are not a formal exact-arithmetic certificate.

For approximate data, never infer a stable phase from an arbitrarily tiny hopping. Drop small tables, or reject them if the requested error cannot pay for dropping them. If reconstructed entries are \(\hat\tau_j\), set

\[
\eta_j=\max_{z_L,z_R}|\tau_j(z_L,z_R)-\hat\tau_j(z_L,z_R)|.
\]

Each hopping-operator discrepancy has norm exactly \(\eta_j\), because its nontrivial blocks are two by two Hermitian offdiagonal matrices. Thus

\[
\|H-\hat H\|\le\sum_j\eta_j,
\qquad |f_A(T)-\hat f_A(T)|\le2T\sum_j\eta_j \tag{C6}
\]

for \(\|A\|\le1\), by unitary Duhamel. The same bound charges a dropped bond. A full input parser must also charge or reject every unmatched term. A formal floating-point certificate would use interval bounds on these residuals; the present code reports ordinary numerical residuals and compares against dense evolution.

## 3. Product-boundary phase-difference contraction

H_0 is quadratic after Jordan–Wigner, but the transformed initial state \(\rho'=W^\dagger(\bigotimes_i\rho_i)W\) need not be Gaussian. Its full state is not required. Local occupations close under the quadratic evolution, and only its two-point fermionic covariance is needed.

The useful operation computes an arbitrary initial dressed Pauli expectation in O(N), including Jordan–Wigner strings. Write a canonical Pauli as

\[
P(x,z)=i^{x\cdot z}\prod_iX_i^{x_i}Z_i^{z_i},
\qquad x_i,z_i\in\{0,1\}.
\]

In the computational-basis sum, P relates a ket bit b_i to the bra bit \(b_i\oplus x_i\). Define

\[
\ell_i(b_i)=(\rho_i)_{b_i,b_i\oplus x_i}(-1)^{z_ib_i},
\qquad s_i=(-1)^{b_i}.
\]

The forward/backward gauge phases cancel on a bond whose endpoint flip parities agree. If they disagree, the surviving phase is \(u_i^{-s_is_{i+1}}\). Therefore

\[
\operatorname{Tr}\rho W P(x,z)W^\dagger
=i^{x\cdot z}\sum_{b_1,\ldots,b_N}
\prod_i\ell_i(b_i)
\prod_{i=1}^{N-1}
u_i^{-s_is_{i+1}(x_i\oplus x_{i+1})}. \tag{C7}
\]

This is a two-state complex transfer contraction. Start \(v_1(b)=\ell_1(b)\) and update

\[
v_{i+1}(c)=\ell_{i+1}(c)\sum_b v_i(b)
u_i^{-(-1)^{b+c}(x_i\oplus x_{i+1})}, \tag{C8}
\]

then sum the final two entries and multiply by \(i^{x\cdot z}\). This operation explicitly cancels the two history phases before summing configurations.

There is no exponential variation hidden in this initial contraction. Positivity of each one-site density matrix gives

\[
\sum_b|\ell_i(b)|\le1:
\]

for x_i=0 it is its trace, and for x_i=1 it is \(2|\rho_{01}|\le1\). Every bond phase has unit magnitude, so each transfer step is a contraction of the row vector's l1 norm. Numerical absolute errors accumulate at most polynomially with N; the exact sum does not require exponentially precise cancellation of exponentially large terms.

## 4. Explicit local readout

Define Majoranas

\[
\gamma_{2j-1}=Z_1\cdots Z_{j-1}X_j,
\qquad \gamma_{2j}=Z_1\cdots Z_{j-1}Y_j,
\qquad c_j=(\gamma_{2j-1}+i\gamma_{2j})/2.
\]

Every \(c_k^\dagger c_j\) is a sum of four Majorana products, each a Pauli string times a known phase. Acquire

\[
\Gamma_{jk}(0)=\operatorname{Tr}\rho Wc_k^\dagger c_jW^\dagger \tag{C9}
\]

by four applications of (C7). There are N-squared entries, each costing O(N), so this acquisition costs O(N-cubed). It is valid for arbitrary mixed or pure product inputs; Wick's theorem for the initial state is not assumed.

Let h be the N by N one-particle matrix with diagonal mu and \(h_{j+1,j}=a_j\), \(h_{j,j+1}=\bar a_j\). Then

\[
U(t)=e^{-ith},\qquad
\Gamma(t)=U(t)\Gamma(0)U(t)^\dagger,
\qquad f_{n_j}(t)=\Gamma_{jj}(t). \tag{C10}
\]

The final equality uses \([n_j,W]=0\). Quadratic Heisenberg evolution closes bilinears for every initial state, not just Gaussian states, so the non-Gaussian dressing does not invalidate it.

One-particle diagonalization and basis preprocessing cost O(N-cubed). For one selected site and time, an energy-basis quadratic form costs O(N-squared); all N occupations cost O(N-cubed) per time. Time enters phase evaluation and required numerical precision, rather than the spatial entanglement. The preparation, recognition and readout are all polynomial. Hermitian propagation is stable under matrix perturbations with a factor T; evaluating highly degenerate eigenvectors individually should not be used as an unproved conditioning assumption.

This bypasses volume-law growth within the restricted class. For example, use the engineered hopping chain in `WORKING_MATH.md` and an alternating occupation product input. W initially acts by a scalar phase. At T/4 the free representative has N/2 bits of half-chain entropy. W has only one gate across the central cut and can change the entropy by at most two bits. Thus the interacting representation has entropy at least N/2 minus two, even though (C9)-(C10) remain polynomial. The finite N=8 example obtains four bits directly from dense evolution.

## 5. Matched baseline and retained obstruction

W is two layers of nearest-neighbor diagonal gates. The transformed initial state's correlators can also be contracted by standard fixed-depth tensor-network methods. Equations (C7)-(C8) are an explicit width-two evaluation of those same initial correlators. They are not an asymptotic advantage over that baseline. The evolving state need not have a small tensor-network bond dimension, but its recognized quadratic conjugacy is the structural reason the query is easy.

The recognizer rejects a perturbed magnitude, an inconsistent local phase table, and spurious boundary dependence. A generic extra density-density interaction, not representable by (C2), cannot be treated as an invisible phase. If an extra term is only bounded and discarded, its long-time error is at best the charged Duhamel bound unless a stronger theorem is proved. General interacting dynamics and gate G1 in `WORKING_MATH.md` remain open.

## 6. Runnable evidence

Run `python3 gauge_quotient.py`. The production functions take local hopping tables, local density matrices and onsite potentials; they never receive W. Dense matrices are used only by the small-system comparison tests. `GAUGE_RESULTS.json` records arbitrary product inputs, complex free hopping, square-root aliases, several zero bonds, N=2 and N=1 boundaries, deliberate rejection cases, and volume-law dynamics in the restricted interacting class. The largest occupation discrepancy against independent dense many-body evolution is about 1.4e-15 in the retained run.

Status: `RECOGNIZED_RESTRICTED_ALGORITHM_DERIVED_AND_FINITE_TESTED`; `NO_HIDDEN_CONJUGACY_INPUT`; `KNOWN_GAUGE_SOLVABLE_PRINCIPLE`; `NOVELTY_UNESTABLISHED`; `GENERAL_INTERACTING_TARGET_OPEN`.
