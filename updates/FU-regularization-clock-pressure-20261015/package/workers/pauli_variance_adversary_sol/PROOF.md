# Independent adversarial audit of the Pauli variance gap

Task: reconstruct the covariance obstruction for the exact three-Pauli
contract, without assuming radial noise, densities, exponential moments, or
agreement with another derivation. All files in this folder are this worker's
output. The supplied source was `../../sources/regularization_pasted.txt`.

## Results and scope

Let `sigma=(sigma_1,sigma_2,sigma_3)` be the standard Pauli tuple. Suppose a
centered scalar probability measure `nu` on `R^3` has finite covariance
`Sigma`, and a normalized positive `2 x 2` operator measure `M` satisfies

\[
\widehat M(t)=\widehat\nu(t)e^{i t\cdot\sigma}\qquad(t\in\mathbb R^3).
\tag{1}
\]

This audit proves, with no radiality assumption,

\[
\boxed{\operatorname{tr}\Sigma\ge
\frac{121507}{16000}=7.5941875.}
\tag{2}
\]

Consequently, if `Sigma=v I`,

\[
\boxed{v\ge\frac{121507}{48000}\simeq2.531395833333.}
\tag{3}
\]

The final scalar inequality in this proof has an exact rational arithmetic
certificate: `certificate.py` and its successful receipt `CERTIFICATE.json`.
The certificate covers the whole half-line using Taylor enclosures,
curvature, and a tail estimate. It is not merely a finite sampled check.
The analytic reduction to this scalar inequality is given below. This is
not a proof-assistant formalization or a proof of the optimal constant.

The originally proposed gap

\[
\operatorname{tr}\Sigma-6\ge\frac{64}{9\pi^4}
\tag{4}
\]

is correct. The stronger Taylor gap `16/pi^3` is also correct. A separate
closed-form radius-only relaxation gives `(3 sqrt(5)-5)/2`; it is included
below because it identifies exactly what the Fourier zeros alone can prove.

This audit also constructs an admissible rank-one covariant POVM with

\[
\boxed{v=\frac{23}{9}-\frac{1}{9W_1}<\frac{23}{9},}
\tag{5}
\]

where a positive delay kernel defines the finite positive number `W_1`.
Non-certified numerical quadrature gives `W_1 approximately 5.09951192194`,
and hence `v approximately 2.53376697798`. The exact construction and its
strict improvement over `23/9` do not depend on those decimals.

An additional elementary exact arithmetic enclosure proves the rigorous
feasible upper bound

\[
\boxed{v<\frac{19529}{7707}\simeq2.533930193331<2.534.}
\tag{5a}
\]

See `construction_bounds.py` and `CONSTRUCTION_BOUND.json`. Consequently
the optimal isotropic variance, whether or not attained, lies in
`[121507/48000,19529/7707)`. The construction's more precise quadrature
decimal is not used as a rigorous endpoint.

Thus the certified lower bound and the new feasible construction leave a
small interval. No equality or optimality claim is made.

## 1. Measures, moments, and integrability

Use the Fourier convention `hat M(t)=integral exp(i t.x) M(dx)`. Put

\[
\mu(E)=\tfrac12\operatorname{tr}M(E).
\]

Then `mu` is a probability measure. Matrix Radon--Nikodym differentiation
gives a measurable Bloch vector `r(x)` with

\[
M(dx)=(I+r(x)\cdot\sigma)\mu(dx),\qquad |r(x)|\le1
\quad\mu\text{-a.e.}
\tag{6}
\]

This uses positivity of a qubit matrix, not a density relative to Lebesgue
measure. The trace of the derivative is two, so its eigenvalues are
`1+|r|` and `1-|r|`.

The moment integrals must be justified before differentiating (1). For a
unit direction `u` and a state with Bloch vector `v`, the scalar probability
measure `tr(rho_v M)` has directional characteristic function

\[
\widehat\nu(ku)\,[\cos k+i(v\cdot u)\sin k].
\]

It is therefore the convolution of the `u`-projection of `nu` with a
two-point law at `+1,-1`, of probabilities `(1+v.u)/2,(1-v.u)/2`.
Uniqueness of characteristic functions establishes this identity of
probability measures without any differentiability argument. Finite second
moments follow from the corresponding assumption on `nu`. In particular,
the three coordinate second moments of `mu` are finite; hence
`integral |x|^2 mu(dx)<infinity`. Since the matrix derivative in (6) is
bounded, all first and second operator moments are absolutely integrable.

The exact moment identities are

