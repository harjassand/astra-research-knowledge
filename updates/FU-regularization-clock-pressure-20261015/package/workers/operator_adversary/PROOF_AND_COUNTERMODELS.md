# Independent adversarial reconstruction: operator regularization

Scope: internal analytic reconstruction from the supplied pasted transcript only. The referenced audit ZIP, PROOF.md, CHECKPOINT.md, and original checks were not supplied or read. No external correctness certification, formal proof, hardware validation, or historical priority clearance is claimed. This worker did not read the concurrent construction or priority workers' results before writing this file.

Input SHA-256: `b7c6fbecc52be279efb784bf895610dda249c6f22436fc4bb2cb7f72f60490dd` (`sources/regularization_pasted.txt`). Capital checkout pin: `0c789ca775808e23e57138b56a393ad1e58cb15c`. Source statements are data; all arguments below are reconstructed here.

## Findings

1. Necessity of pointwise coercive real Laplace transforms is proved below, including nonsmooth scalar noise, weak POVMs, nonseparable Hilbert spaces, and actual exponential moment passage uniformly over vectors. An elementary cutoff argument removes the need to infer moments from analytic continuation.
2. The universal bounded-operator compact Wigner construction and its dimension-independent remote-tail bound survive reconstruction. This file does not independently rebuild the abstract adaptive-ramp sufficiency proof for arbitrary coercive transforms; the full abstract equivalence still needs that separate construction audit.
3. The strict-versus-coercive counterexample survives. A simpler scalar three-atom limiting example explains the necessity of excluding zero Laplace transforms. Weak POVMs must not be silently promoted to norm-additive vector measures.
4. The Pauli cumulant obstruction survives, with the domain `s > 0` stated explicitly. The pasted equation for `K'(s)` is not literally valid for negative `s`; its tail use is unaffected.
5. The Dickman qubit transform, state-independent radius, exact equivalence to the covariant measurement, and classical truncation bound survive analytic derivation.
6. A further finite-variance obstruction is obtained: for the three Pauli observables with unit directional radius, every exact positive scalar convolution has `tr Cov(nu) >= 6 + 16/pi^3`. Radial coordinate variance is at least `2 + 16/(3 pi^3)`, approximately `2.17201`. This strengthens the source's second-moment Clifford lower bound for this contract. Novelty is UNKNOWN. It is a resource lower bound, not a capability.

## 1. Exact hypotheses and elementary cutoff lemma

Let `H` be any complex Hilbert space. Let `T` be a compactly supported distribution with values in the Banach space `B(H)`, continuous for the test-function topology into operator norm. Assume `T(f)` is self-adjoint for real `f`, and `T(1)=I`; values on arbitrary smooth functions mean evaluation after multiplying by any cutoff equal to one on a neighborhood of the support.

Compact support and norm continuity give a compact neighborhood `K`, a finite order `N`, and `C < infinity` such that

`||T(h)|| <= C max_{|alpha|<=N} sup_{y in K} |partial^alpha h(y)|`.

Enlarge `K` into a ball `B_a`. A fixed cutoff used to define the extension can be absorbed into `C` and `N`.

Let `nu` be a scalar Borel probability measure. For `f in C_c^infinity`, define the convolution by

`(T*nu)(f) = integral T_y[f(y+z)] nu(dz)`.

This is a genuine Bochner integral in `B(H)`: the integrand is norm-continuous in `z`, has separable range because `R^m` is separable, and is norm-bounded by the finite-order estimate. No separability of `H` or of `B(H)` is required. Compactness of the support of `f` is not needed for the boundedness of its derivatives, but is the distributional testing convention.

Suppose this convolution agrees on compactly supported smooth tests with a positive weakly countably additive operator measure `M`. Normalization can be assumed, or obtained from the argument at `g=0` below.

Choose a radial smooth function `chi` with `0 <= chi <= 1`, equal to one on `B_1`, zero outside `B_2`, and nonincreasing in the radial argument. For real `g` and `r >= 1`, set

`f_r(x) = exp(g.x) chi(x/r)`.

Then `f_r` is a positive compactly supported smooth test, and `f_r(x)` increases pointwise to `exp(g.x)` as `r` increases. For every `z`,

