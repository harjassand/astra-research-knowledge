# Independent audit of the radial endpoint proof

Date: 2026-10-15. Reviewer: `operator_adversary_v3`. Root authorized this cross-read after the original independent proof/check packet was frozen. This audit changes no original proof or candidate files.

**Verdict: no material analytic gap found in the endpoint existence proof or sharp iterated-log obstruction, with the candidate's moment addendum included.** The conclusions are internally reconstructed and independently checked within this agent team. This is not formal verification, independent external certification, historical priority clearance, or a practical measurement claim.

Audited inputs:

- `radial_endpoint_astra/ENDPOINT_PROOF_v1.md`, SHA-256 `27cc78159b041c0f679dc2372c6eed21e2d1a8ada226ecf5b5e5c6c600c5ad78`.
- `radial_endpoint_astra/ADDENDUM_1_MOMENT_JUSTIFICATION.md`, SHA-256 `16ce40f6c5ac8227850aed26247c18da94ad4a4228f04a1f4eb72951a9eb1a4d`.

Both files were read in full and their hashes matched the author's freeze notice. The original independent operator audit has proof SHA-256 `d4402c89b6816bc1fdfe4ac1cfca39515bf506bc239a9a5357a6e3a3c626a1c5`; it remains unchanged. Its statement that the supplied transcript only proves the strict leading coefficient is a source/reconstruction boundary, superseded for the new endpoint candidate by this separate audit.

## 1. Scope of the result checked

For arbitrary bounded self-adjoint `A_1,...,A_m` on any complex Hilbert space, assume `||sum u_j A_j|| <= R|u|`, `R>0`. Define

`Q(s)=sqrt(e^2+s^2)`,

`f_beta(s)=Q(s)[log Q(s)+beta log log Q(s)]-e`,

`V_{L,beta}(x)=L f_beta(|x|/L)/(2R)`, `p=Z^{-1}exp(-V)`,

where `0<=beta<=1`. The candidate proves the same positive scalar convolution contract as the supplied source, including norm-integrable positive operator densities on arbitrary Hilbert spaces. It gives the explicit sufficient scale

`L >= 800 e^3 m^2(m+1)2^m R / epsilon`.

For fixed `L`,

`-log p(x) = [r/(2R)] [log r + beta log log r - log L + o(1)]`.

The `beta=1` choice attains the critical leading coefficient and the maximum iterated-log coefficient under the stated pointwise radial density envelope. It does not determine the optimal constant offset, minimal regularization scale, or efficient implementation.

## 2. Duhamel estimate: both denominator factors are justified

Let `H=H*`, `q=||H||`, and let the derivative order be `k>=2`. The ordered Duhamel formula has `k!` terms integrated over a simplex of volume `1/k!`. After conjugation by `exp(-H/2)`, a term has exponential norm bound

`exp(q[|t_0-1/2|+|t_k-1/2|+1-t_0-t_k])`.

Fix the two endpoint variables `u=t_0`, `v=t_k`. The remaining simplex has volume `(1-u-v)^(k-2)/(k-2)!`, which is at most `1/(k-2)!`. The endpoint triangle `u,v>=0`, `u+v<=1` splits exactly into the square `0<=u,v<=1/2` and two triangles of total area `1/4`.

- On the square the exponent is `2q(1-u-v)`, giving an integral no larger than `e^(2q)/(4q^2)` for positive `q`.
- On either remaining triangle the exponent is at most `q`, giving together no more than `e^q/4`.
- For `q>=1`, the first bound divided by `e^(2q)/(1+q)^2` is at most one. The second ratio is `(1+q)^2 e^(-q)/4`, at most `e^(-1)` because its derivative is nonpositive on this range.
- For `0<=q<=1`, the triangle's area gives an integral at most `e^(2q)/2`, also no greater than `2e^(2q)/(1+q)^2`.

Multiplication by `k!/(k-2)!=k(k-1)` proves the claimed bound

`||e^(-H/2)D^k exp(H)[K_1,...,K_k]e^(-H/2)||`

` <= 2 k(k-1) e^(2q)/(1+q)^2 product ||K_j||`.

There is no missing factorial. The denominator is not asserted for orders zero or one. Since `e^(2q)/(1+q)^2` is nondecreasing for `q>=0`, replacing `q=||A(g)||` by `R|g|` is legitimate.

Before reading the candidate, I independently derived a slightly weaker version of this same endpoint-simplex bound and identified the two-denominator mechanism. The candidate's partition gives the better stated constant two; the partition and inequalities check.

## 3. Analytic remainder: termwise distribution evaluation is legal

The exact remainder is `h_x(z)=exp[-F_x(z)]-1`,

`F_x(z)=V(x-z)-V(x)+grad V(x).z`.

