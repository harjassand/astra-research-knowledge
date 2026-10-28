# Finite-duration continuum solver and a temporal-span residual obstruction

28 October 2026. New derivation and implementation by the solver-instrument contributor. The model is a finite source qubit coupled through the full bounded sine of a positive-frequency continuum field. This is **not** the P2 baseline circuit or a device claim. The formulas below are analytic; the present numerical integrals and matrix computations are floating diagnostics and are not promoted to certified channel bounds.

## 1. The full smooth model

Use the exact vacuum Gaussian bath with one-particle vectors f_t and

`<f_t,f_u> = 2.1/[1-i(u-t)]`,

corresponding to `rho(omega)=2.1 exp(-omega)` for omega >= 0. For T=0.6,

`H(t)=A(t) S(t) sin Phi(f_t)`,

`A(t)=12 sin²(pi t/T)`, `S(t)=cos(t)X+sin(t)Y`.

The pulse action is 3.6. This includes every nonlinear photon order in the sine, all bath frequencies and memory, and noncommuting source rotations. It uses no Born, Markov, rotating-wave, Fock, or frequency-grid approximation.

Choose a fixed finite set of coherent packets `|alpha_a>`, where `alpha_a=i sum_j n_aj f_(t_j)` and the coefficients n_aj are integers. Their Gram matrix and every Weyl matrix element are exact functions of the supplied kernel. In particular, putting `lambda_a=(n_aj)` and `c_j(t)=<f_(t_j),f_t>`,

`<alpha_a|exp[i q Phi(f_t)]|alpha_b>`

`= G_ab exp[-q²(2.1)/2 + q lambda_a.c(t)-q lambda_b.conj(c(t))]`.

Construct an orthonormal basis Q of a retained packet span, preserving the vacuum as its first vector. The code first removes each other packet's vacuum component, diagonalizes the remaining Gram matrix, and discards small Gram eigenvectors. This is a selection of a trial space, not a declaration that the discarded true bath dynamics vanishes. The full-space residual below charges what the selected space misses.

## 2. A full-input residual computable without a bath grid

Let `B(t)=Q^dagger sin Phi(f_t) Q`, and importantly let

`B2(t)=Q^dagger sin² Phi(f_t) Q`

`= 1/2 I - 1/4 Q^dagger[exp(2i Phi(f_t))+exp(-2i Phi(f_t))]Q`.

In general `B2(t) != B(t)^2`. Replacing B2 by B² would delete the exterior residual and could make a poor basis look accurate.

On time cell j, choose `H_j=A(t_mid) S(t_mid) tensor B(t_mid)` and propagate the proposed finite-coordinate map by the exact matrix exponential `Y(t)=exp[-i(t-t_j)H_j]Y(t_j)`. This defines a continuous proposed map into the fixed physical packet space, even though its derivative changes between cells. It is an isometry in exact arithmetic because Q is orthonormal, the initial vacuum is exact, and every H_j is Hermitian.

The true continuous Hamiltonian is never replaced in the certificate. Its residual matrix is

`R(t)^dagger R(t)`

`= Y(t)^dagger [ A(t)^2 I tensor B2(t) - H_proj(t)H_j - H_j H_proj(t) + H_j² ] Y(t)`,

where `H_proj(t)=A(t)S(t) tensor B(t)`. This is a 2x2 matrix on the complete source-input code. The full source+bath map error is at most

`epsilon = integral_0^T sqrt(lambda_max(R(t)^dagger R(t))) dt`.

The associated channel half-diamond error is bounded by the same epsilon, with arbitrary source/reference entanglement, if the scalar integral and kernel/matrix arithmetic have been reliably enclosed. Our code presently computes this integral by Gauss–Legendre quadrature in float64; therefore its returned number is a diagnostic and **not yet this certified bound**.

The residual decomposes into a positive basis-exterior contribution and a positive time-freeze contribution:

`H2_proj-H_proj² + (H_proj-H_j)²`.

This distinguishes a poor trial space from inaccurate finite-coordinate time propagation. Neither is physical noise. The code logs both contributions, the complete-input positivity checks, full-space exterior eigenvalue checks, finite-coordinate norm drift, and the numerical defect of Q's orthonormality. Floating orthonormality and positivity errors remain part of the unenclosed arithmetic budget.

No derivative of f_t or of moving coherent packets is used. Fixed packets avoid the strong-derivative failure that can occur for the baseline circuit's divergent second spectral moment.

## 3. Exact obstruction for a fixed one-particle temporal span

Let W be the span of the selected time vectors, and let F(W) tensor |0>_(Wperp) be its entire Fock space, without a photon cutoff. Write

`f_t = p_t + q_t`, with p_t in W, q_t perpendicular to W, and `tau(t)=||q_t||²`.

Even if an arbitrarily rich packet basis represents all of F(W), the sine vertex can excite its omitted orthogonal vacuum factor. Let P_W project onto F(W) tensor |0>. For any unit vector psi in F(W),

`||(I-P_W) sin Phi(f_t) (psi tensor |0>)||²`