`T_y[exp(g.(y+z)) chi((y+z)/r)] -> exp(g.z) H_T(g)`

in operator norm, where `H_T(g)=T(exp(g.y))`. In fact, for fixed `z` and sufficiently large `r`, the cutoff is identically one on a neighborhood of `K`, making the equality exact.

Every derivative of `chi(x/r)` of order at most `N` is bounded uniformly for `r >= 1`. Leibniz's rule and `y in B_a` therefore give the uniform majorant

`||T_y[f_r(y+z)]|| <= C_g exp(g.z)`,

where one may take `C_g = C' exp(a|g|) (1+|g|)^N`, independent of `r`, `z`, and vectors in `H`.

Consequently, whenever the single exponential moment `m_nu(g)=integral exp(g.z)nu(dz)` is finite, Bochner dominated convergence gives

`M(f_r) -> m_nu(g) H_T(g)` in operator norm.  (1)

For any vector `v`, the scalar measure `mu_v(E)=<v,M(E)v>` is positive. Scalar monotone convergence, applied to exactly the same cutoffs, yields

`integral exp(g.x) mu_v(dx) = m_nu(g)<v,H_T(g)v>`.  (2)

This proves actual moment integrability, rather than merely a formal analytic continuation identity. For unit vectors,

`sup_{||v||=1} integral exp(g.x) mu_v(dx) = ||m_nu(g)H_T(g)|| < infinity`.

The operator on the right is positive because it is a norm limit of positive cutoff integrals. The weak exponential integral is therefore a bounded positive operator and (1) is also its cutoff norm limit.

At `g=0`, the majorant is constant and no exponential assumption is needed. The limit is `I`, so positivity of the convolution already forces `M(R^m)=I`. If one starts only with positivity of the operator-valued distribution, scalar positive distributions produce Radon measures; the common bound by `I` then reconstructs the normalized weak POVM by polarization. This optional strengthening does not assume norm countable additivity.

The same reasoning works for polynomially weighted cutoffs if `nu` has the corresponding ordinary moments: derivatives of `x^alpha chi(x/r)` have a uniform majorant of the form `C(1+|z|^d)`, and converge locally to the polynomial. This fact is used in Section 6, which needs only finite second moments.

## 2. Necessity, coercivity, and the precise infinite-dimensional issue

Assume both `m_nu(g)` and `m_nu(-g)` are finite. Equations (1)-(2) establish bounded positive operators

`Q_+(g)=m_nu(g)H_T(g)` and `Q_-(g)=m_nu(-g)H_T(-g)`.

For every unit vector `v`, Cauchy-Schwarz in the probability measure `mu_v` gives

`1 = (integral exp(g.x/2) exp(-g.x/2) mu_v(dx))^2`

`  <= <v,Q_+(g)v><v,Q_-(g)v>`.

Thus `Q_-(g)` is nonzero, and

`Q_+(g) >= ||Q_-(g)||^{-1} I`.

Equivalently,

`H_T(g) >= [m_nu(g)m_nu(-g)||H_T(-g)||]^{-1} I`.  (3)

This is pointwise coercivity in operator norm. The lower bound can depend on `g`; there is no asserted single lower bound for all tilts. The proof is valid for nonsmooth `nu`, weak POVMs, and nonseparable `H`. It uses no entire continuation, no interchange with an unbounded distributional test, and no finite-dimensional approximation.

In particular, all exponential moments of `nu` imply coercivity of `H_T(g)` for every real finite `g`. A stronger local statement holds: moments at the two particular tilts `+g,-g` suffice for coercivity at `g`. Uniform radial exponential moments of `M` follow too, since for `b>0`,

`exp(b|x|) <= sum_{epsilon in {-1,1}^m} exp(b epsilon.x)`.

The finite sum of the bounded positive exponential moment operators bounds all unit-vector integrals uniformly.

### 2.1 Strict quadratic-form positivity is insufficient

On `ell^2(N)`, use the source's diagonal measure with entries

`T_n = [(1/16)delta_2 + delta_{-2} + (-1/2+1/n)delta_0]/(9/16+1/n)`.

The coefficients are uniformly bounded, the common support is `{-2,0,2}`, and each entry has total mass one. Its Laplace transform is diagonal with entries

