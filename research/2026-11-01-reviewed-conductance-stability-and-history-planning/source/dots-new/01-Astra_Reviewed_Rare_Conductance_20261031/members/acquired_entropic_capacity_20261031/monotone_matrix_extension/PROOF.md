# Monotone Gaussian geometry: dimension-free capacity beyond commuting fibers

Author construction with the root's proposed organizing inequality. This
extends, and does not alter, the independently reviewed parent checkpoint.
No priority or physical capability claim. All coordinates, matrices, basins
and norms are acquired from exact raw polynomial coefficients below.

## 1. General principle

Let F(y,z)=z^T A(y)z/2 with y scalar and z in R^m, and A globally C² and
SPD on R. On 0<=y<=b assume

* A is C^2 and SPD; A(y)>=a I for a>0;
* A'(y)<=0 in Loewner order and A'(0)=0;
* ||A''(y)||op<=L.

Assume A is globally even, the Gaussian marginal q(y)=det(A(y))^-1/2 is integrable
on R, and the specified reversible diffusion is conservative. The acquired
basins are y<=-b and y>=b. For the physical isotropic diffusion with
generator beta^-1 Delta-grad F.grad, define MA=integral_b^infinity q and
R0=integral_-b^b 1/q. Then

    k_free/[1+L/(2 beta a^2)] <= cap_mu(Aset,Bset)/mu(Aset) <= k_free,
    k_free=1/(beta MA R0).                                         (1)

This does NOT require A(y)A(t)=A(t)A(y). Low-dimensional free energy alone
is not the premise: the Loewner order and curvature metric bound are real
geometry requirements.

### Proof of the hard lower estimate

For the conditional Gaussian covariance C=beta^-1 A^-1, solve the ordinary
Sylvester equation

    A S + S A = -A'

for symmetric S. Then SC+CS=C', so w_y(z)=S(y)z is an exact conditional
continuity velocity. This is a finite rational linear system for rational
polynomial A, not a supplied transport oracle. Its operator is positive:
all eigenvalues lambda_i+lambda_j>=2a; its inverse can be represented by
an adjugate/determinant program or computed by exact linear algebra.

In an orthonormal eigenbasis of A at each FIXED y,

    K=E|Sz|^2
     =(1/(2 beta)) sum_ij |A'_ij|^2/[lambda_i lambda_j(lambda_i+lambda_j)]
     <=Tr(B^2)/(4 beta a),
    B=-A^-1/2 A' A^-1/2 >=0.                                      (2)

