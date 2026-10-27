# A coercive Stein correction with a proved smoothed full-law bound

27 October 2026. Independent mathematical audit and extension within this chat.
This is an analytic construction, not an acquired value-query sampler. The
frozen sources are unchanged. No historical novelty claim is made.

The governing opening is S3, sections 16–18 of the frozen packet. That source
has a formal positive Newton identity and an unbounded source-derivative
obstruction for a baseline Gaussian inverse. The construction below uses a
different inverse, allows globally rather than conditionally centered
corrections, and proves an actual one-step smoothed total-variation estimate.

## 1. Setting and conventions

Let Q have standard Gaussian law gamma_n. Rowwise Gaussian divergence is the
closed adjoint of the weak gradient:

    delta v = Q dot v - div v,
    E[delta v f] = E[v dot Df].

Let X: R^n -> R^d be square integrable, with mean mu. Let B be a d by n
matrix field whose rows are in the divergence domain and satisfy

    delta B = X - mu.

Suppose the horizontal derivative matrix

    tau = B (DX)^T

exists weakly, tau is essentially bounded in operator norm, and

    sym tau >= c I_d,             c > 0,
    ||B||op <= M.

Put R = sym tau - I_d and r = ||R||_{L2(gamma_n;Frobenius)}.
All norms on matrix fields below are Frobenius L2 norms unless indicated.

A convenient sufficient regularity class is: B locally C1 and bounded;
X locally Lipschitz, square integrable; tau bounded. The proofs also extend
to a closed horizontal Sobolev calculus with the stated chain and product
rules. No strong derivative of the correction u is assumed or used in the
full-law bound.

## 2. The closed variational inverse

Let H be the space of symmetric matrix fields S in L2 for which
delta(SB) belongs to L2, with its graph norm. Equivalently one may take the
closure of smooth compactly supported symmetric fields and include the
admissible noncompact test fields by localization. Bounded multiplication by
B and closedness of divergence imply closedness of this graph space.

Define

    u_S = delta(SB),
    a(S,T) = E[u_S dot u_T] + E[<S tau,T>_F].

The form is generally nonsymmetric. It is nevertheless continuous and
coercive:

    a(S,S) = ||u_S||_2^2 + E tr(S^2 sym tau)
           >= ||u_S||_2^2 + c ||S||_2^2.

Lax–Milgram therefore gives a unique S in H satisfying

    a(S,T) = -E[<R,T>_F]                       (2.1)

for every symmetric T in H. Set J=SB and u=delta J. Testing with S gives

    ||u||_2^2 + c ||S||_2^2 <= r ||S||_2,
    ||S||_2 <= r/c,
    ||u||_2 <= r/(2 sqrt(c)),
    ||J||_2 <= Mr/c.                           (2.2)

The middle bound follows by maximizing r s - c s^2 over s>=0; it is not
obtained by separately loosening both terms. Since u is a Gaussian
divergence, E u=0. Thus X+u preserves mu exactly.

For smooth fields, integration by parts identifies (2.1) with

    sym[B (Du)^T + J (DX)^T] = -R.             (2.3)

Only the symmetric horizontal derivative is determined by this equation.
There is no asserted L2 bound on the full Du or on the skew part of B(Du)^T.
Symmetry of T is essential: for unrestricted T, the first integration by
parts produces delta(T^T B), so the displayed energy form does not extend
to arbitrary matrix S by dropping its symmetry restriction.

## 3. An exact weak cancellation, requiring no bound on Du

For a smooth test h on output space let f solve the standard Gaussian Stein
generator equation

    (x-mu) dot Df(x) - Delta f(x) = h(x) - E h(mu+Z),
    Z ~ N(0,I_d).

Assume the derivatives used below are bounded and the integration by parts
is justified. These conditions hold for the smoothed indicators in section 4.
Set T(Q)=D^2 f(X(Q)). This symmetric field is an admissible variational
test by localization. Write m=X-mu. The chain rule gives

    delta(TB)_j = (Tm)_j - sum_{i,l} tau_{il} f_{jil}(X).

Equation (2.1) therefore yields

    E[u dot Tm] + E[<S tau,T>]
      = -E[<R,T>] + E[tau : D^3 f(X)[u]].       (3.1)

Separately, the defining divergence of u gives

    E[u dot Df(X)] = E[<S tau,D^2 f(X)>].       (3.2)