`H_n(g) = [sinh^2(g-log 2)+1/n]/(9/16+1/n)`.

For every nonzero `v`, `<v,H_T(g)v> > 0`: every nonzero coordinate contributes a strictly positive term. However,

`H_n(log 2)=16/(9n+16) -> 0`.

So `H_T(log 2)` has zero lower spectral bound. Formula (3) rules out any common positive convolution whose scalar noise has exponential moments at both `+log 2` and `-log 2`, and hence rules out every all-exponential regularizer.

This is not a counterexample to the claimed coercive criterion. It is a counterexample to replacing coercivity by positivity on each nonzero vector. It is independent of finite truncation experiments.

The one-dimensional scalar limiting measure

`T_infinity = (1/9)delta_2 + (16/9)delta_{-2} - (8/9)delta_0`

already has `H(g)=(16/9)sinh^2(g-log 2) >= 0` with a zero at `log 2`, and is therefore not regularizable with exponential moments at the two tilts. Three atoms are enough to show why nonnegative real Laplace transforms are inadequate; a two-atom normalized scalar signed measure with a negative coefficient fails nonnegativity in one tail.

### 2.2 Weak exponential integrals are not Bochner vector-measure integrals

Let `P_n` be the coordinate projections on `ell^2(N)`, and define

`M = sum_{n>=1} P_n delta_{1/n}`,

with the sum interpreted weakly or strongly. This is a normalized POVM with compact support. It is also a compact, norm-continuous distribution: `T(f)=diag(f(1/n))`, with order-zero estimate `||T(f)|| <= sup_{[0,1]}|f|`. Choose `nu=delta_0`.

All exponential moment operators are the bounded, coercive diagonal operators `diag(exp(g/n))`; actual moments are uniform over vectors. Yet `sum P_n` does not converge in operator norm, since the norm of every tail is one. Thus `M` is not a norm-countably additive `B(H)`-valued vector measure and has infinite operator-norm total variation.

The cutoff proof does not claim otherwise. Its Bochner integral is over translated distribution tests against scalar `nu`, and its exponential integral against `M` is weak. A smooth norm-integrable density is a separate feature of the constructive sufficiency theorem.

## 3. Universal bounded-operator Wigner estimate

Let `A_j` be bounded self-adjoint operators with `||A(u)|| <= R|u|`, `A(u)=sum u_j A_j`, and `R>0`. Use the Fourier convention `hat h(t)=integral exp(-it.y)h(y)dy` and define

`W_A(h)=(2pi)^{-m} integral hat h(t) exp(iA(t))dt`.

This convention has `W_hat_A(t)=exp(iA(t))`. The integral is Bochner integrable in operator norm because `||exp(iA(t))||=1`, and its integrand is norm continuous with separable range. Therefore

`||W_A(h)|| <= (2pi)^{-m}||hat h||_1`.  (4)

For complex `t+is`, the Hermitian part of `iA(t)-A(s)` is `-A(s)`. If `u(q)=exp(q[iA(t)-A(s)])v`, then

`d||u(q)||^2/dq = -2<u(q),A(s)u(q)> <= 2R|s|||u(q)||^2`.

Gronwall gives `||exp(iA(t)-A(s))|| <= exp(R|s|)`. Scalar Paley-Wiener-Schwartz applied to every matrix coefficient implies `supp W_A subset closed B_R`. Matrix coefficients separate operators, so scalarization loses no operator support information. This use of the classical theorem is an explicit standard ingredient, not a new support theorem.

The Fourier-Laplace transform of a compact distribution is entire. Equality on real arguments with `exp(iA(t))`, continued coordinate by coordinate, gives

`W_A(exp(g.y))=exp(A(g))`.

For a fixed smooth cutoff `chi` supported in `B_a`, equal to one near `B_R`, take an integer `k>m/2`, `N=2k`. Integration by parts gives

`|hat(chi h)(t)| <= (1+|t|^2)^(-k)||(1-Delta)^k(chi h)||_1`.

The right side is integrable in `t`, and a product-rule estimate gives

`||W_A(chi h)|| <= C(m,a,R,chi,N)||h||_{C^N(B_a)}`.  (5)

