# Independent audit: Riesz input, cubic lemma, and triangular prior-art scope

Audit date: 2026-10-16. Target: `pr105_nonsep_proof.md`, Sections 4, 5, and the primary comparison in Section 8. Read-only examination of the target and primary papers; no producer program was executed and no canonical proof file was changed.

## Result

The anisotropic second-order Riesz estimate and the dyadic cubic proof pass. The Harris–Kirchheim–Lin comparison is accurate as a scope comparison. Its application to this particular integrand is conditional on the separately established rank-one convexity of the integrand; its published compact-support formulation should be bridged to the stated Sobolev class by approximation. Neither qualification undermines the new proof, which does not use HKL.

## Primary sources inspected

1. Rodrigo Bañuelos and Fabrice Baudoin, *Martingale transforms and their projection operators on manifolds*, arXiv:1109.5751, Section 4.2 and Theorem 4.1(i), printed page 17 (PDF page index 16): https://arxiv.org/pdf/1109.5751 . The theorem bounds a constant-matrix combination of second-order Riesz transforms on a Lie group of compact type by `(p*−1)||M||`. Section 4.2 assumes a bi-invariant metric and an orthonormal left-invariant frame.
2. Terence L. J. Harris, Bernd Kirchheim, and Chun-Chi Lin, *Two-by-two upper triangular matrices and Morrey's conjecture*, arXiv:1708.07849v2, preliminaries and Theorem 2.4, printed pages 2–3: https://arxiv.org/pdf/1708.07849v2 . This identifies homogeneous gradient Young measures supported in the upper-triangular subspace as laminates. Their measure definitions use compact support. The proof explicitly verifies preservation of homogeneous gradient Young measures under `X -> AXB` with invertible domain change `B`.

The calculations below are an independent application and verification of these sources, rather than a claim that the papers state this tube theorem.

## 1. Uniformity over anisotropic torus metrics

Every positive constant metric on the abelian group T² is bi-invariant. Any constant full-rank frame can be declared orthonormal. Consequently the choices `(sqrt(kappa) ∂x, ∂y)` and `(∂x, tau ∂y)` satisfy the source hypotheses for every `kappa > 0` and every `tau > 0`. No lower bound on `tau` enters the theorem's constant. The degenerate endpoint `tau = 0` is never used.

In the first frame, the frequency is `xi = (sqrt(kappa) m, n)`. Apart from an irrelevant overall sign from the Riesz convention, the symbol is `xi^T M xi / |xi|²`. At `p=4`, `p*−1=3`. The diagonal matrix `diag(0,1)` has norm 1. The symmetric cross matrix `[[0,1/2],[1/2,0]]` has norm 1/2, so its symbol is `xi1 xi2 / |xi|²` and its bound is 3/2. There is no missing factor of two.

The metric volume form differs from ordinary torus measure by a constant factor. Normalizing the measure, or multiplying both sides of an L4 bound by the same constant, leaves the operator bound unchanged. Thus no metric-dependent volume or condition-number factor is missing.

Constants are annihilated by each derivative. Define the spectral inverse to be zero on the constant mode. This agrees with the derivative-semigroup representation and makes the zero mode harmless. In the actual applications both inputs A=eta_x and B=eta_y are already mean zero; no potentially costly mean-subtraction estimate is needed.

## 2. Section 4 multiplier and projection checks

For `A=eta_x`, the correction satisfies

- `p_y = (r+1) [n²/(kappa m²+n²)] A`;
- `p_x = (r+1) [mn/(kappa m²+n²)] A`.

The diagonal and cross bounds therefore give exactly

`||p_y||4 <= 3(r+1) epsilon`,

`||p_x||4 <= 3(r+1)/(2 sqrt(kappa)) epsilon`.

The triangle estimate for the vector gradient gives the stated L. All multipliers preserve the real-valued symmetry of Fourier coefficients. The mean-zero correction belongs to W^{1,4} by these derivative bounds and periodic Poincare, or by the bounded multiplier for p itself.

The signs of the projection identity are also correct:

`e_y - kappa k_x = (r+1) eta_xy - p_yy - kappa p_xx = 0`.

Integration by parts yields `<d0 e - kappa c0 k> = 0`. The mixed-frequency condition makes the y-average of e vanish, hence `<a0 e> = 0`. The residual multiplier is

`(r+1)² kappa m²/(kappa m²+n²)` acting on `|Ahat|²`.