Both the constant and the linear Taylor coefficients vanish exactly. This is essential: every remaining term has derivative order at least two, so every term receives the two-denominator Duhamel bound.

If `delta_x=sup_{|z_j|<=rho}|F_x(z)|<=1`, Cauchy estimates give `|c_alpha|<=e delta_x rho^(-|alpha|)`. Choose `R<a<rho` and one smooth cutoff supported in the real ball `B_a`, equal to one near the Wigner support. The Taylor series converges with every fixed finite number of derivatives on `B_a`. Thus distribution continuity justifies evaluation term by term after multiplication by the cutoff and by the fixed exponential `exp(g.y)`.

The use of a smooth, nonanalytic cutoff creates no problem: it multiplies an already convergent smooth series on a fixed compact set. For each fixed `x` the tilt is finite. Uniform positivity follows from the resulting explicit all-`x` bound; it does not require an unstated uniform interchange of the distributional series as `x` tends to infinity.

The degree-`k` coefficient count is exactly `binomial(k+m-1,m-1)`. Consequently,

`sum_{k>=2} k(k-1) binomial(k+m-1,m-1)z^k = m(m+1)z^2/(1-z)^(m+2)`.

At `rho=2R`, the candidate's coefficient sum is `S_m=m(m+1)2^m`. No extra Hilbert-space dimension factor or extra power of the tilt is hidden in this step.

## 4. Complex domains, Hessian constants, and uniform tails

The potential uses the analytic expression `e^2+sum z_j^2`, not the nonholomorphic complex Euclidean norm. Let `Q=sqrt(e^2+s^2)`, `ell=log Q>=1`. For displacement in the closed polydisc of coordinate radius `rho=2R`, the condition `L>=8 sqrt(m)rho/e` gives `d=|z|/L<=Q/8`. Hence

`|D-Q^2|<=2sd+d^2<=(17/64)Q^2`.

It follows that `Re D>0`, the principal square root is separated from its cut, and

`sqrt(47)Q/8 <= |q| <= 9Q/8`, `|arg q|<pi/4`.

Also `Re log q>ell/2`; therefore `log q` stays in the right half-plane and `log log q` has a consistent holomorphic branch. This establishes an open neighborhood of the closed polydisc, as needed for Cauchy estimates.

The derivative bounds `|h_beta'(q)|<=9ell` and `|h_beta''(q)|<=9/Q` are valid uniformly for `0<=beta<=1`. For an especially simple independent constant certificate, use the weaker lower bound `|q|>5Q/6`. The candidate's Hessian estimate is then no greater than

`9 [ (9/8)^2(6/5)^2 + 6/5 + (9/8)^2(6/5)^3 ] ell/Q`

` = (93771/2000) ell/Q < 50 ell/Q`.

This proves the advertised `50ell/Q` with a rational margin. There is no sign issue from the holomorphic transpose in `z^T Hessian z`: its absolute value is bounded by the induced matrix norm times `|z|^2`.

Taylor's remainder therefore gives

`delta_x <= (50mR/L) ell/Q`.

The condition `L>=50mR/e` ensures `delta_x<=1`. The gradient is `|g|=w/(2R)`, where

`w=(s/Q)[ell+beta log ell+1+beta/ell]`.

The candidate's whole-tail scalar estimates check:

`e^w <= e^2 Q ell^beta`,

`1+w/2 >= ell/(2sqrt(2))`,

and thus

`(ell/Q)e^w/(1+w/2)^2 <= 8e^2 ell^(beta-1) <= 8e^2`.

For the denominator lower bound, `s>=e` gives `s/Q>=1/sqrt(2)` and `w>=ell/sqrt(2)`. On the complementary compact range, `ell<sqrt(2)` and the constant one suffices. This covers every real `x`, including arbitrarily remote tails.

Combining the coefficient sum, the Hessian remainder, and this scalar bound produces exactly

`sup_x ||e^(-A(g)/2)E_x e^(-A(g)/2)|| <= 800e^3 m^2(m+1)2^m R/L`.

The final scale dominates both preliminary scales for every `m>=1`, `R>0`, and `0<epsilon<1`.

## 5. Positivity, normalization, and smooth noise

The remainder is self-adjoint on real arguments. A sandwiched norm bound at most `epsilon` therefore gives the two stated Loewner bounds exactly.

For real `q>=e`, `h_beta'(q)>0` and

`h_beta''(q)=[1+beta/log q-beta/(log q)^2]/q>0`.

Both radial and angular Hessian eigenvalues of the potential are positive, including their common origin limit. Thus the density is strictly log-concave. The superlinear potential gives every exponential moment, and its derivative bounds give the claimed rapid decay of every fixed density derivative.

