# Finite positive angular dependencies for anisotropic Maxwell mixtures

## 1. Model and proposed scope

Let `nu_0` be a supplied independently sampleable law of real symmetric
3-by-3 matrices satisfying `a I <= Sigma_0 <= b I`, with `0<a<b`.
Initial velocities have density `f_0(v)=E G_{Sigma_0}(v)` and mean zero.
Consider the normalized homogeneous isotropic-cutoff Maxwell equation

`d phi(k)/dt = E_sigma phi((k+|k|sigma)/2) phi((k-|k|sigma)/2)-phi(k)`,

where sigma is uniform on the unit sphere. The theorem does not change this
kernel, allow spatial transport, or acquire `nu_0` from physical data.

For Haar `R in SO(3)`, set `A=(I+R)/2`, `B=(I-R)/2`. The collision gain is
the law of `A V_1+B V_2`; its Fourier arguments have the required uniform
sphere distribution. Conditional independent Gaussians remain Gaussian,
with covariance `A Sigma_1 A^T+B Sigma_2 B^T`. Since
`A A^T+B B^T=I`, the interval `[aI,bI]` is invariant. The usual measure
integral equation is unique (the gain is TV-Lipschitz). Thus the covariance
smoothing law gives exactly the specified Maxwell solution. This closure
is an ordinary Gaussian/random-linear-collision representation.

Put `c=(a+b)/2`, `h=(b-a)/2`, and `E=(Sigma-cI)/h`, so `-I<=E<=I`.
The collision operation on E is the same linear smoothing operation.
For a real unit direction n define

`m_q(n,t)=E (n^T E_t n)^q`, `m_0=1`.

It is an even polynomial of degree 2q on the sphere and has absolute value
at most one. Importantly, it need not be a radial constant or nonnegative
when q is odd.

## 2. The rotating marked generator

For fixed n, `U=|A^T n|^2` is uniform on `[0,1]`. With an independent
uniform azimuthal unit vector z perpendicular to n, the child directions are

`n_+=sqrt(U)n+sqrt(1-U)z`,
`n_-=sqrt(1-U)n-sqrt(U)z`.

They are orthogonal. Expanding the q-th power and integrating U gives
`binom(q,j) integral U^j(1-U)^(q-j) dU = 1/(q+1)` for each j.

The two nonseparating cases have total rate `r_q=2/(q+1)`. Their conditional
direction transition K_q selects `U~Beta(q+1,1)` and maps
`n -> sqrt(U)n+sqrt(1-U)z`. The separating rate is
`lambda_q=(q-1)/(q+1)`. For a separation, j is uniform on `1,...,q-1`,
`U~Beta(j+1,q-j+1)`, and the above pair of directions feeds independent
descendants with sizes j and q-j. Consequently

`d m_q/dt = r_q(K_q-I)m_q-lambda_q m_q+lambda_q G_q(m_1,...,m_(q-1))`.

This identity follows from the covariance gain, not a radial approximation.
Discarding K_q gives the wrong anisotropic law, including already at q=1.

## 3. Positive finite angular propagation

Let `J_q(s)=exp[s r_q(K_q-I)]`. It is the ordinary compound-Poisson zonal
Markov kernel. On a spherical harmonic of even degree `2l`, its eigenvalue is

`eta_(q,l)(s)=exp{r_q s [kappa_(q,l)-1]}`,

`kappa_(q,l)=(q+1) integral_0^1 u^q P_(2l)(sqrt(u)) du`.

The integral is rational and computed from Legendre polynomial coefficients.
The zonal eigenvalue statement is the Funk-Hecke formula / addition theorem.
It also follows directly by averaging a rotated harmonic over azimuth.

Let X be the squared cosine between n and an actual J_q(s) endpoint. Its
first q moments are determined exactly by the displayed eta's, by expanding
`x^j` in `P_0(sqrt(x)),...,P_(2j)(sqrt(x))`. For `s>0`, the actual law
has a positive absolutely continuous component on `(0,1)` (the event of
exactly one jump suffices). Hence all its finite Hankel forms are strictly
positive. Gaussian quadrature of order `ceil((q+1)/2)` produces positive
weights and nodes in `(0,1)` matching these q moments. One extra moment
may be computed for the Gaussian construction. At `s=0`, use `X=1`.

