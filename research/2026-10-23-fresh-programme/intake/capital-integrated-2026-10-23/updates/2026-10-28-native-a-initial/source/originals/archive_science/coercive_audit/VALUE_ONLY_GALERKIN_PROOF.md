# Value-only acquisition followed by a certified nonlinear scalar correction

27 October 2026. This is an executed interface diagnostic for
`SMOOTHED_LAW_NEWTON_THEOREM.md`. It establishes a positive four-query
runtime sampler with a full-law bound for one checked nonlinear fixture,
after expensive charged calibration. It does not solve the general
high-dimensional polylog-query problem or establish an advantage over
scalar FORS, direct integration, or a known-template exact solution.

## Source, training and independent verification

The fixture is h(x)=(7/20)cos(x), with supplied Lipschitz bound ell=7/20.
The learner `acquire_polynomial` receives only an h-value callback. It has
no source mean, h' or exact K. It fits a total-degree-ten bivariate Hermite
polynomial S(G,Z), with all 66 basis elements present, and freezes dyadic
coefficients before the separate truth evaluator runs. The evaluator is
explicitly allowed to use the cosine formula to verify this fixture.

The executed prototype uses floating-point h values and quadrature to
choose S. The mathematical certificate applies to the precise frozen
rational polynomial and its specified exact-real runtime sampler. Both
runtime and verification read `galerkin_S_rational.csv`; the mathematical
program uses those rational coefficients in unnormalized Hermite bases.
Floating normalization and output samples are execution diagnostics. No
continuous-TV claim is made for finite-bit output; that requires a commonly
rounded target and a separate numerical error budget.

## Derivative-free coefficient acquisition

Use 48-point Gaussian quadrature for G and Z. The fitting mean is the
weighted average of the 48 acquired h(G) values. At each G node use a
32-point Gauss–Legendre rule for rho in [0,1] and a 24-point generalized
Gauss–Laguerre rule of shape 3/2 for R^2/2, R~chi_3. Each cubature pair
uses the R22 two-value secant

    [h(rho G+sqrt(1-rho^2)R)-h(rho G-sqrt(1-rho^2)R)]
                       /[2sqrt(1-rho^2)R].

This chooses K_fit. No unproved fitting-quadrature error is used in the
final law certificate: the frozen coefficient is checked against the true
source independently.

For Hermite basis functions pi_i, form

    u_i=pi_i(h+Z-mu_fit)-K_fit partial_G pi_i-partial_Z pi_i.

The form and right side are obtained without h' values:

    a_ij=E[u_i u_j]+E[pi_i pi_j]+E[h(h-mu)pi_i pi_j]
          -E[Kh((partial_G pi_i)pi_j+pi_i partial_G pi_j)],
    b_i=-E[h(h-mu)pi_i]+E[Kh partial_G pi_i].

These formulas follow by integrating Kh' against the Gaussian measure and
using delta K=h-mu. Training substitutes acquired cubatures and mu_fit.
After the 66-by-66 solve, coefficients are frozen as multiples of 2^(-60)
in the unnormalized Hermite basis. The fixed 1e-12 threshold on normalized
coefficients is a learner choice made before truth evaluation.

The acquisition cost is exactly 48+2*48*32*24 = **73,776 h queries** per
calibration. The tensor rule has 2,304 nodes. Dense Gram formation costs
O(2304*66^2) arithmetic and the solve O(66^3). Basis storage is O(2304*66)
and the coefficient matrix O(66^2). No quadrature or solver cost is free.
The numerical minimum Gram eigenvalue is about 1.969 and its condition
number about 6.119; these are diagnostics, not a substitute for the full
equation residual.

## Actual positive four-query runtime map

Generate independent standard Gaussians G,Z,G',W, fresh R~chi_3 and fresh
U~Unif[0,1]. The uniform is itself generated from three scalar Gaussians
A,B,C as (1+A/sqrt(A^2+B^2+C^2))/2. Set r=sqrt(1-U^2)R and query

    Jhat=[h(UG+r)-h(UG-r)]/(2r).