The constants are scalar and independent of the Hilbert-space dimension and of the tuple inside the specified directional norm ball.

### 3.1 Remote tails and the inverse-conditioning factor

Set `rho(s)=sqrt(1+s^2)`, `f(s)=rho(s)log rho(s)`, `V_L(x)=cL f(|x|/L)`, and `p_L=Z_L^{-1}exp(-V_L)`. For `s>=0`,

`f'(s)=s(1+log rho(s))/rho(s)` and `f''(s)=1/rho(s)+log rho(s)/rho(s)^3 > 0`.

The tangential Hessian eigenvalue is `(1+log rho(s))/rho(s)>0`, with its continuous value at zero. Thus `V_L` is smooth and strictly convex.

Let `h(s)=1+log(1+s)` and `g=grad V_L(x)`. Then `|g|<=c h(s)`, `s=|x|/L`. For every fixed finite derivative order `j>=2`, radial differentiation gives

`|D^j f(z)| <= C_j h(|z|)/(1+|z|)^(j-1)`.

This estimate follows by differentiating the radial expression: derivatives of `sqrt(1+|z|^2)` have orders at most `(1+|z|)^(1-j)`, while each derivative of its logarithm removes one power. It also holds near zero by smoothness and compactness.

For `L>=max(1,2a)` and `|y|<=a`, the scales `1+|x-y|/L` and `1+s` differ by at most fixed factors. Define

`F_x(y)=V_L(x-y)-V_L(x)+g.y`.

Taylor's formula for its zeroth and first derivatives, and the preceding derivative estimates for higher derivatives, give

`||F_x||_{C^N(B_a)} <= C_0 L^(-1) h(s)/(1+s) =: eta(s)`.

Since `h(s)/(1+s)<=1`, `L>=C_0` ensures `eta<=1`. Finite-order chain/product rules then yield

`||exp(-F_x)-1||_{C^N(B_a)} <= C_N eta(s)`.

The exact identity `p_L(x-y)=p_L(x)exp(g.y)exp(-F_x(y))` gives

`(W_A*p_L)(x)/p_L(x)=exp(A(g))+E_x`,

and (5) gives `||E_x|| <= C eta(s) exp(a|g|)(1+|g|)^N`.

Both inverse square roots together cost `||exp(-A(g)/2)||^2 <= exp(R|g|)`. Therefore

`||exp(-A(g)/2)E_x exp(-A(g)/2)||`

` <= (C'/L) h(s)^(N+1)(1+s)^(-alpha)`,

where `alpha=1-c(R+a)`.

If `0<c<1/(2R)`, select `R<a<1/c-R`; then `alpha>0` and the displayed scalar factor is bounded for all `s>=0`. A sufficiently large finite `L`, depending only on the scalar parameters, makes the relative error at most any prescribed `epsilon in (0,1)`. Self-adjointness gives the two operator-order bounds in the source uniformly at every `x`.

This is an analytic all-tail estimate. No finite grid is used. The inverse-conditioning factor is essential and has not been discarded.

The positive density is norm continuous and is dominated by `(1+epsilon)p_L(x)exp(R|grad V_L(x)|)`, an integrable superexponential density times a polynomial in `1+|x|`. It is therefore Bochner integrable even on a nonseparable Hilbert space. Its Fourier transform at zero is `I`, so its integral is `I`. The construction is for bounded observables only.

## 4. Pauli cumulant obstruction, with the tilt domain explicit

Suppose a two-coordinate scalar noise has every exponential moment and `M_hat(t)=nu_hat(t)exp(i[t_1 A+t_2 B])` is positive. The cutoff lemma, also with polynomial factors, gives actual tilted first and second moment operators. Normalize the measure tilted by `exp(s x_1)` by conjugating with `exp(-sA/2)` and dividing by `m_nu(s,0)`.

Let `kappa(s,t)=log m_nu(s,t)` and

`K_l(s)=exp(-sA/2) [partial_t^l exp(sA+tB)]_{t=0} exp(-sA/2)`.

The normalized first and second moment operators in the second coordinate are

`Q_1=kappa_2 I+K_1`,

`Q_2=(kappa_22+kappa_2^2)I+2kappa_2 K_1+K_2`.