\[
\int x_jM(dx)=\sigma_j,\qquad
\int x_jx_kM(dx)=(\Sigma_{jk}+\delta_{jk})I.
\tag{7}
\]

One may obtain the mixed second identity by polarization of the directional
second moments, or by the Pauli anticommutator. There is no imaginary
commutator contribution: a classical product `x_j x_k` corresponds to the
symmetrized operator product, and
`(sigma_j sigma_k+sigma_k sigma_j)/2=delta_jk I`.
Taking Pauli coefficients in (7) gives

\[
\begin{split}
&E_\mu X=0,\quad E_\mu XX^T=\Sigma+I,\quad E_\mu r=0,\\
&E_\mu X_jr_k=\delta_{jk},\qquad
E_\mu X_jX_kr_\ell=0.
\end{split}
\tag{8}
\]

Only the first two lines of moment information used below require finite
second moments; no fourth or exponential moment is assumed.

Writing `R=|X|`, (8) implies

\[
E_\mu X\cdot r=3,\quad ER\ge3,\quad
ER^2=\operatorname{tr}\Sigma+3.
\tag{9}
\]

In particular `tr Sigma>=6`. Define

\[
a=ER-3\ge0,\qquad
\delta=ER^2-9=\operatorname{tr}\Sigma-6.
\]

Then

\[
E(R-3)^2=\delta-6a\le\delta.
\tag{10}
\]

For non-centered input noise of finite mean `m`, translate the outcome by
`-m` and the noise by `-m` first. The covariance is unchanged. Thus
centering is a choice of origin, not an isotropy hypothesis.

## 2. Audit of the proposed and Taylor gaps

The trace of (1) is

\[
\widehat\mu(t)=\widehat\nu(t)\cos|t|.
\tag{11}
\]

Therefore every point on the spheres `|t|=(n+1/2)pi` is a zero. Angular
averaging and bounded Fubini give

\[
E\operatorname{sinc}((n+\tfrac12)\pi R)=0,\qquad n\ge0,
\tag{12}
\]

where `sinc z=sin z/z` and `sinc 0=1`. This is valid for nonradial `mu` and
`nu`: the angular average is performed in frequency space.

For `f(r)=sinc(pi r/2)`,

\[
f(3)=-\frac{2}{3\pi},\qquad
|f'(r)|\le\frac\pi4.
\]

The derivative bound follows from `sinc x=integral_0^1 cos(xu) du` and
`|sinc'(x)|<=integral_0^1 u du=1/2`. Thus

\[
\frac{2}{3\pi}
=|Ef(R)-f(3)|
\le\frac\pi4 E|R-3|
\le\frac\pi4\sqrt\delta,
\]

which proves (4), including its constant.

The second derivative gives the stronger elementary bound. Directly,

\[
f'(3)=\frac{2}{9\pi},\qquad
f''(r)=-\frac{\pi^2}{4}\int_0^1u^2\cos(\pi ru/2)du
\le\frac{\pi^2}{12}.
\]

Global Taylor comparison, including `r<3`, gives

\[
0=Ef(R)\le -\frac{2}{3\pi}
+\frac{\pi^2}{24}\delta
+\left(\frac{2}{9\pi}-\frac{\pi^2}{4}\right)a.
\]

The coefficient of `a` is negative. Hence

\[
\delta\ge\frac{16}{\pi^3}.
\tag{13}
\]

Both arguments are rigorous but discard almost all of the vector-valued
Fourier contract.

## 3. The full scalar-vector Fourier constraints, without radiality

Define a signed measure `Q` on radii by

\[
Q(B)=\int_{|x|\in B,\,x\ne0}
\frac{x\cdot r(x)}{|x|}\,\mu(dx).
\]

Let `P` be the law of `R`. Then `|Q|<=P`, so `Q=qP` with `-1<=q<=1`;
choose `q(0)=0`. Equation (9) gives

\[
\int Rq(R)P(dR)=3.
\tag{14}
\]

Define

\[
A(k)=\int\operatorname{sinc}(kR)P(dR),\qquad
B(k)=\int j_1(kR)q(R)P(dR),
\]

where

\[
j_1(x)=\frac{\sin x-x\cos x}{x^2}
=\int_0^1u\sin(xu)du,\qquad j_1(0)=0.
\]

Angular averaging of the trace and of its spin component in (1) yields

\[
A(k)=\Phi(k)\cos k,\qquad B(k)=\Phi(k)\sin k,
\tag{15}
\]

