# Independent mathematical review of the bosonic ensemble interface

Root independently derives and accepts the following statements at their exact
mathematical scope. This is not a review of every claim in the source or the
worker's production calculation, and establishes no practical speed advantage.
Source: Yu,Wei,Li,[arXiv2610.31541v1](https://arxiv.org/html/2610.31541v1),
22October2026, equationsS95–S108,S157–S163. The worker independently found the
same obstruction and constructs a finite-sector calculation.

## The attractive grand-canonical source is unstable

For U1>0,U2=-g<0 in S157, take the orthonormal Fock vectors with n bosons of
each flavor on one site and none elsewhere. Relative density is zero. Hopping
and pairing have zero expectation. Thus <H-mu N>=-4g n²-2mu n. Convexity of
the exponential gives <exp[-beta(H-mu N)]> >= exp(4beta g n²+2beta mu n).
For beta>0 and finite mu these terms grow without bound. Summing diagonal
matrix elements proves that the uncut grand-canonical trace is infinite.
A finite-occupation reference is a different mathematical model.

## The printed positive determinant weight is itself non-normalizable

Consider Delta=0,U1>0,U2<0, a finite lattice of M sites and any finite positive
Trotter slice count. Split each independent HS Gaussian field into its normalized
uniform all-site/all-time component and orthogonal residuals. Conditional on
residuals, scalar uniform potentials commute through every slice. The single
flavor propagation is

    B = exp(beta mu + a Phi + i b Psi) R,
    a=sqrt(2beta |U2|/M)>0, b=sqrt(2beta U1/M)>0.

R is invertible because it is a finite product of matrix exponentials. Pick any
eigenvalue lambda of R. Finite real Phi0,Psi0 solve
exp(beta mu+a Phi0+i b Psi0)lambda=1. As a function of the complex scalar
s=aPhi+i bPsi, det(I-exp(beta mu+s)R) is analytic and has a zero of integer
multiplicity k>=1 there. Locally the source's conjugate-flavor weight
|det(I-B)|^(-2) behaves as a positive constant times |s-s0|^(-2k).

The two-dimensional Gaussian density is strictly positive at this finite point,
and the map from (Phi,Psi) to complex s is nonsingular. The local radial
integral contains integral_0^epsilon r^(1-2k)dr=infinity. Any additional smooth
positive exponential prefactor stays bounded below on a small neighborhood.
Thus the conditional positive integral diverges for every residual field.
Tonelli's theorem proves divergence of the complete printed positive-weight
integral. For k=1 it is logarithmic; higher multiplicity is worse. This directly
covers the source's finite3x3 attractive-density family, not just a one-site
fixture. Cancellation of positive contributions cannot normalize this measure.

This statement does not apply to the separate U2=0 stable-chemical-potential
regime, for which the source supplies a trace-convergence/pole exclusion bound.
No broad dismissal of its trace-convergent symmetry methods follows.

## A well-defined replacement, with an important sector restriction

For two separately number-conserving conjugate flavor propagators B,B*, fixed
equal populations n,n have weight h_n(B)h_n(B*)=|h_n(B)|²>=0. Here h_n is the
complete homogeneous symmetric polynomial, the finite n-boson trace. It is
finite for every finite B and removes determinant denominators. For finite
slice count its Gaussian integrals and moments are finite: matrix norms bound
the finite-degree polynomial by an exponential linear in absolute field values.
This does not promise small relative variance or uniform low cost as n grows.

Projection onto fixed *total* population does not generally preserve positivity.
For the one-mode pair B=i,B*=-i, the total-number generating function is
1/(1+z²), positive for0<z<1 but with coefficient-1 at total number2. The
balanced1,1 coefficient is1. The ensemble restriction is therefore load-bearing.
Pairing terms that fail to conserve each flavor are not silently included.

Canonical recursion and conjugate-sector positivity are established ordinary
ingredients. Their composition supplies a valid finite-cloud operation; neither
the algebra nor a small exact-diagonalization match proves a new tractability
class, historical priority, large-system accuracy, physical discovery or
civilisation-level advantage.