Positivity of the quadratic moment block gives `Q_2-Q_1^2 >=0`, hence

`kappa_22(s,0)I+K_2-K_1^2 >=0`.  (6)

For `A=R sigma_z`, `B=R sigma_x`, and `s>0`, direct differentiation of

`exp(sA+tB)=cosh(R sqrt(s^2+t^2))I + sinh(R sqrt(s^2+t^2))(s sigma_z+t sigma_x)/sqrt(s^2+t^2)`

gives

`K_1=(sinh(Rs)/s)sigma_x`,

`K_2-K_1^2=diag(-d_R(s),d_R(s))`,

`d_R(s)=[sinh(2Rs)-2Rs]/(2s^2)>0`.

Thus `kappa_22(s,0)>=d_R(s)`. For radial noise, write `K(s)=log m_nu(s,0)`. Radial differentiation gives `kappa_22(s,0)=K'(s)/s`, so

`K'(s)>=[sinh(2Rs)-2Rs]/(2s)` for `s>0`.  (7)

For negative `s`, the correctly symmetric version is `K'(s)/s >= |d_R(s)|`. The source's displayed equation for `K'(s)` must be read with `s>0`; as a claim for all real `s` it would be false by parity. The intended large-positive-tilt tail obstruction is unaffected.

Integrating (7) over a unit interval near large `s` shows `K(s)>=C_R exp(2Rs)/s` eventually. If a radial density were bounded above by `C exp(-c_0 r log r)` with `c_0>1/(2R)`, choose `1/(2R)<c'<c_0`. Then

`sup_{r>0}[sr-c' r log r]=c' exp(s/c'-1)`,

and absorb the radial Jacobian and the remaining tail into an integrable factor. This gives `K(s)<=C+c'exp(s/c'-1)`, contradicting the lower exponential rate. Combined with Section 3, the admissible universal radial tail coefficients have supremum `1/(2R)`; endpoint attainment is not proved.

If the two noise coordinates were independent, `kappa_22(s,0)` would be the fixed second-coordinate variance, contradicting unbounded `d_R(s)`. Dependence is mathematically essential for the exact all-exponential Pauli contract.

## 5. Dickman qubit construction, equivalence, and truncation

Let `V_j=U_j^2`, with iid uniform `U_j`, and `D=sum_{k>=1} product_{j<=k}V_j`. Since `EV=1/3`, the series has mean `1/2` and is finite almost surely. The variables `-log V_j` are iid exponential waiting times of rate `1/2`, so `D` is the sum of `exp(-s)` over the points of a rate-`1/2` Poisson process on `(0,infinity)`. The finite-interval Poisson Laplace formula, followed by monotone convergence for positive real arguments, gives

`F(z)=E exp(zD)=exp[(1/2) integral_0^1 (exp(zu)-1)/u du]`.

The integral defines an entire function, the positive real values are finite, and complex continuation is justified by those exponential moments. Also

`F'(z)=[(exp(z)-1)/(2z)]F(z)`.