where `Phi(k)` is the spherical average of `hat nu(k u)`. For the spin
identity use

\[
\frac1{4\pi}\int_{S^2}u e^{iku\cdot x}d\Omega(u)
=i j_1(k|x|)\frac{x}{|x|}.
\]

All integrands here are bounded, so this step uses no additional moments.
Consequently, for every real `k`,

\[
\int F_k(R,q(R))P(dR)=0,
\quad
F_k(R,q)=\sin k\,\operatorname{sinc}(kR)
-q\cos k\,j_1(kR).
\tag{16}
\]

This direct angular reduction avoids an implicit assumption that the
original noise or measurement was covariant. Equivalently, one could twirl
both over rotations; covariance trace would be unchanged.

## 4. A certified finite-frequency lower bound

Take `k_n=n pi/8`, `n=1,...,24`, and use the exact terminating decimal
coefficients `d_n` in `certificate.py`. Set

\[
\lambda=\frac{14587}{1000},\qquad
c=-\frac{33171}{1000},
\]

and

\[
h_q(R)=R^2-c-\lambda Rq
-\sum_{n=1}^{24}d_n F_{k_n}(R,q).
\tag{17}
\]

The certificate proves, over all `R>=0` and `-1<=q<=1`,

\[
h_q(R)\ge\frac{67}{16000}.
\tag{18}
\]

Here are the precise analytic ingredients checked in exact arithmetic.

1. `h_q` is affine in `q`. The two endpoints suffice. Using
   `|j_1(kR)|<=kR/3`,

   \[
   h_{-1}(R)-h_1(R)
   =2\lambda R-2\sum_nd_n\cos k_n\,j_1(k_nR)\ge0,
   \]

   because the certified upper bound on
   `sum |d_n cos k_n| k_n/3` is `11<lambda`.

2. For `h=h_1`, the integral formulas for `sinc,j_1` give

   \[
   |h''(R)|\le
   2+\sum_n|d_n|k_n^2
   (|\sin k_n|/3+|\cos k_n|/4)<36.
   \]

3. At every node `R=m/40`, `m=0,...,800`, exact rational Taylor enclosures
   certify `h(R)>7/1000`. Between adjacent nodes, the interpolation error is
   at most `36(1/40)^2/8`. Thus on `[0,20]`,

   \[
   h(R)\ge\frac7{1000}-\frac{36}{12800}
   =\frac{67}{16000}.
   \]

4. For `R>=20`, `|sinc|<=1` and `|j_1|<=1/2` give

   \[
   h(R)\ge R^2-\lambda R-c-110.
   \]

   This quadratic is increasing there and is `31431/1000` at `R=20`,
   so the same lower bound (18) holds in the entire tail.

The script brackets `pi` with rational bounds established from Machin's
formula and alternating arctangent series. Trigonometric evaluation first
reduces the phase exactly modulo `2pi`, then uses degree 33/32 Taylor
polynomials. Each grid value has an explicitly justified error at most
`10^-12`. All comparisons, error bounds, and coefficients are rational;
floats in the JSON receipt are display-only. No plot or finite search is
substituted for the continuum implication.

Taking expectations in (17), using (14) and (16), proves

\[
ER^2\ge c+3\lambda+\frac{67}{16000}
=\frac{169507}{16000}.
\]

Combining this with (9) proves (2)--(3). The weaker rounded statement
`tr Sigma>=7.59`, `v>=2.53` follows immediately.

The derivation only uses positivity, normalization, the exact Fourier
contract, and finite covariance. The coefficient search was numerical, but
the final displayed inequality and this certificate do not depend on the
optimizer, its grid, or any optimizer success flag.

## 5. A new feasible kernel with variance below the supplied Dickman law

The following is an exact mathematical construction, separate from the
lower bound. Define `w` by

\[
w(s)=1\quad(0\le s\le2),\qquad
2(s-1)w'(s)+w(s)+w(s-2)=0\quad(s>2).
\tag{19}
\]

Method of steps uniquely defines a continuous, piecewise smooth solution.
For example, on `[2,4]`,

\[
w(s)=\frac2{\sqrt{s-1}}-1.
\]

Differentiate the following difference using (19); its derivative is zero
and its value at `s=2` is zero:

\[
\boxed{2(s-1)w(s)=\int_{s-2}^{s}w(u)du\qquad(s\ge2).}
\tag{20}
\]

A first zero of `w` would contradict (20), since all earlier values in
that integral are positive. Therefore `w(s)>0` for every finite `s`.
Equation (19) now gives `w'(s)<0` for `s>2`. Equation (20) implies

