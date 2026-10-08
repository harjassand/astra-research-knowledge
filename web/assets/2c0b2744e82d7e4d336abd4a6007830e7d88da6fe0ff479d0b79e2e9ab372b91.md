# Research candidate: Steklov spectral-capacity bound for slowly varying cone ends

**Date:** 2026-10-08 (Australia/Brisbane).  
**Research input pinned:** Astra commit `687dfc0640ee80654bcbdbe38cb13d6e1f1586ce`.  
**Status:** independent mathematical derivation, not externally validated or historically cleared. This is an upper-bound theorem under explicitly stated geometric hypotheses; it is **not** an unconditional resolution of Yau's problem or a field-breaking breakthrough.  
**Relation to prior record:** N175–N178 conjectured *one-metric lower/existence* construction and source audits. The upper-bound proof below does not use that construction. Conditional on its correctness, the bound establishes its asymptotic optimal coefficient within this metric class.

## 1. The theorem

Let `n>=3`, `d=n-1`, `omega_d=Vol(B^d(1))`, `A_d=Area(S^d)`, and `kappa_d=omega_d A_d/(2pi)^d=2/d!`.

Let `(M^n,g)` be smooth, complete, diffeomorphic to `R^n`, and outside a compact subset admit global polar coordinates `(r,theta)` with
```
g = dr^2 + f(r)^2 h_(log r)(theta)
```
where `h_t` are smooth metrics on `S^d`, with `Area(h_t)=A_d` for every large `t`, contained in a precompact subset of `C^infinity` and satisfying `||d h_t/dt||_(C^0) -> 0`. Assume
```
f(r)/r -> a > 0,     r f'(r)/f(r) -> 1.
```
Then `AVR(g)=v=a^d`, with volume ratio normalized by Euclidean ball volume. Let `H_k` be the real vector space of global harmonic functions with pointwise growth `|u(x)|<=C_u (1+r(x))^k` and `h_k=dim H_k`. Then all `h_k` are finite and
```
limsup_(k->infinity) h_k / k^d
     <= (2/d!) * v * ((d+1)/d)^d.
```
In dimension `n=3`, `d=2`, this is
```
limsup h_k/(k+1)^2 <= 9v/4.
```
No assumption of nonnegative Ricci curvature is needed for this upper-bound proof. It applies, in particular, to any Ricci-nonnegative metric meeting these additional polar-end regularity hypotheses.

**Consequence:** for `v<4/9` the normalized 3-dimensional asymptotic leading coefficient is strictly below 1; for `v=4/9` it is at most 1. This does NOT preclude isolated finite-degree violations of the Euclidean dimension comparison.

## 2. Proof: a uniform lower bound on high Steklov eigenvalues

Let `Omega_r` denote the enclosed compact ball; its boundary is the sphere `S_r`. Let `Lambda_r` be the positive Dirichlet-to-Neumann map, `Lambda_r phi=partial_r (harmonic extension of phi)`, acting self-adjointly on boundary `L^2(dA_r)`; write its eigenvalues as `0=sigma_0(r)<=sigma_1(r)<=...`, counted with multiplicity, and `mu_j(r)=r sigma_j(r)`.

**Claim (uniform high-index Steklov lower law).** For every `eps>0` there are `R_eps,J_eps` such that for all `r>=R_eps` and `j>=J_eps`,
```
mu_j(r) >= (1-eps) * (j/(kappa_d*v))^(1/d).
```

Fix a logarithmic collar width `delta>0`. For each outer boundary datum `phi`, Dirichlet's principle and restriction to `[r exp(-delta),r]` give
```
<phi,Lambda_r phi>_(S_r)
 = min_(w on Omega_r,w|S_r=phi) int_(Omega_r)|grad w|^2
 >= min_(w on collar,w|S_r=phi) int_(collar)|grad w|^2 .
```
The lower variational problem has *free Neumann* boundary condition at the inner collar edge. Let `t=log r`. The assumptions `dh_t/dt ->0`, `f(r)/(ar)->1` imply that, for large `r`, all collar Dirichlet energies and the outer boundary norm are `(1+o(1))`-comparable (uniformly for all test functions) to those in the frozen exact cone
```
g_cone = ds^2 + a^2 s^2 h_t
```
on the same collar, with the boundary value identified by the polar coordinate `theta`.