Return

    Uhat=S(G,Z)[h(G)-h(G')+Z]-S_G(G,Z)Jhat-S_Z(G,Z),
    Y=h(G)+Z+Uhat+W.

The four h calls are h(G), h(G') and the two endpoints; h(G) is reused.
Polynomial evaluation and differentiation use ordinary arithmetic. The
ideal-real primitive convention uses exact Gaussian seeds and exact h
values. Measure-zero zero denominators can be assigned fixed values.

With Q=(G,Z), the R22 identity and independent fresh source blocks imply

    E[Uhat|Q]=u=S(h+Z-mu)-K S_G-S_Z,
    Var(Uhat|Q)<=ell^2(S^2+S_G^2),
    E Uhat^2<=||u||_2^2+ell^2(||S||_2^2+||S_G||_2^2).

The stochastic variance is therefore charged. No unbiased action is
promoted to a Gaussian covariance square root.

## Full equation residual and full-law comparison

For any frozen smooth S the full residual, rather than its Galerkin
projection, is

    E=2S+Z S_Z-S_ZZ+(1+2S)K h'
      +(Z S_G-2S_GZ)K+2S_G K(h-mu)
      -(G S_G+S_GG)K^2+S_Z(h-mu).

This follows by expanding Vu+S tau+R, with V=K partial_G+partial_Z,
tau=1+Kh', R=Kh', and K'=GK-(h-mu). The exact verifier bounds the L2
norm of this entire field, including directions outside the fitting space.

For standard Gaussian density phi, the scalar constants at reserve a=1 are

    C2=phi(1)log(2),
    C3=[phi(0)+4phi(sqrt(3))](1-pi/4),
    C4=phi(1).

They follow from the zero integrals and exact L1 norms of Gaussian density
derivatives, followed by the OU Stein integral. The full theorem gives

    TV(Law(Y),N(mu,2))
       <=C2||E||_2+C3||R||_2||u||_2
         +C4[||u||_2^2+ell^2(||S||_2^2+||S_G||_2^2)].

## Exact rational certification

Put a=ell exp(-1/2). The source has unnormalized Hermite expansions

    h=a sum_(n>=0) (-1)^n He_(2n)/(2n)!,
    K=a sum_(n>=1) (-1)^n He_(2n-1)/(2n)!,
    h'=a sum_(n>=1) (-1)^n He_(2n-1)/(2n-1)!.

Truncate h before degree 64 and K,h' consistently. Rational arithmetic uses

    He_i He_j=sum_k k! binom(i,k)binom(j,k) He_(i+j-2k),
    ||sum c_ij He_i(G)He_j(Z)||_2^2=sum c_ij^2 i!j!.

The scalar a is enclosed by an alternating rational Taylor series. Its
rational center error is charged. Gaussian hypercontractivity gives

    ||P||_4 <= [sum 3^(i+j)c_ij^2 i!j!]^1/2,
    ||P||_8 <= [sum 7^(i+j)c_ij^2 i!j!]^1/2.

The omitted h tail has L8 norm at most

    a_upper [sum_(m>=64) 7^m/m!]^1/2,

and K,h' use a valid bound from degree 63. Each scalar tail sum is at most
its first term divided by 1-7/(first_degree+1). Holder bounds all residual
products using polynomial L4 bounds, tail L8 bounds and the true bounds
|K|,|h'|<=ell and |h-mu|<=2ell. The exact code encloses sqrt, log(2), pi
(Machin's formula) and Gaussian-density constants rationally. Final ceilings
are verified by exact rational comparisons, not numerical rounding.

The certified upper bounds are

    ||E||_2 <= .001019044385529971...
    ||R||_2 <= .03230463472219946...
    ||u||_2 <= .01575202186173239...
    ell^2 E(S^2+S_G^2) <= .00006918246159069869...
    E Uhat^2 <= .0003173086543231938...

The full residual truncation error is below 6.204e-18. The rigorous sharp
TV expression is below .000330143855941197. In particular,

    TV(Law(Y),N((7/20)exp(-1/2),2)) < 331/1,000,000.

The conservative dimension-independent constants separately certify TV<1/1000.
`galerkin_exact_rational_bounds.csv` saves the exact rational bounds.

## Execution and limitations

The retained floating run generated 100,000 outputs with exactly 400,000
runtime h calls. Including its calibration gives 473,776 calls. An earlier
development run used the same counts before replacing a native uniform draw
with the Gaussian-derived uniform: total across both executed runs was
947,552 h evaluations. Exact certificate replays use analytic source
verification and rational arithmetic, not additional black-box observations.

The output empirical moments only check execution. The law statement rests
on the theorem and exact full-residual/tail certificate for the ideal-real
sampler. The final code explicitly reloads the same frozen coefficient file
used by the verifier; this loading clarification does not change coefficients.

Verification knows the cosine fixture, so this is not a data-only universal
certificate for an arbitrary unknown C1,1 source. The calibration and fixed
degree do not give a polylogarithmic asymptotic query bound. Strong scalar
competitors can be better: known cosine has an analytic mean, direct
quadrature is cheap, and bounded-input FORS already supplies high-accuracy
scalar Gaussian-mean sampling. No practical advantage is claimed.

The completed interface is a source-value-trained coefficient, an actual
positive randomized correction using legal values, and a full-law bound
that includes its complete equation residual and stochastic variance. The
next obligation is to acquire and certify the corresponding high-dimensional
corrections uniformly over the full conservative C1,1 class at the required
cost, rather than assuming the coupled inverse as an oracle.