Select a node X with its positive quadrature weight and a fresh uniform
azimuth z; return `sqrt(X)n+sqrt(1-X)z`. This has EXACTLY the same action as
J_q(s) on every even spherical polynomial of degree at most 2q. It is not
claimed to have the same whole angular law. That weaker equivalence is
exactly what the consumer needs. Gaussian quadrature positivity is an
ordinary moment-problem theorem; this is its particular kinetic use.

For q=1 no quadrature is needed: on quadratic even functions J_1(s) equals
`exp(-s/2) Id + [1-exp(-s/2)] UniformSphere`.

## 4. A bounded anisotropic moment sample

Start a block `(q,n,t)`. For q=0 return one. For q>=2 draw a separating
waiting time of rate lambda_q; for q=1 the waiting time is infinite.
Propagate n by the finite angular rule for the smaller of this time and t.
If terminal, draw a fresh E_0 and return `(n^T E_0 n)^q`. Otherwise perform
the separating transition in Section 2 and multiply the two independent
child outputs with the reduced time. Call the result H_(q,n,t).

Then `|H|<=1` and `E H=m_q(n,t)`. To prove this, condition on the first
separation. The intervening operator is J_q. Induction on q establishes
that the post-separation expected function is an even polynomial of degree
at most 2q: normalization denominators in child directions cancel the
power weights before integration, or equivalently use the original
homogeneous covariance polynomial. Thus the finite angular replacement is
valid at every occurrence. Duhamel's formula gives the displayed generator
and initial condition. Uniqueness of the finite-dimensional inhomogeneous
linear equation at each q completes the induction.

There are at most q-1 separating events, 2q-1 visited blocks, and q initial
matrix draws for ANY finite t. The finite angular quadrature would give a
degree-dependent alternative, but it is unnecessary for expected cost.

**Simpler executed operation.** For every block q>=2, retain the actual
nonseparating rotations. Conditional on the separating wait S, simulate a
Poisson number of them with mean `r_q min(S,t)`. Their expected number is
at most `r_q/lambda_q=2/(q-1)<=2`. Each rotation draws `U~Beta(q+1,1)`.
For q=1 use the exact hold/uniform quadratic propagator in Section 3,
then terminate. Therefore the total expected number of actual angular
rotations is at most `2(q-1)`; total block visits and initial draws have
the deterministic bounds above. Initial powers can be computed in O(q)
total multiplications over terminal blocks. Work is O(q) in ideal random
primitive/arithmetic units, independent of elapsed time. Worst-case work
is unbounded. The Gaussian quadrature route is preserved as a derivation,
not used by the implementation or required by the result.

**Numerical qualification.** The simplified operation avoids moment-matrix
conditioning and algebraic roots. Exponentials, continuous random numbers,
and categorical decisions still have a real/bit distinction. A finite-bit
exact/quantized sampler and its expected bit-cost remain a distinct
interface. Floating executions below are diagnostics of the ideal theorem.

## 5. Complex-direction polarization

For fixed q,t define the homogeneous real polynomial
`F_q(z)=E (z^T E_t z)^q`, extended to complex z. If `z=u+iw` with
`||u||^2+||w||^2=1`, let `z_theta=u cos(theta)+w sin(theta)`. The highest
Fourier coefficient of this degree-2q polynomial gives the exact identity

`F_q(z)=4^q E_theta exp(2iq theta) F_q(z_theta)`.

Here theta is uniform on `[0,2pi]`, `||z_theta||<=1`, and
`F_q(z_theta)=||z_theta||^(2q) E H_(q,z_theta/||z_theta||,t)`.
Zero vectors are assigned zero when q>0. For q=0 return one.
Thus a bounded complex moment sample of magnitude at most `4^q` is
available with O(q) expected work. The factor 4^q is CHARGED below; no
multivariate classical probability representation is being assumed.