This eigenbasis is proof notation only; its derivative is never taken or
supplied to the algorithm. Positivity gives Tr(B²)<=||B||Tr(B). Since
A'(0)=0, ||A'||<=L y, hence ||B||<=L y/a. Put w=1/q=sqrt(det A). Then

    -w'/w=Tr(B)/2,
    K w <= [L y/(2 beta a^2)] (-w').                              (3)

Integration by parts on [0,b], with the negative boundary term retained,

    integral K w <= [L/(2 beta a^2)]
                      [-b w(b)+integral w]
                <= [L/(2 beta a^2)] integral w.

Reflection supplies the other half. The parent's already reconstructed
conditional-transport Dirichlet/Thomson sandwich gives (1). The complete
argument is finite-rate; projected y remains non-Markov in general.

## 2. A raw-input, genuinely noncommuting polynomial family

Set b=1/2, v(y)=(1-y²)^2, and

    A(y)=I+v(y)H1+v(y)^2 H2,
    H1>0, H2>=0 on the m-dimensional fiber.

No commutation is assumed. On 0<=y<=1/2,

    A'=v'(H1+2vH2)<=0, A'(0)=0, A>=I,
    |v''|<=4, |(v²)''|<=8.

The second bound follows directly from
`(v²)''=8(1-y²)^2(7y²-1)`. If exact PSD certificates establish
H1<=u1 I and H2<=u2 I, take a=1 and L=4u1+8u2. Equation (1) becomes

    k_free/[1+(2u1+4u2)/beta] <= k_full <= k_free.                  (4)

These norm bounds are acquired by exact PSD tests and dyadic doubling,
not obtained from a floating eigensystem. For bounded operator norms the
factor is independent of fiber dimension even when eigenvectors rotate.
The actual run has [H1,H2]!=0, so pencils at generic different y do not
commute: their commutator is `v t(t-v)[H1,H2]`.

### Conservative diffusion and finite Gibbs normalization

For a term c(y) z^T H z/2, its contribution to x.grad F is
`[c+(y/2)c'] z^T H z`. For c=v this scalar is the bounded-below polynomial
3y^4-4y²+1, which is at least -1/3. For c=v² it is
`(1-y²)^3(1-5y²)`, at least -4: it is negative only for 1/5<y²<1,
where its absolute value is at most 4. Thus one may take
`C=u1/3+4u2` in x.grad F>=-C|x|².
The stopped quadratic Lyapunov argument gives nonexplosion. Since
A>=I+vH1, the parent's integrable tail bound remains available.
The executable deliberately uses the inherited bound

    q(y)<=det_+(H1)^-1/2(y²-1)^(-m), |y|>1,

with the PHYSICAL fiber dimension m. The determinant polynomial degree
can equal 2m or be intermediate for rank-deficient H2; it is never used
as the physical dimension or substituted into this tail. Positive
determinant coefficients are checked for the Horner backend. No
asymptotic or reflecting-wall approximation is introduced.

## 3. Coordinate and matrices acquired from raw coefficients

Ambient input F(x) is an exact rational degree-ten coefficient list with
n=m+1>=3. Its quadratic Hessian Q=P+H1+H2 has unique kernel span(ell).
Use the parent's simpler ordinary route: acquire rational nullvector u,
Pi=uu^T/(u^Tu), P=I-Pi, and represent ell=u/sqrt(u^Tu) exactly.
Let s=x^T Pi x and let F_j denote the ACTUAL homogeneous degree-j part.
Recover, by exact polynomial division,

    x^T H2 x = 2F_10/s^4,
    x^T(H1+6H2)x = 2F_6/s^2.

Both quotients must be homogeneous quadratics. Extract the symmetric
matrices, check H_i u=0, positive definiteness of H1+Pi, semidefiniteness
of H2, and the ENTIRE identity

    2F=x^TPx+(1-s)^2 x^TH1x+(1-s)^4 x^TH2x.

The fast aligned route performs the same full monomial-dictionary check.
Its sparse joint matrix graph is read from actual nonzero coefficients;
connected components yield paid block determinant/PSD computations. No
block decomposition is handed to the compiler. Dense rotated inputs pay
the full raw expansion and symbolic matrix costs.

The scalar polynomial D(t)=det(I+tH1+t²H2) is acquired exactly, using
connected components only when the raw matrices actually have them.
Its coefficients and acquired norm bounds suffice to evaluate (4).
There is no eigenvector, sampler, conditional mixing oracle, or known
committor input. The exact parent interval arithmetic is reused at its
frozen source hash. UNKNOWN remains possible under resource budgets.

## 4. Scope and fair comparison

The organizing implication is monotone conditional precision + bounded
curvature => bounded integrated transport resistance, not 'small determinant
dimension implies easy kinetics'. Arbitrarily rotating isospectral fibers
need not be Loewner monotone and are excluded. Monotonicity only on the
transition slab is required; normalization/nonexplosion are separate.

The delivered raw polynomial compiler is narrower than the abstract C²
theorem. It recognizes this exact two-matrix family and chooses its
full-fiber basins, not an arbitrary diffusion or arbitrary user basins.
Capacity/mass is not an arbitrary-start MFPT or a fixed-deadline CDF.

The underlying Gaussian transport, Sylvester equation and classical
variational principles are credited ordinary components. The explicit
monotone-matrix integration estimate and its acquired composition are
derived here from the root's proposal. Giving an ordinary comparator
this new certificate lets it reproduce the result; this is not an
independent prior-art victory, historical priority proof, or proprietary
speedup. A broader novelty comparison has not been established.