For a Laplace eigenvalue `lambda>=0` of `-Delta_(h_t)`, the radial equation in this frozen cone has exponents
```
p_+ = -(d-1)/2 + sqrt(((d-1)/2)^2 + lambda/a^2);
p_- = -(d-1) - p_+.
```
Solving the two-end ODE with Neumann condition at `exp(-delta)r` and value prescribed at `r`, the scaled outer Steklov eigenvalue is exactly
```
nu_(lambda,delta)
  = p_+ * [1-exp(-delta*(2*p_+ + d-1))]
      / [1 + p_+/(p_+ + d-1) * exp(-delta*(2*p_+ + d-1))].
```
For `lambda=0` the expression is understood by continuity as zero. Uniformly for `a` fixed as `lambda->infinity`, `nu_(lambda,delta)~sqrt(lambda)/a`. Compactness of the angular metric family yields the uniform Laplace Weyl law
```
lambda_j(h_t) = (j/kappa_d)^(2/d) * (1+o_(j->infinity)(1))
```
uniformly in all large `t` (their volume is fixed `A_d`). Variational min-max comparison with the Neumann collar gives the claimed estimate for `r Lambda_r`. All constants in this argument are uniform in the interior geometry of `Omega_r`.

## 3. Proof: determinant growth and Ky Fan

Choose any `m` linearly independent `k`-growth global harmonic functions `u_1,...,u_m`. Their traces on every `S_r` are linearly independent: a linear combination with zero boundary trace has harmonic extension zero on `Omega_r` by uniqueness, and is then globally zero by unique continuation.

Use `t=log r`, and put
```
dnu_t := r^(-d) dA_(S_r) = (f(r)/r)^d dA_(h_t).
G_ij(t) := int_(S^d) u_i(e^t,theta) u_j(e^t,theta) dnu_t .
```
Thus `G(t)` is positive definite. The boundary logarithmic volume derivative obeys
```
z_t(theta) = d/dt log(dnu_t/dnu_ref)
   = d*(r f'(r)/f(r)-1) + 1/2 tr_(h_t) (d h_t/dt),
||z_t||_infinity -> 0.
```
The radial boundary traces evolve by `partial_t u = r Lambda_r u`. Differentiate `G`, orthonormalize the `m` traces at fixed `t`, and apply Ky Fan:
```
d/dt log det G(t)
 = 2 sum_(i=1)^m <psi_i,r Lambda_r psi_i>_(dnu_t)
   + sum_(i=1)^m <psi_i,z_t psi_i>
 >= 2 sum_(j=0)^(m-1) mu_j(r) - m ||z_t||_infinity .
```
The `u_i` growth bounds and bounded normalized boundary volumes give
```
limsup_(T->infinity) (1/T) log det G(T) <= 2mk.
```
Integrate the lower derivative inequality, divide by `2T`, and send `T->infinity`. The uniform Steklov estimate, discarding the first `J_eps` terms, gives
```
m*k >= (1-eps)*(kappa_d*v)^(-1/d)
                 sum_(j=J_eps)^(m-1) j^(1/d).
```
The integral approximation
```
sum_(j=J)^(m-1) j^(1/d) = d/(d+1) * m^((d+1)/d) + O_J(m^(1/d)+1)
```
gives `k >= (1-eps) d/(d+1) (kappa_d*v)^(-1/d) m^(1/d) (1-o_m(1))`.
Apply to arbitrary `m<=h_k` and send `k->infinity`, then `eps->0`. This proves the theorem and finiteness of `h_k`.