`= c_even(tau)||sin Phi(p_t) psi||² + c_odd(tau)||cos Phi(p_t) psi||²`,

where

`c_even(tau)=(1-exp(-tau))²/2`,

`c_odd(tau)=(1-exp(-2tau))/2`.

Proof: factor the commuting fields and apply the sine addition formula. The residual even-vacuum component of cos Phi(q)|0> and the odd vector sin Phi(q)|0> are orthogonal. Their norms follow from the vacuum characteristic function. Since sine²+cosine²=I and c_even <= c_odd, the squared norm is at least c_even. For the source involution S(t), multiplication by S does not change this norm.

Consequently every normalized differentiable trial curve confined to this full F(W) has a local residual at least `|A(t)|(1-exp(-tau(t)))/sqrt(2)`. Its integrated Duhamel residual certificate cannot be smaller than

`integral |A(t)|(1-exp(-tau(t)))/sqrt(2) dt`.

This is a **floor for this residual-certificate strategy with the fixed temporal span**, not a lower bound on actual endpoint simulation error and not a physical noise floor; coherent cancellations in the exact endpoint error can be smaller.

The missing one-particle norm is available directly from the kernel:

`tau(t)=G(t,t)-c(t)^dagger G_nodes^(-1)c(t)`

for independent node vectors. For this smooth-pulse model, floating numerical values are:

| Time nodes | Maximum tau(t) | Integrated state-independent residual floor |
|---|---:|---:|
| 0, 0.6 | 1.4317e-2 | 2.7921e-2 |
| 0, 0.3, 0.6 | 1.7737e-4 | 2.0743e-4 |
| 0, 0.2, 0.4, 0.6 | 3.7481e-6 | 2.5512e-6 |

Thus adding more packet amplitudes within only the two endpoint directions cannot make this particular rigorous-residual route arbitrarily accurate. Adding temporal directions changes the obstruction. This explains why the tested three-node representation improves much more than simply enlarging the two-node amplitude grid.

## 4. Initial completed diagnostic results

For 80 time cells and fourth-order Gauss quadrature within each cell:

| Temporal nodes | Integer range per direction | Retained rank | Full residual integral | Basis part | Time-freeze part |
|---:|---:|---:|---:|---:|---:|
| 2 | -1..1 | 9 | 1.01469 | 1.01180 | 0.04137 |
| 2 | -2..2 | 25 | 0.51595 | 0.51061 | 0.04770 |
| 2 | -3..3 | 49 | 0.39513 | 0.38811 | 0.04883 |
| 2 | -4..4 | 81 | 0.36501 | 0.35716 | 0.04902 |
| 3 | -1..1 | 27 | 0.46370 | 0.45639 | 0.04804 |
| 3 | -2..2 | 125 | 0.07777 | 0.05314 | 0.05025 |

The full residual is not the sum of the last two columns; their matrices add before the square root. The first two-node trial gives a vacuous channel bound even before rounding certification. The three-node/range-two trial makes the continuous, full-bath computation useful as a nontrivial approximation diagnostic. Increasing that trial to 320 time cells lowers the total to about 0.05572 while leaving the basis contribution near 0.05316; the time-freeze contribution drops to about 0.01256. Therefore further effort should improve the bath trial space before only shrinking the time step.

The completed second refinement enlarges the three-node integer range to -3..3, retaining 343 directions, with 160 time cells. Its full residual integral is about **0.03327**, its basis contribution is **0.01947**, and its time-freeze contribution is **0.02514**. The physical Gram orthonormality defect is 1.86e-10 in floating arithmetic; retained residual-Gram condition is about 5.47e6. All sampled complete-input residual eigenvalues were nonnegative, while the full basis-exterior form had a minimum eigenvalue around -8.19e-11, consistent with the reported numerical arithmetic scale but not a proof of positivity.

The 125-direction/320-cell and 343-direction/160-cell endpoint maps differ by about 0.01548 in full input operator norm. This is less than the sum of their separately computed residual diagnostics; it is an internal consistency check, not an independent reference solution.

A four-node trial with only integer range -1..1 retains 81 directions but has residual integral about 0.17689. Adding temporal nodes alone does not remove the need for enough packet amplitudes to describe strong conversion. The successful refinement needs both temporal coverage and nonlinear displacement depth.

Doubling the per-cell quadrature order from four to eight for the 125-direction/80-cell trajectory changes its residual integral by **3.0115e-4** (from about 0.077774 to about 0.077473). This is a material visible quadrature discrepancy, separately saved in `continuous_three_K2_q8_receipt.json`. It does not change the representation decision, but it prevents treating the displayed fourth-order values as high-precision scalar bounds. More quadrature samples alone would still not supply a rigorous enclosure.

The analytic formulas here supply an evaluable full-output certificate architecture; numerical validation remains separate. The saved receipts and endpoint maps expose its current costs and limitations. No result here asserts a useful computing operation, detector efficiency, baseline/notch circuit compatibility, or scalable solver complexity.
