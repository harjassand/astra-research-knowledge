# Validated Kubo correlations from untrusted full eigensystems

This operation certifies an **unnormalized** finite-dimensional Kubo
correlation. It combines standard Duhamel, Schatten Hölder, polar
decomposition and exact interval arithmetic. No historical-priority claim
is made for those ingredients or for the spectral logarithmic mean. The
deliverable is an explicit error interface, including eigenvector errors,
and a physical implementation with an independent exact comparator.

## 1. Physical quantity and input contract

Let H be a finite Hermitian matrix, beta>=0, and A,B bounded observables.
Define

    C_H(A,B) = integral_0^1 Tr[e^(-(1-t) beta H) A e^(-t beta H) B] dt,
    Z_H = Tr e^(-beta H).

This definition is bilinear, with no adjoint on A and no division by Z.
For Hermitian A,B it is real and symmetric, and C_H(A,A)>=0.
There is no extra factor beta. The conventional normalized
Bogoliubov-Duhamel inner product inserts A* and divides by Z; see
[Brankov–Tonchev (2011), (2.16), (2.20)](https://arxiv.org/pdf/1101.2882).
Their displayed off-diagonal quotient assumes a simple spectrum; the
integral used here and the continuous logarithmic mean below do not.

The intended H is enclosed by a Gaussian-rational Hermitian H0:

    ||H-H0|| <= eta.

An untrusted solver supplies any square Gaussian-rational V and a real
diagonal Lambda containing exactly d diagonal entries, where H is d by d.
Calculate E=V*V-I and R=H0 V-V Lambda **exactly**. Suppose certified bounds
satisfy

    ||E|| <= epsilon <= 1/2,   ||R|| <= residual.

All matrix norms here are operator norms. Row/column sums of absolute real
and imaginary parts give rational upper bounds. Products are promoted to
arbitrary-precision integers before multiplication. Neither floating-point
matrix products nor a solver backward-error model enter the certificate.

The Gram condition proves completeness: V is invertible. Put

    U = V(V*V)^(-1/2),
    delta_original = eta + residual
                          + (3/2) epsilon (||H0||+||Lambda||).

Then U is unitary and

    ||H-U Lambda U*|| <= delta_original.                         (1)

Indeed ||(V*V)^(-1/2)-I||<=epsilon for epsilon<=1/2 and
||V||<=3/2, so ||U-V||<=3epsilon/2. Expanding
H0U-U Lambda=R+H0(U-V)-(U-V)Lambda proves (1).
This is the reviewed trace interface in
`../parent/validated_twist_trace/PROOF.md`; its review here is recorded in
`TRACE_REVIEW.md`.

### Hermitian sharpening through a positive Sylvester equation

There is a stronger bound that removes the large energy-offset term.
Write S0=(V*V)^(1/2), V=U S0, K=U*H0U and Q=U*R. Then

    Q = K S0-S0 Lambda.

The matrix T=K-Lambda is Hermitian, and exactly

    T S0+S0 T = Q+Q*.

Since S0 is positive definite, its Sylvester equation has the integral
solution

    T = integral_0^infinity e^(-t S0) (Q+Q*) e^(-t S0) dt.

Differentiating the integrand verifies the identity directly. Its norm is
at most 2||R|| integral_0^infinity exp[-2t lambda_min(S0)]dt. Therefore

    ||H-U Lambda U*|| <= eta+residual/sqrt(1-epsilon)
                     <= eta+residual/(1-epsilon)
                     = delta_hermitian.                         (1a)

The implementation selects delta=min(delta_original,delta_hermitian).
The new expression has no eigenvalue-gap assumption and is invariant
under a simultaneous scalar shift of H0 and Lambda. It uses only the
Gram and residual bounds already calculated. The stable Sylvester
integral is standard matrix analysis; see
[Higham's author explanation](https://nhigham.com/2020/09/01/what-is-the-sylvester-equation/).
This specialized residual application is proved here, with no claim of
historical priority. It applies to the parent trace operation as well as
to the Kubo extension.

## 2. A trace-weighted perturbation bound

For a Hermitian K, nonnegative a_1,...,a_m summing to 1, and arbitrary
matrices M_1,...,M_m, Schatten Hölder gives

    |Tr[e^(a_1 K) M_1 ... e^(a_m K) M_m]|
        <= (Tr e^K) product_j ||M_j||.                            (2)

Choose Schatten exponent 1/a_j on each exponential and infinity on the
insertions; zero a_j causes no difficulty. Each exponential contributes
(Tr e^K)^a_j. This proves (2) without commuting any insertion past K.
The standard Hölder inequality and Duhamel derivative used here are stated
in [Alhambra (2023), (7), (178), (187)](https://arxiv.org/html/2204.08349v2).

**Theorem.** If H and Htilde are Hermitian and ||H-Htilde||<=delta, then

    |C_H(A,B)-C_Htilde(A,B)|
        <= (exp(beta delta)-1) Z_Htilde ||A|| ||B||.              (3)

**Proof.** Write K0=-beta Htilde, D=-beta(H-Htilde),
K_s=K0+sD, and rho=beta delta. Duhamel's formula differentiates
each of the two exponentials in C(K_s;A,B). In the first differentiated
term the insertion D is integrated over an interval of length 1-t; in
the second it is integrated over length t. Every resulting product has
total exponential time 1. Applying (2), and then integrating t, proves

    |d C(K_s;A,B)/ds| <= rho Z_s ||A|| ||B||.

Weyl's eigenvalue inequality gives Z_s<=exp(s rho) Z_0, hence integration
in s proves (3), with the rho=0 case obtained directly. This improves the
looser rho exp(rho) factor; neither bound has an explicit dimension factor.
The partition trace Z can of course itself grow with dimension.

The same argument yields |C_H(A,B)|<=Z_H||A||||B||. For the optional
normalized quantity Q_H=C_H/Z_H, differentiating the quotient and using
|dZ_s/ds|<=rho Z_s gives

    |Q_H(A,B)-Q_Htilde(A,B)| <= 2 beta delta ||A|| ||B||.           (4)

No normalized quantity is substituted for the physical source input.
No eigenvalue gaps, isolated spectral clusters or differentiable
eigenvector choices occur in these arguments.

## 3. Observable transport from the polar factor to the exact dyadic V

Computing U is unnecessary. Let S0=(V*V)^(1/2), so V=U S0. Define

    alpha(epsilon) = epsilon(4+epsilon)/(4-2epsilon).

The spectrum of S0 lies in [sqrt(1-epsilon),sqrt(1+epsilon)], whence

    ||S0-I|| <= epsilon/(2-epsilon),
    ||S0|| <= 1+epsilon/2.

Consequently, with A_U=U*AU and A_V=V*AV=S0 A_U S0,

    ||A_U-A_V|| <= alpha(epsilon)||A||,
    ||A_V|| <= (1+epsilon)||A||.                                (5)

The same holds for B. Bilinearity and (2) give

    |C_Lambda(A_U,B_U)-C_Lambda(A_V,B_V)|
        <= alpha(epsilon)(2+epsilon) Z_Lambda ||A|| ||B||.        (6)

For example, split the difference as
C_Lambda(A_U-A_V,B_U)+C_Lambda(A_V,B_U-B_V) and apply (5).
This alpha is a rational bound, so no square roots of Gram eigenvalues
need be enclosed.

Combining (1), (3) and (6), the implementable absolute error is

    |C_H(A,B)-C_Lambda(V*AV,V*BV)|
      <= Z_Lambda ||A|| ||B||
            [exp(beta delta)-1 + alpha(epsilon)(2+epsilon)].     (7)

If the physical system is a direct sum of invariant blocks and A,B
preserve those blocks, use **the sum of block errors**, rather than a
maximum delta times the whole partition function. For endpoint spin-two
Sz observables ||A||=||B||=2, the error is at most

    4 sum_m Z_Lambda,m
          [exp(beta delta_m)-1+alpha(epsilon_m)(2+epsilon_m)].   (8)

Every physical block must be retained or else separately bounded. If A or
B connects different blocks, (8) cannot be applied as written; use a full
space certificate or retain all cross-block contributions explicitly.

Exact rational observables suffice for the present spin problem. More
generally, if A0 approximates A with ||A-A0||<=eta_A and ||A0||<=a0, set
Delta_A=eta_A+alpha a0, and similarly Delta_B. A valid observable error is

    Z_Lambda [Delta_A ||B|| + (1+epsilon)a0 Delta_B].             (9)

This follows by the same two-term split; ||B|| may be bounded by b0+eta_B.
Swapping the two observables can give a smaller rational bound. The demo
does not need (9), since both observables are exact integer diagonal.

## 4. Exact signed summation and degeneracy-safe logarithmic means

For real diagonal Lambda with entries lambda_i,

    C_Lambda(A_V,B_V) = sum_i,j L_ij (A_V)_ij (B_V)_ji,
    L_ij = integral_0^1 exp[-beta((1-t)lambda_i+t lambda_j)]dt.

For Hermitian observables, form the real signed sum exactly as

    sum_i L_ii (A_V)_ii (B_V)_ii
       + 2 sum_i<j L_ij Re[(A_V)_ij (B_V)_ji].                  (10)

The coefficients in (10) are exact Gaussian-rational products. Interval
multiplication respects each coefficient's sign. Self-correlations can
additionally be clipped below at zero; cross-correlations need not be
positive.

Let c=min_i lambda_i and x_i=beta(lambda_i-c)>=0. Work with reduced weights

    Lhat_ij = exp[-min(x_i,x_j)] psi(|x_i-x_j|),
    psi(x) = integral_0^1 exp(-t x)dt,
    psi(0)=1.

The common multiplier exp(-beta c) restores the unnormalized physical
quantity. It also restores Z and every term of the error in (7). Shifting
both H and U Lambda U* by cI does not change delta. All reduced weights
lie in [0,1], and at least one reduced trace weight equals 1.

**Scalar enclosure algorithm.** All bounds are rational, with outward
fixed-point rounding at denominator 2^112 in the demonstrator.

* For exp(x), reduce nonnegative x by repeated halving to x<=1/2. The
  degree-D positive Taylor partial sum is a lower bound; the omitted first
  term divided by 1-x/(D+2) bounds the whole tail. Outward squaring restores
  the original argument. Negative arguments use outward reciprocals.
* For psi(0), return [1,1] exactly. For x>0, reduce by halving. On the
  reduced interval, enclose phi(x)=(exp(x)-1)/x using

      phi(x)=sum_n>=0 x^n/(n+1)!.

  Its degree-D partial sum has a positive tail bounded by its next term
  divided by 1-x/(D+3). Multiply by an enclosure for exp(-x).
* Restore each doubling with

      psi(2x)=psi(x)(1+exp(-x))/2,
      exp(-2x)=exp(-x)^2.

  Use the old exp(-x) before squaring. Known upper bounds 1 can be applied
  after outward rounding. Finally multiply by exp[-min(x_i,x_j)].

Here D=28. This algorithm never subtracts two nearly equal exponentials
and never divides by an energy gap. Exact degeneracies and arbitrarily
small gaps are allowed. A finite chosen scalar precision does not promise
a useful relative width for every possible input; it always supplies an
enclosure, and can be increased. No scalar eigengap cutoff is hidden.

`review_controls.py` checks zero, tiny and ordinary gaps through a second
scalar identity, including x=2^-160. At that x, the stable psi interval
has width 2^-112, while dividing the outward interval for 1-exp(-x) by x
has width 2^48 at the same fixed-point precision. This is a verified
arithmetic control, not a novelty claim for stable divided differences.

## 5. Actual physical input: the spin-two dimer

`certify_kubo.py` builds the complete 25-state open dimer in the product
basis (m,n), m,n in {-2,-1,0,1,2}. For h=S_left dot S_right,

    h_(m,n),(m,n) = mn,
    h_(m+step,n-step),(m,n)
        = sqrt[(6-m(m+step))(6-n(n-step))]/2.

Every off-diagonal entry is 2, 3 or sqrt(6). The actual Hamiltonian is
H_eff=3h, beta_eff=1. A=Sz_left and B=Sz_right have exact norms 2.
All states are present in one full matrix; no magnetization symmetry or
negative-sector multiplicity is assumed.

The physical matrix is enclosed in Q(sqrt(6)) before rounding H0 to
denominator 2^40. An integer square root encloses sqrt(6) with width
2^-80. The solver proposes V and Lambda at denominator 2^40. The exact
certificate gives approximately

    epsilon = 1.5603202372642698e-12,
    residual = 2.1827872842550278e-11,
    delta_original = 1.068911564729842e-10,
    delta = delta_hermitian = 2.2633863660747693e-11.

There are 50 exact zero-gap unordered pairs in the rounded Lambda and
the smallest positive proposed gap is 2^-40. Nothing branches on a
nonzero gap. Exact rational endpoints, including every scalar rounding
error, are stored in `KUBO_CERTIFICATE.json`. Their displayed values are

    C_H(Sz_left,Sz_right)
        in [-85344764.65381819, -85344764.63826092],
    Z_H in [75507543.67273098, 75507543.67614903].

The decimal displays are not the rational endpoint certificate. The
generic correlation interval has absolute width about 0.015557275, and
relative width about 1.823e-10 for this nonzero correlation. The earlier
delta_original gives width about0.066453765 on the same proposal.

### Independent ordinary comparator

The dimer is exactly solvable by total angular momentum. The code does
not trust that diagonalization: it constructs the polynomial matrices

    P_J = product_K!=J (h-e_K I)/(e_J-e_K),
    e_J = [-6,-5,-3,0,4], J=0,...,4,

over Q(sqrt(6)), and checks entrywise that each is Hermitian and
idempotent, (h-e_J I)P_J=0, sum P_J=I, and Tr P_J=2J+1. Thus completeness,
energies and multiplicities are verified with exact matrix operations,
without relying on an eigensolver or representation theory alone.
The physical energies are [-18,-15,-9,0,12].

The exact cross-correlation coefficients Tr(P_J A P_K B) are

    [  0,   -2,     0,  0,  0 ]
    [ -2,  1/2,  -7/2,  0,  0 ]
    [  0, -7/2,   5/2, -4,  0 ]
    [  0,    0,    -4,  7, -3 ]
    [  0,    0,     0, -3, 15 ].

All sqrt(6) coefficients cancel exactly. With the same rigorous scalar
weights, this comparator yields approximately

    C_H(A,B) = -85344764.64600967.

Its much narrower scalar interval is wholly contained in the generic
certificate. At beta_eff=1 this can also be checked directly from

    C_H(A,B) = -(4/3)e^18 + (2/3)e^15 + (25/9)e^9
                    +133/18 +(31/2)e^-12.

Additional exact controls are Tr h=0, Tr h^2=300, Tr H_eff^2=2700;
at beta_eff=0, C(A,A)=50, C(A,B)=0 and C(A+B,A+B)=100. The total
magnetization commutes with h, and the code verifies

    C(A+B,A+B)=sum_J e^(-3e_J) J(J+1)(2J+1)/3,
    C(A,A)+C(A,B)=C(A+B,A+B)/2,

including the coefficient identities, not merely floating-point values.
A duplicated proposal column fails the Gram condition. A deliberately
degraded proposal still contains the exact comparator, with a wider
interval. These test the validation contract rather than solver accuracy.

The generic physical certificate took about 0.015 seconds, the exact
projector comparator about 0.031 seconds, and the whole replay with
controls about 0.052 seconds on this run. These are measured small-model
elapsed times. The standard closed dimer formula is an especially strong
ordinary comparator and is cheaper once known; no speed or discovery
advantage is claimed for the generic eigensystem interface on this model.
Larger blocks have O(d^3) exact dense matrix products and O(d^2) scalar
summation per observable pair; arbitrary-precision bit costs are additional.
Six-site cost and peak memory have not been measured.

The additional complex two-state control has H=sigma_y and observables
sigma_x, sigma_z, sigma_y, so it exercises imaginary proposal vectors and
imaginary observable entries. At beta=3/2 it encloses the independent
formulas C_xx=(exp(beta)-exp(-beta))/beta, C_xz=0,
C_yy=exp(beta)+exp(-beta), as well as the beta=0 trace controls.
`CONTROL_REPLAY.json` stores these and the scalar tests.

That replay also recalculates the full 625-state parent trace using the
producer's reviewed exact physical builder read-only and this directory's
independent exact validation kernel. Every original eta,epsilon,residual
and delta_original is exactly reproduced. Substituting (1a) gives

    Z_4(3,(3+4i)/5)
      in [5.245258943309217e25, 5.245258964625708e25],

with relative width about4.063954145e-9, a 6.5498-fold width improvement
over the original interval on the same proposals. Maximum delta is about
7.019378456e-10. The new interval is wholly contained in the original.
The replay took about1.124 seconds, including the original and strengthened
bounds, and is not a runtime comparison. Parent sources were not edited.

## 6. Exact zero-time-frequency thermal source interface

The thermal worker's `../thermal_spin_projection/TIME_PROJECTION.md`
derives its P0 source form. For a source form power p=d+e+q, q=0,1,2,
the physical chain has n=p+2 sites and dimensionless couplings

    p=0:    (3 r s),
    p>=1:   (3r, 3,...,3, 3s),

with beta_eff=1. The source moment is exactly

    (-1)^p [-C_H(Sz_left,Sz_right)] / 5^p.                       (11)

There is no division by Z and no further beta multiplier. Equation (11)
applies a known rational factor to the final interval, with sign-aware
endpoint reversal. A blockwise implementation can use (8), since both
endpoint Sz observables preserve total magnetization.

This demonstrator acquires only p=0,r=s=1. Its source moment interval is

    [85344764.63826092, 85344764.65381819].

It contains the thermal worker's numerical beta=3 dimer preview
85344764.64600961, using the same physical normalization. The trace-only
four-site twisted-ring certificate does not by itself provide these
observable-weighted quantities. No complete higher source Gram/Rayleigh/
second-form family, later connected input, thermal gap or positive
precision ratio has been acquired here. The negative larger preview does
not justify a six-site/grid validation job.

## 7. Established operation and limits

An arbitrary full Hermitian eigensolver proposal can now be converted
into a rigorous signed physical Kubo interval with an error proportional
to the partition trace and observable norms. The eigensolver may mix
degenerate states arbitrarily. The logarithmic mean needs no gap cutoff,
and exact observable transport is certified without evaluating a polar
square root. This completes a reusable physical-input operation for the
thermal P0 message if its preview later warrants acquisition.

This is an explicit composition of established tools with a validated
finite physical example. It is not a claim of a new general perturbation
theory, a faster eigensolver, a new dimer solution, or a completed thermal
research target.