## 6. A bounded full-density-ratio sample

Assume now `b<7a/5`. With c,h as above put

`beta=c-4h=(5a-3b)/2>0`, `g=c+4h=(5b-3a)/2<2a`,
`C=(g/beta)^(3/2)`.

For a proposed velocity v, draw `xi~N(0,beta^(-1) I)` and set
`z=xi-i v/g`, `L=2h ||z||^2`. Draw `K~Poisson(L)` and a uniform theta.
For K>0 set `z_theta=Re(z/||z||) cos(theta)+Im(z/||z||) sin(theta)`;
draw the real-direction H of Section 4 at degree K, and return

`W(v)=C Re[(-1)^K exp(i[2K theta+(c/g-1)xi.v])
                 ||z_theta||^(2K) H]`.

For K=0, the last two factors are one. Then `|W(v)|<=C` uniformly over
v,t, and `E W(v)=f_t(v)/G_g(v)`.

Proof: Fourier inversion of a Gaussian covariance mixture is absolutely
integrable. Shift its contour to `xi-i v/g`; bounded covariance gives the
required entire extension and domination. Relative to G_g the resulting
Gaussian integral has prefactor

`(g/c)^(3/2) exp[-(g-c)|v|^2/(2g^2)]`

and phase `exp[i(c/g-1)xi.v]`. Expand
`exp[-(h/2) z^T E_t z]` and apply Section 5 at each degree. Poissonization
with mean L absorbs the factor `4^K (h||z||^2/2)^K/K!` and introduces
`exp[L]`. Its `exp[2h||xi||^2]` changes the frequency Gaussian precision
from c to beta. Its `exp[2h|v|^2/g^2]` cancels the prefactor's v decay
because `g-c=4h`. The remaining prefactor is exactly C. Absolute sums are
dominated by this broadened Gaussian, justifying Fubini. This derivation
is a contour/polarization construction, not the radial Laguerre formula.

## 7. Exact ideal one-particle sampler and full expected cost

Every covariance in `[aI,bI]` has density at least
`(2pi b)^(-3/2) exp[-|v|^2/(2a)]`. Hence

`R(v)=f_t(v)/G_g(v) >= ell(v)` where
`ell(v)=(g/b)^(3/2) exp[-|v|^2(1/a-1/g)/2]>0`.

A fresh W and a uniform random number give a p-coin with conditional
probability `(1-W/C)/2`, so `p=(1-R/C)/2`. Huber's credited linear factory
with multiplier 2 and known margin `ell/C` yields a 2p-coin using at most
`19 C/ell` input coins in expectation. Complement it. This is an acceptance
coin of mean `R/C`. Repeating iid proposals `v~G_g` therefore accepts with
probability 1/C and returns exactly f_t in the ideal real/random model.

The whole proposal/factory cost, including failures, is controlled by

`I = integral G_g(v)/ell(v) dv = [ab/(g(2a-g))]^(3/2) < infinity`.

Expected W queries per output are at most `19 C^2 I`. For one W query,
`E[K|v]=2h[3/beta+|v|^2/g^2]`; the fresh query's random cost can correlate
with its outcome, but whether it is requested depends only on previous
outcomes. The stopping/renewal argument therefore charges that mean cost
correctly. Under normalized `G_g/ell`, v is Gaussian with variance
`a g/(2a-g)`. Consequently

`E total degree <= 19 C^2 I * 6h [1/beta+a/(g(2a-g))]`.

Together with Section 4 this bounds all initial draws, separating events,
nonseparating rotations and arithmetic by a constant times
`C+19 C^2 I [1+6h(1/beta+a/(g(2a-g)))](1+c_0)`, where c_0 charges an
initial covariance draw. It is uniform over finite t, and deteriorates as
the admitted bracket approaches b=7a/5. It counts ideal real/random
primitives, not exact output bits, time-input bits, or native gas fitting.

Independent repetitions give iid one-particle samples only. No correlated
N-particle ensemble, molecular trajectory or path observable is supplied.
The condition b<7a/5 is sufficient for this receiver, not a no-go beyond it.
