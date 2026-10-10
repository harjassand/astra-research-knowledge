# Exact finite-expression certificate

2026-10-09 UTC. This is the mathematical specification of the implemented a posteriori certificate. It is separate from the uniform complexity theorem and does not require the numerical eigensystem/normal-form computations to be accurate. The code is not formally verified. One internal inspection and reproducible exact witness replays were performed; no external validation or publication was undertaken.

## Object being certified

On a panel t=c+h s, s in [-1,1], the supplied original rational Hamiltonian gives the exact rational Hermitian generator A(s). The finite candidate expression is

    F(s) = sum_a C_a(s) exp(-i phi_a(s)).

Every matrix coefficient of C_a and every real coefficient of phi_a is an explicitly stored dyadic rational with denominator 2^128. All phase constants are exactly zero. The floating eigensystem, Kato transport and Taylor computations propose these coefficients; they are not assumptions in the certificate.

The exact witness contains the original rational input, Omega, rescaling parameters, panel endpoints, centers and halfwidths, all C coefficients, all phase coefficients, and their denominator convention. The verifier checks the original coefficient identity for this three-channel family using rational arithmetic. It checks exact panel contiguity and full coverage, c-h=a and c+h=b, positive widths, and zero phase constants. No inferred root location is trusted.

## Residual and center defect

For each group form the finite polynomial

    R_a(s) = i C_a'(s) + phi_a'(s) C_a(s) - A(s) C_a(s).

Then iF'-AF = sum_a exp(-i phi_a) R_a. On real s the phase factors have modulus one. Define the rational entrywise norm upper bound

    L(M) = sum_(i,j) (|Re M_ij| + |Im M_ij|).

This is an upper bound for the operator norm. If R_a(s)=sum_r R_ar s^r, both half-panel residual integrals are at most

    rho = sum_(a,r) L(R_ar)/(r+1).

All coefficients are acquired by exact integer arithmetic. In the current family, A has denominator dividing 3*2^128, so the residual common denominator is 3*2^256. The division by r+1 is rational and exact. There is no omitted analytic Taylor tail: the candidate itself is a finite expression and its complete residual is bounded.

Since phi_a(0)=0, the center defect satisfies

    delta = L(sum_a C_a(0)-I).

The exact target fundamental matrix U(s), anchored at zero, is unitary on the real interval. Variation of constants gives

    ||F(+/-1)-U(+/-1)|| <= e = delta+rho.

The matrices F are not presumed unitary. For the panel transition F(1)F(-1)*, the resulting error is bounded by 2e+e^2 before endpoint evaluation errors.

## Certified scalar exponentials

Phase values at the endpoints are exact dyadic rationals. The evaluator uses 256 fractional bits. It constructs rational intervals for

    pi = 16 arctan(1/5) - 4 arctan(1/239)

using the alternating arctangent series, outward-rounded rational terms, and its next-term remainder. A floating computation chooses an integer range-reduction index only; any such integer is valid. The subsequent integer check requires the reduced center to have magnitude at most 4. The exact pi interval bounds the reduction error, multiplied by the magnitude of that integer.

At the reduced real center theta, a degree-64 Taylor polynomial evaluates exp(-i theta). Its mathematical remainder is bounded by

    4^65 / 65!.

The fixed-point Horner implementation rounds each coordinate and Taylor coefficient down. Its accumulated Euclidean error is bounded by the deliberately generous rational quantity

    2*65*4^64 / 2^256.

Indeed one Horner step has at most 3/2^256 error and multiplies prior error by at most 4; the displayed quantity exceeds the resulting geometric sum, including the leading-coefficient error. The range-reduction error is added by the unit Lipschitz bound for exp(-ix) on real x. No ordinary-library sine, cosine, exponential or pi value is trusted as an enclosure.

Five high-precision numerical checks of this enclosure code are saved separately as sanity checks, not as its proof.

## Endpoints, products and exact reported output

The endpoint matrix polynomials are evaluated exactly at +/-1. Their entrywise norm bounds multiply the certified scalar phase errors. If the resulting endpoint errors relative to the exact target are e_plus and e_minus, the transition error is at most

    e_plus + e_minus + e_plus e_minus.

The exact product is rounded down coordinatewise to denominator 2^128; 18/2^128 bounds this 3-by-3 complex matrix rounding error. The reported local error is rounded upward to denominator 2^160.

Global matrix products are also computed with exact integers and rounded to denominator 2^128. If E is the previous global error and d is a certified local transition error, update

    E_new <= E + d + E d + 18/2^128,

rounding the bound upward to denominator 2^160 after each panel. The final success test compares integers against the requested 2^-s threshold. The exact output matrix is stored as integer pairs with its denominator power of two.

## What this establishes

A successful replay certifies this exact reported endpoint against this exact supplied Hermitian polynomial. It does not establish the general theorem's runtime, the accuracy of a physical model, a certified CF4 implementation, or historical novelty. The proposer may fail or the conservative coefficient norm may reject a good approximation. Those are performance/termination limitations; no unverified numerical proposal can cause acceptance without passing the exact residual and output error bound.