\[
0<w(s)\le\frac{w(s-2)}{s-1}\qquad(s\ge2).
\tag{21}
\]

Iterating proves a factorial tail bound and hence
`integral exp(b s)w(s) ds<infinity` for every finite `b`. In particular all
the following integrals exist:

\[
W_j=\int_0^\infty s^j w(s)ds,\qquad C=\frac1{2W_1}>0.
\]

Let the radial noise radius have law

\[
K(ds)=2Cs w(s)ds,
\tag{22}
\]

and let its direction be uniform on `S^2`. This is a centered scalar
probability law with every exponential moment. Its directional marginal
density is the even function

\[
h(z)=C\int_{|z|}^\infty w(s)ds.
\tag{23}
\]

Define a radius law for the POVM by

\[
P(dr)=Cr[\,w(r-1)+w(r+1)\,]\,\mathbf1_{r\ge1}dr,
\tag{24}
\]

and use the usual rank-one covariant spin measurement,

\[
M(dr,dn)=P(dr)\,(I+n\cdot\sigma)\frac{d\Omega(n)}{4\pi},
\qquad X=rn.
\tag{25}
\]

Normalization follows directly:

\[
\int_1^\infty r[w(r-1)+w(r+1)]dr=2W_1,
\]

because `integral_0^2 (s-1)w(s)ds=0`. Positivity is immediate from (25).

It remains essential to verify the **exact** scalar multiplier, not only
the coordinate first moments. For every `r>0`, (19)--(20) and the constant
initial segment give

\[
\int_{|r-1|}^{r+1}w(s)ds=2r w(r+1).
\tag{26}
\]

For `0<r<1`, both endpoints are in `[0,2]` and this is just `2r=2r`.
For `r>=1`, it is (20) at `s=r+1`.

The scalar and spin parts of the `z`-projection of (25) have densities

\[
g(z)=\frac12\int_{r\ge|z|}\frac{P(dr)}r,\qquad
d(z)=\frac z2\int_{r\ge|z|}\frac{P(dr)}{r^2}.
\]

Here `P` vanishes below one. Differentiation, (23), and (26) give

\[
g(z)=\tfrac12[h(z-1)+h(z+1)],\qquad
d(z)=\tfrac12[h(z-1)-h(z+1)].
\tag{27}
\]

For the scalar identity, compare derivatives on `(0,1)` and `(1,infinity)`
and use their zero limits at infinity. For the spin identity compare the
derivatives of `d(z)/z` and
`[h(z-1)-h(z+1)]/(2z)`; (26) is precisely the equality needed. The
identities extend to negative `z` by even/odd symmetry and to zero by
continuity.

Thus the operator-valued directional marginal is

\[
h(z-1)\Pi_+\,dz+h(z+1)\Pi_-\,dz,
\]

where `Pi_+/-=(I+/-sigma_z)/2`. Its Fourier transform is
`hat h(k)(cos k I+i sin k sigma_z)`. Rotation covariance gives (1) for
every vector `t`. This proves exact positive regularization.

Integrating (19) against `s,s^2,s^3` on `[2,infinity)` and using the
constant initial segment gives

\[
W_1=2W_0-1,\qquad
W_2=5W_0-\frac83,\qquad
W_3=\frac{46}{3}W_0-8.
\tag{28}
\]

All boundary terms at infinity vanish by (21). Therefore the scalar noise
has isotropic variance

\[
v=\frac{W_3}{3W_1}
=\frac{23}{9}-\frac1{9W_1},
\]

which proves (5). It also gives `ER=3` and `ER^2=3+3v`. This construction
uses ancillary radius randomness added to the same covariant spin POVM as
the source's Dickman example. No additional quantum information or physical
advantage follows from lowering this representation's raw noise variance.

For the rigorous numerical upper bound (5a), the integrating-factor
solution of (19) on `[4,6]` gives

\[
w(6)=1+\frac{2-2\sqrt3+\operatorname{arcosh}2-
\operatorname{arcosh}4}{\sqrt5}.
\]

Equation (20) at six gives `integral_4^6 w=10 w(6)`. From (21), the
integral over `[6,infinity)` is at most

\[
2w(6)\left(1+\frac17+\frac1{7\cdot9}+\cdots\right)
\le\frac73w(6).
\]

The exact integral on `[0,4]` is `4 sqrt(3)-4`. Hence

\[
W_0\le4\sqrt3-4+\frac{37}{3}w(6)<\frac{3069}{1000}.
\]