**Important interface:** The crucial lower Steklov spectral law must be uniform in `r`. Pointwise Weyl asymptotics at each `r` alone cannot be interchanged with the `r->infinity` limit. The fixed-width collar argument supplies uniformity and insulates the proof from the geometry of the entire growing ball.

## 4. Spectral-transport explanation and sharpness scope

More generally, if a family of nonnegative self-adjoint growth generators has high spectrum bounded below by `(j/kappa)^(1/d)` and the logarithmic Hilbert-space volume form varies by `o(1)`, the identical determinant argument gives
```
limsup h_k/k^d <= kappa*((d+1)/d)^d .
```
This is a *reusable spectral-transport bound*, not restricted to harmonic functions.

At the abstract eigenline-permutation level the numerical constant cannot be lowered: take the first `m` frequencies `alpha_1<=...<=alpha_m`, with `alpha_j~(j/kappa)^(1/d)`, and cycle all `m` labels equally through all positions. Every averaged exponent is `bar_alpha_m=(1/m)sum_(j<=m)alpha_j~[d/(d+1)](m/kappa)^(1/d)`. Thus `m/bar_alpha_m^d->kappa*((d+1)/d)^d`. This is **not** a claim that an arbitrary such permutation is realizable by a Ricci-nonnegative metric.

For `n=3`, the N175 single-metric existence proof would yield arbitrarily close lower coefficients `9v/4` for each `4/9<v<1`. If N175 is independently verified, the new upper theorem then proves sharpness within its stated regularity class. N175 currently remains source-derived/unreviewed.

## 5. Independently reproducible finite check

Run `python3 state/2026-10-08-steklov-capacity/verify_spectral_ratio.py`. For `v=.81`, the *exact frozen-cone* frequencies `p_l=(-1+sqrt(1+4 l(l+1)/v))/2`, each repeated `2l+1` times for `0<=l<=M`, have average `bar p_M`. The ratio `(M+1)^2/bar p_M^2` tends to `9v/4=1.8225`. Example calculations: `M=10:2.08034906;30:1.90583945;100:1.84722369;300:1.83071459;1000:1.82496158`. This verifies the capacity algebra but does not verify any metric existence or infinite-dimensional PDE.

## 6. Primary literature, novelty, and unresolved audit obligations

- OpenAI, October 2026 result family 361, original source: `https://github.com/openai/math/blob/main/preprints/A-Three-Dimensional-Counterexample-to-Integer-Degree-Harmonic-Dimension-Comparison-September-26-2026/build/sections/introduction.tex` (the authors explicitly leave optimality of `9v/4` unclaimed and give metrics indexed by degree).
- Astra N175–N178 and their source proof file `web/pages/d-413da5591afd120a.html` at the input commit (countable-metric existence still unreviewed).
- Huang, *Harmonic functions with polynomial growth on manifolds with nonnegative Ricci curvature*, arXiv:2109.07534 (exact asymptotic coefficient `v` under a **unique** tangent-cone hypothesis, so this bound does not contradict it).
- Classical Steklov-Weyl law and Dirichlet-to-Neumann min-max (e.g. review `https://doi.org/10.1007/s13163-023-00480-3`); Ky Fan minimum principle; Dirichlet uniqueness.
- Searches for the exact factor in the restricted slowly varying setting did not locate a source stating this theorem. This is **not** exhaustive priority clearance and the argument combines established tools; experts should check earlier Colding–Minicozzi/Li methods and asymptotic-volume spectral bounds before any novelty claim.

**Unresolved:** (1) external review of uniform collar comparison, including the trace-measure evolution; (2) confirm the scope against all earlier dimension-growth estimates, not merely abstracts; (3) determine whether a general volume-ratio/no-foliation version holds or fails; (4) independent verification of N175 existence candidate to get matching geometric lower bound; (5) for general manifolds where no uniform rescaled collar geometry exists, the proof gives **no bound**.

**Research-state class:** `derived_and_internally_checked`; `peer_reviewed=false`; `formalized=false`; `historical_novelty=UNKNOWN`; `field_breaking_discovery=NOT_ESTABLISHED`.