The upper Loewner bound majorizes the density's operator norm by `p(x)exp(R|grad V(x)|)` times a fixed constant. The additional factor is only polynomial in the radius up to logarithms, while `p` is superexponential. The operator density is therefore norm integrable; its continuous range is separable regardless of the Hilbert space. The convolution identity is an equality of continuous Fourier transforms, so evaluation at zero proves normalization. No weak-POVM-to-Bochner promotion occurs here: a norm-integrable density has already been established.

The tail expansion is correct. In particular, with `beta=1` the positive `r log log r/(2R)` term eventually dominates the fixed negative linear offset `-r log L/(2R)`, so the stated eventual upper envelope at the exact leading critical coefficient is valid. The `beta=0` tail expansion by itself would not give that upper envelope when `L>1`; the candidate correctly invokes `beta=1` for that particular assertion.

## 6. Actual moments for arbitrary all-exponential noise

The main proof originally flagged a general-noise moment-justification dependency. The frozen addendum resolves it fully for the Wigner contract.

For a unit vector `v` and a real direction `u`, the positive scalar law of `u.X` has characteristic function

`nu_hat(tu)<v,exp(itA(u))v>`.

Uniqueness of characteristic functions identifies this law with the convolution of the projected scalar noise and the positive spectral law of the bounded self-adjoint `A(u)`. Therefore its actual Laplace integral is

`integral exp(g.x)<v,M(dx)v> = m_nu(g)<v,exp(A(g))v>`.

The right side is bounded uniformly over unit vectors by `m_nu(g)exp(R|g|)`. This proves the required weak moment operators without analytic-continuation assumptions. Polynomial factors and derivatives are dominated by finite sums of nearby exponential envelopes. Uniform quadratic-form bounds on the Taylor remainders imply the claimed operator-norm differentiation as well.

The resulting normalized tilted positive POVM has transverse moments `I`, `B_1`, and `[K'(s)/s]I+B_2`, for `s>0`. Its moment-block Schur complement is therefore legal for weakly countably additive POVMs and nonsmooth scalar noise. This also agrees with the more general compact-distribution cutoff lemma in my original independent proof.

## 7. Sharp iterated-log obstruction and fixed offset

For a Pauli pair, the Schur-complement calculation gives

`K'(s)>=[sinh(as)-as]/(2s)`, `a=2R`, `s>0`.

Integration yields `liminf_{s->infinity} s exp(-as)K(s)>=1/(4a)`. The factor is correct: the leading derivative is `exp(as)/(4s)`, whose integral has leading term `exp(as)/(4as)`.

For the density envelope `p(x)<=C exp[-f_b(r)]`,

`f_b(r)=r[log r+log log r+b]/a`,

the large-radius Legendre maximizer satisfies

`as=y+log y+b+1+1/y`, `y=log r_s`.

Thus `r_s~exp(as-b-1)/(as)` and

`f_b^*(s)~exp(as-b-1)/(a^2s)`.

The integration step preserves this precise coefficient. With `d_s=s^(-2)`, bound the integrand by `exp(f_b^*(s+d_s)) exp(-d_s r)` and integrate the radial Jacobian. The additional `Gamma(m)d_s^(-m)` contributes `O(log s)` to the logarithm. The bounded-radius portion is only `O(s)` there. Both are negligible compared with `exp(as)/s`. Since `d_s->0`, shifting to `s+d_s` changes the asymptotic coefficient by `1+o(1)`.

Comparison with the Pauli lower bound forces

`exp(-b-1)/a^2 >=1/(4a)`, equivalently `b<=log(2/R)-1`.

If `b(r)->+infinity`, its pointwise envelope implies every fixed-offset envelope beyond a sufficiently large radius. Choosing a fixed offset violating the necessary bound gives a contradiction. No regularity or monotonicity of `b(r)` is required. In particular a coefficient greater than one of `log log r`, or any further positive divergent correction after the coefficient-one term, is ruled out under this density-envelope contract.

## 8. Remaining limits and concrete recommendation

Retain the endpoint theorem and coefficient-one iterated-log sharpness as internally audited mathematical results, with both input hashes and the moment addendum attached. They strengthen the pasted source. There is no need for a corrective proof patch within this audit's scope.

Retain explicit open status for the optimal constant offset, tight sufficient scale, historical priority, external correctness, efficient measurement compilation, and matched operational advantage. The conservative scale grows as `m^2(m+1)2^m`; the existence proof does not establish inexpensive noise or control.

No finite grid or simulation is a premise of this audit. The accompanying finite check evaluates only the rational Hessian margin, algebraic coefficient sum, and formula constants. The simplex, complex-domain, all-tail, moment, and asymptotic arguments above carry the analytic scope.