The final strict inequality is enclosed using rational square-root brackets
and the positive series `log z=2 sum_{j>=0} y^(2j+1)/(2j+1)`,
`y=(z-1)/(z+1)`, with a geometric remainder bound. It does not use the
numerical ODE solution. It implies `W_1<2569/500` and then
`v<23/9-500/(9*2569)=19529/7707<2.534`.

Forward floating-point integration of (19) eventually creates artificial
negative values of size about `10^-17` after `s approximately 24`. The
positive integral identity (20) disproves their physical interpretation.
Those values are numerical cancellation, not a counterexample to this
construction. Numerical moment diagnostics are truncated before this
instability. Their decimal outputs are not rigorous interval bounds on
`W_1`.

## 6. Sharp closed-form bound for the radius-only zero relaxation

This optional result uses only `ER>=3` and (12), and is superseded by (2)
for the actual operator contract. It is useful for avoiding an incorrect
claim that a single Fourier zero, or even all the trace zeros, proves the
strong finite-frequency bound above.

Set

\[
s=\sqrt5,\quad y=(3+s)/2,\quad
\lambda_0=3+7/s,\quad c_0=-(25+27s)/10,
\quad G(r)=r^3-\lambda_0r^2-c_0r.
\]

For `theta in [0,1]`, put
`H(theta)=min{G(theta),G(2-theta)}`. Extend it to an odd, four-periodic
Lipschitz function `g` with `g(r+2)=-g(r)` by setting it equal to `H` on
`[0,1]` and to `H(2-r)` on `[1,2]`.

The following elementary identities prove `g(r)<=G(r)` for all `r>=0`:

\[
\begin{split}
G(a)+G(a+2)&=2(a+1-y)^2(a+1-2/s)\ge0\quad(a\ge0),\\
G(a)+G(4-a)&=A+(2\lambda_0-12)a(4-a)>0\quad(0\le a\le2),\\
G(r+4)-G(r)&=12r^2+(24-56s/5)r+A>0,
\end{split}
\]

where `A=26-58s/5>0`. The discriminant of the final quadratic is
`(96s-224)/5<0`. These verify every combination of the two positive and two
negative branches in one period and then every later period.

The odd antiperiodic Fourier expansion of `g` only contains the frequencies
`(n+1/2)pi`. Fejer approximants `g_N` retain this property, remain odd and
uniformly Lipschitz, and converge uniformly to `g`. Each
`E[g_N(R)/R]=0` by (12), with the value at zero interpreted as `g_N'(0)`.
The quotients are uniformly bounded by the Lipschitz constant. Since `g`
is smooth near zero, `g_N'(0)` tends to `g'(0)` as well. Dominated
convergence gives

\[
E[g(R)/R]=0.
\]

Dividing `g<=G` by `r` and using its continuous limiting value at zero gives

\[
ER^2\ge\lambda_0ER+c_0\ge3\lambda_0+c_0
=\frac{13+3\sqrt5}{2}.
\tag{29}
\]

This radius-only bound is sharp. Put `a=y-1=(1+sqrt5)/2` and let `R` take
the values `a,a+2` with probabilities proportional to those radii. Then
`ER=3`, every constraint (12) holds, and equality holds in (29).
Its trace transform is

\[
E\operatorname{sinc}(kR)=\cos k\operatorname{sinc}(yk).
\]

This scalar extremizer does **not** by itself produce a positive exact
POVM. If it did, `ER=3` would force the rank-one alignment `q=1`. The cubic
coefficient of the spin Fourier identity would then require
`ER^3=5(1+y^2)=15y`, whereas the two-shell law has `ER^3=13y`.
This is a direct contradiction. No theorem about attainment or the full
operator optimum is inferred from this scalar relaxation.

## Reproduction and limits

Run `python3 certificate.py` in this folder for the exact continuum
certificate. It requires only the Python standard library. `EXPLORATION.json`
records the numerical LP from which the coefficients were proposed; that
file is explicitly not a certificate. `numerical_checks.py` and its JSON
receipt record optional quadrature/transform diagnostics for the delay
construction and the constants.
Run `python3 construction_bounds.py` for the rigorous feasible upper
bound, also using only the standard library.

The lower bound is an exact internally reconstructed mathematical proof
with an exact arithmetic auxiliary inequality. The upper construction is
an analytic existence proof with non-certified decimal diagnostics. Neither
establishes historical originality, formal verification, a hardware
implementation, an exact optimum, or quantum-information advantage.