Differentiate the output-space Stein equation and combine (3.1)–(3.2).
The completely symmetric third derivative removes the skew part of tau:

    E[Dh(X) dot u]
      = -E[<R,D^2 f(X)>]
        + E[R : D^3 f(X)[u]].                 (3.3)

The usual Stein identity for X is

    E h(X)-E h(mu+Z) = E[<R,D^2 f(X)>].

Consequently the exact first-order law cancellation is

    E h(X) + E[Dh(X) dot u] - E h(mu+Z)
       = E[R : D^3 f(X)[u]].                  (3.4)

Ordinary Taylor's theorem in output space, applied pathwise to the positive
pushforward X+u, now proves

    |E h(X+u) - E h(mu+Z)|
      <= ||D^3 f||_{infinity,F} r ||u||_2
         + (1/2)||D^2 h||_{infinity,op} ||u||_2^2.    (3.5)

This estimate has no hidden source derivative norm. In particular it does
not infer a full-law conclusion from moment matching. It tests every
smoothed bounded indicator and bounds the resulting probability difference.

## 4. Explicit total-variation theorem

Fix a>0, and let Z' be fresh independent N(0,I_d). Then

    TV(Law(X+u+a Z'), N(mu,(1+a^2)I_d))
       <= min(1, C(a,c) r^2),                  (4.1)

where

    C(a,c) = sqrt(6)/(2 sqrt(c)) [1/a - arctan(1/a)]
             + sqrt(2)/(8 c a^2).             (4.2)

The noise a Z' is paid output noise, and the comparison Gaussian has the
same enlarged covariance. It is not permissible to keep covariance I_d
on the right of (4.1).

### Proof of all dimension-independent derivative constants

For any Borel event A, put

    h(x) = P[x+a Z' belongs to A].

Gaussian Hermite orthogonality/Bessel gives, for any bounded measurable
H with ||H||infinity<=1 and any k>=1,

    ||D^k(H * gamma_s)(x)||_F <= sqrt(k!)/s^k.

Indeed the ordered-index Frobenius sum equals k! times the sum of squared
Hermite coefficients weighted by the corresponding multi-index factorials;
Bessel bounds the latter sum by E H(x+sZ)^2<=1. Thus

    ||D^2 h||_{infinity,op} <= ||D^2 h||_{infinity,F}
                           <= sqrt(2)/a^2.

Use the Ornstein–Uhlenbeck representation of f. Its third derivative obeys

    ||D^3 f||_{infinity,F}
      <= sqrt(6) integral_0^infinity
         e^(-3t)/(a^2+1-e^(-2t))^(3/2) dt
      = sqrt(6) integral_0^1
         s^2/(a^2+1-s^2)^(3/2) ds
      = sqrt(6) [1/a - arctan(1/a)].

The last expression is positive. Insert these constants and (2.2) into
(3.5), then take the supremum over all Borel A. This proves (4.1).

For comparison, before correction the same calculation gives

    TV(Law(X+aZ'), N(mu,(1+a^2)I_d))
      <= min(1, log(1+a^(-2)) r/sqrt(2)).       (4.3)

Thus the new estimate is quadratic in the total Frobenius Stein residual.

## 4A. Actual randomized corrections and incomplete solves

The same argument applies to an implemented random vector Uhat, with fresh
internal randomness conditionally on the complete source Q, provided

    E[Uhat | Q] = u,             v^2 = E||Uhat||^2 < infinity.

Indeed the linear Taylor term still equals E[Dh(X) dot u]. Every effect of
the extra randomization is charged in the second-order remainder. Therefore

    TV(Law(X+Uhat+aZ'), N(mu,(1+a^2)I))
      <= sqrt(6)[1/a-arctan(1/a)] r ||u||_2
         + sqrt(2) v^2/(2a^2).                 (4A.1)

If b(Q)=E[Uhat|Q]-u is nonzero, add ||b||_2/a to this bound, using the
first-derivative Hermite bound ||Dh||<=1/a. No derivative of Uhat, no
Gaussian law for Uhat, and no substitution of an estimator inside a
covariance square root is asserted. In particular a conditional unbiased
estimator with huge second moment does not close the theorem.

If S is only an approximate variational solution, suppose its *full*
equation residual E satisfies

    a(S,T) = -E[<R,T>] + E[<E,T>]

for all admissible symmetric test fields, with E in L2. The right side of
(4A.1) receives the additional term

    log(1+a^(-2)) ||E||_2/sqrt(2).               (4A.2)

Here ||u|| must be bounded independently or directly from the approximate
energy inequality. A residual checked only against finitely many Galerkin
basis elements is not the full equation residual needed in (4A.2).

These are conditional implementation-error theorems. They identify exactly
which source-conditional mean, bias, second moment and variational residual
must be proved for an actual value-only program; they do not assume that
such a program has already acquired u.

## 4B. Sharper scalar constants

In output dimension one, write phi for the standard Gaussian density. Since
every nonzero Gaussian density derivative has integral zero, maximizing its
integral over a measurable event gives half its L1 norm. Consequently

    ||(1_A * gamma_a)''||infinity <= 2 phi(1)/a^2,
    ||(1_A * gamma_a)'''||infinity
       <= [phi(0)+4 phi(sqrt(3))]/a^3.

The second formula follows by integrating |He_3| phi across its roots
-sqrt(3), 0, sqrt(3). Applying the same OU integrals as above gives the
valid scalar constants

    C2_scalar(a) = phi(1) log(1+a^(-2)),
    C3_scalar(a) = [phi(0)+4phi(sqrt(3))]
                    [1/a-arctan(1/a)],
    C4_scalar(a) = phi(1)/a^2.

For a full equation residual E and conditionally unbiased random correction,

    TV <= C2_scalar ||E||_2
          + C3_scalar ||R||_2 ||u||_2
          + C4_scalar E|Uhat|^2.                (4B.1)

These scalar constants are used by the exact-rational cosine-fixture
certificate in the accompanying acquisition diagnostic.

## 5. Application to the frozen conservative-gradient source

Let h be a globally ell-Lipschitz conservative vector field with ell<1.
Let G,Z be independent standard Gaussians, and use the frozen source's
canonical Gaussian Stein resolvent K, satisfying

    delta_G K = h-E h(G),       ||K||op<=ell.

Take

    X=h(G)+Z,
    B=[K(G), I_d],
    tau=I_d+K(G)(Dh(G))^T.

The assumptions hold in the weak sense under C1,1 potential regularity:

    c=1-ell^2,
    M=sqrt(1+ell^2),
    ||tau||op<=1+ell^2,
    r<=sqrt(d) ell^2.

The theorem constructs a positive mean-preserving correction and proves

    TV(Law(X+u+aZ'), N(Eh(G),(1+a^2)I_d))
       <= min(1, C(a,1-ell^2) d ell^4).        (5.1)

This is a valid finite-step full-law statement about the variationally
defined correction. It is not merely the formal cubic cancellation in S3.
It also does not provide the requested polylog-query theorem: the initial
Frobenius residual is sqrt(d) ell^2, and the estimate squares that whole
quantity. The factor d ell^4 must not be reported as sqrt(d) ell^4.

## 6. Exact limitations and next scientific obligations

1. **Acquisition.** B, tau and the global variational solve are analytical
   objects. The two-value source factory acquires unbiased actions of K,
   not these coupled fields or this solve. In the pointwise formula
   u=delta(SB)=S(X-mu)-div_B S, the unknown mu is visible. This proof does
   not grant an acquired mean, derivative, conditional expectation or PDE
   oracle. A legal value-only implementation needs its own query and
   arithmetic accounting, and its own implemented-law perturbation bound.

2. **Iteration.** The positive output X+u need not inherit a bounded,
   coercive pointwise Stein matrix. The matrix residual contains a
   commutator with the uncontrolled skew horizontal derivative. Equation
   (4.1) resolves one-step law control; it does not by itself authorize an
   all-order matrix Newton iteration.

3. **Dimension.** A useful polylog route would need a stronger structured
   norm or cancellation yielding dimension dependence only at the terminal
   comparison, not a fresh square of sqrt(d) at every step.

4. **Comparison.** Gaussian Stein equations, Lax–Milgram, Gaussian
   smoothing, Hermite Bessel bounds and conventional Newton ideas are
   established tools. This note proves their stated assembly for this
   opening; it does not claim priority or practical superiority over the
   fixed-exponent compiler or the cloud/FORS competitors in the packet.

5. **Exact-real versus finite-bit law.** No finite-bit implementation is
   claimed. If implemented discretely, compare to the commonly rounded
   Gaussian target and charge numerical acquisition and solver errors.