These are established generalized Dickman/perpetuity ingredients; see the primary paper [Bhattacharjee and Goldstein](https://arxiv.org/abs/1706.08192). The following transform calculation is reconstructed independently.

Let `C=BU` with independent fair Bernoulli `B` and uniform `U`; let `S=1+2(D+C)`. Let `Y` have the mixture law `U` with probability `1/4`, `1+U` with probability `1/4`, and `1` with probability `1/2`, independent of `D`; let `R_*=2(D+Y)`.

Write `H(k)=exp(ik)F(2ik)`. The characteristic function `G(k)=E exp(ikS)` satisfies `H'(k)=2iG(k)`. A uniform-sphere scalar noise `Z=S omega` consequently has radial transform

`phi(k)=E sinc(kS)=k^(-1) integral_0^k Re G(v)dv = Im H(k)/(2k)`,

with `phi(0)=1` by continuity.

Perform the covariant qubit POVM `N(dn)=(I+n.sigma)dOmega/(4pi)`, independently choose `R_*`, and report `X=R_*n`. Its characteristic operator is

`A(k)I+iB(k)t_hat.sigma`,

where `A(k)=E sinc(kR_*)`, `B(k)=E j_1(kR_*)`, and `j_1(z)=sin(z)/z^2-cos(z)/z`.

The radial characteristic function `J(k)=E exp(ikR_*)` is

`J(k)=F(2ik)[(exp(4ik)-1)/(8ik)+(1/2)exp(2ik)]`

`     =(1/(2i)) d[H(k)cos k]/dk`.

Using `sinc(z)=integral_0^1 cos(uz)du` gives

`A(k)=k^(-1) integral_0^k Re J(v)dv=phi(k)cos k`.

Using `j_1(z)=integral_0^1 u sin(uz)du` gives

`B(k)=k^(-2) integral_0^k v Im J(v)dv`.

Integration by parts and the identity

`integral_0^k cos v Re H(v)dv = k Re F(2ik)`

give `B(k)=phi(k)sin k`. The identity follows by differentiating its right side and substituting the displayed differential equation for `F`. Thus

`M_hat(t)=phi(|t|)exp(i t.sigma)`.

All exponential moments of both radii follow from those of `D`; this construction is a scalar convolution with all exponential moments. It is not a replacement for the smooth universal density in Section 3.

### 5.1 Exact information comparison

The radius `R_*` is independent of the state and is positive almost surely. Therefore the map `X -> X/|X|` recovers `n` almost surely, and an independent radius draw maps `n` back to `X`. The two quantum measurement experiments are exactly related by classical channels in both directions.

No statistical decision task gains quantum information from the new radius. The covariant qubit measurement can itself be implemented by choosing a uniform axis `a`, measuring `a.sigma` projectively, and reporting `n=(outcome)a`.

The moments are obtained from `ED=1/2`, `Var D=1/4`, `EY=1`, `Var Y=1/6`, `EC=1/4`, and `Var C=5/48`:

`ER_*=3`, `ER_*^2=32/3`, `ES^2=23/3`, `Cov Z=(23/9)I`.

For a unit direction, `E(u.X)^2=32/9`. The existing unbiased score `3n` has second moment `3`, giving the source's ratio `32/27`; this is a raw-score comparison. Exact experiment equivalence is the stronger no-advantage statement.

The phase of `H(k)` is `theta(k)=k+(1/2)Si(2k)`. Its derivative is `1+sin(2k)/(2k)>0` for positive `k`, and it tends to infinity. The modulus of `H` never vanishes, so `phi(k)` has infinitely many positive zeros. Raw Fourier deconvolution fails at those zeros, while the bounded score `3X/|X|` still decodes the Bloch vector. These are different statistical assertions.

### 5.2 Total-variation truncation, analytically

Set `D_0=0` and `D_N=sum_{k=1}^N product_{j<=k}V_j`. There is a monotone coupling with `E(D-D_N)=(1/2)3^(-N)`.

Conditional on a nonnegative input `a`, the perpetuity kernel `V(1+a)` has density

`q_a(x)=[2 sqrt(1+a) sqrt(x)]^(-1) 1_{0<x<1+a}`.

For `0<=a<=b`, the densities cross once at the smaller support endpoint, and direct integration gives

`TV(q_a,q_b)=1-sqrt((1+a)/(1+b)) <= (b-a)/2`.

Apply this kernel to the monotone coupled inputs `D_{N-1}` and `D`. Convexity of total variation under mixing gives, for `N>=1`,

`TV(D_N,D) <= (1/2)E(D-D_{N-1}) = (1/4)3^(-(N-1))`.

Any common classical randomization and subsequent quantum measurement channel contracts this bound, so it holds uniformly over input states for the output approximation using `D_N`.

This statement is in ideal real arithmetic. A discrete finite-bit output and an unrounded continuous target have total variation one; common rounding, arithmetic accuracy, gate error, and tail handling require their own contract.

## 6. New resource refinement: exact Pauli convolution has a variance gap

This result is an internal analytic consequence of the exact convolution contract. It does not require all exponential moments, radial noise, or the Dickman construction. Novelty is UNKNOWN.

Take `A_j=sigma_j`, `j=1,2,3`. Suppose a scalar probability law `nu` has finite covariance and a normalized positive POVM satisfies

`M_hat(t)=nu_hat(t)exp(i t.sigma)`.

Translate the output and noise by the noise mean. The contract and covariance are unchanged, so assume the scalar noise is centered. The polynomial cutoff lemma makes the actual first and second moment identities valid with only finite second noise moments.

Every qubit POVM has the Radon-Nikodym form

`M(dx)=mu(dx)[I+r(x).sigma]`,

where `mu=(1/2)Tr M` is a probability measure and `|r(x)|<=1` almost everywhere. This follows from positivity and the scalar trace dominating every matrix component in dimension two.

The first moment identities give `integral x_j r_k(x)mu(dx)=delta_{jk}`. Therefore, with `Q=|X|` under `mu`,

`EQ >= integral x.r(x)mu(dx)=3`.

The second moments give `EQ^2=tr Sigma+3`, where `Sigma=Cov(nu)`. Write

`a=EQ-3>=0`, `delta=EQ^2-9=tr Sigma-6`,

so `E(Q-3)^2=delta-6a`.

The scalar characteristic function of `mu` is `nu_hat(t)cos|t|`. It vanishes for every direction at `|t|=k=pi/2`. Averaging over directions and interchanging bounded integrals gives

`E f(Q)=0`, where `f(q)=sinc(kq)`.

At `q=3`,

`f(3)=-2/(3pi)`, `f'(3)=2/(9pi)`.

Since `f(q)=integral_0^1 cos(kqu)du`,

`f''(q)=-k^2 integral_0^1 u^2 cos(kqu)du <= k^2/3=pi^2/12`

for every real `q`. Taylor's inequality therefore gives

`f(q) <= -2/(3pi) + [2/(9pi)](q-3) + (pi^2/24)(q-3)^2`.

Taking expectations,

`0 <= -2/(3pi) + (pi^2/24)delta + [2/(9pi)-pi^2/4]a`

`  <= -2/(3pi) + (pi^2/24)delta`,

because the coefficient of `a>=0` is negative. Hence

`tr Sigma >= 6 + 16/pi^3`.  (8)

For radial noise `Sigma=vI`, this is

`v >= 2 + 16/(3pi^3) = 2.1720...`.  (9)

For `A_j=R sigma_j`, multiply (8)-(9) by `R^2`. For universal radial regularizers with `m>=3` and directional radius `R`, restriction to this Pauli triple also forces (9) on each coordinate. The bound is not claimed optimal, and no matching construction is supplied.

The weaker first-pass bound `tr Sigma >= 6+64/(9pi^4)` follows from `|sinc'|<=1/2` and Cauchy-Schwarz. It was reported during discovery, then superseded by the Taylor bound (8). Both are analytic arguments; numerical checks only evaluate constants.

## 7. Operational and audit boundaries

The qubit exact representation is completely implemented at the ideal measurement-and-classical-randomization level, but is experiment-equivalent to the existing covariant qubit measurement. Its scalar radius cannot improve information. Section 6 adds a cost restriction specific to the exact all-linear scalar-convolution contract.

For arbitrary bounded tuples, Section 3 produces an abstract POVM. No efficient circuit, all-observable hardware operation, favorable precision cost, acquisition method, or advantage over a matched known joint/IC measurement has been derived here. Existence of the Naimark isometry `psi -> M(x)^(1/2)psi` does not supply a measurement compiler. A candidate benefit beyond existing covariant postprocessing remains NOT_ESTABLISHED.

The abstract necessity direction is complete at its stated hypotheses. The source's abstract sufficiency ramp construction is absent from the supplied file, so the full equivalence must not be certified by this worker alone. The bounded-operator Wigner sufficient construction is reconstructed separately above.

Primary source pointers inspected during this independent audit: [Schwonnek and Werner, generalized Wigner distribution](https://arxiv.org/abs/1802.08343) (search abstract only; attempted HTML fetch failed), [Bhattacharjee and Goldstein, Dickman approximation](https://arxiv.org/abs/1706.08192) (abstract), and [Sabbagh et al., particle approximations](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.7.013102) (publisher abstract and references). The latter is about signed particle approximations and supplies no certification of the new characterization. No claim about uninspected full-text contents is made.

Saved finite checks are supplementary algebra/constant diagnostics only. They do not verify the infinite-dimensional theorem, arbitrary tail inequalities, historical priority, or physical utility.