For m nonzero, the squared ratio for the claimed Riesz control is

`(kappa m²+n²) / [kappa (r+1)² (m²+n²)] <= max(1,kappa^(-1))/(r+1)²`.

The m=0 contribution vanishes. This confirms the stated `C_a`.

## 3. Section 5 dyadic cubic constant

The compatibility identity gives `A_tau = tau T_tau B` exactly, including the signs of Fourier derivatives. In the frame `(∂x,tau ∂y)`, the cross-matrix estimate gives `||A_tau||4 <= (3/2) tau ||B||4`. Set K=3/2.

The multiplier of `A−A_1` is `m²/(m²+n²)`, whose absolute value is at most `|m|/sqrt(m²+n²)`. Hence the claimed L2 initial estimate is valid.

For non-axis modes, putting `v=|m|/(tau|n|)` gives the difference multiplier `3v²/[(1+v²)(1+4v²)]`. Relative to the multiplier defining `q_*`, its magnitude is

`3v sqrt(1+tau² v²) / [tau(1+v²)(1+4v²)] <= 3/(4tau)`.

Here `tau<=1`, `sqrt(1+v²)>=1`, and `4v<=1+4v²`. On either coordinate axis the dyadic difference is zero. For the initial difference, n=0 is also correctly controlled by `q_*`.

Hölder applied to the difference of absolute cubes gives initial coefficient `1+K+K²`. The scale-tau coefficient is

`[3/(4tau)] K² tau² (1+1/2+1/4) = (21K²/16) tau`.

Summing `tau=1,1/2,...` gives `21K²/8`. The total is

`1+3/2+9/4+189/32 = 341/32 = 10.65625 < 11`.

The terminal L3 norm tends to zero because the normalized torus has `||A_tau||3 <= ||A_tau||4 <= K tau ||B||4`. Thus the telescope proves the absolute-value cubic inequality without a cutoff. The proof works for arbitrary periodic W^{1,4} eta, not just mixed-frequency eta.

## 4. Exact scope of the HKL comparison

For a smooth periodic vector field, the distribution of its gradient under normalized torus measure is a compactly supported homogeneous gradient Young measure. Let P exchange the two coordinates.

- If `f=F(x)`, then `D(f,g)=[[F',0],[g_x,g_y]]`. The transformation `V -> P V P` gives `[[g_y,g_x],[0,F']]`, which is upper triangular.
- If `f=H(y)`, then `D(f,g)=[[0,H'],[g_x,g_y]]`. The transformation `V -> P V` gives `[[g_x,g_y],[0,H']]`, which is upper triangular.

These transformations are allowed matrix-side/domain changes, not an unjustified appeal to transposition of gradient measures. HKL makes the transformed measure a laminate. Inverting these rank-one-preserving transformations preserves its Jensen property for rank-one convex integrands. Adding a constant background is handled by applying Jensen to the translated integrand `V -> J_r(sI+V)`, whose rank-one convexity follows from that of J_r.

This gives qualitative `E_r >= 0` in either one-profile case, provided J_r's rank-one convexity has been established separately. HKL does not itself establish that integrand property, the strict quartic reserve, this explicit relative radius, or the generic mixed perturbation theorem.

For W^{1,4} profiles and second potentials, smooth periodic convolution preserves the one-profile structure. Apply the compact-support result to each smooth pair and pass to the limit using strong W^{1,4} convergence and quartic continuity. Hence compact support is a readily bridged qualification, not an obstruction.

A generic mixed perturbation has no promised fixed rank-one linear functional vanishing on every gradient matrix, which is the structural constraint furnished by a triangular subspace after invertible left/right transformations. Some specially structured mixed examples may still reduce; the proof correctly says there is no general triangular-support promise and does not assert impossibility for every mixed example.

Suggested precise replacement for the comparison sentence:

“Assuming the separately established rank-one convexity of J_r, Harris–Kirchheim–Lin, Theorem 2.4, gives the qualitative Jensen inequality in the one-profile cases, after a row/coordinate exchange and smooth approximation. Generic mixed perturbations have no corresponding triangular-support hypothesis.”

## Limits of this audit

This audit does not verify the Astra N885 attribution, global rank-one convexity of J_r, the inherited Gram certificate, or historical novelty beyond the named comparison. It does independently validate the external analytic input and all numerical constants in the dyadic cubic argument.
